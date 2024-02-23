import os
import glob
import pytest
import preprocess.cif_parser as cif_parser
import preprocess.supercell as supercell
import filter.format as format

def preprocess_supercell_operation(file_path):
    result = cif_parser.get_compound_phase_tag_id_from_third_line(file_path)
    _, compound_formula, _, _ = result
    format.preprocess_cif_file(file_path, compound_formula)
    CIF_block = cif_parser.get_CIF_block(file_path)
    CIF_loop_values = cif_parser.get_loop_values(CIF_block, cif_parser.get_loop_tags())
    all_coords_list = supercell.get_coords_list(CIF_block, CIF_loop_values)
    _, _, _, = supercell.get_points_and_labels(all_coords_list, CIF_loop_values)

def run_test_for_error_type(error_dir, expected_error_message):
    files = glob.glob(os.path.join(error_dir, "*.cif"))

    for file_path in files:
        with pytest.raises(Exception) as excinfo:
            preprocess_supercell_operation(file_path)
        assert str(excinfo.value) == expected_error_message, f"Failed on {file_path}"

def test_bad_cif_files():
    error_cases = [
        ("test/bad_cif_files/error_thrid_line", "The CIF file is wrongly formatted in the third line"),
        ("test/bad_cif_files/error_format", "Wrong number of values in the loop"),
        ("test/bad_cif_files/error_op", "An error occurred while processing symmetry operation"),
        ("test/bad_cif_files/error_coords", "Missing atomic coordinates"),
        ("test/bad_cif_files/error_label", "Different elements found in atom site and label"),
    ]

    for error_dir, expected_error_message in error_cases:
        run_test_for_error_type(error_dir, expected_error_message)


# Assuming preprocess_supercell_operation is defined as before
def test_good_cif_files():
    good_files_dir = "test/good_cif_files"
    files = glob.glob(os.path.join(good_files_dir, "*.cif"))

    for file_path in files:
        try:
            preprocess_supercell_operation(file_path)
        except Exception as e:
            assert False, f"An unexpected error occurred for {file_path}: {str(e)}"


# Test properly formatted CIF files return no error