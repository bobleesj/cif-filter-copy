import matplotlib.pyplot as plt


def plot_distance_histogram(distances, save_path, num_of_files):
    """
    Plot the histogram of the min distances in CIF files.
    """
    plt.figure(figsize=(10, 6))
    plt.hist(distances, bins=50, color="blue", edgecolor="black")
    plt.title(f"Histogram of Shortest Distances of {num_of_files} files")
    plt.xlabel("Distance (Å)")
    plt.ylabel("Number of CIF Files")
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.savefig(save_path, dpi=300)
