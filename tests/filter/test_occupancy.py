from os.path import join
from cifcleaner.filter.occupancy import (
    copy_files_based_on_atomic_occupancy_mixing,
)
from cifcleaner.util.folder import (
    get_cif_file_count_from_directory,
    remove_directories,
)


# Move files - should be 2 files per each folder
def test_copy_files_based_on_atomic_occupancy_mixing():
    base_dir = "tests/cifs/occupancy"
    deficiency_atomic_mixing_dir = join(
        base_dir, "occupancy_deficiency_atomic_mixing"
    )
    full_occupancy_atomic_mixing_dir = join(
        base_dir, "occupancy_full_occupancy_atomic_mixing"
    )
    deficiency_no_atomic_mixing_dir = join(
        base_dir, "occupancy_deficiency_no_atomic_mixing"
    )
    full_occupancy_dir = join(base_dir, "occupancy_full_occupancy")

    directory_list = [
        deficiency_atomic_mixing_dir,
        full_occupancy_atomic_mixing_dir,
        deficiency_no_atomic_mixing_dir,
        full_occupancy_dir,
    ]
    # Setup: Ensure the environment is clean before testing
    remove_directories(directory_list)

    copy_files_based_on_atomic_occupancy_mixing(base_dir, False)
    assert (
        get_cif_file_count_from_directory(base_dir) == 8
    ), "Expected 8 files in the test folder"

    deficiency_atomic_mixing_dir_cif_count = get_cif_file_count_from_directory(
        deficiency_atomic_mixing_dir
    )
    full_occupancy_atomic_mixing_dir_cif_count = (
        get_cif_file_count_from_directory(full_occupancy_atomic_mixing_dir)
    )
    deficiency_no_atomic_mixing_dir_cif_count = (
        get_cif_file_count_from_directory(deficiency_no_atomic_mixing_dir)
    )
    full_occupancy_dir_cif_count = get_cif_file_count_from_directory(
        full_occupancy_dir
    )

    assert (
        deficiency_atomic_mixing_dir_cif_count == 2
    ), "Not all expected files were copied."
    assert (
        full_occupancy_atomic_mixing_dir_cif_count == 2
    ), "Not all expected files were copied."
    assert (
        deficiency_no_atomic_mixing_dir_cif_count == 2
    ), "Not all expected files were copied."
    assert (
        full_occupancy_dir_cif_count == 2
    ), "Not all expected files were copied."

    # Finish: remove generated folders
    remove_directories(directory_list)
