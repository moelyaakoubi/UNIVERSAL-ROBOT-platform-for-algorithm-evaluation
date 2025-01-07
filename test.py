import socket
import time

# Robot IP address and port
ROBOT_IP = '192.168.0.1'  # Replace with your robot’s IP address
PORT = 30002              # Port for primary interface

# Define three points with six joint angles each (in radians)
# Replace these values with your desired joint positions
#point1 = [0.0, -1.57, 1.57, -1.57, -1.57, 0.0]
#point2 = [0.5, -1.2, 1.2, -1.2, -1.2, 0.5]
#point3 = [-0.5, -1.0, 1.0, -1.0, -1.0, -0.5]

point1 = [-0.05247, -0.2361, 0.36177, 1.111, 2.9, -0.107]
point2 = [-0.44061, -0.1536, 0.22177, 1.188, 3.029, 0.013]
point3 = [-0.50093,-0.16878 , 0.04021, 1.185, 2.917, 0.087]


# Create a list of the points to loop over
points = [point1, point2, point3]

# Function to format joint positions into a URScript command
def movej_command(joints, a=1.4, v=1.05):
    # URScript format for movej command with joint positions
    return f"movej([{', '.join(map(str, joints))}], a={a}, v={v})\n"

# Connect to the robot
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((ROBOT_IP, PORT))
    print("Connected to the robot")

    # Loop through each point and send the move command
    for i, point in enumerate(points):
        # Create the move command for the current joint positions
        command = movej_command(point)
        print(f"Sending command to move to point {i+1}: {command}")

        # Send the command to the robot
        s.sendall(command.encode('utf-8'))

        # Wait a bit to ensure the robot has time to reach the target position
        time.sleep(3)  # Adjust the sleep time as needed for your application

    print("Motion complete")