import pandas as pd
import time
from core.utils import folder, prompt
from cifkit import CifEnsemble

def get_cif_folder_info(cif_dir_path):
    results = []
    overall_start_time = time.perf_counter()

    ensemble = CifEnsemble(cif_dir_path)

    for i, cif in enumerate(ensemble.cifs, start=1):
        file_start_time = time.perf_counter()

        prompt.print_progress_current(
            i, cif.file_name, cif.supercell_atom_count, ensemble.file_count
        )


        min_distance = round(cif.shortest_distance, 3)
        elapsed_time = time.perf_counter() - file_start_time
        # Append a row to the log csv file
        data = {
            "Filename": cif.file_name_without_ext,  # Corrected spelling error
            "Formula": cif.formula,
            "Structure": cif.structure,
            "Tag": cif.tag,
            "Site mixing type": cif.site_mixing_type,
            "Composition type": cif.composition_type,
            "Supercell atom count": cif.supercell_atom_count,
            "Min distance (Å)": min_distance,
            "Processing time": round(elapsed_time, 3),
        }
        results.append(data)
        prompt.print_finished_progress(cif.file_name, cif.supercell_atom_count, elapsed_time)

    # Save csv
    folder.save_to_csv_directory(cif_dir_path, pd.DataFrame(results), "info")
    ensemble.generate_stat_histograms()
    total_elapsed_time = time.perf_counter() - overall_start_time
    print(f"Total processing time for all files: {total_elapsed_time:.2f} s")


