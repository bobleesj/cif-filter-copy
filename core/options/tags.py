import shutil
import pandas as pd
import os
from core.utils import folder
from cifkit.utils.folder import move_files
from cifkit import CifEnsemble


def move_files_based_on_tags(cif_dir_path):
    print(
        "This script moves CIF files based on specific tags present in their third line."
    )

    # Dataframe setup
    df_rows = []

    # Process each file
    ensemble = CifEnsemble(cif_dir_path)
    for idx, cif in enumerate(ensemble.cifs, start=1):
        print(f"Processing {cif.file_name_without_ext}, ({idx}/{ensemble.file_count})")

        if cif.tag:
            subfolder_path = os.path.join(
                cif_dir_path, f"{os.path.basename(cif_dir_path)}_{cif.tag}"
            )
            move_files(subfolder_path, [cif.file_path])
            print(
                f"{os.path.basename(cif.file_name)} has been moved to {subfolder_path}"
            )
            df_rows.append(
                {
                    "Filename": cif.file_name_without_ext,
                    "Formula": cif.formula,
                    "Tag(s)": cif.tag,
                }
            )
    # Create and save DataFrame
    df = pd.DataFrame(df_rows)
    folder.save_to_csv_directory(cif_dir_path, df, "tags_log")
