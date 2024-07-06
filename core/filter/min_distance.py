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
    dir_path = ensemble.dir_path
    saved_folder_path = join(dir_path, f"min_dist_below_{dist_threshold}")
    if filtered_file_paths:
        ensemble.move_cif_files(filtered_file_paths, saved_folder_path)
    print(f"Moved {len(filtered_file_paths)} files to {saved_folder_path}")
