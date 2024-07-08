import pytest
import shutil
from core.options.tag import move_files_based_on_tags
from cifkit.utils.folder import get_file_count


@pytest.mark.now
def test_move_files_based_on_tags(tmpdir):
    source_dir = "tests/data/tag"
    tmp_dir_path = shutil.copytree(source_dir, tmpdir.join("tag"))

    # Initially there are 4 files
    assert get_file_count(tmp_dir_path) == 4

    # Move files based on tags
    move_files_based_on_tags(tmp_dir_path)

    ht_path = tmp_dir_path.join("tag_ht")
    rt_path = tmp_dir_path.join("tag_rt")

    # 2 files are be ht, 1 file is rt
    assert get_file_count(ht_path) == 2
    assert get_file_count(rt_path) == 1

    # 1 file remaining in the original directory
    assert get_file_count(tmp_dir_path) == 1
