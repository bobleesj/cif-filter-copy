

import glob
import os
import pandas as pd
import shutil
import numpy as np
from filter.info import get_CIF_files_info


def test_get_CIF_files_info():
    base_dir = "test/info_cif_files"
    csv_file_path = os.path.join(base_dir, "csv", "info_cif_files_info.csv")
    
    # Setup: Ensure the environment is clean before testing
    if os.path.exists(csv_file_path):
        os.remove(csv_file_path)

    # There should be 1 file
    initial_cif_files_count = len(glob.glob(os.path.join(base_dir, "*.cif")))
    get_CIF_files_info(base_dir, False)
    print("initial_cif_files_count", initial_cif_files_count)
    assert os.path.exists(csv_file_path), "CSV log file was not created."
    csv_data = pd.read_csv(csv_file_path)

    # Compare the # of files and # of rows
    assert len(csv_data.index) == initial_cif_files_count, "CSV log does not match the number of moved files."

    # Test the number of atoms for URhIn
    URhIn_supercell_atom_count = csv_data[csv_data['CIF file'] == 'URhIn.cif']['Number of atoms in supercell'].iloc[0]
    error_msg_supercell_atom_count = f"Incorrect number of atoms for URhIn, expected 206, got {URhIn_supercell_atom_count}"
    assert URhIn_supercell_atom_count == 206,error_msg_supercell_atom_count

    # Test the shortest distance for URhIn
    error_msg_shortest_dist = "Incorrect shortest distance for URhIn, expected ~2.69678, got {urhIn_min_distance}"
    URhIn_shortest_dist = csv_data[csv_data['CIF file'] == 'URhIn.cif']['Min distance'].iloc[0]
    assert np.isclose(URhIn_shortest_dist, 2.69678, atol=1e-4), error_msg_shortest_dist

    # Cleanup: Remove the folders and files created by the test
    if os.path.exists(csv_file_path):
        shutil.rmtree(os.path.dirname(csv_file_path), ignore_errors=True)