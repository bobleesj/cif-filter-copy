import os
import pandas as pd
import glob
import util.folder as folder
import preprocess.cif_parser as cif_parser
import preprocess.supercell as supercell



def preprocess_cif_file_on_label_element(file_path):
    is_cif_file_updated = False

    with open(file_path, 'r') as f:
        content = f.read()

    CIF_block = cif_parser.get_CIF_block(file_path)
    CIF_loop_values = cif_parser.get_loop_values(CIF_block, cif_parser.get_loop_tags())
    num_element_labels = len(CIF_loop_values[0])

    # Get lines in _atom_site_occupancy only
    modified_lines = []
    content_lines = cif_parser.get_atom_site_loop_content(file_path, "_atom_site_occupancy")
    
    if content_lines is None:
        raise RuntimeError ("Could not find atom site loop.")

    if num_element_labels < 2:
        raise RuntimeError("Wrong number of values in the loop")

        
    for line in content_lines:
        line = line.strip()
        atom_type_label, atom_type_symbol = line.split()[:2]
        atom_type_from_label = cif_parser.get_atom_type(atom_type_label)

        if atom_type_symbol != atom_type_from_label:

            '''
            Type 1.
            Ex) test/format_label_cif_files/symbolic_atom_label_type_1/250165.cif

            M1 Th 4 a 0 0 0 0.99
            M2 Ir 4 a 0 0 0 0.01

            to
            
            Th1 Th 4 a 0 0 0 0.99
            Ir2 Ir 4 a 0 0 0 0.01
            '''
            if (len(atom_type_label) == 2 and
                atom_type_label[-1].isdigit() and
                atom_type_label[-2].isalpha()):

                # Get the new label Ex) M1 -> Ge1
                new_label = atom_type_label.replace(atom_type_from_label, atom_type_symbol)
                line = line.replace(atom_type_label, new_label)  # Modify the line
                is_cif_file_updated = True
        
            '''
            Type 2.
            Ex) test/format_label_cif_files/symbolic_atom_label_type_2/312084.cif

            M1A Ge 8 h 0 0.06 0.163 0.500
            M1B Pd 8 h 0 0.06 0.163 0.500
            Ce1 Ce 4 e 0 0.25 0.547 1

            to 
            
            Ge1A Ge 8 h 0 0.06 0.163 0.500
            Pd1B Pd 8 h 0 0.06 0.163 0.500
            Ce1 Ce 4 e 0 0.25 0.547 1
            '''
        
            if (len(atom_type_label) == 3 and
                atom_type_label[-1].isalpha() and
                atom_type_label[-2].isdigit() and
                atom_type_label[-3].isalpha()):
                new_label = atom_type_label.replace(atom_type_from_label, atom_type_symbol)
                line = line.replace(atom_type_label, new_label)  # Modify the line
                is_cif_file_updated = True

            '''
            Type 3.
            Ex) test/format_label_cif_files/symbolic_atom_label_type_3/1603834.cif

            Sb Sb 24 g 0 0.15596 0.34021 1
            Os Os 8 c 0.25 0.25 0.25 1
            R Nd 2 a 0 0 0 1

            to 

            Sb Sb 24 g 0 0.15596 0.34021 1
            Os Os 8 c 0.25 0.25 0.25 1
            Nd Nd 2 a 0 0 0 1
            '''

            if len(atom_type_label) == 1 and atom_type_label[-1].isalpha():
                new_label = atom_type_label.replace(atom_type_from_label, atom_type_symbol)
                line = line.replace(atom_type_label, new_label)
                is_cif_file_updated = True

            '''
            Type 4.
            Ex) test/format_label_cif_files/symbolic_atom_label_type_4/1711694.cif

            Sb Sb 2 b 0.333333 0.666667 0.2751 1
            Pd Pd 2 b 0.333333 0.666667 0.6801 1
            Ln Gd 2 a 0 0 0.0 1

            to

            Sb Sb 2 b 0.333333 0.666667 0.2751 1
            Pd Pd 2 b 0.333333 0.666667 0.6801 1
            Gd Gd 2 a 0 0 0.0 1

            '''
            
            if len(atom_type_label) == 2 and atom_type_label[-1].isalpha() and atom_type_label[-2].isalpha():
                new_label = atom_type_label.replace(atom_type_from_label, atom_type_symbol)
                line = line.replace(atom_type_label, new_label)
                is_cif_file_updated = True
        
        modified_lines.append(line + '\n')

    if is_cif_file_updated:
        with open(file_path, 'r') as f:
            original_lines = f.readlines()
        
        start_index, end_index = cif_parser.get_atom_site_loop_end_start_line_indexes(file_path, "_atom_site_occupancy")
        # Replace the specific section in original_lines with modified_lines
        original_lines[start_index:end_index] = modified_lines

        # Write the modified content back to the file
        with open(file_path, 'w') as f:
            f.writelines(original_lines)

