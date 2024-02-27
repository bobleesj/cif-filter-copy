import os
import glob
import pytest
import preprocess.cif_parser as cif_parser
import preprocess.supercell as supercell
import filter.format as format
from util.folder import get_cif_file_path_list_from_directory


def preprocess_supercell_operation(file_path):
    """
    Processes a CIF file by extracting compound information, formatting the file,
    extracting CIF block and loop values, and getting coordinates and labels from the supercell.
    Raises exceptions if the CIF file is improperly formatted or if there is an error in processing.
    """
    result = cif_parser.get_compound_phase_tag_id_from_third_line(file_path)
    _, compound_formula, _, _ = result
    format.preprocess_cif_file(file_path, compound_formula)
    CIF_block = cif_parser.get_CIF_block(file_path)
    CIF_loop_values = cif_parser.get_loop_values(CIF_block, cif_parser.get_loop_tags())
    all_coords_list = supercell.get_coords_list(CIF_block, CIF_loop_values)
    _, _, _, = supercell.get_points_and_labels(all_coords_list, CIF_loop_values)


def run_test_for_error_type(error_dir, expected_error_message):
    """
    Runs tests for CIF files in a specified directory expected to raise specific error messages.
    Verifies that the correct exception is raised for each file, ensuring error handling works as expected.
    """

    cif_file_path_list = get_cif_file_path_list_from_directory(error_dir)

    for cif_file_path in cif_file_path_list:
        with pytest.raises(Exception) as excinfo:
            preprocess_supercell_operation(cif_file_path)
        assert str(excinfo.value) == expected_error_message, f"Failed on {cif_file_path}"


def test_bad_cif_files_with_error_message():
    """
    Tests various types of known bad CIF files that should raise specific errors.
    Each test case checks for a particular type of formatting or content error within the CIF file.
    """
    error_cases = [
        ("test/bad_cif_files/error_thrid_line", "The CIF file is wrongly formatted in the third line"),
        ("test/bad_cif_files/error_format", "Wrong number of values in the loop"),
        ("test/bad_cif_files/error_op", "An error occurred while processing symmetry operation"),
        ("test/bad_cif_files/error_coords", "Missing atomic coordinates"),
        ("test/bad_cif_files/error_label", "Different elements found in atom site and label"),
    ]

    for error_dir, expected_error_message in error_cases:
        run_test_for_error_type(error_dir, expected_error_message)


def test_bad_cif_files_without_error_message():
    """
    Tests CIF files known to be bad but without checking for specific error messages.
    Ensures that any processing error is caught, verifying that problematic files are indeed recognized.
    """
    cif_error_others = "test/bad_cif_files_error_others"
    cif_file_path_list = get_cif_file_path_list_from_directory(cif_error_others)

    for cif_file_path in cif_file_path_list:
        with pytest.raises(Exception):
            preprocess_supercell_operation(cif_file_path)


def test_good_cif_files():
    """
    Verifies that CIF files considered to be correctly formatted are processed without errors.
    This function ensures the preprocessing operation can handle valid CIF files as expected.
    """

    good_files_dir = "test/good_cif_files"
    cif_file_path_list = get_cif_file_path_list_from_directory(good_files_dir)
    for cif_file_path in cif_file_path_list:
        try:
            preprocess_supercell_operation(cif_file_path)
        except Exception as e:
            assert False, f"An unexpected error occurred for {cif_file_path}: {str(e)}"

