import os
import shutil
import textwrap
import click
from click import echo
import pandas as pd
import matplotlib.pyplot as plt

from preprocess import cif_parser, cif_parser_handler, supercell_handler
from filter import neighbor
from util import folder, prompt


def print_intro_prompt():
    """Filters and moves CIF files based on the shortest atomic distance."""
    introductory_paragraph = textwrap.dedent(
        """\
    ===
    Welcome to the CIF Atomic Distance Filter Tool!

    This tool reads CIF files and calculates the shortest atomic distance.

    At the end, a comprehensive log will be saved in CSV format, capturing:
    1. File names of CIFs.
    2. Compound formula for each CIF.
    3. Shortest atomic distance computed.
    4. Whether the file was moved (filtered) based on the threshold.
    5. Number of atoms in each file's supercell.
    ===
    """
    )

    print(introductory_paragraph)

def get_min_dist_per_file(file_path):
    all_labels_connections = {}
    result = cif_parser_handler.get_cif_info(
        file_path, cif_parser.get_loop_tags()
    )
    _, lengths, angles, _, supercell_points, labels, _ = result

    unitcell_points = supercell_handler.get_flattened_points_from_unitcell(
        file_path
    )
    cutoff_radius = 10.0


    # PART 3: Process each atomic label
    for site_label in labels:
        filtered_unitcell_points = [
            point for point in unitcell_points if point[3] == site_label
        ]

        dist_result = neighbor.get_nearest_dists_per_site(
            filtered_unitcell_points,
            supercell_points,
            cutoff_radius,
            lengths,
            angles,
        )

        dist_dict, dist_set = dist_result

        (
            label,
            connections,
        ) = neighbor.get_most_connected_point_per_site(
            site_label, dist_dict, dist_set
        )

        all_labels_connections[label] = connections

    all_labels_connections = neighbor.filter_connections_with_CN(
        all_labels_connections
    )
    min_dist = float("inf")  # Initialize min_dist to infinity

    for site_label, pair_data in all_labels_connections.items():
        # Here, we correctly retrieve the distance from the first tuple in pair_data
        dist = pair_data[0][1]  # Access the distance directly
        if dist < min_dist:
            min_dist = (
                dist  # Update min_dist if a new smaller distance is found
            )
    return min_dist, supercell_points

def get_min_dist_list(file_path_list):
    file_min_dist_list = []
    num_of_files = len(file_path_list)
    

    for i, file_path in enumerate(file_path_list):
        filename_with_ext = os.path.basename(file_path)
        filename, _ = os.path.splitext(filename_with_ext)
        min_dist, supercell_points = get_min_dist_per_file(file_path)
        prompt.print_progress_current(
            i, filename_with_ext, supercell_points, num_of_files
        )
        # Dictionary to store connections for each label
        file_min_dist_list.append(min_dist)
        
        

    return file_min_dist_list


def get_filered_file_list_with_dist(
    file_path_list, file_min_dist_list, min_dist_threshold
):
    paired_list = list(zip(file_path_list, file_min_dist_list))
    filtered_files = [
        file for file, dist in paired_list if dist < min_dist_threshold
    ]
    return filtered_files


def plot_histogram(distances, save_path, num_of_files):
    plt.figure(figsize=(10, 6))
    plt.hist(distances, bins=50, color="blue", edgecolor="black")
    plt.title(f"Histogram of Shortest Distances of {num_of_files} files")
    plt.xlabel("Distance (Å)")
    plt.ylabel("Number of CIF Files")
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.savefig(save_path, dpi=300)


def move_files_based_on_min_dist(cif_dir, isInteractiveMode=True):
    print_intro_prompt()
    file_path_list = folder.get_cif_file_path_list_from_directory(cif_dir)
    num_of_files = folder.get_cif_file_count_from_directory(cif_dir)
    min_dist_threshold = 2.0

    if isInteractiveMode:
        supercell_method = prompt.get_user_input_on_supercell_method()

        if not supercell_method:
            echo(
                "> Your default option is generating a 2-2-2 supercell for "
                "files more than 100 atoms in the unit cell.",
            )
            supercell_method = 3

    file_min_dist_list = get_min_dist_list(file_path_list)
    # Create histogram directory and save
    plot_directory = os.path.join(cif_dir, "plot")
    if not os.path.exists(plot_directory):
        os.makedirs(plot_directory)

    histogram_save_path = os.path.join(
        cif_dir, "plot", "histogram-min-dist.png"
    )

    plot_histogram(file_min_dist_list, histogram_save_path, num_of_files)
    print("Histogram saved. Please check the 'plot' folder of the cif folder.")

    if isInteractiveMode:
        prompt_dist_threshold = (
            "\nNow, please enter the threashold distance (unit in Å)"
        )
        min_dist_threshold = click.prompt(prompt_dist_threshold, type=float)
    # Pair each file path with its corresponding minimum distance
    filtered_files = get_filered_file_list_with_dist(
        file_path_list, file_min_dist_list, min_dist_threshold
    )

    # Check if there are any files to process
    if filtered_files:
        # Create a new directory to store files that meet the condition
        new_folder_path = os.path.join(
            cif_dir, f"min_dist_below_{min_dist_threshold}"
        )
        os.makedirs(new_folder_path, exist_ok=True)

        # Move the filtered files to the new directory
        for file_path in filtered_files:
            shutil.move(file_path, new_folder_path)

        print(f"Moved {len(filtered_files)} files to {new_folder_path}")

        # Create a DataFrame using the filenames and distances
        df = pd.DataFrame(
            {"file": file_path_list, "dist": file_min_dist_list}
        )
        folder.save_to_csv_directory(cif_dir, df, "min_dist_log")
