import os
import filter.excel as excel
import filter.tags as tags
import filter.min_distance as min_distance
import filter.format as format
import filter.info as info
import filter.occupancy as occupancy

def main():  
    script_directory = os.path.dirname(os.path.abspath(__file__))

    print("\nWelcome! Please choose an option to proceed:")
    options = {
        "1": "Move files based on unsupported CIF format",
        "2": "Move files based on unreasonable distance",
        "3": "Move files based on tags",
        "4": "Copy files based on atomic occupancy and mixing",
        "5": "Get file info in the folder",
        "6": "Check CIF folder content against Excel file"
    }

    for key, value in options.items():
        print(f"[{key}] {value}")
    
    choice = input("Enter your choice (1-6): ")

    if choice in options:
        print(f"You have chosen: {options[choice]}\n")
    else:
        print("Invalid choice!")
        return

    # 1. Relocate CIF format with error
    if choice == '1':
        format.move_files_based_on_format_error(script_directory)

    # 2. Relocate CIF files with unreasonable distances
    elif choice == '2':
        min_distance.move_files_based_on_min_dist(script_directory)

    # 3. Relocate CIF based on tags
    elif choice == '3':
        tags.move_files_based_on_tags(script_directory)
        
    # 4. Copy files based on atomic occupancy and atomic mixing
    elif choice == '4':
        occupancy.copy_files_based_on_atomic_occupancy_mixing(script_directory)

    # 6. Get info on the supercell
    elif choice == '5':
        info.get_CIF_files_info(script_directory)
    
    # 6. Check missing files against Excel sheet
    elif choice == '6':
        excel.get_new_Excel_with_matching_entries(script_directory)

    
if __name__ == "__main__":
    main()
