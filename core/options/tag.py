import shutil
import os
from core.utils import prompt, intro, object
from cifkit import CifEnsemble


def move_files_based_on_tags(cif_dir_path: str) -> None:
    intro.prompt_tag_intro()

    ensemble = object.init_cif_ensemble(cif_dir_path)
    filtered_files_paths = set()
    # Process each file
    for cif in ensemble.cifs:
        tag = cif.tag
        file_name = cif.file_name
        file_path = cif.file_path

        if tag:
            destination_path = os.path.join(
                cif_dir_path, f"{os.path.basename(cif_dir_path)}_{tag}"
            )
            os.makedirs(destination_path, exist_ok=True)
            shutil.move(file_path, destination_path)
            print(f"{file_name} with {tag} moved.")
            filtered_files_paths.add(file_path)

    prompt.print_moved_files_summary(filtered_files_paths, ensemble.file_count)
    prompt.print_done_with_option("Tags")