def move_files_based_on_format_error(script_directory):

    print("\nCIF Preprocessing has started...\n") 

    directory_path = folder.choose_CIF_directory(script_directory)
    if not directory_path:
        print("No directory chosen. Exiting.")
        return
    
    chosen_directory_name = os.path.basename(directory_path)

    # Define the directory paths for different error types
    CIF_directory_path_bad_CIF = os.path.join(directory_path, f"{chosen_directory_name}_error_format")
    CIF_directory_path_bad_op = os.path.join(directory_path, f"{chosen_directory_name}_error_op")
    CIF_directory_path_bad_coords = os.path.join(directory_path, f"{chosen_directory_name}_error_coords")
    CIF_directory_path_bad_label = os.path.join(directory_path, f"{chosen_directory_name}_error_label")
    CIF_directory_path_bad_third_line = os.path.join(directory_path, f"{chosen_directory_name}_error_third_line")
    CIF_directory_path_bad_other_error = os.path.join(directory_path, f"{chosen_directory_name}_error_others")

    # Initialize counters for each error directory
    num_files_bad_op = 0
    num_files_bad_CIF = 0
    num_files_bad_coords = 0
    num_files_bad_label = 0
    num_files_bad_third_line = 0
    num_files_bad_others = 0
    
    # Get the list of all CIF files in the directory
    files = glob.glob(os.path.join(directory_path, "*.cif"))
    total_files = len(files)
    file_errors = []

    for idx, file_path in enumerate(files, start=1):  # Use enumerate to get the index
        filename = os.path.basename(file_path)

        try:
            result = cif_parser.get_compound_phase_tag_id_from_third_line(file_path)
            _, compound_formula, _, _ = result

            preprocess_cif_file_on_label_element(file_path)
            print(f"Processing {filename} ({idx} out of {total_files})")

            CIF_block = cif_parser.get_CIF_block(file_path)
            CIF_loop_values = cif_parser.get_loop_values(CIF_block, cif_parser.get_loop_tags())
            all_coords_list = supercell.get_coords_list(CIF_block, CIF_loop_values)
            _, _, _ = supercell.get_points_and_labels(all_coords_list, CIF_loop_values)
            

        except Exception as e:
            error_message = str(e)
            print(error_message)

            # Append file and error details to the list
            file_errors.append({
                'filename': file_path,
                'error_message': error_message
            })

            if 'An error occurred while processing symmetry operation' in error_message:
                os.makedirs(CIF_directory_path_bad_op, exist_ok=True) 
                debug_filename = os.path.join(CIF_directory_path_bad_op, filename)
                os.rename(file_path, debug_filename)
                num_files_bad_op += 1
            elif 'Wrong number of values in the loop' in error_message:
                os.makedirs(CIF_directory_path_bad_CIF, exist_ok=True)
                debug_filename = os.path.join(CIF_directory_path_bad_CIF, filename)
                os.rename(file_path, debug_filename)
                num_files_bad_CIF += 1
            elif 'Missing atomic coordinates' in error_message:
                os.makedirs(CIF_directory_path_bad_coords, exist_ok=True)
                debug_filename = os.path.join(CIF_directory_path_bad_coords, filename)
                os.rename(file_path, debug_filename)
                num_files_bad_coords += 1
            elif 'Different elements found in atom site and label' in error_message:
                os.makedirs(CIF_directory_path_bad_label, exist_ok=True)
                debug_filename = os.path.join(CIF_directory_path_bad_label, filename)
                os.rename(file_path, debug_filename)
                num_files_bad_label += 1
            elif 'The CIF file is wrongly formatted in the third line' in error_message:
                os.makedirs(CIF_directory_path_bad_third_line, exist_ok=True)
                debug_filename = os.path.join(CIF_directory_path_bad_third_line, filename)
                os.rename(file_path, debug_filename)
                num_files_bad_third_line += 1
            else:
                os.makedirs(CIF_directory_path_bad_other_error, exist_ok=True)
                debug_filename = os.path.join(CIF_directory_path_bad_other_error, filename)
                os.rename(file_path, debug_filename)
                num_files_bad_others += 1
            print()
    
    # Display the number of files moved to each folder
    print("\nSUMMARY")
    print(f"Number of files moved to 'error_op' folder: {num_files_bad_op}")
    print(f"Number of files moved to 'error_format' folder: {num_files_bad_CIF}")
    print(f"Number of files moved to 'error_coords' folder: {num_files_bad_coords}")
    print(f"Number of files moved to 'error_label' folder: {num_files_bad_label}")
    print(f"Number of files moved to 'error_third_line' folder: {num_files_bad_third_line}")
    print(f"Number of files moved to 'error_others' folder: {num_files_bad_others}")
    
    df_errors = pd.DataFrame(file_errors)

    # Use the save_to_csv_directory function to save the DataFrame
    folder.save_to_csv_directory(directory_path, df_errors, "error_log")