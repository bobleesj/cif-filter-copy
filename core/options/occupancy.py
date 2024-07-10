import os
import shutil
from core.utils import intro, object


def copy_files_based_on_atomic_occupancy_mixing(cif_dir_path):
    intro.prompt_occupancy_intro()
    ensemble = object.init_cif_ensemble(cif_dir_path)

    for cif in ensemble.cifs:
        copy_to_dir(ensemble.dir_path, cif.site_mixing_type, cif.file_path)


def copy_to_dir(cif_dir_path, suffix, file_path):
    """
    Copy a file to a directory, skipping if the file already exists.
    """
    folder_name = os.path.basename(cif_dir_path)
    destination_directory = os.path.join(cif_dir_path, f"{folder_name}_{suffix}")
    destination_file_path = os.path.join(
        destination_directory, os.path.basename(file_path)
    )

    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    if not os.path.exists(destination_file_path):
        shutil.copy(file_path, destination_file_path)
