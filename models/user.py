import math
from shared.RandomGenerator import regular_random
import matplotlib.pyplot as plt
from typing import List, Tuple
from models.cache_worker import CacheWorker
from models.edge_node import EdgeNode
from models.enums.user_category import UserCategory
from models.request import Request
from decimal import *
from parameters import AREA_DIMENSIONS, NUMBER_OF_USER_TYPES, USER_CATEGORY_DISTRIBUTION, USER_SPEED, USER_WAYPOINTS


class User:
    def __init__(self, id, start_position=None, speed=USER_SPEED, area_dimension=AREA_DIMENSIONS,
                 category_distribution=USER_CATEGORY_DISTRIBUTION, waypoints=USER_WAYPOINTS,
                 number_of_types=NUMBER_OF_USER_TYPES):
        self.i = 0
        self.id = id
        self.speed = Decimal(speed)
        self.area_dimension = area_dimension
        self.time_in_s = Decimal(0)
        self.reached_end_position = False
        self.requests: List[Request] = []
        self.category_distribution = category_distribution
        self.start_position: Tuple[Decimal, Decimal] = self.get_random_point(
        ) if start_position is None else start_position
        self.waypoints = [self.get_random_point() for i in range(waypoints)]
        self.waypoint_index = 0
        self.current_position: Tuple[Decimal, Decimal] = self.start_position
        self.category = self.choose_random_category()
        self.number_of_types = number_of_types
        self.type = regular_random.randint(
            0, self.number_of_types-1) if self.category is UserCategory.TYPE else None
        self.number_of_requests = 1
        self.distance = 0

    def check_request(self, time_in_ms):
        return (self.requests[0].execution_time == time_in_ms) if len(self.requests) > 0 else False

    def get_request(self):
        return self.requests.pop(0)

    def _move(self, time_passed_in_ms: Decimal, apply_movement: bool = False):
        if (time_passed_in_ms == 0):
            return self.current_position
        position = self.current_position
        waypoint_index = self.waypoint_index
        distance_to_waypoint = self._distance_to(position, self.waypoints[self.waypoint_index])
        total_movement = self.speed * time_passed_in_ms
        while total_movement > 0:
            if distance_to_waypoint <= total_movement:
                # Move to waypoint and update index
                position = self.waypoints[waypoint_index]
                waypoint_index = (waypoint_index + 1) % len(self.waypoints)
                total_movement -= distance_to_waypoint
                distance_to_waypoint = self._distance_to(position, self.waypoints[waypoint_index])
            else:
                # Move towards waypoint
                position = self._move_towards(position, self.waypoints[waypoint_index], total_movement)

                if apply_movement:
                    self.current_position = position
                    self.waypoint_index = waypoint_index
                return position

    def _calculate_distance_and_direction_to_endpoint(self, position, waypoint_index):
        end_position = self.waypoints[waypoint_index]
        dx = end_position[0] - position[0]
        dy = end_position[1] - position[1]
        distance = Decimal(math.sqrt(dx**2 + dy**2))
        direction = (dx/distance, dy/distance)
        return distance, direction

    def get_position(self):
        return self.current_position

    def get_random_point(self) -> tuple:
        """
        Get a random point inside the area dimensions.

        Returns:
            tuple: Random point as (x, y) coordinates.
        """

        # Choose a random grid index in the x and y directions
        x = Decimal(regular_random.randint(0, self.area_dimension - 1))
        y = Decimal(regular_random.randint(0, self.area_dimension - 1))

        return x, y

    def get_closest_edge_node(self, edge_nodes: List[EdgeNode], time_epoch_in_ms: int = None):
        time_epoch_in_ms = self.time_in_ms if time_epoch_in_ms is None else time_epoch_in_ms
        min_distance = Decimal('inf')
        closest_edge_node = None
        user_position = self._move(time_epoch_in_ms)

        for edge_node in edge_nodes:
            edge_node_position = edge_node.get_position()
            quad_distance = (user_position[0] - edge_node_position[0]) ** 2 + (
                user_position[1] - edge_node_position[1]) ** 2
            distance = math.sqrt(quad_distance)
            if distance < min_distance:
                min_distance = distance
                closest_edge_node = edge_node

        return closest_edge_node

    def closest_cache_worker(self, cache_workers: List[CacheWorker]):
        cache_worker_id = self.closest_cache_worker_by_id(cache_workers)
        return cache_workers[cache_worker_id]

    def closest_cache_worker_by_id(self, cache_workers: List[CacheWorker]):
        min_distance = Decimal('inf')
        closest_cache_worker_index = None
        user_position = self.current_position

        for index, cache_worker in enumerate(cache_workers):
            edge_node_position = cache_worker.edge_node.get_position()
            distance = math.sqrt((user_position[0] - edge_node_position[0]) ** 2 +
                                 (user_position[1] - edge_node_position[1]) ** 2)
            if distance < min_distance:
                min_distance = distance
                closest_cache_worker_index = index

        return closest_cache_worker_index

    def closest_cache_worker_by_index_in_time(
            self, cache_workers: List[CacheWorker],
            time_epoch_in_ms: int):
        min_distance = Decimal('inf')

        closest_cache_worker_index = None
        user_position = self.current_position  # self._move(time_epoch_in_ms)
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
        u = regular_random.random()

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

    def epoch_passed(self, time_epoch_in_ms):
        time_epoch_in_ms = Decimal(time_epoch_in_ms)
        passed_time_in_ms = time_epoch_in_ms - self.time_in_s
        self.time_in_s = time_epoch_in_ms
        self._move(passed_time_in_ms, True)

    def get_position_at_time(self, time_in_ms):
        return self._move(time_in_ms)

    def _move_towards(self, current_position: Tuple[Decimal, Decimal],
                      target_position: Tuple[Decimal, Decimal],
                      total_distance: Decimal) -> Tuple[Decimal, Decimal]:
        distance = self._distance_to(current_position, target_position)
        if distance == 0:
            return current_position
        ratio = total_distance / distance
        x = current_position[0] + (target_position[0] - current_position[0]) * ratio
        y = current_position[1] + (target_position[1] - current_position[1]) * ratio
        return (x, y)

    def _distance_to(self, current_position, other_position):
        dx = other_position[0] - current_position[0]
        dy = other_position[1] - current_position[1]
        distance = Decimal(math.sqrt(dx ** 2 + dy ** 2))
        return distance

    def __str__(self):
        return f"User {self.id} - Current Position: {self.current_position} - Time: {self.time_in_s}"
