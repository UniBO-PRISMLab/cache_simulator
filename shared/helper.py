import math

def calculate_distance(point1: tuple, point2: tuple) -> float:
    """
    Calculates the Euclidean distance between two points given as tuples.

    Args:
    - point1 (tuple): The first point as a tuple (x1, y1).
    - point2 (tuple): The second point as a tuple (x2, y2).

    Returns:
    - float: The Euclidean distance between the two points.
    """
    x1, y1 = point1
    x2, y2 = point2
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance