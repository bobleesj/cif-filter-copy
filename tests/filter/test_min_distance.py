import pandas as pd
from os.path import join, exists
from filter.min_distance import move_files_based_on_min_dist
from util.folder import (
    remove_directories,
    remove_file,
    get_cif_file_count_from_directory,
    move_files,
    get_cif_file_path_list_from_directory,
)

"""
def test_move_files_based_on_min_dist():
    base_dir = "test/filter/cif/min_dist"
    filtered_dir = join(base_dir, "min_dist_filter_dist_min")

    histogram_path = join(base_dir, "plot", "histogram-min-dist.png")
    csv_file_path = join(base_dir, "csv", "min_dist_filter_dist_min_log.csv")

    # Step 1. Setup
    remove_directories([filtered_dir])
    remove_file(histogram_path)
    remove_file(csv_file_path)
    
    # Count the number of .cif files in base_dir before the test
    initial_cif_files_count = get_cif_file_count_from_directory(base_dir)

    # Step 2. Run the function in non-interactive mode
    move_files_based_on_min_dist(base_dir, isInteractiveMode=False)
    
    # Assertions for moved files
    moved_files_count = get_cif_file_count_from_directory(filtered_dir)
    assert moved_files_count == initial_cif_files_count, "Not all expected files were moved."

    filtered_cif_file_path_list = get_cif_file_path_list_from_directory(filtered_dir)
    assert len(filtered_cif_file_path_list) > 0, "Expected files to be moved to the filter directory."

    # Check that a non-empty CSV file is produced
    assert exists(csv_file_path), "CSV log file was not created."
    csv_data = pd.read_csv(csv_file_path)
    assert len(csv_data.index) == moved_files_count, f"CSV log does not match the # of moved files."
    
    # Bring the filtered CIF files back to the base directory
    move_files(base_dir, filtered_cif_file_path_list)

    # Step 3. Clean up
    remove_directories([filtered_dir])
    remove_file(csv_file_path)
    remove_file(histogram_path)
"""
