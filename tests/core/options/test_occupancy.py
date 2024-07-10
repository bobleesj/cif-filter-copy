import pytest
import shutil
from core.options.occupancy import copy_files_based_on_atomic_occupancy_mixing
from cifkit.utils.folder import get_file_count


@pytest.fixture
def tmp_dir_path(tmpdir):
    source_dir = "tests/data/occupancy"
    tmp_dir_path = shutil.copytree(source_dir, tmpdir.join("occupancy"))
    return tmp_dir_path


@pytest.mark.fast
def test_copy_files_based_on_atomic_occupancy_mixing(tmp_dir_path):
    assert get_file_count(tmp_dir_path) == 8

    copy_files_based_on_atomic_occupancy_mixing(tmp_dir_path)

    deficiency_atomic_mixing_dir = tmp_dir_path.join(
        "occupancy_deficiency_atomic_mixing"
    )
    full_occupancy_atomic_mixing_dir = tmp_dir_path.join(
        "occupancy_deficiency_without_atomic_mixing"
    )
    deficiency_no_atomic_mixing_dir = tmp_dir_path.join("occupancy_full_occupancy")
    full_occupancy_dir = tmp_dir_path.join("occupancy_full_occupancy_atomic_mixing")

    assert get_file_count(deficiency_atomic_mixing_dir) == 2
    assert get_file_count(full_occupancy_atomic_mixing_dir) == 2
    assert get_file_count(deficiency_no_atomic_mixing_dir) == 2
    assert get_file_count(full_occupancy_dir) == 2
