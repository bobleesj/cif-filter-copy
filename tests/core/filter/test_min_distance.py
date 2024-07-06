import pytest
from core.options.min_distance import filter_files_by_min_dist
from cifkit.utils.folder import get_file_paths, copy_files, get_file_count


@pytest.mark.slow
def test_filter_files_by_min_dist(tmpdir):
    # Setup initial directory paths
    source_dir = "tests/data/min_dist"
    copy_files(tmpdir, get_file_paths(source_dir))

    # Paths for filtered results and logs
    tmp_filtered_dir = tmpdir / "min_dist_below_2.6"

    """
    ("tests/data/min_dist/311764.cif", 2.613),
    ("tests/data/min_dist/382882.cif", 2.584),
    ("tests/data/min_dist/453919.cif", 2.621),
    ("tests/data/min_dist/453316.cif", 2.625),
    ("tests/data/min_dist/382886.cif", 2.592),
    """

    # Initial file count (For non-interactive default is 2.6 A)
    assert get_file_count(tmpdir) == 5
    filter_files_by_min_dist(str(tmpdir), isInteractiveMode=False)
    assert get_file_count(tmp_filtered_dir) == 2
    assert get_file_count(tmpdir) == 3
