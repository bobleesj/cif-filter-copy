import os
import sys
from pathlib import Path

from filter import format, min_distance, excel, tags, supercell_size, info, occupancy
from util import folder

def main():
    script_dir_path = os.path.dirname(os.path.abspath(__file__))

    print("\nWelcome! Please choose an option to proceed:")
    options = {
        "1": "Move files based on unsupported CIF format after standardizing atomic labels",
        "2": "Move files based on unreasonable distance",
        "3": "Move files based on tags",
        "4": "Move files based on supercell atom count",
        "5": "Copy files based on atomic occupancy and mixing",
        "6": "Get file info in the folder",
        "7": "Check CIF folder content against Excel file",
    }

    for key, value in options.items():
        print(f"[{key}] {value}")

    choice = input("Enter your choice (1-7): ")

    if choice in options:
        print(f"You have chosen: {options[choice]}\n")
    else:
        print("Invalid choice!")
        return

    # Choose the folder
    cif_dir_path = folder.choose_dir(script_dir_path)
    
    if not cif_dir_path:
        print("No directory chosen. Exiting.")
        return
    
    # 1. Relocate CIF format with error
    if choice == "1":
        format.move_files_based_on_format_error(cif_dir_path)

    # 2. Relocate CIF files with unreasonable distances
    elif choice == "2":
        min_distance.move_files_based_on_min_dist(cif_dir_path)

    # 3. Relocate CIF based on tags
    elif choice == "3":
        tags.move_files_based_on_tags(cif_dir_path)

    # 4. Relocate CIF based the number of atoms in the supercell
    elif choice == "4":
        supercell_size.move_files_based_on_supercell_size(cif_dir_path)

    # 5. Copy files based on atomic occupancy and atomic mixing
    elif choice == "5":
        occupancy.copy_files_based_on_atomic_occupancy_mixing(cif_dir_path)

    # 6. Get info on the supercell
    elif choice == "6":
        info.get_cif_folder_info(cif_dir_path)

    # 7. Check missing files against Excel sheet
    elif choice == "7":
        excel.get_new_Excel_with_matching_entries(cif_dir_path, script_dir_path)


if __name__ == "__main__":
    main()
