import os
from os.path import join, exists
import glob


def choose_dir(script_directory):
    """
    Allows the user to select a directory from the given path.
    """

    directories = [
        d
        for d in os.listdir(script_directory)
        if os.path.isdir(join(script_directory, d))
        and any(file.endswith(".cif") for file in os.listdir(join(script_directory, d)))
    ]

    if not directories:
        print("No directories found in the current path containing .cif files!")
        return None
    print("\nAvailable folders containing CIF files:")
    for idx, dir_name in enumerate(directories, start=1):
        num_of_cif_files = len(glob.glob(join(dir_name, "*.cif")))
        print(f"{idx}. {dir_name}, {num_of_cif_files} files")
    while True:
        try:
            choice = int(
                input(
                    "\nEnter the number corresponding to the folder containing .cif files: "
                )
            )
            if 1 <= choice <= len(directories):
                return join(script_directory, directories[choice - 1])
            else:
                print(f"Please enter a number between 1 and {len(directories)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def save_to_csv_directory(dir_path, df, base_filename):
    """
    Saves the dataframe as a CSV inside a 'csv' sub-directory of the provided folder.
    """

    csv_directory = join(dir_path, "csv")
    if not os.path.exists(csv_directory):
        os.mkdir(csv_directory)

    # Extract the name of the chosen folder
    folder_name = os.path.basename(dir_path)

    # Set the name for the CSV file based on the chosen folder
    csv_filename = f"{folder_name}_{base_filename}.csv"

    # Save the DataFrame to the desired location (within the 'csv' sub-directory)
    df.to_csv(join(csv_directory, csv_filename), index=False)

    print(csv_filename, "saved")

