import os
import click
from core.utils import intro, prompt
from cifkit import CifEnsemble
from cifkit.utils import folder


def move_files_based_on_elements(cif_dir_path):
    """
    Move CIF files based on elements specified by the user, with the option
    to exactly match or contain the elements in the file's composition.
    """
    intro.prompt_element_intro()
    ensemble = CifEnsemble(cif_dir_path)

    # Prompt for elements
    elements_input = click.prompt(
        "Q1. Enter the elements to filter by, separated by a space (Ex: 'Er Co')",
        type=str,
    )
    elements = elements_input.split()
    elements_str = "_".join(elements)

    # Ask user for the type of filter
    click.echo("\nQ2. Now choose the filter method:")
    click.echo("[1] Exactly match the elements")
    click.echo("[2] Contain at least one of the elements ")
    filter_choice = click.prompt("Enter your choice (1 or 2)", type=int)

    # Folder info
    folder_name = os.path.basename(cif_dir_path)

    if filter_choice == 1:
        filtered_file_paths = ensemble.filter_by_elements_exact_matching(
            elements
        )
        destination_directory = os.path.join(
            cif_dir_path, f"{folder_name}_exact_{elements_str}"
        )
    else:
        filtered_file_paths = ensemble.filter_by_elements_containing(elements)
        destination_directory = os.path.join(
            cif_dir_path, f"{folder_name}_contain_{elements_str}"
        )

    # Move files
    folder.move_files(destination_directory, filtered_file_paths)

    # Print summary:
    print("Summary:")
    print(
        f"{len(filtered_file_paths)} moved to"
        f" {destination_directory} out of {ensemble.file_count} files."
    )
    prompt.print_done_with_option("filter by elements")
