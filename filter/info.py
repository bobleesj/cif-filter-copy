import click
import os
import pandas as pd
import time
from click import style, echo
from preprocess import cif_parser, supercell
from util import folder, prompt
import matplotlib.pyplot as plt


def get_cif_folder_info(cif_dir_path, is_interactive_mode=True):
    global results
    results = []
    supercell_method = None

    start_time = time.time()
    if is_interactive_mode:
        is_dist_computed, supercell_method = get_user_input()

    if not is_interactive_mode:
        cif_dir_path = cif_dir_path
        is_dist_computed = True

    files_lst = [
        os.path.join(cif_dir_path, file)
        for file in os.listdir(cif_dir_path)
        if file.endswith(".cif")
    ]
    overall_start_time = time.time()
    supercell_atom_count_list = []

    if not supercell_method:
        echo(
            "> Your default option is generating a 2x2x2 supercell for "
            "files more than 100 atoms in the unit cell.",
        )
        supercell_method = 3

    for idx, file_path in enumerate(files_lst, start=1):
        start_time = time.time()
        filename_base = os.path.basename(file_path)
        num_of_atoms, min_distance = get_num_of_atoms_shortest_dist(
            file_path, is_dist_computed, supercell_method
        )
        click.echo(
            style(f"Processing {filename_base} with {num_of_atoms} atoms...")
        )
        supercell_atom_count_list.append(num_of_atoms)

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

        prompt.print_progress(filename_base, num_of_atoms, elapsed_time, True)

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


def get_user_input():
    supercell_method = None
    is_min_dist_computed = click.confirm(
        "Do you want to calculate the minimum distance?",
        default=False,
    )

    supercell_method = prompt.get_user_input_on_supercell_method()
    return is_min_dist_computed, supercell_method


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


def save_results_to_csv(results, folder_info):
    if results:
        if "Min distance" in results[0]:
            folder.save_to_csv_directory(
                folder_info, pd.DataFrame(results), "info"
            )


def get_num_of_atoms_shortest_dist(
    file_path, is_dist_computed, supercell_method
):
    CIF_block = cif_parser.get_cif_block(file_path)
    cell_lengths, cell_angles_rad = cif_parser.get_cell_lenghts_angles_rad(
        CIF_block
    )
    CIF_loop_values = cif_parser.get_loop_values(
        CIF_block, cif_parser.get_loop_tags()
    )
    all_coords_list = supercell.get_coords_list(CIF_block, CIF_loop_values)
    all_points, _, _ = supercell.get_points_and_labels(
        all_coords_list, CIF_loop_values, supercell_method
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
