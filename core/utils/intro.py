import textwrap


def prompt_format_intro():
    intro_prompt = textwrap.dedent(
        """\
    ==========================FORMAT=============================
    Process for this option:
    
    [1] All .cif files are initialized using CifEnsemble from`cifkit`
    [2] Standarlize site labels
    [3] Relocate ill-formated .cif files to separate folders=
    
    Note: please refer to bobleesj.github.io/cifkit for preprocessing
    ============================================================
    """
    )
    print(intro_prompt)


def prompt_min_dist_intro():
    intro_prompt = textwrap.dedent(
        """\
    ==========================DISTANCE=============================
    Process for this option:
    
    [1] Compute the minimum distance between atoms in each .cif file
    [2] View histogram of minimum distances
    [3] Enter the min distance threshold
    [4] Move files below the min distance threshold to separate folder
    ============================================================
    """
    )
    print(intro_prompt)


def prompt_occupancy_intro():
    intro_prompt = textwrap.dedent(
        """\
    ==========================OCCUPANCY=============================
    This tool uses `cifkit`to copy .cif files based based on the
    the 4 categories below:

    [1] Files with full occupancy
    [2] Files with site deficiency and atomic mixing
    [3] Files with full occupancy and atomic mixing
    [4] Files with site deficiency but no atomic mixing

    Note: refere to bobleesj.github.io/cifkit for site mixing.
    ==================================================================
    """
    )
    print(intro_prompt)


def prompt_composition_intro():
    intro_prompt = textwrap.dedent(
        """\
    ==========================COMPOSITION=============================
    Process for this option:
    
    [1] Get the composition type for each .cif file (unary, binary, etc.)
    [2] Move files to subfolders based on the composition type
    ==================================================================
    """
    )
    print(intro_prompt)


def prompt_element_intro():
    intro_prompt = textwrap.dedent(
        """\
    ==========================ELEMENT=============================
    Process for this option:
    
    [1] Enter the elements of interest separated by a space
    [2] Choose to filter by exactly matching or containing the elements 
    ==================================================================
    """
    )
    print(intro_prompt)


def prompt_coordination_number_intro():
    intro_prompt = textwrap.dedent(
        """\
    ==========================COORDINAITON_NUMBER=============================
    Process for this option:
    
    [1] Enter coordination numbers by d/min_dist method separated by a space
    [2] Choose to filter by exactly matching or containing coordination numbers
    ==================================================================
    """
    )
    print(intro_prompt)


def prompt_suppercell_size_intro():
    intro_prompt = textwrap.dedent(
        """\
    ==========================SUPERCELL=============================
    Process for this option:
    
    [1] Compute the number of atoms in the supercell for each .cif file
    [2] View histogram of supercell atom counts
    [3] Enter the supercell min and max atom counts
    [4] Move files above the min and below the max to separate folder
    ==================================================================
    """
    )
    print(intro_prompt)


def prompt_tag_intro():
    intro_prompt = textwrap.dedent(
        """\
    ==========================TAG=============================
    Process for this option:
    
    [1] Parse tag (i.g. ht, rt) from the thrid line in each .cif file
    [2] Move files to subfolders based on the tag
    ============================================================
    """
    )
    print(intro_prompt)


def prompt_info_intro():
    intro_prompt = textwrap.dedent(
        """\
    ==========================INFO=============================
    Process for this option:
    
    [1] Get formula, structure, tag, mixing type, composition type
    [2] Ask whether to compute min distance (requires computation)
    [3] Save a .csv file for each file
    ============================================================
    """
    )
    print(intro_prompt)
