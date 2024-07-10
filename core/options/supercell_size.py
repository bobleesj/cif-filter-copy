import click
from os.path import join
from core.utils import prompt, intro, object
from core.utils.histogram import plot_supercell_size_histogram


def move_files_based_on_supercell_size(
    cif_dir_path,
    is_interactive_mode=True,
    min_atom_count: int = None,
    max_atom_count: int = None,
):
    intro.prompt_suppercell_size_intro()
    ensemble = object.init_cif_ensemble(cif_dir_path)
    # Generate all supercell in the file and plot histogram
    atom_counts = []
    for idx, cif in enumerate(ensemble.cifs, start=1):
        atom_counts.append(cif.supercell_atom_count)

    plot_supercell_size_histogram(cif_dir_path, atom_counts, ensemble.file_count)

    if is_interactive_mode:
        min_atom_count = click.prompt(
            "\nEnter the min number of atoms in the supercell", type=int
        )

        max_atom_count = click.prompt(
            "\nEnter the max number of atoms in the supercell", type=int
        )

    # Enter the range
    filtered_file_paths = ensemble.filter_by_supercell_count(
        min_atom_count, max_atom_count
    )

    # Filter files based on the minimum distance
    destination_path = join(
        ensemble.dir_path,
        f"supercell_above_{min_atom_count}_below_{max_atom_count}",
    )

    # Move filtered files to a new directory
    if filtered_file_paths:
        ensemble.move_cif_files(filtered_file_paths, destination_path)

    prompt.print_moved_files_summary(
        filtered_file_paths, ensemble.file_count, destination_path
    )
    prompt.print_done_with_option(
        f"supercell_above_{min_atom_count}_below_{max_atom_count}"
    )
