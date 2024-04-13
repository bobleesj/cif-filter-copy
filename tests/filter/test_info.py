import pandas as pd
import numpy as np
from os.path import join, exists

from filter.info import get_cif_folder_info
from util.folder import (
    remove_file,
    get_cif_file_count_from_directory,
)


def test_cif_folder_info():
    base_dir = "tests/cifs/info"
    csv_file_path = join(base_dir, "csv", "info_info.csv")

    # Setup
    remove_file(csv_file_path)
    initial_cif_file_count = get_cif_file_count_from_directory(base_dir)

    # Start
    get_cif_folder_info(base_dir, False)
    assert exists(csv_file_path), "CSV log file was not created."
    csv_data = pd.read_csv(csv_file_path)
    assert (
        len(csv_data.index) == initial_cif_file_count
    ), "CSV log does not match the # of moved files."

    # Test the Number of atoms
    URhIn_supercell_atom_count = csv_data[csv_data["CIF file"] == "URhIn.cif"][
        "Number of atoms in supercell"
    ].iloc[0]
    error_msg_supercell_atom_count = (
        f"Incorrect number of atoms for URhIn, expected 206"
    )
    assert URhIn_supercell_atom_count == 206, error_msg_supercell_atom_count

    # Test the shortest distance for URhIn
    error_msg_shortest_dist = "Incorrect shortest distance for URhIn, expected ~2.69678, got {urhIn_min_distance}"
    URhIn_shortest_dist = csv_data[csv_data["CIF file"] == "URhIn.cif"][
        "Min distance"
    ].iloc[0]
    assert np.isclose(
        URhIn_shortest_dist, 2.69678, atol=1e-4
    ), error_msg_shortest_dist

    # Cleanup
    remove_file(csv_file_path)
