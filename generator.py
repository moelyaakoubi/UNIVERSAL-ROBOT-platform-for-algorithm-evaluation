import CartesianPoint_class


point1 = CartesianPoint_class.CartesianPoint(-0.05247, -0.2361, 0.36177, 1.111, 2.9, -0.107)
point2 = CartesianPoint_class.CartesianPoint(-0.44061, -0.1536, 0.22177, 1.188, 3.029, 0.013)
point3 = CartesianPoint_class.CartesianPoint(-0.50093,-0.16878 , 0.04021, 1.185, 2.917, 0.087)
point4 = CartesianPoint_class.CartesianPoint(-0.45639, -0.16748, 0.16421, 1.212, 2.920, 0.007)
point5 = CartesianPoint_class.CartesianPoint(-0.16163, -0.27849, 0.26036, 0.924, 3.082, -0.048)
point6 = CartesianPoint_class.CartesianPoint(0.02844, -0.39761, 0.19901, 0.562, 3.021, -0.084)
point7 = CartesianPoint_class.CartesianPoint(-0.00672, -0.44786, 0.04548, 1.088, 2.917, -0.001)
point8 = CartesianPoint_class.CartesianPoint(0.04738,-0.34733,0.35249,0.693,3.001,-0.322)


points=[point1,point2,point3,point4,point5,point6,point7,point8]

#nombre de trajectoires
for i in range(6):
    print(f"trajectoire {i+1}:")
    print(f"Point1: {CartesianPoint_class.generate_point_with_margin( point1, x=0.001, y=0.001, z=0.001)}")
    print(f"Point2: {CartesianPoint_class.generate_point_with_margin( point2,  z=0.001)}")
    print(f"Point3: {CartesianPoint_class.generate_point_with_margin( point3)}")
    print(f"Point4: {CartesianPoint_class.generate_point_with_margin( point4, z=0.001)}")
    print(f"Point5: {CartesianPoint_class.generate_point_with_margin( point5, x=0.001, y=0.001, z=0.001)}")
    print(f"Point6: {CartesianPoint_class.generate_point_with_margin( point6, z=0.001)}")
    print(f"Point7: {CartesianPoint_class.generate_point_with_margin( point7)}")
    print(f"Point8: {CartesianPoint_class.generate_point_with_margin( point8, z=0.001)}")


