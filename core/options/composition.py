import os
import shutil
from core.utils import intro, prompt, object


def move_files_based_on_composition_type(cif_dir_path: str) -> None:
    """
    Organize CIF files in directories based on their composition type.
    """
    intro.prompt_composition_intro()

    ensemble = object.init_cif_ensemble(cif_dir_path)

    # Define the composition type naming conventions
    composition_types = {
        1: "unary",
        2: "binary",
        3: "ternary",
        4: "quaternary",
        5: "quinary",
    }

    for cif in ensemble.cifs:
        # Use 'other' for any composition type beyond 5
        comp_type_name = composition_types.get(cif.composition_type, "other")
        move_to_dir(ensemble.dir_path, comp_type_name, cif.file_path)

    print_summary(ensemble.composition_type_stats, ensemble.file_count)

    prompt.print_done_with_option("move files based on composition type")


def move_to_dir(cif_dir_path: str, suffix: str, file_path: str) -> None:
    """
    Copy a CIF file to a directory based on composition type,
    skipping if the file already exists.
    """
    folder_name = os.path.basename(cif_dir_path)
    destination_directory = os.path.join(cif_dir_path, f"{folder_name}_{suffix}")

    # Make folder
    os.makedirs(destination_directory, exist_ok=True)

    destination_file_path = os.path.join(
        destination_directory, os.path.basename(file_path)
    )

    # Move the file if it does not exist
    if not os.path.exists(destination_file_path):
        shutil.move(file_path, destination_file_path)


def print_summary(stats, total_files_moved):
    """
    Print a summary of files moved by composition type and their percentage.
    """
    print(f"Total files moved: {total_files_moved}")
    for comp_type, count in stats.items():
        percentage = (count / total_files_moved) * 100
        print(f"Composition type {comp_type}: {count} files ({percentage:.2f}%)")
