import os
import matplotlib.pyplot as plt


def create_plot_directory(folder_path):
    """
    Ensure the plot directory exists.
    """
    plot_directory = os.path.join(folder_path, "plot")
    if not os.path.exists(plot_directory):
        os.makedirs(plot_directory)
    return plot_directory


def save_histogram(data, bins, title, xlabel, ylabel, file_path):
    """
    Save histogram plot to a file.
    """
    plt.figure(figsize=(10, 6))
    plt.hist(data, bins=bins, color="blue", edgecolor="black")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.savefig(file_path, dpi=300)
    plt.close()  # Close the plot to free up memory
    print(f"\nHistogram saved at {file_path}")


def plot_distance_histogram(cif_dir, distances, num_of_files):
    """
    Plot the histogram of the min distances in CIF files.
    """
    plot_directory = create_plot_directory(cif_dir)
    histogram_path = os.path.join(plot_directory, "histogram-min-dist.png")
    title = f"Histogram of Shortest Distances of {num_of_files} files"
    save_histogram(
        distances,
        50,
        title,
        "Distance (Å)",
        "Number of CIF Files",
        histogram_path,
    )


def plot_supercell_size_histogram(cif_dir, supercell_atom_counts, num_of_files):
    """
    Plot the histogram of the supercell atom count in CIF files.
    """
    plot_directory = create_plot_directory(cif_dir)
    histogram_path = os.path.join(plot_directory, "histogram-supercell-size.png")
    title = f"Histogram of Supercell Atom Count of {num_of_files} files"
    save_histogram(
        supercell_atom_counts,
        50,
        title,
        "Number of atoms",
        "Number of CIF Files",
        histogram_path,
    )
