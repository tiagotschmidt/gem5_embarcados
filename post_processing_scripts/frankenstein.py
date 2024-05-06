import os
import statistics


def get_sym_insts(filename):
    """
    This function reads a file and extracts the number of cpu cycles simulated.

    Args:
        filename: The name of the file to read.

    Returns:
        The number of cpu cycles simulated, or None if the line is not found.
    """
    with open(filename, 'r') as f:
        for line in f:
            if "sim_insts" in line:
                values = line.split()
                return int(values[1])
    return None


def get_overall_misses(filename):
    """
    This function reads a file and extracts the number of cpu cycles simulated.

    Args:
        filename: The name of the file to read.

    Returns:
        The number of cpu cycles simulated, or None if the line is not found.
    """
    with open(filename, 'r') as f:
        for line in f:
            if "system.cpu.dcache.overall_misses::total" in line:
                values = line.split()
                return int(values[1])
    return None


def get_cpu_cycles(filename):
    """
    This function reads a file and extracts the number of cpu cycles simulated.

    Args:
        filename: The name of the file to read.

    Returns:
        The number of cpu cycles simulated, or None if the line is not found.
    """
    with open(filename, 'r') as f:
        for line in f:
            if "system.cpu.numCycles" in line:
                values = line.split()
                return int(values[1])
    return None


def main():
    """
    This function reads all files with the naming pattern, extracts the data, 
    and saves the statistics to a file.
    """
    data_cpu_cycles = []
    data_sym_ints = []
    data_overall_misses = []
    for filename in os.listdir():
        if filename.startswith("frankenstein_") and filename.endswith(".txt"):
            cpu_cycles = get_cpu_cycles(filename)
            if cpu_cycles:
                data_cpu_cycles.append(cpu_cycles)
            sym_insts = get_sym_insts(filename)
            if sym_insts:
                data_sym_ints.append(sym_insts)
            overall_misses = get_overall_misses(filename)
            if overall_misses:
                data_overall_misses.append(overall_misses)

    if not data_cpu_cycles:
        print("No data found in the files.")
        return

    average_cycles = statistics.mean(data_cpu_cycles)
    median_cycles = statistics.median(data_cpu_cycles)
    stddev_cycles = statistics.stdev(data_cpu_cycles)
    average_insts = statistics.mean(data_sym_ints)
    median_insts = statistics.median(data_sym_ints)
    stddev_insts = statistics.stdev(data_sym_ints)
    average_misses = statistics.mean(data_overall_misses)
    median_misses = statistics.median(data_overall_misses)
    stddev_misses = statistics.stdev(data_overall_misses)

    with open("frankenstein_statistics.txt", 'w') as f:
        f.write("Average CPU Cycles: {}\n".format(average_cycles))
        f.write("Median CPU Cycles: {}\n".format(median_cycles))
        f.write("Standard Deviation CPU Cycles: {}\n".format(stddev_cycles))
        f.write("Average Simulation Instructions: {}\n".format(average_insts))
        f.write("Median Simulation Instructions: {}\n".format(median_insts))
        f.write("Standard Deviation Simulation Instructions: {}\n".format(
            stddev_insts))
        f.write("Average CPU L1 misses: {}\n".format(average_misses))
        f.write("Median CPU L1 misses:: {}\n".format(median_misses))
        f.write("Standard Deviation CPU L1 misses:: {}\n".format(stddev_misses))

    print("Statistics saved to frankenstein_statistics.txt")


if __name__ == "__main__":
    main()
