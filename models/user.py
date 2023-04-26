import math
import random
import matplotlib.pyplot as plt
from typing import List
from models.cache_worker import CacheWorker
from models.edge_node import EdgeNode
from models.enums.user_category import UserCategory
from models.request import Request

from parameters import AREA_DIMENSIONS, GRID_SIZE, NUMBER_OF_USER_TYPES, USER_CATEGORY_DISTRIBUTION, USER_SPEED


class User:
    def __init__(self, id, start_position=None, end_position=None, speed=USER_SPEED, area_dimension=AREA_DIMENSIONS, category_distribution=USER_CATEGORY_DISTRIBUTION):
        self.id = id
        self.speed = speed
        self.area_dimension = area_dimension
        self.time_in_s = 0
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

    def check_request(self, time_in_ms):
        return self.requests[0] == time_in_ms

    def get_request(self):
        return self.requests.pop(0)

    def move(self, time_in_s=1):
        self.time_in_s = time_in_s
        # Calculate the distance and direction to the end position
        dx = self.end_position[0] - self.current_position[0]
        dy = self.end_position[1] - self.current_position[1]
        distance = math.sqrt(dx**2 + dy**2)
        if distance == 0:
            # print('reached end position - assign new random end position')
            self.reached_end_position = True
            self.end_position = self.get_random_point()
            return True
        self.reached_end_position = False
        direction = (dx/distance, dy/distance)

        # Calculate the maximum distance the user can move in this time step
        max_distance = self.speed * time_in_s

        # Check if the user can reach the end position in this time step
        if max_distance >= distance:
            # print('reached end position in this epoch')
            self.current_position = self.end_position
            return

        # Calculate the new position of the user based on their speed and the time passed
        new_position = (self.current_position[0] + direction[0] * max_distance,
                        self.current_position[1] + direction[1] * max_distance)

        # Check if the new position is closer to the end position than the current position
        new_dx = self.end_position[0] - new_position[0]
        new_dy = self.end_position[1] - new_position[1]
        new_distance = math.sqrt(new_dx**2 + new_dy**2)
        if new_distance < distance:
            # print(f'move towards end position - new position {new_position}')
            self.current_position = new_position

    def get_position(self):
        return self.current_position

    def get_position_at_time(self, time_in_s):
        if time_in_s > self.time_in_s:
            self.move(time_in_s - self.time_in_s)
        return self.current_position

    def get_random_point(self) -> tuple:
        """
        Get a random point inside the area dimensions.

        Returns:
            tuple: Random point as (x, y) coordinates.
        """

        # Choose a random grid index in the x and y directions
        x = random.randint(0, self.area_dimension - 1)
        y = random.randint(0, self.area_dimension - 1)

        return x, y

    def get_closest_edge_node(self, edge_nodes: List[EdgeNode], time_epoch_in_ms: int = None):
        time_epoch_in_s = time_epoch_in_ms / 1000
        time_epoch_in_s = self.time_in_s_in_s if time_epoch_in_s is None else time_epoch_in_s
        min_distance = float('inf')
        closest_edge_node = None
        user_position = self.get_position_at_time(time_epoch_in_s)

        for edge_node in edge_nodes:
            edge_node_position = edge_node.get_position()
            quad_distance = (user_position[0] - edge_node_position[0]) ** 2 + (
                user_position[1] - edge_node_position[1]) ** 2
            distance = math.sqrt(quad_distance)
            if distance < min_distance:
                min_distance = distance
                closest_edge_node = edge_node

        return closest_edge_node

    def closest_cache_worker(self, cache_workers: List[CacheWorker], time_epoch_in_ms: int) -> (CacheWorker | None):
        min_distance = float('inf')

        closest_cache_worker = None
        time_epoch_in_s = time_epoch_in_ms / 1000
        user_position = self.get_position_at_time(time_epoch_in_s)

        for cache_worker in cache_workers:
            edge_node_position = cache_worker.edge_node.get_position()
            distance = math.sqrt((user_position[0] - edge_node_position[0]) ** 2 +
                                 (user_position[1] - edge_node_position[1]) ** 2)
            if distance < min_distance:
                min_distance = distance
                closest_cache_worker = cache_worker

        return closest_cache_worker

    def closest_cache_worker_by_index(self, cache_workers: List[CacheWorker], time_epoch_in_ms: int) -> (int | None):
        min_distance = float('inf')

        closest_cache_worker_index = None
        time_epoch_in_s = time_epoch_in_ms / 1000
        user_position = self.get_position_at_time(time_epoch_in_s)

        for index, cache_worker in enumerate(cache_workers):
            edge_node_position = cache_worker.edge_node.get_position()
            distance = math.sqrt((user_position[0] - edge_node_position[0]) ** 2 +
                                 (user_position[1] - edge_node_position[1]) ** 2)
            if distance < min_distance:
                min_distance = distance
                closest_cache_worker_index = index

        return closest_cache_worker_index

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

    def plot_trajectory(self, max_time=100):
        x = [self.start_position[0]]
        y = [self.start_position[1]]
        plt.rcParams['agg.path.chunksize'] = 10000

        plt.plot(self.end_position[0], self.end_position[1], 'ro')
        plt.plot(self.start_position[0], self.start_position[1], 'ro')

        current_position = self.start_position
        for t in range(1, max_time+1):
            self.move(t)
            if self.reached_end_position:
                print('new end position')
                plt.plot(self.end_position[0], self.end_position[1], 'ro')
            current_position = self.current_position
            x.append(current_position[0])
            y.append(current_position[1])
        plt.plot(self.start_position[0], self.start_position[1], 'ro')
        plt.plot(self.end_position[0], self.end_position[1], 'ro')
        plt.plot(x, y)
        plt.show()

    def __str__(self):
        return f"User {self.id} - Current Position: {self.current_position} - Time: {self.time_in_s}"
