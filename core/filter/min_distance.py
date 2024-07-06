import pandas as pd
import click
from cifkit import CifEnsemble
from os.path import join


def move_files_based_on_min_dist(cif_dir):
    filter_files_by_min_dist(cif_dir)


def filter_files_by_min_dist(cif_dir, isInteractiveMode=True):
    if isInteractiveMode:
        prompt_dist_threshold = (
            "\nNow, please enter the threashold distance (unit in Å)"
        )
        dist_threshold = click.prompt(prompt_dist_threshold, type=float)
    else:
        dist_threshold = 2.6  # Default to 2.6 for testing

    ensemble = CifEnsemble(cif_dir)
    filtered_file_paths = ensemble.filter_by_min_distance(0.0, dist_threshold)
    saved_folder_path = join(ensemble.dir_path, f"min_dist_below_{dist_threshold}")
    if filtered_file_paths:
        ensemble.move_cif_files(filtered_file_paths, saved_folder_path)
    print(f"Moved {len(filtered_file_paths)} files to {saved_folder_path}")

    # Generate histogram

    # Generate log file

    # Create a DataFrame using the filenames and distances
    # df = pd.DataFrame({"file": file_path_list, "dist": file_min_dist_list})
    # folder.save_to_csv_directory(cif_dir, df, "min_dist_log")

    # # Create histogram directory and save
    # plot_directory = os.path.join(cif_dir, "plot")
    # if not os.path.exists(plot_directory):
    #     os.makedirs(plot_directory)

    # histogram_save_path = os.path.join(cif_dir, "plot", "histogram-min-dist.png")

    # plot_histogram(file_min_dist_list, histogram_save_path, num_of_files)
    # print("Histogram saved. Please check the 'plot' folder of the cif folder.")
