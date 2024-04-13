import time
from click import style, echo
from preprocess import cif_parser_handler, supercell
from util import prompt
import os


def get_shortest_dist_list_and_skipped_indices(
    files_lst, loop_tags, supercell_method=3
):
    """
    Process each CIF file to find the shortest atomic distance.
    """
    shortest_dist_list = []
    skipped_indices = set()

    for idx, file_path in enumerate(files_lst, start=1):
        start_time = time.perf_counter()
        filename = os.path.basename(file_path)
        print(f"Processing {filename} ({idx}/{len(files_lst)})")

        result = cif_parser_handler.get_CIF_info(
            file_path, loop_tags, supercell_method
        )
        _, cell_lengths, cell_angles_rad, _, all_points, _, _ = result
        num_of_atoms = len(all_points)

        atomic_pair_list = supercell.get_atomic_pair_list(
            all_points, cell_lengths, cell_angles_rad
        )

        sorted_atomic_pairs = sorted(
            atomic_pair_list, key=lambda x: x["distance"]
        )

        shortest_distance_pair = sorted_atomic_pairs[0]
        shortest_dist = shortest_distance_pair["distance"]
        shortest_dist_list.append(shortest_dist)
        elapsed_time = time.perf_counter() - start_time

        prompt.print_progress(filename, num_of_atoms, elapsed_time, True)

    return shortest_dist_list, skipped_indices
