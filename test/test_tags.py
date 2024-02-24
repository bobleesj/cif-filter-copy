
import glob
import os
import pandas as pd
import shutil
from filter.tags import move_files_based_on_tags

def test_move_files_based_on_tags():
    """
    Tests the move_files_based_on_tags function to ensure it correctly moves CIF files based on the tags appearing on the 3rd line

    The function is expected to sort CIF files into 'ht' and 'm' subdirectories based on specific tags found within each file.
    This test will:
    - Clean up any pre-existing test directories and files.
    - Run the move_files_based_on_tags function in non-interactive mode.
    - Check that exactly one file has been moved to each of the 'ht' and 'm' directories, respectively.
    - Verify that a CSV log file is created and contains entries matching the number of moved files.
    - Perform cleanup after assertions to ensure a clean state for subsequent tests.
    
    Out of the 3 files present, only 2 should be moved according to their tags, with one file remaining unmoved.
    The test will fail if these conditions are not met, indicating an issue with the file moving process.
    """

    # Setup
    base_dir = "test/tag_cif_files"
    dir_tags_ht = os.path.join(base_dir, "tag_cif_files_ht")
    dir_tags_m = os.path.join(base_dir, "tag_cif_files_m")
    csv_file_path = os.path.join(base_dir, "csv", "tag_cif_files_tags_log.csv")  # Assuming the CSV log is stored here
    
    # Setup: Ensure the environment is clean before testing
    if os.path.exists(dir_tags_ht):
        shutil.rmtree(dir_tags_ht)
    if os.path.exists(dir_tags_m):
        shutil.rmtree(dir_tags_m)
    if os.path.exists(csv_file_path):
        os.remove(csv_file_path)

    # Count the number of .cif files in base_dir before the test
    initial_cif_files_count = len(glob.glob(os.path.join(base_dir, "*.cif")))

    # Run the function in non-interactive mode
    move_files_based_on_tags(base_dir, isInteractiveMode=False)

    # There should be one file in each ht and m tags for testing
    moved_ht_files_count = len(glob.glob(os.path.join(dir_tags_ht, "*.cif")))
    print(moved_ht_files_count)
    assert moved_ht_files_count == 1, "Not all expected files were moved."

    moved_m_files_count = len(glob.glob(os.path.join(dir_tags_m, "*.cif")))
    assert moved_m_files_count == 1, "Not all expected files were moved."

    # Check that a non-empty CSV file is produced
    assert os.path.exists(csv_file_path), "CSV log file was not created."

    total_files_moved_count= moved_ht_files_count+ moved_m_files_count
    csv_data = pd.read_csv(csv_file_path)
    assert len(csv_data.index) == total_files_moved_count, f"CSV log does not match the number of moved files. Expected {total_files_moved_count}, got {len(csv_data.index)}."

    # Move the files back to their original location
    moved_ht_files = glob.glob(os.path.join(dir_tags_ht, "*.cif"))
    moved_m_files = glob.glob(os.path.join(dir_tags_m, "*.cif"))

    for file_path in moved_ht_files:
        shutil.move(file_path, base_dir)

    for file_path in moved_m_files:
        shutil.move(file_path, base_dir)

    # Cleanup: Remove the folders and files created by the test
    if os.path.exists(csv_file_path):
        shutil.rmtree(os.path.dirname(csv_file_path), ignore_errors=True)  # Removes the CSV directory

    if os.path.exists(dir_tags_ht):
        shutil.rmtree(dir_tags_ht, ignore_errors=True)  # Removes the directory

    if os.path.exists(dir_tags_m):
        shutil.rmtree(dir_tags_m, ignore_errors=True)  # Corrected to remove directory

    # Check the folder contains a total of 3 CIF files as started
    assert initial_cif_files_count == len(glob.glob(os.path.join(base_dir, "*.cif")))









