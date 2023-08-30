import math
import csv
import os
from typing import List
from parameters import TRACE_FILE_NAME
from shared.RandomGenerator import regular_random


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
        x = regular_random.randint(0, dimension)
        y = regular_random.randint(0, dimension)

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

def calculate_decimal_distance(point1, point2):
    distance = math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
    return distance


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


def write_objects_to_csv(objects, file_name=TRACE_FILE_NAME):
    if not objects:
        print("No objects to write.")
        return

    # Get attribute names from the first object's class
    attribute_names = list(vars(objects[0]).keys())

    # Check if the file exists, and create it if it doesn't
    if not os.path.exists(file_name):
        with open(file_name, 'w', newline='') as empty_file:
            pass

    with open(file_name, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Write the header only if the file was just created
        if os.path.getsize(file_name) == 0:
            writer.writerow(attribute_names)

        # Write object attributes as rows
        for obj in objects:
            row = [getattr(obj, attr_name) for attr_name in attribute_names]
            writer.writerow(row)