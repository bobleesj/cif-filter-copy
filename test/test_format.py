import os
import glob
import pytest
import preprocess.cif_parser as cif_parser
import preprocess.supercell as supercell
import filter.format as format


"""
This test module contains a suite of tests for the CIF file preprocessing and validation functions.
It includes tests that:

- Verify the preprocessing of CIF files for extracting compound information, formatting the file, 
  and extracting structural data through the 'preprocess_supercell_operation' function.
- Ensure that known bad CIF files raise appropriate exceptions, with specific error messages 
  for different types of expected issues. This is done through the 'test_bad_cif_files_with_error_message' function.
- Check for the handling of CIF files that are expected to be problematic but do not have a defined error message 
  through the 'test_bad_cif_files_without_error_message' function.
- Confirm that CIF files without any known issues are processed correctly and do not raise any exceptions, 
  ensuring that the system works correctly with valid input data through the 'test_good_cif_files' function.
"""

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

    files = glob.glob(os.path.join(error_dir, "*.cif"))

    for file_path in files:
        with pytest.raises(Exception) as excinfo:
            preprocess_supercell_operation(file_path)
        assert str(excinfo.value) == expected_error_message, f"Failed on {file_path}"


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
    files = glob.glob(os.path.join(cif_error_others, "*.cif"))

    for file_path in files:
        with pytest.raises(Exception):
            preprocess_supercell_operation(file_path)


def test_good_cif_files():
    """
    Verifies that CIF files considered to be correctly formatted are processed without errors.
    This function ensures the preprocessing operation can handle valid CIF files as expected.
    """

    good_files_dir = "test/good_cif_files"
    files = glob.glob(os.path.join(good_files_dir, "*.cif"))

    for file_path in files:
        try:
            preprocess_supercell_operation(file_path)
        except Exception as e:
            assert False, f"An unexpected error occurred for {file_path}: {str(e)}"

