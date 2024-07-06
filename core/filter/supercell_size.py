import click
import os
import pandas as pd
import shutil
from click import style
from os.path import join, exists
from core.utils import folder
from cifkit import CifEnsemble


def get_user_input():
    max_atoms_count = click.prompt(
        "\nEnter the maximum number of atoms in the supercell"
        " (files above this number will be moved)",
        type=int,
    )
    return max_atoms_count


def print_intro_prompt():
    print(
        "Move CIF files to a separate directory if the number"
        " of atoms in the supercell exceeds the input provided by the user."
    )


def move_files_based_on_supercell_size(
    cif_dir_path, is_interactive_mode=True, max_atoms_threshold=1000
):
    print_intro_prompt()
    
    df_rows = []

    if is_interactive_mode:
        max_atoms_threshold = get_user_input()

    file_moved_count = 0
    filtered_folder_name = f"supercell_size_above_{max_atoms_threshold}"
    filtered_folder_path = join(cif_dir_path, filtered_folder_name)
    os.makedirs(filtered_folder_path, exist_ok=True)
    
    ensemble = CifEnsemble(cif_dir_path)
    
    for idx, cif in enumerate(ensemble.cifs, start=1):
        filtered_flag = False
        
        if cif.supercell_atom_count > max_atoms_threshold:
            filtered_flag = True
            file_moved_count += 1

        data = {
            "CIF file": cif.file_name_without_ext,
            "Formula": cif.formula,
            "Number of atoms in supercell": cif.supercell_atom_count,
            "Moved": filtered_flag,
        }
        df_rows.append(data)
        
        # Move
        shutil.move(cif.file_path, filtered_folder_path) if filtered_flag else None

    
    print(f"{file_moved_count} files were moved to {filtered_folder_path}")
    folder.save_to_csv_directory(cif_dir_path, pd.DataFrame(df_rows), f"supercell_above_{max_atoms_threshold}")
