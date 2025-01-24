import time
import click
from os.path import join
from core.utils import prompt, intro, object
from core.utils.histogram import plot_distance_histogram


def move_files_based_on_min_dist(cif_dir):
    intro.prompt_min_dist_intro()
    filter_files_by_min_dist(cif_dir)


def filter_files_by_min_dist(cif_dir_path, is_interactive_mode=True):
    """
    Filter files for files below the minimum distance threshold.
    """

    # Initialize the ensemble
    ensemble = object.init_cif_ensemble(cif_dir_path)
    min_dists = []

    # Get all the distances
    for idx, cif in enumerate(ensemble.cifs, start=1):
        start_time = time.perf_counter()
        file_name = cif.file_name
        atom_count = cif.supercell_atom_count
        file_count = ensemble.file_count

        prompt.print_progress_current(idx, file_name, atom_count, file_count)

        # Compute min distance
        min_dist = cif.shortest_distance
        min_dists.append(min_dist)
        elasped_time = time.perf_counter() - start_time

        prompt.print_finished_progress(file_name, atom_count, elasped_time)

    # Folder to save the histogram
    plot_distance_histogram(cif_dir_path, min_dists, ensemble.file_count)

    if is_interactive_mode:
        click.echo("Note: .cif with minimum distance below threashold are relocated.")
        prompt_dist_threshold = "\nEnter the threashold distance (unit in Å)"
        dist_threshold = click.prompt(prompt_dist_threshold, type=float)
    else:
        dist_threshold = 2.6  # For testing set to 2.6

    # Filter files based on the minimum distance
    filtered_file_paths = ensemble.filter_by_min_distance(0.0, dist_threshold)
    destination_path = join(ensemble.dir_path, f"min_dist_below_{dist_threshold}")

    # Move filtered files to a new directory
    if filtered_file_paths:
        ensemble.move_cif_files(filtered_file_paths, destination_path)

    prompt.print_moved_files_summary(
        filtered_file_paths, ensemble.file_count, destination_path
    )
    prompt.print_done_with_option("min_dist_below_{dist_threshold}")
