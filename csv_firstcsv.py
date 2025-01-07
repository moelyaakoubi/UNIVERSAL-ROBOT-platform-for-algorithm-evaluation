import socket
import time
import csv
from math import sqrt
from rtde_receive import RTDEReceiveInterface

ROBOT_IP = '192.168.0.1'
PORT = 30002
CSV_FILE = 'trajectories.csv'
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
    #start= [-0.05247, -0.2361, 0.36177, 1.111, 2.9, -0.107]
    #target= [-0.44061, -0.1536, 0.22177, 1.188, 3.029, 0.013]
    distances = [abs(target - start) for start, target in zip(start, target)]
    #distances = [abs(-0.44061-(-0.05247)), abs(-0.1536-(-0.2361)), abs(0.22177-0.36177), abs(1.188-1.111), abs(3.029-2.9), abs(0.013-(-0.107))]
    return max(distances) / speed

# Function to calculate motion time for Cartesian points with euclidean distance
def calculate_Euc_motion_time(start, target, speed=0.7):
    from math import sqrt
    distance = sqrt(sum((t - s) ** 2 for s, t in zip(start[:3], target[:3])))  # Euclidean distance
    return distance / speed

# Function to log robot current consumption
def log_data_values(rtde_r, log_writer):
    cartesian_position = rtde_r.getActualTCPPose()  # Current Cartesian pose
    joint_position = rtde_r.getActualQ()  # Current joint positions
    #joint_speeds = rtde_r.getActualQd()  # Joint velocities
    #forces = rtde_r.getActualTCPForce()  # TCP forces
    current = rtde_r.getActualCurrent()  # joint current consumption in amperes
    voltage= rtde_r.getActualJointVoltage() # joint voltage
    timestamp = time.time()
    # Write to log file
    log_writer.writerow([timestamp] + joint_position + cartesian_position +current +voltage)

try:
    points = read_points_from_csv(CSV_FILE)  # Read points from the CSV file
    print(f"Loaded {len(points)} points from CSV.")

    # Initialize RTDE interface for real-time data
    rtde_r = RTDEReceiveInterface(ROBOT_IP)

    with open(LOG_FILE, mode='w', newline='') as log_file:
        log_writer = csv.writer(log_file)
        # Write header for log file
        log_writer.writerow(
            ["Timestamp"] + 
            [f"Joint_{i+1}" for i in range(6)] + 
            [f"Cartesian_{axis}" for axis in ["x", "y", "z", "rx", "ry", "rz"]] +
            [f"Current_{i+1}" for i in range(6)]+
            [f"Voltage_{i+1}" for i in range(6)]

        )

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ROBOT_IP, PORT))
            print("Connected to the robot")

            for i, point in enumerate(points):
                start = point
                print(f"Start point {i}: {start}")

                if i + 1 < len(points):
                    target = points[i + 1]
                    print(f"Target point {i + 1}: {target}")

                    # Send movel command
                    command = movel_command_cart(start)
                    print(f"Sending command to move to point {i}: {command}")
                    s.sendall(command.encode('utf-8'))

                    # Calculate motion time and log current consumption
                    motion_time = calculate_motion_time(start, target)
                    print(f"Motion time estimated: {motion_time:.2f} seconds")

                    start_time = time.time()
                    while time.time() - start_time < motion_time + 2:
                        log_data_values(rtde_r, log_writer)
                        time.sleep(0.1)  # Log data at 10 Hz


                else:
                    print("No next target, motion sequence complete.")

            print("All motions completed.")
except Exception as e:
    print(f"An error occurred: {e}")
