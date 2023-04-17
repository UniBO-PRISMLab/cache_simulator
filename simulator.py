import random
import math


def generate_edge_node_position(dimension, min_distance, edge_nodes):
    """
    Generates a random (x, y) position for a single edge node,
    ensuring that it is not closer than X from any other edge node.

    Args:
        edge_nodes (list): The list of all edge nodes.
        dimension (int): dimension of the area (square)
        min_distance (int): minimum distance between edge nodes
    Returns:
        tuple: The randomly generated (x, y) position as a tuple.
    """
    while True:
        x = random.uniform(0, dimension)
        y = random.uniform(0, dimension)
        # Check if the generated (x, y) position is farther than min_distance from all other edge nodes
        if all(distance((x, y), edge_node.get_position()) >= min_distance for edge_node in edge_nodes):
            return x, y


def distance(p1, p2):
    """
    Calculates the Euclidean distance between two points p1 and p2.

    Args:
        p1 (tuple): The first point as a (x, y) tuple.
        p2 (tuple): The second point as a (x, y) tuple.

    Returns:
        float: The Euclidean distance between the two points.
    """
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5


def get_closest_edge_node(user, edge_nodes):
    min_distance = float('inf')
    closest_edge_node = None
    user_position = user.get_position()

    for edge_node in edge_nodes:
        edge_node_position = edge_node.get_position()
        distance = math.sqrt((user_position[0] - edge_node_position[0]) ** 2 +
                             (user_position[1] - edge_node_position[1]) ** 2)
        if distance < min_distance:
            min_distance = distance
            closest_edge_node = edge_node

    return closest_edge_node

def get_closest_edge_node_in_time(user, edge_nodes, time):
    min_distance = float('inf')
    closest_edge_node = None
    user_position = user.get_position_at_time(time)

    for edge_node in edge_nodes:
        edge_node_position = edge_node.get_position()
        distance = math.sqrt((user_position[0] - edge_node_position[0]) ** 2 +
                             (user_position[1] - edge_node_position[1]) ** 2)
        if distance < min_distance:
            min_distance = distance
            closest_edge_node = edge_node

    return closest_edge_node

