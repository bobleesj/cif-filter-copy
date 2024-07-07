import pandas as pd
import os
from core.utils import prompt, intro
from cifkit import CifEnsemble
from cifkit.utils.folder import move_files


def move_files_based_on_tags(cif_dir_path):
    intro.prompt_tag_intro()
    ensemble = CifEnsemble(cif_dir_path)
    file_moved = 0
    # Process each file
    for idx, cif in enumerate(ensemble.cifs, start=1):
        print(f"Processing {cif.file_name} ({idx}/{ensemble.file_count})")

        if cif.tag:
            subfolder_path = os.path.join(
                cif_dir_path, f"{os.path.basename(cif_dir_path)}_{cif.tag}"
            )
            move_files(subfolder_path, [cif.file_path])
            print(f"{cif.file_name} moved to {subfolder_path}")
            file_moved += 1

    print("Number of files moved based on tags:", file_moved)
    prompt.print_done_with_option("Tags")
