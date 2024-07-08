import pytest
import shutil
from core.options.min_distance import filter_files_by_min_dist
from cifkit.utils.folder import get_file_count


@pytest.mark.slow
def test_filter_files_by_min_dist(tmpdir):
    # Setup initial directory paths
    source_dir = "tests/data/min_dist"
    tmp_dir_path = shutil.copytree(source_dir, tmpdir.join("dist"))

    """
    ("tests/data/min_dist/311764.cif", 2.613),
    ("tests/data/min_dist/382882.cif", 2.584),
    ("tests/data/min_dist/453919.cif", 2.621),
    ("tests/data/min_dist/453316.cif", 2.625),
    ("tests/data/min_dist/382886.cif", 2.592),
    """

    # Initial file count (For non-interactive default is 2.6 A)
    min_dist_below_path = tmp_dir_path.join("min_dist_below_2.6")
    assert get_file_count(tmp_dir_path) == 5
    filter_files_by_min_dist(tmp_dir_path, is_interactive_mode=False)

    # 2 files should be moved
    assert get_file_count(min_dist_below_path) == 2

    # 3 files should remain in the original directory
    assert get_file_count(tmp_dir_path) == 3
