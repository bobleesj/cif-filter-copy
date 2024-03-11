from click import style, echo
import preprocess.cif_parser_handler as cif_parser_handler
import preprocess.supercell as supercell
import os


def get_shortest_dist_list_and_skipped_indices(
    files_lst, loop_tags, max_atom_count
):
    """
    Process each CIF file to find the shortest atomic distance.

    Parameters:
    - files_lst: List of CIF files to process.
    - loop_tags: Tags used for parsing CIF data.
    - MAX_ATOMS_COUNT: Maximum number of atoms allowed for processing a file.

    Returns:
    - shortest_dist_list: List of shortest distances for each processed file.
    - skipped_indices: Set of indices for files that were skipped.
    """
    shortest_dist_list = []
    skipped_indices = set()

    for idx, file_path in enumerate(files_lst, start=1):
        filename = os.path.basename(file_path)
        print(f"Processing {filename} ({idx}/{len(files_lst)})")

        result = cif_parser_handler.get_CIF_info(file_path, loop_tags)
        _, cell_lengths, cell_angles_rad, _, all_points, _, _ = result
        num_of_atoms = len(all_points)
        file_skip_message = f"Skipped - {filename} has {num_of_atoms} atoms"

        if num_of_atoms > max_atom_count:
            echo(style(file_skip_message, fg="yellow"))
            skipped_indices.add(idx)
            continue

        atomic_pair_list = supercell.get_atomic_pair_list(
            all_points, cell_lengths, cell_angles_rad
        )

        sorted_atomic_pairs = sorted(
            atomic_pair_list, key=lambda x: x["distance"]
        )

        shortest_distance_pair = sorted_atomic_pairs[0]
        shortest_dist = shortest_distance_pair["distance"]
        shortest_dist_list.append(shortest_dist)

    return shortest_dist_list, skipped_indices
