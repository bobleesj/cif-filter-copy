
import click
import os
import glob
import pandas as pd
import time
import shutil
from click import style
import preprocess.cif_parser as cif_parser
import preprocess.supercell as supercell
import util.folder as folder
import numpy as np
import matplotlib.pyplot as plt
import util.log as log
import textwrap

def plot_histogram(distances, save_path, num_of_files):
    plt.figure(figsize=(10,6))
    plt.hist(distances, bins=50, color='blue', edgecolor='black')
    plt.title(f"Histogram of Shortest Distances of {num_of_files} files")
    plt.xlabel('Distance (Å)')
    plt.ylabel('Number of CIF Files')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    # Save the figure with 300 DPI
    plt.savefig(save_path, dpi=300)
    plt.show()
    print("histogram.png saved in the plot folder")        


def parse_CIF(file_path, loop_tags):
    """
    Parse the CIF data from the given file path.
    """
    CIF_block = cif_parser.get_CIF_block(file_path)
    cell_lengths, cell_angles_rad = supercell.process_cell_data(CIF_block)
    CIF_loop_values = cif_parser.get_loop_values(CIF_block, loop_tags)
    all_coords_list = supercell.get_coords_list(CIF_block, CIF_loop_values)
    all_points, unique_labels, unique_atoms_tuple = supercell.get_points_and_labels(all_coords_list, CIF_loop_values)
    
    return CIF_block, cell_lengths, cell_angles_rad, all_coords_list, all_points, unique_labels, unique_atoms_tuple


def move_files_based_on_min_dist(script_directory):
    """Filters and moves CIF files based on the shortest atomic distance."""
    introductory_paragraph = textwrap.dedent("""\
    ===
    Welcome to the CIF Atomic Distance Filter Tool!

    This tool reads CIF files and calculates the shortest atomic distance for each file. 
    Once these distances are determined, it displays a histogram, allowing you to visually 
    understand the distribution of the shortest atomic distances for all processed CIF files.

    You will then be prompted to enter a distance threshold after you close the histogram.
    Based on this threshold, CIF files having the shortest atomic distance less than the given
    threshold will be moved to a new sub-directory.

    At the end, a comprehensive log will be saved in CSV format, capturing:
    1. File names of CIFs.
    2. Compound formula for each CIF.
    3. Shortest atomic distance computed.
    4. Whether the file was moved (filtered) based on the threshold.
    5. Number of atoms in each file's supercell.

    Additionally, you can optionally choose to skip files based on the number of unique atoms 
    present in the supercell.

    Let's get started!
    ===
    """)
    
    print(introductory_paragraph)
    shortest_dist_list = []
    # This set will store the indices of the skipped files
    skipped_indices = set()

    result_df = pd.DataFrame()

    
    click.echo("\nQ . Do you want to skip any CIF files based on the number of unique atoms in the supercell? Any file above the number will be skipped.")
    skip_based_on_atoms = click.confirm('(Default: N)', default=False)
    print()

    if skip_based_on_atoms:
        click.echo("Enter the threshold for the maximum number of atoms in the supercell.")
        MAX_ATOMS_COUNT = click.prompt('Files with atoms exceeding this count will be skipped', type=int)
    else:
        MAX_ATOMS_COUNT = float('inf')  # A large number to essentially disable skipping
    

    # Get folder info, loop tags, files
    folder_info = folder.choose_CIF_directory(script_directory)
    folder_name = os.path.basename(folder_info)  # Extract the name of the chosen folder
    filtered_folder_name = f"{folder_name}_filter_dist_min"
    filtered_folder = os.path.join(folder_info, filtered_folder_name)  # Adjusted path to be a sub-directory of chosen folder
    files_lst = [os.path.join(folder_info, file) for file in os.listdir(folder_info) if file.endswith('.cif')]
    num_of_files = len(files_lst)
    loop_tags = cif_parser.get_loop_tags()


    # Process each CIF file
    for idx, file_path in enumerate(files_lst, start=1):
        
        filename_base = os.path.basename(file_path)
        print(f"Processing {filename_base} ({idx}/{num_of_files})")
        
        result = parse_CIF(file_path, loop_tags)
        CIF_block, cell_lengths, cell_angles_rad, _, all_points, _, _ = result
        num_of_atoms = len(all_points)

        if num_of_atoms > MAX_ATOMS_COUNT:
            click.echo(style(f"Skipped - {filename_base} has {num_of_atoms} atoms", fg="yellow"))
            skipped_indices.add(idx)
            continue

        atomic_pair_list = supercell.get_atomic_pair_list(all_points, cell_lengths, cell_angles_rad)
        # Sort the atomic_pair_list based on the 'distance' key
        sorted_atomic_pairs = sorted(atomic_pair_list, key=lambda x: x['distance'])

        # The atomic pair with the shortest distance
        shortest_distance_pair = sorted_atomic_pairs[0]
        shortest_dist = shortest_distance_pair['distance']        
        shortest_dist_list.append(shortest_dist)


    # Create histogram
    plot_directory = os.path.join(folder_info, "plot")
    if not os.path.exists(plot_directory):
        os.makedirs(plot_directory)

    histogram_save_path = os.path.join(folder_info, "plot", "histogram.png")
    plot_histogram(shortest_dist_list, histogram_save_path, num_of_files)

    # Prompt the user for the threshold after they've seen the histogram
    DISTANCE_THRESHOLD = click.prompt('\nNow, please enter the threashold distance (unit in Å)', type=float)

    # Now, use the computed shortest distances to move the files based on the provided threshold
    processed_files_count = 0
    for idx, file_path in enumerate(files_lst, start=1):
        # Skip indices above MAX_ATOMS_COUNT
        if idx in skipped_indices:
            continue

        filename_base = os.path.basename(file_path)
        shortest_dist = shortest_dist_list[processed_files_count]  # Retrieve the precomputed shortest distance based on processed files count
        processed_files_count += 1

        # Re-calculate the formula_string here before using it for the DataFrame
        result = parse_CIF(file_path, loop_tags)
        CIF_block, cell_lengths, cell_angles_rad, all_coords_list, all_points, unique_labels, unique_atoms_tuple = result
        num_of_atoms = len(all_points)
        _, _, formula_string = cif_parser.extract_formula_and_atoms(CIF_block)

        # Initialize the "Filtered" flag
        filtered_flag = "No"

        # If the file meets the threshold criterion, update the flag
        if shortest_dist < DISTANCE_THRESHOLD:
            if not os.path.exists(filtered_folder):
                os.mkdir(filtered_folder)
            
            # Full path to where the file will be moved
            new_file_path = os.path.join(filtered_folder, os.path.basename(file_path))
            
            # If the file already exists in the destination, delete it
            if os.path.exists(new_file_path):
                os.remove(new_file_path)

            filtered_flag = "Yes"
            shutil.move(file_path, new_file_path)

        new_row = pd.DataFrame({
            "Entry": [CIF_block.name],
            "Compound": [formula_string],
            "Shortest distance": [shortest_dist],
            "Filtered": [filtered_flag],
            "Number of atoms": [len(all_points)]
        })

        result_df = pd.concat([result_df, new_row], ignore_index=True)

    folder.save_to_csv_directory(folder_info, result_df, "filter_dist_min_log")
