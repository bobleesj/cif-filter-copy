import os
import glob
import pytest
import pandas as pd
import shutil
from filter.min_distance import move_files_based_on_min_dist

def test_files_removed():
    base_dir = "test/bad_cif_files/min_dist"
    target_dir = os.path.join(base_dir, "min_dist_filter_dist_min")
    histogram_path = os.path.join(base_dir, "plot", "histogram.png")
    csv_file_path = os.path.join(base_dir, "csv", "min_dist_filter_dist_min_log.csv")

    # Setup: Ensure the environment is clean before testing
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    if os.path.exists(csv_file_path):
        os.remove(csv_file_path)
    if os.path.exists(histogram_path):
        os.remove(histogram_path)

    # Count the number of .cif files in base_dir before the test
    initial_cif_files_count = len(glob.glob(os.path.join(base_dir, "*.cif")))

    # Run the function in non-interactive mode
    move_files_based_on_min_dist(base_dir, isInteractiveMode=False)
    
    # Assertions for moved files
    moved_files_count = len(glob.glob(os.path.join(target_dir, "*.cif")))
    assert moved_files_count == initial_cif_files_count, "Not all expected files were moved."

    moved_files = glob.glob(os.path.join(target_dir, "*.cif"))
    assert len(moved_files) > 0, "Expected files to be moved to the filter directory."

    # Check that a non-empty CSV file is produced
    assert os.path.exists(csv_file_path), "CSV log file was not created."
    csv_data = pd.read_csv(csv_file_path)
    assert len(csv_data.index) == moved_files_count, f"CSV log does not match the number of moved files. Expected {moved_files_count}, got {len(csv_data.index)}."

    # # Move the files back to their original location
    for file_path in moved_files:
        shutil.move(file_path, base_dir)

    # Cleanup: Remove the folders and files created by the test
    shutil.rmtree(target_dir, ignore_errors=True)  # Remove the target directory and its contents
    if os.path.exists(csv_file_path):
        os.remove(csv_file_path)  # Remove the CSV file
    if os.path.exists(histogram_path):
        os.remove(histogram_path)  # Remove the histogram image file
    if os.path.exists(os.path.dirname(csv_file_path)):
        shutil.rmtree(os.path.dirname(csv_file_path), ignore_errors=True)  # Remove the csv directory if it's empty
    if os.path.exists(os.path.dirname(histogram_path)):
        shutil.rmtree(os.path.dirname(histogram_path), ignore_errors=True)  # Remove the plot directory if it's empty