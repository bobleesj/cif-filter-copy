import click
import os
import pandas as pd
import time
from click import style, echo
from preprocess import cif_parser, supercell
from filter import min_distance
from util import folder, prompt
import matplotlib.pyplot as plt


def get_cif_folder_info(cif_dir_path, is_interactive_mode=True):
    global results
    results = []
    supercell_method = None

    start_time = time.time()
    if is_interactive_mode:
        supercell_method = get_user_input()

    if not is_interactive_mode:
        cif_dir_path = cif_dir_path

    cif_file_list = folder.get_cif_file_path_list_from_directory(cif_dir_path)
    overall_start_time = time.time()
    supercell_atom_count_list = []

    if not supercell_method:
        echo(
            "> Your default option is generating a 2x2x2 supercell for "
            "files more than 100 atoms in the unit cell.",
        )
        supercell_method = 3

    for i, file_path in enumerate(cif_file_list, start=1):
        start_time = time.time()
        min_dist, supercell_points = min_distance.get_min_dist_per_file(file_path)
        num_of_atoms = len(supercell_points)
        filename_base = os.path.basename(file_path)
        prompt.print_progress_current(i, filename_base, supercell_points, len(cif_file_list))

        elapsed_time = time.time() - start_time

        # Append a row to the log csv file
        data = {
            "file": filename_base,
            "supecell_atom_count": num_of_atoms,
            "min_dist": round(min_dist, 3),
            "processing_time_s": round(elapsed_time, 3),
        }
        results.append(data)

        prompt.print_finished_progress(filename_base, num_of_atoms, elapsed_time)

    # Save histogram on size
    supercell_size_histogram_save_path = os.path.join(
        cif_dir_path, "plot", "histogram-supercell-size.png"
    )
    plot_supercell_size_histogram(
        supercell_atom_count_list,
        supercell_size_histogram_save_path,
        len(cif_file_list),
        cif_dir_path,
    )

    # Save csv
    save_results_to_csv(results, cif_dir_path)
    total_elapsed_time = time.time() - overall_start_time
    print(f"Total processing time for all files: {total_elapsed_time:.2f} s")


def get_user_input():
    supercell_method = None

    supercell_method = prompt.get_user_input_on_supercell_method()
    return supercell_method


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

