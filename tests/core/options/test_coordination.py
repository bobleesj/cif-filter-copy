import pytest
import shutil
from core.options.coordination import move_files_based_on_coordination_number
from cifkit.utils.folder import get_file_count


@pytest.fixture
def tmp_dir_path(tmpdir):
    source_dir = "tests/data/coordination"
    tmp_dir_path = shutil.copytree(source_dir, tmpdir.join("coordination"))
    return tmp_dir_path


@pytest.mark.slow
def test_move_files_based_on_one_number_containing(tmp_dir_path):
    """
    Test contain 1 number
    """
    assert get_file_count(tmp_dir_path) == 10

    numbers = [12]
    # Move files based on composition
    move_files_based_on_coordination_number(
        tmp_dir_path,
        is_interactive_mode=False,
        numbers=numbers,
        option=2,
    )

    dest_path = tmp_dir_path.join("coordination_CN_contain_12")
    assert get_file_count(dest_path) == 8
    assert get_file_count(tmp_dir_path) == 2


@pytest.mark.slow
def test_move_files_based_on_one_number_containing(tmp_dir_path):
    """
    Test contain 2 numbers
    """
    assert get_file_count(tmp_dir_path) == 10

    numbers = [11, 14]
    # Move files based on composition
    move_files_based_on_coordination_number(
        tmp_dir_path,
        is_interactive_mode=False,
        numbers=numbers,
        option=2,
    )

    dest_path = tmp_dir_path.join("coordination_CN_contain_11_14")
    assert get_file_count(dest_path) == 2
    assert get_file_count(tmp_dir_path) == 8


@pytest.mark.slow
def test_move_files_based_on_one_number_containing(tmp_dir_path):
    """
    Test match 1 number
    """
    assert get_file_count(tmp_dir_path) == 10

    numbers = [12]
    # Move files based on composition
    move_files_based_on_coordination_number(
        tmp_dir_path,
        is_interactive_mode=False,
        numbers=numbers,
        option=1,
    )

    dest_path = tmp_dir_path.join("coordination_CN_exact_12")
    assert get_file_count(dest_path) == 7
    assert get_file_count(tmp_dir_path) == 3
