import os
import click
import time
from core.utils import intro, prompt, object
from cifkit import CifEnsemble
from cifkit.utils import folder
from core.utils import connections


def move_files_based_on_coordination_number(
    cif_dir_path: str,
    is_interactive_mode=True,
    numbers: list[int] = None,
    option: int = None,
) -> None:
    intro.prompt_coordination_number_intro()
    ensemble = object.init_cif_ensemble(cif_dir_path)

    if is_interactive_mode:
        # Prompt for elements
        CN_input = click.prompt(
            "Q1. Enter the coordination number(s) to filter by,"
            " separated by a space (Ex: '12 16')",
            type=str,
        ).strip()

        # Split by space
        numbers = [number for number in CN_input.split() if number]

        # Convert to int
        numbers = [int(num) for num in numbers]

        # Ask user for the type of filter
        click.echo("\nQ2. Now choose your option:")
        click.echo("[1] Move files exactly matching the coordination numbers")
        click.echo("[2] Move files containing at least one of the coordination numbers")
        filter_choice = click.prompt("Enter your choice (1 or 2)", type=int)
    else:
        filter_choice = option

    _filter_and_move_files(ensemble, filter_choice, cif_dir_path, numbers)


def _filter_and_move_files(
    ensemble: CifEnsemble,
    filter_choice: int,
    cif_dir_path: str,
    numbers: list[int],
) -> None:
    # Folder info
    numbers_str = "_".join(str(number) for number in numbers)
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
        try:
            CN_values_computed = connections.get_CN_values(cif)
        except Exception as e:
            print(f"Skip {file_name} due to error occurred while computing CN: {e}")
            continue
        if filter_choice == 1:
            destination_path = os.path.join(
                cif_dir_path, f"{folder_name}_CN_exact_{numbers_str}"
            )
            # Check if the CN values are exactly the same
            if set(numbers) == CN_values_computed:
                filtered_file_paths.add(cif.file_path)

        elif filter_choice == 2:
            destination_path = os.path.join(
                cif_dir_path, f"{folder_name}_CN_contain_{numbers_str}"
            )
            # Check if at least one of the CN values is present
            if any(num in CN_values_computed for num in numbers):
                filtered_file_paths.add(cif.file_path)

        elapsed_time = time.perf_counter() - file_start_time
        prompt.print_finished_progress(file_name, atom_count, elapsed_time)

    _move_files_and_prompt(
        filtered_file_paths, destination_path, file_count, overall_start_time
    )


def _move_files_and_prompt(
    filtered_file_paths: set[str],
    destination_path: str,
    file_count: int,
    overall_start_time: float,
) -> None:
    if filtered_file_paths:
        # Create folder and move files
        folder.move_files(destination_path, filtered_file_paths)

    overall_elapsed_time = time.perf_counter() - overall_start_time
    prompt.print_total_time(overall_elapsed_time, file_count)
    prompt.print_moved_files_summary(filtered_file_paths, file_count, destination_path)
    prompt.print_done_with_option("filter by coordination numbers")
