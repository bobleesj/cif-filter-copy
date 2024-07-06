from cifkit import CifEnsemble
from core.utils import prompt


def format_files(cif_dir_path):
    CifEnsemble(cif_dir_path)
    prompt.print_done_with_option("format files")
