import os
import pytest
import preprocess.cif_parser as cif_parser
import preprocess.supercell as supercell
import filter.format as format
from util.folder import get_cif_file_path_list_from_directory
import preprocess.cif_editor as cif_editor
import shutil
import tempfile


def preprocess_supercell_operation(file_path):
    """
    Processes a CIF file by extracting compound information, formatting the file,
    extracting CIF block and loop values, and getting coordinates and labels from the supercell.
    Raises exceptions if the CIF file is improperly formatted or if there is an error in processing.
    """
    cif_parser.get_compound_phase_tag_id_from_third_line(file_path)
    cif_editor.preprocess_cif_file_on_label_element(file_path)
    CIF_block = cif_parser.get_CIF_block(file_path)
    CIF_loop_values = cif_parser.get_loop_values(CIF_block, cif_parser.get_loop_tags())
    print(CIF_loop_values)
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
    Verifies that CIF files considered to be correctly formatted with no errors.
    This function ensures the preprocessing operation can handle valid CIF files as expected.
    """

    good_files_dir = "test/good_cif_files_test"
    cif_file_path_list = get_cif_file_path_list_from_directory(good_files_dir)
    for cif_file_path in cif_file_path_list:
        try:
            cif_editor.preprocess_supercell_operation(cif_file_path)
        except Exception as e:
            assert False, f"An unexpected error occurred for {cif_file_path}: {str(e)}"


def test_preprocess_cif_file_on_label_element_on_type_1():
    cif_directory = "test/format_label_cif_files/symbolic_atom_label_type_1"

    # Create a temporary directory to store the copied folder
    temp_dir = tempfile.mkdtemp()
    temp_cif_directory = os.path.join(temp_dir, os.path.basename(cif_directory))
    shutil.copytree(cif_directory, temp_cif_directory)

    cif_file_path_list = get_cif_file_path_list_from_directory(temp_cif_directory)
    for temp_cif_file_path in cif_file_path_list:   
        cif_editor.preprocess_cif_file_on_label_element(temp_cif_file_path)
        
        # Perform your tests on the modified temporary file
        CIF_block = cif_parser.get_CIF_block(temp_cif_file_path)
        CIF_loop_values = cif_parser.get_loop_values(CIF_block, cif_parser.get_loop_tags())
        num_element_labels = len(CIF_loop_values[0])

        for i in range(num_element_labels):
            atom_type_label = CIF_loop_values[0][i]
            atom_type_symbol = CIF_loop_values[1][i]
            parsed_atom_type_symbol = cif_parser.get_atom_type(atom_type_label)
            error_msg = "atom_type_symbol and atom_type_label do not match after preprocessing."
            assert atom_type_symbol == parsed_atom_type_symbol, error_msg
            

def run_preprocess_test_on_cif_files(cif_directory):
    # Create a temporary directory to store the copied folder
    temp_dir = tempfile.mkdtemp()
    temp_cif_directory = os.path.join(temp_dir, os.path.basename(cif_directory))
    shutil.copytree(cif_directory, temp_cif_directory)

    cif_file_path_list = get_cif_file_path_list_from_directory(temp_cif_directory)
    for temp_cif_file_path in cif_file_path_list:
        cif_editor.preprocess_cif_file_on_label_element(temp_cif_file_path)
        
        # Perform tests on the modified temporary file
        CIF_block = cif_parser.get_CIF_block(temp_cif_file_path)
        CIF_loop_values = cif_parser.get_loop_values(CIF_block, cif_parser.get_loop_tags())
        num_element_labels = len(CIF_loop_values[0])

        for i in range(num_element_labels):
            atom_type_label = CIF_loop_values[0][i]
            atom_type_symbol = CIF_loop_values[1][i]
            parsed_atom_type_symbol = cif_parser.get_atom_type(atom_type_label)
            assert atom_type_symbol == parsed_atom_type_symbol, \
                   "atom_type_symbol and atom_type_label do not match after preprocessing."
    
    # Clean up the temporary directory after tests
    shutil.rmtree(temp_dir)

def test_preprocess_cif_file_on_label_element_type_1():
    cif_directory = "test/format_label_cif_files/symbolic_atom_label_type_1"
    run_preprocess_test_on_cif_files(cif_directory)

def test_preprocess_cif_file_on_label_element_type_2():
    cif_directory = "test/format_label_cif_files/symbolic_atom_label_type_2"
    run_preprocess_test_on_cif_files(cif_directory)

def test_preprocess_cif_file_on_label_element_type_3():
    cif_directory = "test/format_label_cif_files/symbolic_atom_label_type_3"
    run_preprocess_test_on_cif_files(cif_directory)

def test_preprocess_cif_file_on_label_element_type_4():
    cif_directory = "test/format_label_cif_files/symbolic_atom_label_type_4"
    run_preprocess_test_on_cif_files(cif_directory)

def test_preprocess_cif_file_on_label_element_type_5():
    cif_directory = "test/format_label_cif_files/symbolic_atom_label_type_5"
    run_preprocess_test_on_cif_files(cif_directory)

def test_preprocess_cif_file_on_label_element_type_6():
    cif_directory = "test/format_label_cif_files/symbolic_atom_label_type_6"
    run_preprocess_test_on_cif_files(cif_directory)

def test_preprocess_cif_file_on_label_element_type_7():
    cif_directory = "test/format_label_cif_files/symbolic_atom_label_type_7"
    run_preprocess_test_on_cif_files(cif_directory)

# Manual testing from each CIF File from a folder
def test_preprocess_cif_file_on_label_element_type_mixed():
    cif_directory = "test/format_label_cif_files/symbolic_atom_label_type_mixed"
    
    temp_dir = tempfile.mkdtemp()
    temp_cif_directory = os.path.join(temp_dir, os.path.basename(cif_directory))
    shutil.copytree(cif_directory, temp_cif_directory)

    cif_file_path_list = get_cif_file_path_list_from_directory(temp_cif_directory)

    for temp_cif_file_path in cif_file_path_list:
        cif_editor.preprocess_cif_file_on_label_element(temp_cif_file_path)
        content_lines = cif_parser.get_loop_content(temp_cif_file_path,
                                                              "_atom_site_occupancy")

        filename = os.path.basename(temp_cif_file_path)
        if filename == "1020250.cif":
            assert len(content_lines) == 3
            assert content_lines[1].strip() == "Co Co 8 c 0.25 0.25 0.25 1"

        if filename == "312084.cif":
            assert len(content_lines) == 3
            assert content_lines[0].strip() == "Ge1A Ge 8 h 0 0.06 0.163 0.500"
            assert content_lines[1].strip() == "Pd1B Pd 8 h 0 0.06 0.163 0.500"

        if filename == "1020251.cif":
            assert len(content_lines) == 3
            assert content_lines[1].strip() == "Rh Rh 8 c 0.25 0.25 0.25 1"

        if filename == "1633288.cif":
            assert len(content_lines) == 7
            assert content_lines[2].strip() == "Dy Dy 4 i 0 0.5 0.1935 1"

        if filename == "1049941.cif":
            assert len(content_lines) == 11
            assert content_lines[0].strip() == "Pr1 Pr 4 j 0.02076 0.5 0.30929 1"
            assert content_lines[-1].strip() == "In4 In 2 a 0 0 0 1"

        if filename == "381111.cif":
            assert len(content_lines) == 6
            assert content_lines[0].strip() == "Ni1A Ni 4 j 0 0.172 0.5 0.88(1)"
            assert content_lines[1].strip() == "Ga1B Ga 4 j 0 0.172 0.5 0.12(1)"
        
        # Type 7
        if filename == "1817279.cif":
            assert len(content_lines) == 3
            assert content_lines[0].strip() == "Fe1 Fe 1 d 0.5 0.5 0.5 0.99(4)"
            assert content_lines[1].strip() == "Pt2 Pt 1 d 0.5 0.5 0.5 0.01(4)"

        # Type 7
        if filename == "1817275.cif":
            assert len(content_lines) == 4
            assert content_lines[0].strip() == "Fe1 Fe 1 d 0.5 0.5 0.5 0.97(4)"
            assert content_lines[1].strip() == "Pt2 Pt 1 d 0.5 0.5 0.5 0.03(4)"
            assert content_lines[2].strip() == "Pt1 Pt 1 a 0 0 0 0.98(4)"
            assert content_lines[3].strip() == "Fe2 Fe 1 a 0 0 0 0.02(4)"
            
    shutil.rmtree(temp_dir)
