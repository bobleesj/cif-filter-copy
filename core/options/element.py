import os
import click
from core.utils import intro, prompt, object
from cifkit.utils import folder


def move_files_based_on_elements(
    cif_dir_path: str,
    is_interactive_mode=True,
    elements: list[str] = None,
    option: int = None,
) -> None:
    """
    Move CIF files based on elements specified by the user, with the option
    to exactly match or contain the elements in the file's composition.
    """
    intro.prompt_element_intro()
    ensemble = object.init_cif_ensemble(cif_dir_path)

    if is_interactive_mode:
        elements_input = click.prompt(
            "Q1. Enter the elements to filter by, separated by a space (Ex: 'Er Co')",
            type=str,
        ).strip()
        elements = [element for element in elements_input.split() if element]
        elements_str = "_".join(elements)

        # Ask user for the type of filter
        click.echo("\nQ2. Now choose your option:")
        click.echo("[1] Move files exactly matching the elements")
        click.echo("[2] Move files containing at least one of the elements")
        filter_choice = click.prompt("Enter your choice (1 or 2)", type=int)
    else:
        elements_str = "_".join(elements)
        filter_choice = option

    # Folder info
    folder_name = os.path.basename(cif_dir_path)

    if filter_choice == 1:
        filtered_file_paths = ensemble.filter_by_elements_exact_matching(elements)
        destination_path = os.path.join(
            cif_dir_path, f"{folder_name}_exact_{elements_str}"
        )
    else:
        filtered_file_paths = ensemble.filter_by_elements_containing(elements)
        destination_path = os.path.join(
            cif_dir_path, f"{folder_name}_contain_{elements_str}"
        )

    if filtered_file_paths:
        # Move files
        folder.move_files(destination_path, filtered_file_paths)

    # Show summary of files moved
    prompt.print_moved_files_summary(
        filtered_file_paths, ensemble.file_count, destination_path
    )
    prompt.print_done_with_option("filter by elements")
