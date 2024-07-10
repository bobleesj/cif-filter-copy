import time
from click import secho
from cifkit import CifEnsemble


def init_cif_ensemble(cif_dir_path) -> CifEnsemble:
    start_time = set_initial_time()
    ensemble = CifEnsemble(cif_dir_path, preprocess=False)
    print_elasped_time(start_time)
    return ensemble


def set_initial_time() -> float:
    """
    Set the initial time of the system.
    """
    return time.perf_counter()


def print_elasped_time(start_time: float) -> None:
    """
    Get the elapsed time from the start time.
    """
    elapsed_time = time.perf_counter() - start_time
    secho(f"Elapsed time: {elapsed_time:.2f} seconds\n", fg="green")
