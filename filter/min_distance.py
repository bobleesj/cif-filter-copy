import os
import shutil
import textwrap

import click
from click import echo
import pandas as pd
import matplotlib.pyplot as plt

from preprocess import cif_parser, cif_parser_handler, supercell_handler
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


def move_files_save_csv(
    files_lst,
    skipped_indices,
    shortest_dist_list,
    loop_tags,
    dist_threshold,
    filtered_folder,
    folder_info,
    result_df,
):
    # Now, use the computed shortest distances to move the files
    processed_files_count = 0
    for idx, file_path in enumerate(files_lst, start=1):
        # Skip indices above MAX_ATOMS_COUNT
        if idx in skipped_indices:
            continue

        shortest_dist = shortest_dist_list[processed_files_count]
        processed_files_count += 1

        # Re-calculate the formula_string here before
        result = cif_parser_handler.get_CIF_info(file_path, loop_tags)
        cif_block, _, _, _, all_points, _, _ = result
        _, _, formula_string = cif_parser.extract_formula_and_atoms(cif_block)

        # Initialize the "Filtered" flag
        filtered_flag = "No"

        # If the file meets the threshold criterion, update the flag
        if shortest_dist < dist_threshold:
            if not os.path.exists(filtered_folder):
                os.mkdir(filtered_folder)

            # Full path to where the file will be moved
            new_file_path = os.path.join(
                filtered_folder, os.path.basename(file_path)
            )

            # If the file already exists in the destination, delete it
            if os.path.exists(new_file_path):
                os.remove(new_file_path)

            filtered_flag = "Yes"
            shutil.move(file_path, new_file_path)

        new_row = pd.DataFrame(
            {
                "Entry": [cif_block.name],
                "Compound": [formula_string],
                "Shortest distance": [shortest_dist],
                "Filtered": [filtered_flag],
                "Number of atoms": [len(all_points)],
            }
        )

        result_df = pd.concat([result_df, new_row], ignore_index=True)

    folder.save_to_csv_directory(folder_info, result_df, "filter_dist_min_log")


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
    shortest_dist_list = []
    skipped_indices = set()
    result_df = pd.DataFrame()
    supercell_max_atom_count = float("inf")
    dist_threshold = 1.0  # Set a default value of 1.0 Å
    (
        folder_info,
        filtered_folder,
        files_lst,
        num_of_files,
        loop_tags,
    ) = cif_parser_handler.get_folder_and_files_info(
        cif_dir, isInteractiveMode
    )

    if isInteractiveMode:
        supercell_method = prompt.get_user_input_on_supercell_method()

        if not supercell_method:
            echo(
                "> Your default option is generating a 2-2-2 supercell for "
                "files more than 100 atoms in the unit cell.",
            )
            supercell_method = 3

    # Process CIF files
    (
        shortest_dist_list,
        skipped_indices,
    ) = supercell_handler.get_shortest_dist_list(
        files_lst, loop_tags, supercell_max_atom_count, supercell_method
    )

    # Create histogram directory and save
    plot_directory = os.path.join(folder_info, "plot")
    if not os.path.exists(plot_directory):
        os.makedirs(plot_directory)

    histogram_save_path = os.path.join(
        folder_info, "plot", "histogram-min-dist.png"
    )
    plot_histogram(shortest_dist_list, histogram_save_path, num_of_files)

    print("Histogram saved. Please check the 'plot' folder of the cif folder.")

    if isInteractiveMode:
        prompt_dist_threshold = (
            "\nNow, please enter the threashold distance (unit in Å)"
        )
        dist_threshold = click.prompt(prompt_dist_threshold, type=float)

    # Move CIF files with min distance below the threshold
    move_files_save_csv(
        files_lst,
        skipped_indices,
        shortest_dist_list,
        loop_tags,
        dist_threshold,
        filtered_folder,
        folder_info,
        result_df,
    )
