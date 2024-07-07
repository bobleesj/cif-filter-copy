from cifkit import CifEnsemble
from core.utils import prompt, intro


def format_files(cif_dir_path):
    intro.prompt_format_intro()
    CifEnsemble(cif_dir_path)
    prompt.print_done_with_option("format files")
