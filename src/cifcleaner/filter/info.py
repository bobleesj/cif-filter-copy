import click
import os
import pandas as pd
import time
from click import style
from ..preprocess import cif_parser, supercell
from ..util import folder
import matplotlib.pyplot as plt


def plot_supercell_size_histogram(
    supercell_atom_count_list, save_path, num_of_files, folder_info
):
    plot_directory = os.path.join(folder_info, "plot")
    if not os.path.exists(plot_directory):
        os.makedirs(plot_directory)

    plt.figure(figsize=(10, 6))
    plt.hist(
        supercell_atom_count_list, bins=50, color="blue", edgecolor="black"
    )
    plt.title(f"Histogram of supercell atom count of {num_of_files} files")
    plt.xlabel("Number of atoms")
    plt.ylabel("Number of CIF Files")
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.savefig(save_path, dpi=300)
    print(f"Supercell size histogram has been also saved in {save_path}.")


def get_user_input():
    click.echo(
        "Do you want to skip any CIF files based on the number of unique atoms in the supercell?"
    )
    skip_based_on_atoms = click.confirm("(Default: N)", default=False)
    print()

    if skip_based_on_atoms:
        click.echo(
            "Enter the threshold for the maximum number of atoms in the supercell."
        )
        max_atoms_count = click.prompt(
            "Files with atoms exceeding this count will be skipped", type=int
        )
    else:
        max_atoms_count = float(
            "inf"
        )  # A large number to essentially disable skipping

    compute_min_distance = click.confirm(
        "Do you want to calculate the minimum distance? (it may require heavy computation)",
        default=False,
    )
    print()
    return max_atoms_count, compute_min_distance


def save_results_to_csv(results, folder_info):
    if results:
        if "Min distance" in results[0]:
            folder.save_to_csv_directory(
                folder_info, pd.DataFrame(results), "info"
            )


def get_num_of_atoms_shortest_dist(file_path, is_dist_computed):
    CIF_block = cif_parser.get_CIF_block(file_path)
    cell_lengths, cell_angles_rad = cif_parser.get_cell_lenghts_angles_rad(
        CIF_block
    )
    CIF_loop_values = cif_parser.get_loop_values(
        CIF_block, cif_parser.get_loop_tags()
    )
    all_coords_list = supercell.get_coords_list(CIF_block, CIF_loop_values)
    all_points, _, _ = supercell.get_points_and_labels(
        all_coords_list, CIF_loop_values
    )
    num_of_atoms = len(all_points)

    min_distance = None
    if is_dist_computed:
        atomic_pair_list = supercell.get_atomic_pair_list(
            all_points, cell_lengths, cell_angles_rad
        )
        sorted_atomic_pairs = sorted(
            atomic_pair_list, key=lambda x: x["distance"]
        )
        min_distance = sorted_atomic_pairs[0]["distance"]

    return num_of_atoms, min_distance


def get_cif_folder_info(cif_dir_path, is_interactive_mode=True):
    # Declare both variables as global
    global results
    results = []

    start_time = time.time()  # Start the timer
    if is_interactive_mode:
        max_atoms_count, is_dist_computed = get_user_input()

    if not is_interactive_mode:
        cif_dir_path = cif_dir_path
        max_atoms_count = 10000
        is_dist_computed = True

    files_lst = [
        os.path.join(cif_dir_path, file)
        for file in os.listdir(cif_dir_path)
        if file.endswith(".cif")
    ]
    overall_start_time = time.time()
    supercell_atom_count_list = []
    for idx, file_path in enumerate(files_lst, start=1):
        start_time = time.time()
        filename_base = os.path.basename(file_path)
        num_of_atoms, min_distance = get_num_of_atoms_shortest_dist(
            file_path, is_dist_computed
        )
        click.echo(
            style(
                f"Processing {filename_base} with {num_of_atoms} atoms...",
                fg="blue",
            )
        )
        supercell_atom_count_list.append(num_of_atoms)

        if num_of_atoms > max_atoms_count:
            click.echo(
                style(
                    f"Skipped - {filename_base} has {num_of_atoms} atoms",
                    fg="yellow",
                )
            )
            continue

        elapsed_time = time.time() - start_time

        # Append a row to the log csv file
        data = {
            "CIF file": filename_base,
            "Number of atoms in supercell": num_of_atoms,
            "Min distance": (
                min_distance if is_dist_computed else "N/A"
            ),  # Set to "N/A" if min distance wasn't computed
            "Processing time (s)": round(elapsed_time, 3),
        }
        results.append(data)

        print(
            f"Processed {filename_base} with {num_of_atoms} atoms ({idx}/{len(files_lst)})"
        )

    # Save histogram on size
    supercell_size_histogram_save_path = os.path.join(
        cif_dir_path, "plot", "histogram-supercell-size.png"
    )
    plot_supercell_size_histogram(
        supercell_atom_count_list,
        supercell_size_histogram_save_path,
        len(files_lst),
        cif_dir_path,
    )

    # Save csv
    save_results_to_csv(results, cif_dir_path)
    total_elapsed_time = time.time() - overall_start_time
    print(f"Total processing time for all files: {total_elapsed_time:.2f} s")
