import textwrap


def print_occupacny_intro_paragraph():
    introductory_paragraph = textwrap.dedent(
        """\
    ===
    Welcome to the CIF Atomic Occupancy and Mixing Filter Tool!

    This tool reads CIF files and sorts them based on atomic occupancy
    and the presence of atomic mixing. The tool offers 4 filtering options:

    [1] Files with full occupancy
    [2] Files with site deficiency and atomic mixing
    [3] Files with full occupancy and atomic mixing
    [4] Files with site deficiency but no atomic mixing

    After you choose one of the above options, the files will be copied to
    corresponding sub-directories within the chosen folder.

    Let's get started!
    ===
    """
    )

    print(introductory_paragraph)
