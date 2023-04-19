from parameters import CACHE_DEFAULT_SIZE
from models.cache import Cache

import time


class EdgeNode:
    """
    Represents an edge node with a position defined as (x, y) coordinates.
    """

    def __init__(self, id, cache_size=CACHE_DEFAULT_SIZE):
        """
        Initializes an edge node with a randomly generated (x, y) position.

        Args:
            edge_nodes (list): The list of all edge nodes.
        """
        self.id = id
        self.x, self.y = (None, None)
        self.cache = Cache(cache_size)

    def get_position(self):
        """
        Returns the (x, y) position of the edge node.

        Returns:
            tuple: The (x, y) position of the edge node as a tuple.
        """
        return self.x, self.y

    def set_position(self, x: float, y: float):
        """
        Sets the position of the edge node to the given (x, y) coordinates.

        Args:
            x (float): The new x-coordinate of the edge node.
            y (float): The new y-coordinate of the edge node.
        """
        self.x = x
        self.y = y

    def store_resource(self, resource_id: str, validity_time):
        if self.cache.current_size < self.cache.max_size:
            self.cache.add_resource(resource_id, validity_time)
            print(
                f"Resource {resource_id} stored in cache of EdgeNode {self.edge_node_id}")
        else:
            print(
                f"Cache of EdgeNode {self.edge_node_id} is full. Resource {resource_id} not stored.")

    def retrieve_resource(self, resource_id: str):
        for resource in self.cache.resources:
            if resource.resource_id == resource_id:
                current_time = time.time()
                if current_time - resource.storage_time <= resource.validity_time:
                    print(
                        f"Resource {resource_id} retrieved from cache of EdgeNode {self.edge_node_id}")
                    return resource
                else:
                    print(
                        f"Resource {resource_id} has expired in cache of EdgeNode {self.edge_node_id}.")
                    self.cache.remove_expired_resources()
                    return None
        print(
            f"Resource {resource_id} not found in cache of EdgeNode {self.edge_node_id}.")
        return None
    def __str__(self):
        return f"Edge Node {self.id} - Current Position: {self.get_position()}"
