import pytest
import shutil
from core.options.supercell_size import move_files_based_on_supercell_size
from cifkit.utils.folder import get_file_count
from cifkit import CifEnsemble


@pytest.mark.now
def test_move_files_based_on_supercell_size(tmpdir):
    # Setup initial directory paths
    source_dir = "tests/data/supercell"
    tmp_dir_path = shutil.copytree(source_dir, tmpdir.join("supercell"))

    dest_path = tmp_dir_path.join("supercell_above_300_below_500")

    # 12 files should be present in the original directory
    assert get_file_count(tmp_dir_path) == 12

    move_files_based_on_supercell_size(tmp_dir_path, is_interactive_mode=False)

    # 2 files should be moved
    assert get_file_count(dest_path) == 9

    # 3 files should remain in the original directory
    assert get_file_count(tmp_dir_path) == 3
