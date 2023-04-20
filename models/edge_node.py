from parameters import CACHE_DEFAULT_SIZE
from models.cache import Cache


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

    def __str__(self):
        return f"Edge Node {self.id} - Current Position: {self.get_position()}"
