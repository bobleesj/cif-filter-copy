import time
from click import style, echo
from preprocess import cif_parser_handler, supercell, cif_parser
from util import prompt
import os
import numpy as np



def get_flattened_points_from_unitcell(file_path):
    loop_tags = cif_parser.get_loop_tags()
    cif_block = cif_parser.get_cif_block(file_path)
    cif_loop_values = cif_parser.get_loop_values(cif_block, loop_tags)
    all_coords_list = supercell.get_coords_list(
        cif_block, cif_loop_values
    )
    points, _, _ = supercell.get_points_and_labels(
        all_coords_list,
        cif_loop_values,
        1,
        is_flatten_points_only=True,
    )
    return points



def get_nearest_dists_per_site(
    filtered_unitcell_points,
    supercell_points,
    cutoff_radius,
    lengths,
    angles_rad,
):
    # Initialize a dictionary to store the relationships
    dist_dict = {}
    dist_set = set()

    # Loop through each point in the filtered list
    for i, point_1 in enumerate(filtered_unitcell_points):
        point_2_info = []
        for j, point_2 in enumerate(supercell_points):
            if point_1 == point_2:
                continue  # Skip comparison with itself
            # Convert fractional to Cartesian coordinates
            cart_1 = supercell.fractional_to_cartesian(
                [point_1[0], point_1[1], point_1[2]],
                lengths,
                angles_rad,
            )
            cart_2 = supercell.fractional_to_cartesian(
                [point_2[0], point_2[1], point_2[2]],
                lengths,
                angles_rad,
            )

            # Calculate the dist between two points
            dist = supercell.calc_dist_two_cart_points(cart_1, cart_2)
            dist = np.round(dist, 3)

            # Check the dist
            if dist < cutoff_radius and dist > 0.1:
                point_2_info.append(
                    (
                        point_2[3],  # site label
                        dist,
                        [
                            np.round(cart_1[0], 3),  # x
                            np.round(cart_1[1], 3),  # y
                            np.round(cart_1[2], 3),  # z
                        ],
                        [
                            np.round(cart_2[0], 3),  # x
                            np.round(cart_2[1], 3),  # y
                            np.round(cart_2[2], 3),  # z
                        ],
                    )
                )
            dist_set.add(dist)
        # Store the list in the dictionary with `i` as the key
        if point_2_info:
            dist_dict[i] = point_2_info

    return dist_dict, dist_set

