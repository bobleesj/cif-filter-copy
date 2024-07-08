import pytest
import shutil
from core.options.format import format_files
from cifkit.utils.folder import get_file_count


@pytest.mark.fast
def test_files_with_format_problem(tmpdir):
    # Assuming 'format' is a directory and copying it to a temporary directory
    source_dir_path = "tests/data/format"
    tmp_dir_path = shutil.copytree(source_dir_path, tmpdir.join("format"))

    # Apply formatting to files in the temporary directory
    format_files(tmp_dir_path)

    # Constructing the error path correctly
    error_path = tmp_dir_path.join("error_wrong_loop_value")
    assert get_file_count(error_path) == 1
