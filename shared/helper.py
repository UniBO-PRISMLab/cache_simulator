import math
import random
from typing import List


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
        x = random.randint(0, dimension)
        y = random.randint(0, dimension)

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


def pass_time(time_epoch, user, cache_workers, edge_nodes):
    for cache_worker in cache_workers:
        cache_worker.epoch_passed(time_epoch)
    for edge_node in edge_nodes:
        edge_node.cache.epoch_passed(time_epoch)
    user.epoch_passed(time_epoch)
