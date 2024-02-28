
# 132 136

from preprocess.cif_parser import (get_atom_site_loop_end_start_line_indexes,
                                   get_atom_site_loop_content)
                                   

def test_get_atom_site_loop_end_start_line_indexes_URhIn():
    file_path = "test/parser_cif_files/URhIn.cif"
    start_index, end_index = get_atom_site_loop_end_start_line_indexes(file_path, "_atom_site_occupancy")
    assert (start_index, end_index) == (132, 136)


def test_get_atom_site_loop_end_start_line_indexes_ThSb():
    file_path = "test/parser_cif_files/ThSb.cif"
    start_index, end_index = get_atom_site_loop_end_start_line_indexes(file_path, "_atom_site_occupancy")
    print("start_index", start_index, end_index)
    assert (start_index, end_index) == (164, 166)


def test_get_atom_site_loop_content_URhIn():
    # Example usage, modify as needed for your specific requirements
    file_path = "test/parser_cif_files/URhIn.cif"
    content_lines = get_atom_site_loop_content(file_path, "_atom_site_occupancy")
    assert len(content_lines) == 4
    assert content_lines[0].strip() == "In1 In 3 g 0.2505 0 0.5 1"
    assert content_lines[3].strip() == "Rh2 Rh 1 a 0 0 0 1"


def test_get_atom_site_loop_content_ThSb():
    file_path = "test/parser_cif_files/ThSb.cif"
    content_lines = get_atom_site_loop_content(file_path, "_atom_site_occupancy")
    assert len(content_lines) == 2
    assert content_lines[0].strip() == "Sb Sb 1 b 0.5 0.5 0.5 1"
    assert content_lines[1].strip() == "Th Th 1 a 0 0 0 1"