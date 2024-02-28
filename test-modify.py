import gemmi




def get_atom_site_loop_end_start_line_indexes(lines, start_keyword):
    """
    Find the start and end indexes of a section in the CIF file.
    
    :param lines: List of all lines in the CIF file.
    :param start_keyword: The keyword marking the beginning of the section.
    :return: A tuple containing the start and end indexes.
    """
    start_index = None
    end_index = None

    # Find the start index
    for i, line in enumerate(lines):
        if start_keyword in line:
            start_index = i + 1
            break

    if start_index is None:
        return None, None

    # Find the end index
    for i in range(start_index, len(lines)):
        if lines[i].strip() == '':
            end_index = i
            break

    return start_index, end_index

# file_path = '/Users/imac/Documents/GitHub/cif-filter-copy/cif_files/URhIn.cif'
# update_cif_content(file_path)




# def update_cif_content(file_path):
#     with open(file_path, 'r') as f:
#         lines = f.readlines()

#     # Find the index of the line containing '_atom_site_occupancy'
#     start_index = None
#     for i, line in enumerate(lines):
#         if '_atom_site_occupancy' in line:
#             start_index = i + 1  # Modification starts from the next line
#             break
#     print("_atom_site_occupancy line index", start_index)
#     # If '_atom_site_occupancy' is not found, we do nothing
#     if start_index is None:
#         print("'_atom_site_occupancy' not found in the file.")
#         return

#     # Find the index of the first empty space after '_atom_site_occupancy'
#     end_index = None
#     for i in range(start_index, len(lines)):
#         if lines[i].strip() == '':  # Checking for an empty line
#             end_index = i
#             break

#     # Modify the content between '_atom_site_occupancy' and the first empty space
#     for i in range(start_index, end_index):
#         print(start_index, end_index)
#         # Here you can modify each line as needed
#         # For demonstration, appending "_mod" to each non-empty line
#         lines[i] = lines[i].rstrip() + "_mod\n"

#     # Write the modified content back to a new file
#     new_file_path = file_path.replace('.cif', '_modified.cif')
#     with open(new_file_path, 'w') as f:
#         f.writelines(lines)

#     print(f"Modified CIF file saved as {new_file_path}")

# # Example usage
# file_path = '/Users/imac/Documents/GitHub/cif-filter-copy/cif_files/URhIn.cif'
# update_cif_content(file_path)


# # Here is the goal
# # Find the line of _atom_site_occupancy
# # Then find the line until there is a space 