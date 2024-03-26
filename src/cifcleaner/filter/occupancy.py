import os
import glob
import shutil
from ..preprocess import cif_parser
from ..util import folder
import textwrap


def copy_files_based_on_atomic_occupancy_mixing(
    cif_dir_path, is_interactive_mode=True
):
    introductory_paragraph = textwrap.dedent(
        """\
    ===
    Welcome to the CIF Atomic Occupancy and Mixing Filter Tool!

    This tool reads CIF files and sorts them based on atomic occupancy
    and the presence of atomic mixing. The tool offers 4 filtering options:

    [1] Files with full occupancy
    [2] Files with site deficiency and atomic mixing
    [3] Files with full occupancy and atomic mixing
    [4] Files with site deficiency but no atomic mixing

    After you choose one of the above options, the files will be copied to
    corresponding sub-directories within the chosen folder.

    Let's get started!
    ===
    """
    )

    print(introductory_paragraph)
    files = get_cif_files_and_folder_info(cif_dir_path)
    if len(files) is not None:
        process_files(files, cif_dir_path)

    print("Finished - relevant folder(s) and file(s) moved!")


def get_cif_files_and_folder_info(cif_dir_path):
    files = glob.glob(os.path.join(cif_dir_path, "*.cif"))
    return files


def get_atom_info(CIF_loop_values, i):
    label = CIF_loop_values[0][i]
    occupancy = float(cif_parser.remove_string_braket(CIF_loop_values[7][i]))
    coordinates = (
        cif_parser.remove_string_braket(CIF_loop_values[4][i]),
        cif_parser.remove_string_braket(CIF_loop_values[5][i]),
        cif_parser.remove_string_braket(CIF_loop_values[6][i]),
    )
    return label, occupancy, coordinates


def copy_to_dir(cif_dir_path, folder_suffix, file):
    folder_name = os.path.basename(cif_dir_path)

    destination_directory = os.path.join(
        cif_dir_path, f"{folder_name}_{folder_suffix}"
    )

    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    shutil.copy(
        file, os.path.join(destination_directory, os.path.basename(file))
    )


def process_files(files, folder_path):
    for idx, file in enumerate(files, start=1):
        filename = os.path.basename(file)
        cif_block = cif_parser.get_CIF_block(file)
        cif_loop_values = cif_parser.get_loop_values(
            cif_block, cif_parser.get_loop_tags()
        )
        num_atom_labels = len(cif_loop_values[0])

        # Check for full occupancy
        coord_occupancy_sum = {}
        is_full_occupancy = True

        for i in range(num_atom_labels):
            _, occupancy, coordinates = get_atom_info(cif_loop_values, i)
            occupancy_num = coord_occupancy_sum.get(coordinates, 0) + occupancy
            coord_occupancy_sum[coordinates] = occupancy_num

        # Now check summed occupancies
        for coordinates, sum_occ in coord_occupancy_sum.items():
            if sum_occ != 1:
                is_full_occupancy = False
                print(f"Summed occupancy at {coordinates}: {sum_occ}")
                break

        # Check for atomic mixing
        is_atomic_mixing = len(coord_occupancy_sum) != num_atom_labels

        print(filename)
        print("is_atomic_mixing", is_atomic_mixing)
        print("is_full_occupancy", is_full_occupancy)
        print()

        if is_atomic_mixing and not is_full_occupancy:
            copy_to_dir(folder_path, "deficiency_atomic_mixing", file)

        elif is_atomic_mixing and is_full_occupancy:
            copy_to_dir(folder_path, "full_occupancy_atomic_mixing", file)

        elif not is_atomic_mixing and not is_full_occupancy:
            copy_to_dir(folder_path, "deficiency_no_atomic_mixing", file)

        elif is_full_occupancy:
            copy_to_dir(folder_path, "full_occupancy", file)
