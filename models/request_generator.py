import random
import math
import hashlib
import numpy as np

from typing import List, Tuple
from models.enums.provider_type import ProviderType
from models.enums.user_category import UserCategory
from models.provider import Provider
from models.user import User
from models.request import Request

from parameters import AREA_DIMENSIONS, EXPERIMENT_DURATION, NUMBER_OF_USER_TYPES, NUMBER_OF_USERS, POPULARITY_DISTRIBUTION, PROVIDER_DISTRIBUTION, RATE_OF_EVENT, SUBAREAS, TIME_WINDOW_SIZE

# TODO: move Area class to a dedicated class file


class Area:
    def __init__(self, id,  x1, y1, x2, y2):
        self.id = id
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.popularity: List[Provider] = []

    def __str__(self):
        return f"Area #{self.id} - X: ({self.x1}, {self.x2}) Y: ({self.y1}, {self.y2}) "


class RequestGenerator:
    """
        Responsible to generate the list of requests for each user
    """

    def __init__(self, users: List[User], providers: List[Provider], time_window=TIME_WINDOW_SIZE, popularity_distribution=POPULARITY_DISTRIBUTION, experiment_duration=EXPERIMENT_DURATION, seed=42):
        np.random.seed(seed=seed)
        random.seed(seed)
        self.providers = providers
        self.experiment_duration = experiment_duration
        self.users = users
        self.time_window = time_window
        self.popularity_distribution = popularity_distribution
        self.popularity = {
            UserCategory.TYPE.value: self.generate_popularity_per_type(),
            UserCategory.LOCATION.value: self.generate_popularity_per_location(),
            UserCategory.ID.value: self.generate_popularity_per_user()
        }
        self.generate_requests()

    def generate_requests(self):
        """
        Populate the request list of each users with request for the EXPERIMENT_DURATION.
        The inter-arrival times between events follow an exponential distribution with rate RATE_OF_EVENT .
        The popularity of each provider is given by a Zipf distribution  with popularity given by POPULARITY_DISTRIBUTION and truncate according to the NUMBER OF PROVIDER PER TYPE
        """
        for user in self.users:
            current_time = 0
            while current_time <= self.experiment_duration:
                next_request_execution_time = self.next_event_time() + current_time
                current_time += next_request_execution_time
                if next_request_execution_time >= self.experiment_duration:
                    break
                provider = self.choose_provider_id(user, current_time)
                new_request = Request(
                    next_request_execution_time, provider)
                user.requests.append(new_request)

    def next_event_time(self, rate: float = RATE_OF_EVENT):
        """
        Generates the time of the next event according to an exponential distribution.

        Args:
            rate (float): The average rate of events per unit of time (ms).

        Returns:
            int: The time of the next event in ms.
        """
        # Generate a random value from a uniform distribution between 0 and 1
        u = random.random()

        # Calculate the time of the next event using the inverse of the cumulative distribution function (CDF) of the exponential distribution
        time = -math.log(1 - u) / rate

        return int(time)

    def choose_provider_id(self, user: User, request_time: int) -> Provider:
        provider_index = np.random.zipf(a=self.popularity_distribution)
        if provider_index > len(self.providers):
            return self.choose_provider_id()
        if user.category == UserCategory.TYPE:
            return self.popularity[UserCategory.TYPE.value][user.type][provider_index]
        elif user.category == UserCategory.ID:
            return self.popularity[UserCategory.ID.value][user.id][provider_index]
        elif user.category == UserCategory.LOCATION:
            user_location = user.get_position_at_time(request_time)
            user_subarea = self.find_subarea(
                user_location, self.popularity[UserCategory.LOCATION.value])
            return user_subarea.popularity[provider_index]
        else:
            print(
                f"Invalid user category {user.category} - cannot choose provider id")
            return

    @staticmethod
    def generate_request_id(provider_id: int, provider_type: ProviderType):
        plain_id = f"{provider_type}/{provider_id}"
        return hashlib.sha256(plain_id.encode())

    def generate_popularity_per_type(self) -> List[List[Provider]]:
        return [random.sample(self.providers, len(self.providers)) for i in range(NUMBER_OF_USER_TYPES)]

    def generate_popularity_per_location(self) -> List[Area]:
        subareas = self.divide_square_area()
        for subarea in subareas:
            subarea.popularity = random.sample(
                self.providers, len(self.providers))
        return subareas

    def generate_popularity_per_user(self) -> List[List[Provider]]:
        return [random.sample(self.providers, len(self.providers)) for i in range(NUMBER_OF_USERS)]

    def divide_square_area(self, dimensions: int = AREA_DIMENSIONS, portions: int = SUBAREAS) -> List[Area]:
        """
        Divides a square area of given dimensions into N square portions of equal size.
        Each portion is assigned an id and its dimensions are returned as a tuple.

        Args:
            dimensions (int): The dimensions of the square area.
            portions (int): The number of portions to divide the area into.

        Returns:
            List[Area]: The list of subareas, where each subarea is a tuple containing an id and its dimensions.
        """
        subarea_dimensions = dimensions // int(portions ** 0.5)
        subareas = []
        for i in range(portions):
            row = i // int(portions ** 0.5)
            col = i % int(portions ** 0.5)
            x1, y1 = col * subarea_dimensions, row * subarea_dimensions
            x2, y2 = x1 + subarea_dimensions, y1 + subarea_dimensions
            subarea = Area(i, x1, y1, x2, y2)
            subareas.append(subarea)
        return subareas

    def find_subarea(self, point: Tuple[int, int], subareas: List[Area]) -> Area:
        """
        Finds the subarea that the given point belongs to.

        Args:
            point (Tuple[int, int]): The point to find the subarea for.
            subareas (List[Area]): The list of subareas to search.

        Returns:
            int: The id of the subarea that the point belongs to.
        """
        for subarea in subareas:
            if subarea.x1 <= point[0] < subarea.x2 and subarea.y1 <= point[1] < subarea.y2:
                return subarea
        return -1  # If point does not belong to any subarea
