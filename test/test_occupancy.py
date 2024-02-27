
import glob
import os
import pandas as pd
import shutil
import numpy as np
from filter.occupancy import copy_files_based_on_atomic_occupancy_mixing
from os.path import join, exists

def get_cif_count(directory):
    """Helper function to count .cif files in a given directory."""
    return len(glob.glob(os.path.join(directory, "*.cif")))

# Move files - should be 2 files per each folder
def test_copy_files_based_on_atomic_occupancy_mixing():
    base_dir = "test/occupancy_cif_files"
    deficiency_atomic_mixing_dir = join(base_dir, "occupancy_cif_files_deficiency_atomic_mixing")
    full_occupancy_atomic_mixing_dir = join(base_dir, "occupancy_cif_files_full_occupancy_atomic_mixing")
    deficiency_no_atomic_mixing_dir = join(base_dir, "occupancy_cif_files_deficiency_no_atomic_mixing")
    full_occupancy_dir = join(base_dir, "occupancy_cif_files_full_occupancy")

    # Setup: Ensure the environment is clean before testing
    if exists(deficiency_atomic_mixing_dir):
        shutil.rmtree(deficiency_atomic_mixing_dir)
    if exists(full_occupancy_atomic_mixing_dir):
        shutil.rmtree(full_occupancy_atomic_mixing_dir)
    if exists(deficiency_no_atomic_mixing_dir):
        shutil.rmtree(deficiency_no_atomic_mixing_dir)
    if exists(full_occupancy_dir):
        shutil.rmtree(full_occupancy_dir)

    # There should be a total of 8 files in the test folder
    copy_files_based_on_atomic_occupancy_mixing(base_dir, False)

    initial_cif_files_count = len(glob.glob(join(base_dir, "*.cif")))
    print(initial_cif_files_count)
    assert initial_cif_files_count == 8, "Expected 8 files in the test folder"
    
    deficiency_atomic_mixing_dir_cif_count = get_cif_count(deficiency_atomic_mixing_dir)
    full_occupancy_atomic_mixing_dir_cif_count = get_cif_count(full_occupancy_atomic_mixing_dir)
    deficiency_no_atomic_mixing_dir_cif_count = get_cif_count(deficiency_no_atomic_mixing_dir)
    full_occupancy_dir_cif_count = get_cif_count(full_occupancy_dir)

    assert deficiency_atomic_mixing_dir_cif_count == 2, "Not all expected files were copied."
    assert full_occupancy_atomic_mixing_dir_cif_count == 2, "Not all expected files were copied."
    assert deficiency_no_atomic_mixing_dir_cif_count == 2, "Not all expected files were copied."
    assert full_occupancy_dir_cif_count == 2, "Not all expected files were copied."

    shutil.rmtree(deficiency_atomic_mixing_dir, ignore_errors=True) 
    shutil.rmtree(full_occupancy_atomic_mixing_dir, ignore_errors=True)
    shutil.rmtree(deficiency_no_atomic_mixing_dir, ignore_errors=True)
    shutil.rmtree(full_occupancy_dir, ignore_errors=True)

