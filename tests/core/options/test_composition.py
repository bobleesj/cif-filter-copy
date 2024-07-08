import pytest
import shutil
from core.options.composition import move_files_based_on_composition_type
from cifkit.utils.folder import get_file_count


@pytest.mark.fast
def test_move_files_based_on_composition(tmpdir):
    source_dir = "tests/data/composition"
    tmp_dir_path = shutil.copytree(source_dir, tmpdir.join("composition"))

    # Initially there are 5 files
    assert get_file_count(tmp_dir_path) == 5

    # Move files based on composition
    move_files_based_on_composition_type(tmp_dir_path)

    binary_path = tmp_dir_path.join("composition_binary")
    ternary_path = tmp_dir_path.join("composition_ternary")

    # 2 files are binary, 3 files are ternary
    assert get_file_count(binary_path) == 2
    assert get_file_count(ternary_path) == 3

    # 0 file remaining in the original directory
    assert get_file_count(tmp_dir_path) == 0
