import math
import random
from typing import List
from models.cache_worker import CacheWorker
from models.edge_node import EdgeNode
from models.enums.user_category import UserCategory
from models.request import Request

from parameters import AREA_DIMENSIONS, GRID_SIZE, NUMBER_OF_USER_TYPES, USER_CATEGORY_DISTRIBUTION, USER_SPEED


class User:
    def __init__(self, id, start_position=None, end_position=None, speed=USER_SPEED, area_dimension=AREA_DIMENSIONS, grid_size=GRID_SIZE, category_distribution=USER_CATEGORY_DISTRIBUTION):
        self.id = id
        self.speed = speed
        self.area_dimension = area_dimension
        self.grid_size = grid_size
        self.time = 0
        self.reached_end_position = False
        self.requests: List[Request] = []
        self.category_distribution = category_distribution
        self.start_position = self.get_random_point(
        ) if start_position is None else start_position
        self.end_position = self.get_random_point(
        ) if end_position is None else end_position
        self.current_position = self.start_position

        self.category = self.choose_random_category()
        self.type = random.randint(
            0, NUMBER_OF_USER_TYPES) if self.category is UserCategory.TYPE else None

    def check_request(self, time):
        return self.requests[0] == time

    def get_request(self):
        return self.requests.pop(0)

    def move(self, time):
        self.time = time
        distance = self.speed * time
        dx = self.end_position[0] - self.start_position[0]
        dy = self.end_position[1] - self.start_position[1]
        total_distance = ((dx ** 2) + (dy ** 2)) ** 0.5
        if distance >= total_distance:
            self.current_position = self.end_position
            self.reached_end_position = True
        else:
            unit_x = dx / total_distance
            unit_y = dy / total_distance
            # Calculate grid-based position
            grid_x = int(self.start_position[0] + (unit_x * distance))
            grid_y = int(self.start_position[1] + (unit_y * distance))
            # Adjust position to fit within grid size
            grid_x = max(min(grid_x, self.grid_size), 0)
            grid_y = max(min(grid_y, self.grid_size), 0)
            self.current_position = (grid_x, grid_y)
            self.reached_end_position = False

    def get_position(self):
        return self.current_position

    def get_position_at_time(self, time):
        if time >= self.time:
            self.move(time - self.time)
        return self.current_position if self.current_position != self.end_position else self.end_position

    def has_reached_end_position(self):
        return self.reached_end_position

    def update_end_position(self):
        if self.reached_end_position:
            self.end_position = self.get_random_point()

    def get_random_point(self) -> tuple:
        """
        Get a random point inside the area dimensions that respects the grid layout.

        Returns:
            tuple: Random point as (x, y) coordinates.
        """
        # Calculate the number of grids in the x and y directions
        num_grids = self.area_dimension // self.grid_size

        # Choose a random grid index in the x and y directions
        grid_index_x = random.randint(0, num_grids - 1)
        grid_index_y = random.randint(0, num_grids - 1)

        # Calculate the starting point coordinates within the chosen grid
        starting_point_x = grid_index_x * \
            self.grid_size + random.uniform(0, self.grid_size)
        starting_point_y = grid_index_y * \
            self.grid_size + random.uniform(0, self.grid_size)

        # Return the random starting point as (x, y) coordinates
        return starting_point_x, starting_point_y

    def get_closest_edge_node(self, edge_nodes: List[EdgeNode], time_epoch: int):
        min_distance = float('inf')
        closest_edge_node = None
        user_position = self.get_position_at_time(time_epoch)

        for edge_node in edge_nodes:
            edge_node_position = edge_node.get_position()
            distance = math.sqrt((user_position[0] - edge_node_position[0]) ** 2 +
                                 (user_position[1] - edge_node_position[1]) ** 2)
            if distance < min_distance:
                min_distance = distance
                closest_edge_node = edge_node

        return closest_edge_node

    def closest_cache_worker(self, cache_workers: List[CacheWorker], time_epoch: int):
        min_distance = float('inf')
        closest_cache_worker = None
        user_position = self.get_position_at_time(time_epoch)

        for cache_worker in cache_workers:
            edge_node_position = cache_worker.edge_node.get_position()
            distance = math.sqrt((user_position[0] - edge_node_position[0]) ** 2 +
                                 (user_position[1] - edge_node_position[1]) ** 2)
            if distance < min_distance:
                min_distance = distance
                closest_cache_worker = cache_worker

        return closest_cache_worker

    def choose_random_category(self) -> UserCategory:
        """
        Chooses a random user category type according to the probabilities defined in the USER_CATEGORY_DISTRIBUTION.

        Returns:
            UserCategory: The chosen user category.
        """
        # Generate a random value from a uniform distribution between 0 and 1
        u = random.random()

        # Initialize cumulative probability
        cumulative_prob = 0

        # Iterate through the user categories and their probabilities
        for category, prob in self.category_distribution.items():
            # Add the probability of the current user category to the cumulative probability
            cumulative_prob += prob

            # If the cumulative probability exceeds the random value, choose the current user category
            if u <= cumulative_prob:
                return category

        # If the loop completes without choosing a user category, return None (or raise an error, depending on your requirements)
        return None

    def __str__(self):
        return f"User {self.id} - Current Position: {self.current_position} - Time: {self.time}"
