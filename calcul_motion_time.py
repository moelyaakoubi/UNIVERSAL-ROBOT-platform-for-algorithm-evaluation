import time

point1= [0.704240353,-1.534144413,0.386590429,-0.469493569,-1.502553953,-0.13840461]
point2= [0.078365283, -0.853291471, 0.31503193, -1.132718685, -1.619840079, -0.748571716]
point3= [0.096691241, -0.429176463, 0.330216294, -1.455604596, -1.616174887, -0.700749695]
point4= [0.083775804, -0.720646448, 0.320791517, -1.188918286, -1.576206847, -0.700924228]
point5= [0.660258056, -1.554564765, 1.114392727, -1.201833723, -1.609368103, -0.331438025]
point6= [1.260651319, -1.303586418, 1.11456726, -1.429773723, -1.490685714, 0.058992129]
point7= [1.24284896, -0.956614963, 1.30550628, -1.922131105, -1.537286005, 0,388161226]

points = [point1,point2, point3,point4,point5,point6,point7]



def calculate_motion_time(start, target, speed):
    distances = [abs(target - start) for start, target in zip(start, target)]
    return max(distances) / speed

           

for i in range(len(points)-1):
        start=points[i]
        target=points[i+1]
        print(start)
        print(target)
        motion_time = calculate_motion_time(start, target, speed=1.05)
        print(motion_time)

            
