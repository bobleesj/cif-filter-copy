import pytest
import shutil
from core.options.element import move_files_based_on_elements
from cifkit.utils.folder import get_file_count


@pytest.fixture
def tmp_dir_path(tmpdir):
    source_dir = "tests/data/element"
    tmp_dir_path = shutil.copytree(source_dir, tmpdir.join("element"))
    return tmp_dir_path


@pytest.mark.fast
def test_move_files_based_on_one_element_containing(tmp_dir_path):
    """
    Test contain 1 element
    """
    # Initially there are 5 files
    assert get_file_count(tmp_dir_path) == 5

    elements = ["Ni"]
    # Move files based on composition
    move_files_based_on_elements(
        tmp_dir_path, is_interactive_mode=False, elements=elements, option=2
    )
    dest_path = tmp_dir_path.join("element_contain_Ni")
    assert get_file_count(dest_path) == 2
    assert get_file_count(tmp_dir_path) == 3


@pytest.mark.fast
def test_move_files_based_on_two_elements_containing(tmp_dir_path):
    """
    Test contain 2 elements
    """
    # Initially there are 5 files
    assert get_file_count(tmp_dir_path) == 5

    elements = ["Ni", "Si"]
    # Move files based on composition
    move_files_based_on_elements(
        tmp_dir_path, is_interactive_mode=False, elements=elements, option=2
    )
    dest_path = tmp_dir_path.join("element_contain_Ni_Si")
    assert get_file_count(dest_path) == 4
    assert get_file_count(tmp_dir_path) == 1


@pytest.mark.fast
def test_move_files_based_on_one_elements_matching(tmp_dir_path):
    """
    Test exact match 3 elements
    """
    # Initially there are 5 files
    assert get_file_count(tmp_dir_path) == 5

    elements = ["Y", "Fe", "Si"]
    # Move files based on composition
    move_files_based_on_elements(
        tmp_dir_path, is_interactive_mode=False, elements=elements, option=1
    )
    dest_path = tmp_dir_path.join("element_exact_Y_Fe_Si")
    assert get_file_count(dest_path) == 1
    assert get_file_count(tmp_dir_path) == 4
