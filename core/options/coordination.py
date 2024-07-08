import os
import click
import time
from core.utils import intro, prompt
from cifkit import CifEnsemble
from cifkit.utils import folder


def move_files_based_on_coordination_number(cif_dir_path: str) -> None:
    intro.prompt_coordination_number_intro()
    ensemble = CifEnsemble(cif_dir_path)

    # Prompt for elements
    CN_input = click.prompt(
        "Q1. Enter the coordination number(s) to filter by,"
        " separated by a space (Ex: '12 16')",
        type=str,
    )

    numbers = CN_input.split()
    # click.echo("You've entered:", numbers)
    numbers_str = "_".join(numbers)
    numbers = [int(num) for num in numbers]

    # Ask user for the type of filter
    click.echo("\nQ2. Now choose your option:")
    click.echo("[1] Move files exactly matching the coordination numbers")
    click.echo(
        "[2] Move files containing at least one of the coordination numbers"
    ).strip()
    filter_choice = click.prompt("Enter your choice (1 or 2)", type=int)

    # Folder info
    overall_start_time = time.perf_counter()
    folder_name = os.path.basename(cif_dir_path)
    filtered_file_paths = set()

    for i, cif in enumerate(ensemble.cifs, start=1):
        file_name = cif.file_name
        atom_count = cif.supercell_atom_count
        file_count = ensemble.file_count

        # Track time
        file_start_time = time.perf_counter()
        prompt.print_progress_current(i, file_name, atom_count, file_count)

        # Compute CN values for each .cif
        CN_values = cif.CN_unique_values_by_min_dist_method

        if filter_choice == 1:
            destination_path = os.path.join(
                cif_dir_path, f"{folder_name}_CN_exact_{numbers_str}"
            )
            # Check if the CN values are exactly the same
            if set(numbers) == CN_values:
                filtered_file_paths.add()

        elif filter_choice == 2:
            destination_path = os.path.join(
                cif_dir_path, f"{folder_name}_CN_contain_{numbers_str}"
            )
            # Check if at least one of the CN values is present
            if any(num in CN_values for num in numbers):
                filtered_file_paths.add(cif.file_path)

        elapsed_time = time.perf_counter() - file_start_time
        prompt.print_finished_progress(file_name, atom_count, elapsed_time)

    if filtered_file_paths:
        # Create folder and move files
        folder.move_files(destination_path, filtered_file_paths)

    overall_elapsed_time = time.perf_counter() - overall_start_time
    prompt.print_total_time(overall_elapsed_time, file_count)
    prompt.print_moved_files_summary(
        filtered_file_paths, file_count, destination_path
    )
    prompt.print_done_with_option("filter by coordination numbers")
