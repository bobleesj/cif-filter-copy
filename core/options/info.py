import click
import pandas as pd
import time
from core.utils import folder, prompt, intro, object

def get_cif_folder_info(cif_dir_path, is_interactive_mode=True, compute_dist=False):
    intro.prompt_info_intro()

    # Keep track of data for .csv
    results = []

    # Keep track overall time
    overall_start_time = time.perf_counter()

    ensemble = object.init_cif_ensemble(cif_dir_path)

    # Ask user to calculate distance
    if is_interactive_mode:
        click.echo("\nQ. Do you want to compute minimum distance per file (slow)?")
        compute_dist = click.confirm("(Default: N)", default=False)
    else:
        compute_dist = compute_dist

    # Process each cif object
    for i, cif in enumerate(ensemble.cifs, start=1):
        file_start_time = time.perf_counter()

        prompt.print_progress_current(
            i, cif.file_name, cif.supercell_atom_count, ensemble.file_count
        )
        min_distance = None
        if compute_dist:
            min_distance = round(cif.shortest_distance, 3)
        elapsed_time = time.perf_counter() - file_start_time

        data = {
            "Filename": cif.file_name_without_ext,
            "Formula": cif.formula,
            "Structure": cif.structure,
            "Tag": cif.tag,
            "Supercell atom count": cif.supercell_atom_count,
            "Site mixing type": cif.site_mixing_type,
            "Composition type": cif.composition_type,
            "Min distance (Å)": min_distance,
            "Processing time (s)": round(elapsed_time, 3),
        }
        results.append(data)

        prompt.print_finished_progress(
            cif.file_name, cif.supercell_atom_count, elapsed_time
        )

    # Save csv
    if compute_dist:
        folder.save_to_csv_directory(
            cif_dir_path, pd.DataFrame(results), "info_with_dist"
        )
    else:
        folder.save_to_csv_directory(cif_dir_path, pd.DataFrame(results), "info")

    # Total processing time
    total_elapsed_time = time.perf_counter() - overall_start_time
    prompt.print_total_time(total_elapsed_time, ensemble.file_count)

    # Done message
    prompt.print_done_with_option("Info")
