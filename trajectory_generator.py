import csv
import CartesianPoint_class

# Define the points
points = [
    CartesianPoint_class.CartesianPoint(-0.05247, -0.2361, 0.36177, 1.111, 2.9, -0.107),
    CartesianPoint_class.CartesianPoint(-0.44061, -0.1536, 0.22177, 1.188, 3.029, 0.013),
    CartesianPoint_class.CartesianPoint(-0.50093, -0.16878, 0.04021, 1.185, 2.917, 0.087),
    CartesianPoint_class.CartesianPoint(-0.45639, -0.16748, 0.16421, 1.212, 2.920, 0.007),
    CartesianPoint_class.CartesianPoint(-0.16163, -0.27849, 0.26036, 0.924, 3.082, -0.048),
    CartesianPoint_class.CartesianPoint(0.02844, -0.39761, 0.19901, 0.562, 3.021, -0.084),
    CartesianPoint_class.CartesianPoint(-0.00672, -0.44786, 0.04548, 1.088, 2.917, -0.001),
    CartesianPoint_class.CartesianPoint(0.04738, -0.34733, 0.35249, 0.693, 3.001, -0.322)
]

# Write trajectories to a CSV file
file_name = "trajectories.csv"

with open(file_name, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Write header
    writer.writerow(["X", "Y", "Z", "w", "p", "r"])
    
    # Generate trajectories
    for i in range(10):
        for idx, point in enumerate(points, start=1):
            modified_point = CartesianPoint_class.generate_point_with_margin(
                point, 
                x=(0.001 if idx in {1, 5} else None), 
                y=(0.001 if idx in {1, 5} else None), 
                z=(0.001 if idx in {1,2,4,5,6,8} else None)
            )
            writer.writerow([ *modified_point.to_tuple()])


print(f"{i+1} Trajectories written to {file_name}.")