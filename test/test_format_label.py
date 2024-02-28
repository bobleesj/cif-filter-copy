import os
import glob
import pytest
import preprocess.cif_parser as cif_parser
import preprocess.supercell as supercell
import filter.format as format
from util.folder import get_cif_file_path_list_from_directory
import pandas as pd
from os.path import join, exists
from filter.tags import move_files_based_on_tags
from util.folder import (
    remove_directories,
    remove_file,
    get_cif_file_count_from_directory,
    move_files,
    get_cif_file_path_list_from_directory
)

def test_preprocess_cif_file_on_label_element():
    print("let's get this over")
    base_dir = "test/format_label_cif_files"
    initial_cif_files_count = get_cif_file_count_from_directory(base_dir)

    # assert initial_cif_files_count == 1
    # cif_file_path_list = get_cif_file_path_list_from_directory(base_dir)
    # for idx, file_path in enumerate(cif_file_path_list, start=1):  # Use enumerate to get the index        
    #     error_msg_compoudn_formula = "The compound formula and the atom type symbol do not match."

    #     with pytest.raises(Exception) as excinfo:
    #         filename = os.path.basename(file_path)
    #         result = cif_parser.get_compound_phase_tag_id_from_third_line(file_path)
    #         _, compound_formula, _, _ = result
    #     assert str(excinfo.value) == error_msg_compoudn_formula

    # # Grab files


    # base_dir = "test/tag_cif_files"
    # cif_ht_tag_dir = join(base_dir, "tag_cif_files_ht")
    # cif_m_tag_dir = join(base_dir, "tag_cif_files_m")
    # csv_file_path = join(base_dir, "csv", "tag_cif_files_tags_log.csv")
    # cif_tag_dir_list = [cif_ht_tag_dir, cif_m_tag_dir]

    # result = cif_parser.get_compound_phase_tag_id_from_third_line(file_path)
    #         _, compound_formula, _, _ = result
    # # Setup: ensure the environment is clean before testing
    # remove_directories(cif_tag_dir_list)
    # remove_file(csv_file_path)

    # # Count the number of .cif files in base_dir before the test
    # initial_cif_files_count = get_cif_file_count_from_directory(base_dir)

    # # Run the function in non-interactive mode
    # move_files_based_on_tags(base_dir, is_interactive_mode=False)


# def preprocess_supercell_operation(file_path):
#     """
#     Processes a CIF file by extracting compound information, formatting the file,
#     extracting CIF block and loop values, and getting coordinates and labels from the supercell.
#     Raises exceptions if the CIF file is improperly formatted or if there is an error in processing.
#     """
#     result = cif_parser.get_compound_phase_tag_id_from_third_line(file_path)
#     _, compound_formula, _, _ = result
#     format.preprocess_cif_file_on_label_element(file_path, compound_formula)
#     CIF_block = cif_parser.get_CIF_block(file_path)
#     CIF_loop_values = cif_parser.get_loop_values(CIF_block, cif_parser.get_loop_tags())
#     print(CIF_loop_values)
#     all_coords_list = supercell.get_coords_list(CIF_block, CIF_loop_values)
#     _, _, _, = supercell.get_points_and_labels(all_coords_list, CIF_loop_values)


# def test_good_cif_files():
#     """
#     Verifies that CIF files considered to be correctly formatted are processed without errors.
#     This function ensures the preprocessing operation can handle valid CIF files as expected.
#     """

#     good_files_dir = "test/good_cif_files"
#     cif_file_path_list = get_cif_file_path_list_from_directory(good_files_dir)
#     for cif_file_path in cif_file_path_list:
#         try:
#             preprocess_supercell_operation(cif_file_path)
#         except Exception as e:
#             assert False, f"An unexpected error occurred for {cif_file_path}: {str(e)}"

