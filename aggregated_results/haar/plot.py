import matplotlib.pyplot as plt

# Define data dictionary to store values
data = {
    "Average CPU Cycles": [],
    "Median CPU Cycles": [],
    "Standard Deviation CPU Cycles": [],
    "Average Simulation Instructions": [],
    "Median Simulation Instructions": [],
    "Standard Deviation Simulation Instructions": [],
    "Average CPU L1 misses": [],
    "Median CPU L1 misses": [],
    "Standard Deviation CPU L1 misses": [],
}


def read_data(filename):
    """
    Reads data from a file and stores it in the data dictionary.
    """
    with open(filename, "r") as f:
        for line in f:
            key, value = line.strip().split(": ")
            data[key].append(float(value))


def plot_data():
    """
    Plots graphs for each value, comparing the three versions and highlighting data points.
    """
    versions = ["small_haar", "medium_haar", "large_haar"]

    # Loop through each data key
    for key, values in data.items():
        if key.startswith("Average"):
            plt.figure()
            for i, value in enumerate(values):
                plt.plot(versions[i], value, marker="o", label=versions[i])
                # Add annotation to highlight each point with its Y value
                plt.annotate(str(value), (versions[i], value), textcoords="offset points", xytext=(0, 10), fontsize=8)
            plt.xlabel("Version")
            plt.ylabel(key)
            plt.title(f"{key} Comparison")
            plt.grid(True)
            plt.legend()  # Add legend after plotting for proper label placement
            plt.show()


# Read data from each file
read_data("small_haar_statistics.txt")
read_data("medium_haar_statistics.txt")
read_data("large_haar_statistics.txt")

# Plot the data
plot_data()

print("Graphs generated! Check for open figures.")
