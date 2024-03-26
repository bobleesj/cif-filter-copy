import pandas as pd
from os.path import join, exists
from cifcleaner.filter.tags import move_files_based_on_tags
from cifcleaner.util.folder import (
    remove_directories,
    remove_file,
    get_cif_file_count_from_directory,
    move_files,
    get_cif_file_path_list_from_directory,
)


def test_move_files_based_on_tags():
    """
    Tests the move_files_based_on_tags function to ensure it
    correctly moves CIF files based on the tags appearing on the 3rd line

    Out of the 3 files present, only 2 should be moved according to their tags, with one file remaining unmoved.
    The test will fail if these conditions are not met, indicating an issue with the file moving process.
    """

    base_dir = "tests/cifs/tags"
    cif_ht_tag_dir = join(base_dir, "tags_ht")
    cif_m_tag_dir = join(base_dir, "tags_m")
    csv_file_path = join(base_dir, "csv", "tags_tags_log.csv")
    cif_tag_dir_list = [cif_ht_tag_dir, cif_m_tag_dir]

    # Setup: ensure the environment is clean before testing
    remove_directories(cif_tag_dir_list)
    remove_file(csv_file_path)

    # Count the number of .cif files in base_dir before the test
    initial_cif_files_count = get_cif_file_count_from_directory(base_dir)

    # Run the function in non-interactive mode
    move_files_based_on_tags(base_dir, is_interactive_mode=False)

    # There should be one file in each ht and m tags for testing
    moved_ht_cif_file_count = get_cif_file_count_from_directory(cif_ht_tag_dir)
    moved_m_cif_file_count = get_cif_file_count_from_directory(cif_m_tag_dir)

    assert moved_ht_cif_file_count == 1, "Not all expected files were moved."
    assert moved_m_cif_file_count == 1, "Not all expected files were moved."
    assert exists(csv_file_path), "CSV log file was not created."

    total_cif_file_moved_count = (
        moved_ht_cif_file_count + moved_m_cif_file_count
    )
    csv_data = pd.read_csv(csv_file_path)
    assert (
        len(csv_data.index) == total_cif_file_moved_count
    ), f"CSV log does not match the # of moved files."

    # Move the files back to their original location
    moved_ht_cif_file_path_list = get_cif_file_path_list_from_directory(
        cif_ht_tag_dir
    )
    moved_m_cif_file_path_list = get_cif_file_path_list_from_directory(
        cif_m_tag_dir
    )

    move_files(base_dir, moved_ht_cif_file_path_list)
    move_files(base_dir, moved_m_cif_file_path_list)

    # Check the folder contains a total of 3 CIF files as started
    assert initial_cif_files_count == get_cif_file_count_from_directory(
        base_dir
    )

    # Cleanup: Remove the folders and files created by the test
    remove_directories(cif_tag_dir_list)
    remove_file(csv_file_path)
