from cifkit.preprocessors.environment import get_site_connections
from cifkit.coordination.method import compute_CN_max_gap_per_site
from cifkit.data.radius_handler import (
    compute_radius_sum,
)
from cifkit.coordination.filter import (
    get_CN_connections_by_min_dist_method,
)
from cifkit.coordination.composition import (
    get_unique_CN_values,
)
from cifkit.coordination.site_distance import (
    get_shortest_distance,
)


def get_CN_values(cif):
    """
    The reason we are not using the `cif.CN_connections_by_min_dist_method`
    directly is that when the connections are computed, we also compute the
    volume of the polyhedron. But when the polyhedron is flat, the function
    provides error but it has nothing to do with determining the CN values.
    Hence, we copy a portion of the cif code here to compute the CN_values
    in order to not compute the polyhedron and volume.
    """
    connections = _get_conncetions(cif)
    radius_sum = compute_radius_sum(cif.radius_values, cif.is_radius_data_available)
    CN_max_gap_per_site = compute_CN_max_gap_per_site(
        radius_sum,
        connections,
        cif.is_radius_data_available,
        cif.site_mixing_type,
    )

    CN_connections_by_min_dist_method = get_CN_connections_by_min_dist_method(
        CN_max_gap_per_site, connections
    )

    CN_values_computed = get_unique_CN_values(CN_connections_by_min_dist_method)
    return CN_values_computed


def compute_min_dist(cif):
    """
    Get the minimum distance between atoms in the CIF file without using
    `cif.CN_connections_by_min_dist_method` directly with the reason explained
    above.
    """
    connections = _get_conncetions(cif)
    min_dist = get_shortest_distance(connections)
    return min_dist


def _get_conncetions(cif):
    # Determine CN_values based on the filter choice
    connections = get_site_connections(
        [
            cif.site_labels,
            cif.unitcell_lengths,
            cif.unitcell_angles,
        ],
        cif.unitcell_points,
        cif.supercell_points,
        cutoff_radius=10.0,
    )
    return connections
