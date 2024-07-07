# import pytest
# from cifkit.utils.folder import get_file_paths, copy_files, get_file_count
# from core.options.tags import move_files_based_on_tags


# @pytest.mark.now
# def test_move_files_based_on_tags(tmpdir):
#     source_dir = "tests/data/tags"
#     copy_files(tmpdir, get_file_paths(source_dir))
#     assert get_file_count(tmpdir) == 3
#     move_files_based_on_tags(str(tmpdir))
#     assert get_file_count(tmpdir) == 1
