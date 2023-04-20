import math
import random
from typing import List
from models.cache_worker import CacheWorker
from models.edge_node import EdgeNode
from models.enums.user_category import UserCategory
from models.request import Request

from parameters import AREA_DIMENSIONS, GRID_SIZE, USER_SPEED


class User:
    def __init__(self, user_id, user_category: UserCategory, user_type=None, start_position=None, end_position=None, speed=USER_SPEED, area_dimension=AREA_DIMENSIONS, grid_size=GRID_SIZE):
        self.user_id = user_id
        self.user_category = user_category
        if user_category is UserCategory.TYPE:
            self.user_type = user_type
        self.start_position = start_position
        self.end_position = end_position
        self.speed = speed
        self.area_dimension = area_dimension
        self.grid_size = grid_size
        self.time = 0
        self.reached_end_position = False
        self.requests: List[Request] = []
        if end_position is None:
            self.end_position = self.get_random_point()
        if start_position is None:
            self.start_position = self.get_random_point()
        self.current_position = self.start_position

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

    def __str__(self):
        return f"User {self.user_id} - Current Position: {self.current_position} - Time: {self.time}"
