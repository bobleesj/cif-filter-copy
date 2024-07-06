import os
import shutil

import pandas as pd
from core.utils import folder, intro
from cifkit import CifEnsemble


def copy_files_based_on_atomic_occupancy_mixing(cif_dir_path):
    intro.print_occupacny_intro_paragraph()
    ensemble = CifEnsemble(cif_dir_path)

    # Dataframe setup
    df_rows = []

    for idx, cif in enumerate(ensemble.cifs, start=1):
        copy_to_dir(ensemble.dir_path, cif.site_mixing_type, cif.file_path)
        df_rows.append(
            {
                "Filename": cif.file_name_without_ext,
                "Formula": cif.formula,
                "Site mixing type": cif.site_mixing_type,
            }
        )

        print(
            f"({idx}/{ensemble.file_count}) {cif.file_name} is {cif.site_mixing_type}"
        )

    # Create and save DataFrame
    df = pd.DataFrame(df_rows)
    folder.save_to_csv_directory(cif_dir_path, df, "occupancy")


def copy_to_dir(cif_dir_path, suffix, file_path):
    """
    Coopy a file to the directroy, skipping if the file already exists.
    """
    folder_name = os.path.basename(cif_dir_path)

    destination_directory = os.path.join(cif_dir_path, f"{folder_name}_{suffix}")

    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    shutil.copy(
        file_path, os.path.join(destination_directory, os.path.basename(file_path))
    )
