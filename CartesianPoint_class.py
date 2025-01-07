import random

# The class to represent a point in Cartesian coordinate system:
class CartesianPoint:
    def __init__(self, x=0.0, y=0.0, z=0.0, w=0.0, p=0.0, r=0.0):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.p = p
        self.r = r

    def __repr__(self):
        return f"{self.to_tuple()}"

    def to_tuple(self):
        return (self.x, self.y, self.z, self.w, self.p, self.r)

# The function to generate a new point with margin:
def generate_point_with_margin(base_point, **kwargs):
    if not isinstance(base_point, CartesianPoint):
        raise TypeError("base_point must be a CartesianPoint.")
    
    x, y, z, w, p, r = base_point.x, base_point.y, base_point.z, base_point.w, base_point.p, base_point.r
    
    # Handle margin for each coordinate, only if a margin is provided
    if "x" in kwargs and kwargs["x"] is not None:
        margin = kwargs["x"]
        x = random.uniform(x - margin, x + margin)
        x = round(x, 5)  # Round to 5 decimal places
    if "y" in kwargs and kwargs["y"] is not None:
        margin = kwargs["y"]
        y = random.uniform(y - margin, y + margin)
        y = round(y, 5)
    if "z" in kwargs and kwargs["z"] is not None:
        margin = kwargs["z"]
        z = random.uniform(z - margin, z + margin)
        z = round(z, 5)
    if "w" in kwargs and kwargs["w"] is not None:
        margin = kwargs["w"]
        w = random.uniform(w - margin, w + margin)
        w = round(w, 5)
    if "p" in kwargs and kwargs["p"] is not None:
        margin = kwargs["p"]
        p = random.uniform(p - margin, p + margin)
        p = round(p, 5)
    if "r" in kwargs and kwargs["r"] is not None:
        margin = kwargs["r"]
        r = random.uniform(r - margin, r + margin)
        r = round(r, 5)
    
    return CartesianPoint(x, y, z, w, p, r)
