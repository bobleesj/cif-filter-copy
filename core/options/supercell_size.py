import click
from os.path import join
from core.utils import prompt
from core.utils.histogram import plot_supercell_size_histogram
from cifkit import CifEnsemble


def move_files_based_on_supercell_size(
    cif_dir_path, is_interactive_mode=True, max_atoms_threshold=1000
):
    ensemble = CifEnsemble(cif_dir_path)
    # Generate all supercell in the file and plot histogram
    atom_counts = []
    for idx, cif in enumerate(ensemble.cifs, start=1):
        atom_counts.append(cif.supercell_atom_count)

    plot_supercell_size_histogram(cif_dir_path, atom_counts, ensemble.file_count)

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
    filtered_dir_path = join(
        ensemble.dir_path, f"supercell_above_{min_atom_count}_below{max_atom_count}"
    )

    # Move filtered files to a new directory
    if filtered_file_paths:
        ensemble.move_cif_files(filtered_file_paths, filtered_dir_path)

    print(f"Moved {len(filtered_file_paths)} files to {filtered_dir_path}")
    prompt.print_done_with_option(
        f"supercell_above_{min_atom_count}_below_{max_atom_count}"
    )
