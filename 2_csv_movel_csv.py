import socket
import time
import csv
from math import sqrt
from rtde_receive import RTDEReceiveInterface

ROBOT_IP = '192.168.56.101'
PORT = 30002
CSV_FILE = 'Generated_trajectories.csv'
LOG_FILE = 'robot_data_current.csv'


# Function to read points from a CSV file
def read_points_from_csv(file_path):
    points = []
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            points.append([float(value) for value in row])
    return points

# Function to format the movel command with pose (Cartesian point) a=1.2, v=0.25)
def movel_command_cart(pose, a=1.2, v=0.7):
    return f"movej(p[{', '.join(map(str, pose))}], a={a}, v={v})\n"

# Function to calculate motion time for Cartesian points with x1-x2 values
def calculate_motion_time(start, target, speed=0.7):
    distances = [abs(target - start) for start, target in zip(start, target)]
    return max(distances) / speed


# Function to log robot data for each trajectory
def log_data_values(rtde_r, log_writer, trajectory_id):
    cartesian_position = rtde_r.getActualTCPPose()  # Cartesian pose
    joint_position = rtde_r.getActualQ()  # joint positions
    current = rtde_r.getActualCurrent()  # Joint current consumption in amperes
    voltage = rtde_r.getActualJointVoltage()  # Joint voltage
    timestamp = time.time()
    # Write to log file with trajectory ID
    log_writer.writerow([trajectory_id, timestamp] + joint_position + cartesian_position + current + voltage)

try:
    points = read_points_from_csv(CSV_FILE)  # Read points from the CSV file
    print(f"Loaded {len(points)} points from CSV.")
    
    # Initialize RTDE interface for real-time data
    rtde_r = RTDEReceiveInterface(ROBOT_IP)

    with open(LOG_FILE, mode='w', newline='') as log_file:
        log_writer = csv.writer(log_file)
        # Write header for log file
        log_writer.writerow(
            ["Trajectory_ID", "Timestamp"] + 
            [f"Joint_{i+1}" for i in range(6)] + 
            [f"Cartesian_{axis}" for axis in ["x", "y", "z", "rx", "ry", "rz"]] +
            [f"Current_{i+1}" for i in range(6)] +
            [f"Voltage_{i+1}" for i in range(6)]
        )

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ROBOT_IP, PORT))
            print("Connected to the robot")

            trajectory_id = 0  # Initialize trajectory counter

            for i, point in enumerate(points):
                if i % 8 == 0:  # Increment trajectory ID every 8 points because every trajectory has 8 points
                    trajectory_id += 1
                    print(f"Starting new trajectory: {trajectory_id}")

                start = point
                print(f"Start point {i}: {start}")

                # Check if there is a next target
                if i + 1 < len(points):
                    target = points[i + 1]
                    print(f"Target point {i + 1}: {target}")
                else:
                    # Handle the last point
                    target = start
                    print(f"Final point reached: {target}")

                # Send movel command to the robot
                command = movel_command_cart(start)
                print(f"Sending command to move to point {i}: {command}")
                s.sendall(command.encode('utf-8'))

                # Calculate motion time and log current consumption
                motion_time = calculate_motion_time(start, target)
                
                start_time = time.time()
                while time.time() - start_time < motion_time + 2:
                    log_data_values(rtde_r, log_writer, trajectory_id)
                    time.sleep(0.1)  # Log data at 10 Hz

            print("All motions completed.")
except Exception as e:
    print(f"An error occurred: {e}")
