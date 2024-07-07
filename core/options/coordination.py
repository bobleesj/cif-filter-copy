import os
import click
from core.utils import intro, prompt
from cifkit import CifEnsemble
from cifkit.utils import folder


def move_files_based_on_coordination_number(cif_dir_path):
    intro.prompt_element_intro()
    ensemble = CifEnsemble(cif_dir_path)

    # Prompt for elements
    CN_input = click.prompt(
        "Q1. Enter the coordination number to filter by, separated by a space (Ex: '12 16')",
        type=str,
    )

    numbers = CN_input.split()
    numbers_str = "_".join(numbers)
    numbers = [int(num) for num in numbers]

    # Ask user for the type of filter
    click.echo("\nQ2. Now choose the filter method:")
    click.echo("[1] Exactly match the coordination numbers")
    click.echo("[2] Contain at least one of the coordination numbers ")
    filter_choice = click.prompt("Enter your choice (1 or 2)", type=int)

    # Folder info
    folder_name = os.path.basename(cif_dir_path)

    if filter_choice == 1:
        filtered_file_paths = (
            ensemble.filter_by_CN_min_dist_method_exact_matching(numbers)
        )
        destination_directory = os.path.join(
            cif_dir_path, f"{folder_name}_exact_{numbers_str}"
        )
    else:
        filtered_file_paths = ensemble.filter_by_CN_min_dist_method_containing(
            numbers
        )
        destination_directory = os.path.join(
            cif_dir_path, f"{folder_name}_contain_{numbers_str}"
        )

    if filtered_file_paths:
        # Create folder and move files
        folder.move_files(destination_directory, filtered_file_paths)

    # Print summary:
    print("Summary:")
    print(
        f"{len(filtered_file_paths)} moved to"
        f" {destination_directory} out of {ensemble.file_count} files."
    )
    prompt.print_done_with_option("filter by coordination numbers")
