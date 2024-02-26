import click
import os
import pandas as pd
import time
from click import style
import preprocess.cif_parser as cif_parser
import preprocess.supercell as supercell
import util.folder as folder
import filter.info as info
import shutil

def get_user_input():
    max_atoms_count = click.prompt('Enter the maximum atoms in the supercell (files above this number will be moved)', type=int)
    return max_atoms_count

def print_intro_prompt():
    print("Move CIF files to a separate directory if the number of atoms in the supercell exceed the input provided by the user")

def move_files_based_on_supercell_size(script_directory):
    print_intro_prompt()

    global results, folder_info  # Declare both variables as global # This allows the results variable to be accessed by other functions
    results = []

    max_atoms_count = get_user_input()

    folder_info = folder.choose_CIF_directory(script_directory)
    folder_name = os.path.basename(folder_info)
    filtered_folder_name = f"{folder_name}_filter_max_atom_count"
    filtered_folder = os.path.join(folder_info, filtered_folder_name)

    files_lst = [os.path.join(folder_info, file) for file in os.listdir(folder_info) if file.endswith('.cif')]

    for idx, file_path in enumerate(files_lst, start=1):
        # Extract filename and number of atoms first
        filename_base = os.path.basename(file_path)
        CIF_block = cif_parser.get_CIF_block(file_path)
        CIF_loop_values = cif_parser.get_loop_values(CIF_block, cif_parser.get_loop_tags())
        all_coords_list = supercell.get_coords_list(CIF_block, CIF_loop_values)
        all_points, _, _ = supercell.get_points_and_labels(all_coords_list, CIF_loop_values)
        num_of_atoms = len(all_points)

        # Display the information
        click.echo(style(f"Processing {filename_base} with {num_of_atoms} atoms...", fg="blue"))
        if not os.path.exists(filtered_folder):
                os.mkdir(filtered_folder)
                
        if num_of_atoms > max_atoms_count:
            click.echo(style(f"Moved - {filename_base} has {num_of_atoms} atoms", fg="yellow"))
            new_file_path = os.path.join(filtered_folder, os.path.basename(file_path))
        
            filtered_flag = "Yes"
            shutil.move(file_path, new_file_path)
        
        data = {
            "CIF file": filename_base,
            "Number of atoms in supercell": num_of_atoms,
        }
        results.append(data)

        print(f"Processed {filename_base} with {num_of_atoms} atoms ({idx}/{len(files_lst)})")

    folder.save_to_csv_directory(folder_info, pd.DataFrame(results), "supercell_size")
    # Get the # of atoms from each CIF file

    # Move files

    # Save log

