from core.utils import prompt, intro
from cifkit import Cif
from cifkit.utils.folder import (
    get_file_paths,
)

from cifkit.preprocessors.format import (
    preprocess_label_element_loop_values,
)
from cifkit.utils.cif_editor import remove_author_loop
from cifkit.preprocessors.error import move_files_based_on_errors
from cifkit.utils.cif_parser import (
    check_unique_atom_site_labels,
)


def format_files(cif_dir_path):
    intro.prompt_format_intro()
    file_paths = get_file_paths(cif_dir_path)
    for file_path in file_paths:
        try:
            remove_author_loop(file_path)
            preprocess_label_element_loop_values(file_path)
            check_unique_atom_site_labels(file_path)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    move_files_based_on_errors(cif_dir_path, file_paths)

    prompt.print_done_with_option("format files")
