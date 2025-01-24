import time
import click
from os.path import join
from core.utils import prompt, intro
from core.utils.histogram import plot_distance_histogram
from core.utils import connections
from cifkit.utils.folder import get_file_paths
from cifkit import Cif
import os


def move_files_based_on_min_dist(cif_dir):
    intro.prompt_min_dist_intro()
    filter_files_by_min_dist(cif_dir)


def filter_files_by_min_dist(cif_dir_path, is_interactive_mode=True):
    """
    Filter files for files below the minimum distance threshold.
    When errors occur in computing distances, they are caught and filtered.

    First, we aren't using CifEnsemble because we also want to relocate
    .cif files that have errors while computing the connections.
    """

    min_dist_info = {}
    all_cif_file_paths = get_file_paths(cif_dir_path)
    all_file_count = len(all_cif_file_paths)
    # Get all the distances
    for idx, file_path in enumerate(all_cif_file_paths, start=1):
        cif = Cif(file_path)
        prompt.print_progress_current(idx, cif.file_name, cif.supercell_atom_count, all_file_count)
        start_time = time.perf_counter()
        try:
            min_dist = connections.compute_min_dist(cif)
        except Exception as e:
            min_dist_info[cif.file_name] = None
            print("Relocated to error folder due to", e)
            # Relocate the file to the error folder
            error_dir_path = join(cif_dir_path, "error_files")
            if not os.path.exists(error_dir_path):
                os.makedirs(error_dir_path)
            os.rename(file_path, join(error_dir_path, os.path.basename(file_path)))
            continue

        # Min distances are used for histogram generation
        min_dist_info[cif.file_name] = min_dist
        elasped_time = time.perf_counter() - start_time
        prompt.print_finished_progress(cif.file_name, cif.supercell_atom_count, elasped_time)
        

    # Get all min_dist values from the dictionary
    min_dists = [
        min_dist for min_dist in min_dist_info.values() if min_dist is not None
    ]

    # Folder to save the histogram
    plot_distance_histogram(cif_dir_path, min_dists, len(min_dists))

    if is_interactive_mode:
        click.echo("Note: .cif with minimum distance below threshold are relocated.")
        prompt_dist_threshold = "\nEnter the threshold distance (unit in Å)"
        dist_threshold = click.prompt(prompt_dist_threshold, type=float)
    else:
        dist_threshold = 2.6  # For testing set to 2.6

    # Now, move files anything below dist threshold to a new folder
    filtered_file_paths, destination_path = move_files_to_sub_directory(min_dist_info, cif_dir_path, dist_threshold)

    # Move files based on distance threshold
    prompt.print_moved_files_summary(
        filtered_file_paths, all_file_count, destination_path
    )
    prompt.print_done_with_option(f"min_dist_below_{dist_threshold}")


def move_files_to_sub_directory(min_dist_info, cif_dir_path, dist_threshold):
    filtered_file_paths = []
    destination_path = join(cif_dir_path, f"min_dist_below_{dist_threshold}")
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
    for file_name, min_dist in min_dist_info.items():
        if min_dist is not None and min_dist < dist_threshold:
            filtered_file_paths.append(file_name)
            os.rename(join(cif_dir_path, file_name), join(destination_path, file_name))
    
    return filtered_file_paths, destination_path