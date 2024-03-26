import os
import click
from click import style
from ..preprocess import cif_parser, supercell
from ..util import folder


def get_CIF_info(file_path, loop_tags):
    """
    Parse the CIF data from the given file path.
    """
    cif_block = cif_parser.get_CIF_block(file_path)
    cell_lengths, cell_angles_rad = cif_parser.get_cell_lenghts_angles_rad(
        cif_block
    )
    cif_loop_values = cif_parser.get_loop_values(cif_block, loop_tags)
    all_coords_list = supercell.get_coords_list(cif_block, cif_loop_values)
    (
        all_points,
        unique_labels,
        unique_atoms_tuple,
    ) = supercell.get_points_and_labels(all_coords_list, cif_loop_values)

    return (
        cif_block,
        cell_lengths,
        cell_angles_rad,
        all_coords_list,
        all_points,
        unique_labels,
        unique_atoms_tuple,
    )


def get_folder_and_files_info(cif_dir_path, is_interactive_mode):
    """
    Get the folder information, list of CIF files, and loop tags for processing.

    Parameters:
    - script_directory: The base directory from which to select the CIF directory.

    Returns:
    - folder_info: Information about the selected folder.
    - filtered_folder: Path to the folder where filtered files will be stored.
    - files_lst: List of CIF files to process.
    - num_of_files: Number of CIF files found.
    - loop_tags: Loop tags used for parsing CIF files.
    """

    # With graphic user interface
    cif_dir_name = os.path.basename(cif_dir_path)

    filtered_dir_name = f"{cif_dir_name}_filter_dist_min"
    filtered_dir_path = os.path.join(cif_dir_path, filtered_dir_name)
    files_lst = [
        os.path.join(cif_dir_path, file)
        for file in os.listdir(cif_dir_path)
        if file.endswith(".cif")
    ]
    num_of_files = len(files_lst)
    loop_tags = cif_parser.get_loop_tags()

    return cif_dir_path, filtered_dir_path, files_lst, num_of_files, loop_tags
