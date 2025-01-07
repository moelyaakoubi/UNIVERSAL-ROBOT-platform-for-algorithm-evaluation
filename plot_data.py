import csv
import matplotlib.pyplot as plt

# Function to read the log data
def read_log_data(file_path):
    timestamps = []
    joint_positions = [[] for _ in range(6)]
    cartesian_positions = [[] for _ in range(6)]
    current_data = [[] for _ in range(6)]
    voltage_data = [[] for _ in range(6)]  

    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row

        for row in reader:
            timestamp = float(row[0])
            timestamps.append(timestamp)

            for i in range(6):
                joint_positions[i].append(float(row[i + 1]))

            for i, axis in enumerate(["x", "y", "z","r","w","p"]):
                cartesian_positions[i].append(float(row[i + 7]))

            for i in range(6):
                current_data[i].append(float(row[14 + i])) 
            
            for i in range(6):
                voltage_data[i].append(float(row[19 + i]))

    return timestamps, joint_positions, cartesian_positions, current_data,voltage_data

# Function to plot Cartesian positions (x, y, z) over time
def plot_cartesian_positions(timestamps, cartesian_positions):
    plt.subplot(3,1, 1)
    for i, joint in enumerate(cartesian_positions):
        plt.plot(timestamps, joint, label=f"cartesian {i + 1}")
    plt.xlabel("Time (seconds)")
    plt.ylabel("cartesian Position ")
    plt.title("cartesian Over Time")
    plt.legend()


def plot_joint_positions(timestamps, joint_positions):
    plt.subplot(3, 1, 2)
    for i, joint in enumerate(joint_positions):
        plt.plot(timestamps, joint, label=f"Joint {i + 1}")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Joint Position (radians)")
    plt.title("Joint Positions Over Time")
    plt.legend()


def plot_current(timestamps, current_data):
    plt.subplot(3, 1, 3)
    for i, joint in enumerate(current_data):
        plt.plot(timestamps, joint, label=f"Curent {i + 1}")
    plt.xlabel("Time (seconds)")
    plt.ylabel("joint current")
    plt.title("joint current Over Time")
    plt.legend()


def plot_voltage(timestamps, voltage_data):
    plt.subplot(4, 2, 2)
    for i, joint in enumerate(voltage_data):
        plt.plot(timestamps, joint, label=f"voltage {i + 1}")
    plt.xlabel("Time (seconds)")
    plt.ylabel("voltage")
    plt.title("voltage Over Time")
    plt.legend()





# Main function to read the log data and plot the results
def plot_robot_data(log_file):
    timestamps, joint_positions, cartesian_positions, current_data,voltage_data = read_log_data(log_file)

    # Plot Cartesian positions (x, y, z)
    plot_cartesian_positions(timestamps, cartesian_positions)

    plot_joint_positions( timestamps,joint_positions)

    plot_current(timestamps,current_data)

    plot_voltage(timestamps,voltage_data)


    plt.tight_layout()
    plt.show()

# Call the plotting function with the log file
plot_robot_data('robot_data_current.csv')
