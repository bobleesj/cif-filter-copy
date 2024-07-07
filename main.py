import os

from core.options import (
    min_distance,
    tags,
    supercell_size,
    info,
    format,
    occupancy,
)
from core.utils import folder


def main():
    script_dir_path = os.path.dirname(os.path.abspath(__file__))

    print("\nWelcome! Please choose an option to proceed:")
    options = {
        "1": "Move files based on unsupported format after pre-formatting",
        "2": "Move files based on unreasonable distance",
        "3": "Move files based on supercell atom count",
        "4": "Move files based on tags",
        "5": "Copy files based on atomic occupancy and mixing",
        "6": "Get file info in the folder",
    }

    for key, value in options.items():
        print(f"[{key}] {value}")

    choice = input("Enter your choice (1-6): ")

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
        format.format_files(cif_dir_path)

    # 2. Relocate CIF files with unreasonable distances
    elif choice == "2":
        min_distance.move_files_based_on_min_dist(cif_dir_path)

    # 4. Relocate CIF based the number of atoms in the supercell
    elif choice == "3":
        supercell_size.move_files_based_on_supercell_size(cif_dir_path)
    # 3. Relocate CIF based on tags

    elif choice == "4":
        tags.move_files_based_on_tags(cif_dir_path)

    # 5. Copy files based on atomic occupancy and atomic mixing
    elif choice == "5":
        occupancy.copy_files_based_on_atomic_occupancy_mixing(cif_dir_path)

    # 6. Get info per file in the folder
    elif choice == "6":
        info.get_cif_folder_info(cif_dir_path)


if __name__ == "__main__":
    main()
