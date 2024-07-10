import pandas as pd
import pytest
import shutil
from os.path import exists
from core.options.info import get_cif_folder_info
from cifkit.utils.folder import get_file_count


@pytest.fixture
def tmp_dir_path(tmpdir):
    source_dir = "tests/data/info"
    tmp_dir_path = shutil.copytree(source_dir, tmpdir.join("info"))
    return tmp_dir_path


@pytest.mark.fast
def test_cif_folder_info(tmp_dir_path):
    assert get_file_count(tmp_dir_path) == 3
    get_cif_folder_info(tmp_dir_path, is_interactive_mode=False, compute_dist=False)

    csv_file_path = tmp_dir_path.join("csv", "info_info.csv")
    assert exists(csv_file_path)
    csv_data = pd.read_csv(csv_file_path)
    assert len(csv_data.index) == 3
    expected_filenames = {250134, 250143, 250164}
    assert set(csv_data["Filename"]) == expected_filenames


@pytest.mark.fast
def test_cif_folder_info_with_dist(tmp_dir_path):
    assert get_file_count(tmp_dir_path) == 3
    get_cif_folder_info(tmp_dir_path, is_interactive_mode=False, compute_dist=True)

    csv_file_path = tmp_dir_path.join("csv", "info_info_with_dist.csv")
    assert exists(csv_file_path)
    csv_data = pd.read_csv(csv_file_path)
    assert len(csv_data.index) == 3
    expected_filenames = {250134, 250143, 250164}
    assert set(csv_data["Filename"]) == expected_filenames
