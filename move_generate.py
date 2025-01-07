import socket
import time

ROBOT_IP = '192.168.0.1'
PORT = 30002

# Define Cartesian points (position + orientation)
point1 = [-0.05247, -0.2361, 0.36177, 1.111, 2.9, -0.107]
point2 = [-0.44061, -0.1536, 0.22177, 1.188, 3.029, 0.013]
point3 = [-0.50093,-0.16878 , 0.04021, 1.185, 2.917, 0.087]
point4 = [-0.45639, -0.16748, 0.16421, 1.212, 2.920, 0.007]
point5 = [-0.16163, -0.27849, 0.26036, 0.924, 3.082, -0.048]
point6 = [0.02844, -0.39761, 0.19901, 0.562, 3.021, -0.084]
point7 = [-0.00672, -0.44786, 0.04548, 1.088, 2.917, -0.001]
point8 = [0.04738,-0.34733,0.35249,0.693,3.001,-0.322]


points = [point1,point2, point3,point4,point5,point6,point7,point8]


# Function to format the movej command with pose (Cartesian point)
def movej_command_cartesian(pose,a=1.2, v=0.4):
    return f"movej(p[{', '.join(map(str, pose))}], a={a}, v={v})\n"


def calculate_motion_time(start, target, speed=1.05):
    #start= [0.704240353,-1.534144413,0.386590429,-0.469493569,-1.502553953,-0.13840461]
    #target= [0.078365283, -0.853291471, 0.31503193, -1.132718685, -1.619840079, -0.748571716]
    distances = [abs(target - start) for start, target in zip(start, target)]
    #distances = [abs(0.078365283-0.704240353), abs(-0.853291471-(-1.534144413)), abs(0.31503193-0.386590429), abs(-1.132718685-(-0.469493569)), abs(-1.619840079-(-1.502553953)), abs(-0.748571716-(-0.13840461))]
    return max(distances) / speed


try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ROBOT_IP, PORT))
        print("Connected to the robot")


        for i, point in enumerate(points):
            start=points[i]
            print("start",start)
            if i+1<len(points):
                target=points[i+1]
                print("target",target)
            

            command = movej_command_cartesian(start)
            print(f"Sending command to move to point {i}: {command}")
            s.sendall(command.encode('utf-8'))

            motion_time = calculate_motion_time(start, target)
            #time.sleep(motion_time+2)  # Add buffer time
            time.sleep(motion_time+2.5)  # Add buffer time


    print("Motion complete")
except Exception as e:
    print(f"An error occurred: {e}")