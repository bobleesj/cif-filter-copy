import os
import pandas as pd
import glob
import util.folder as folder
import preprocess.cif_parser as cif_parser
import preprocess.cif_editor as cif_editor
import preprocess.supercell as supercell


def move_files_based_on_format_error(script_directory):
    print("\nCIF Preprocessing has started...\n")

    directory_path = folder.choose_CIF_directory(script_directory)
    if not directory_path:
        print("No directory chosen. Exiting.")
        return

    chosen_dir_name = os.path.basename(directory_path)

    # Define the directory paths for different error types
    cif_dir_path_bad_CIF = os.path.join(
        directory_path, f"{chosen_dir_name}_error_format"
    )
    cif_dir_path_bad_op = os.path.join(
        directory_path, f"{chosen_dir_name}_error_op"
    )
    cif_dir_path_bad_coords = os.path.join(
        directory_path, f"{chosen_dir_name}_error_coords"
    )
    cif_dir_path_bad_label = os.path.join(
        directory_path, f"{chosen_dir_name}_error_label"
    )
    cif_dir_path_bad_third_line = os.path.join(
        directory_path, f"{chosen_dir_name}_error_third_line"
    )
    cif_dir_path_bad_other_error = os.path.join(
        directory_path, f"{chosen_dir_name}_error_others"
    )

    # Initialize counters for each error directory
    num_files_bad_op = 0
    num_files_bad_cif = 0
    num_files_bad_coords = 0
    num_files_bad_label = 0
    num_files_bad_third_line = 0
    num_files_bad_others = 0

    # Get the list of all CIF files in the directory
    files = glob.glob(os.path.join(directory_path, "*.cif"))
    total_files = len(files)
    file_errors = []

    for idx, file_path in enumerate(
        files, start=1
    ):  # Use enumerate to get the index
        filename = os.path.basename(file_path)

        try:
            cif_editor.preprocess_cif_file_by_removing_author_loop(file_path)
            cif_editor.preprocess_cif_file_on_label_element(file_path)
            cif_parser.get_compound_phase_tag_id_from_third_line(file_path)

            print(f"Processing {filename} ({idx} out of {total_files})")
            # Apply operations that would be done in practice
            CIF_block = cif_parser.get_CIF_block(file_path)
            CIF_loop_values = cif_parser.get_loop_values(
                CIF_block, cif_parser.get_loop_tags()
            )
            all_coords_list = supercell.get_coords_list(
                CIF_block, CIF_loop_values
            )
            supercell.get_points_and_labels(all_coords_list, CIF_loop_values)

        except Exception as e:
            error_message = str(e)
            print(error_message)

            # Append file and error details to the list
            file_errors.append(
                {"filename": file_path, "error_message": error_message}
            )

            if (
                "An error occurred while processing symmetry operation"
                in error_message
            ):
                os.makedirs(cif_dir_path_bad_op, exist_ok=True)
                debug_filename = os.path.join(cif_dir_path_bad_op, filename)
                os.rename(file_path, debug_filename)
                num_files_bad_op += 1
            elif "Wrong number of values in the loop" in error_message:
                os.makedirs(cif_dir_path_bad_CIF, exist_ok=True)
                debug_filename = os.path.join(cif_dir_path_bad_CIF, filename)
                os.rename(file_path, debug_filename)
                num_files_bad_cif += 1
            elif "Missing atomic coordinates" in error_message:
                os.makedirs(cif_dir_path_bad_coords, exist_ok=True)
                debug_filename = os.path.join(cif_dir_path_bad_coords, filename)
                os.rename(file_path, debug_filename)
                num_files_bad_coords += 1
            elif (
                "Different elements found in atom site and label"
                in error_message
            ):
                os.makedirs(cif_dir_path_bad_label, exist_ok=True)
                debug_filename = os.path.join(cif_dir_path_bad_label, filename)
                os.rename(file_path, debug_filename)
                num_files_bad_label += 1
            elif (
                "The CIF file is wrongly formatted in the third line"
                in error_message
            ):
                os.makedirs(cif_dir_path_bad_third_line, exist_ok=True)
                debug_filename = os.path.join(
                    cif_dir_path_bad_third_line, filename
                )
                os.rename(file_path, debug_filename)
                num_files_bad_third_line += 1
            else:
                os.makedirs(cif_dir_path_bad_other_error, exist_ok=True)
                debug_filename = os.path.join(
                    cif_dir_path_bad_other_error, filename
                )
                os.rename(file_path, debug_filename)
                num_files_bad_others += 1
            print()

    # Display the number of files moved to each folder
    print("\nSUMMARY")
    print(f"# of files moved to 'error_op' folder: {num_files_bad_op}")
    print(f"# of files moved to 'error_format' folder: {num_files_bad_cif}")
    print(f"# of files moved to 'error_coords' folder: {num_files_bad_coords}")
    print(f"# of files moved to 'error_label' folder: {num_files_bad_label}")
    print(
        f"# of files moved to 'error_third_line' folder: {num_files_bad_third_line}"
    )
    print(f"# of files moved to 'error_others' folder: {num_files_bad_others}")

    df_errors = pd.DataFrame(file_errors)

    # Use the save_to_csv_directory function to save the DataFrame
    folder.save_to_csv_directory(directory_path, df_errors, "error_log")
