from decimal import Decimal
from shared.helper import calculate_decimal_distance
from models.resource import Resource
from models.time_trace_loader import time_trace_loader
from shared.RandomGenerator import regular_random, np_random
import math
import hashlib
import sys

from typing import List, Tuple
from models.enums.provider_type import ProviderType
from models.enums.user_category import UserCategory
from models.provider import Provider
from models.user import User
from models.request import Request

from parameters import AREA_DIMENSIONS, EXPERIMENT_DURATION, GENERATE_TRACE, MAX_PERIODICITY_PER_SUBAREA, MIN_PERIODICITY_PER_SUBAREA, MIN_REQUESTS_FARTHEST, NUMBER_OF_USER_TYPES, NUMBER_OF_USERS, PERIOD, POPULARITY_DISTRIBUTION, RATE_OF_EVENT, SUBAREAS

# TODO: move Area class to a dedicated class file


class Area:
    def __init__(self, id,  x1, y1, x2, y2, periodicity=0):
        self.id = id
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.popularity: List[Provider] = []
        self.periodicity = periodicity

    def __str__(self):
        return f"Area #{self.id} - p: {self.periodicity} - X: ({self.x1}, {self.x2}) Y: ({self.y1}, {self.y2}) "


class RequestGenerator:
    """
        Responsible to generate the list of requests for each user
    """

    def __init__(
            self, users: List[User],
            providers: List[Provider],
            popularity_distribution=POPULARITY_DISTRIBUTION, experiment_duration=EXPERIMENT_DURATION,
            number_of_users=NUMBER_OF_USERS, number_of_types=NUMBER_OF_USER_TYPES, generate_trace=GENERATE_TRACE):
        self.providers = providers
        self.experiment_duration = experiment_duration
        self.users = users
        self.popularity_distribution = popularity_distribution
        self.number_of_types = number_of_types
        self.number_of_users = number_of_users
        self.popularity = {
            UserCategory.TYPE.value: self.generate_popularity_per_type(),
            UserCategory.LOCATION.value: self.generate_popularity_per_location(),
            UserCategory.ID.value: self.generate_popularity_per_user()
        }
        self.generate_trace = generate_trace
        self.point_of_interest = self.random_point_of_interest()
        self.max_distance = None

        self.generate_requests()

    def generate_requests(self):
        """
        Populate the request list of each users with request for the EXPERIMENT_DURATION.
        The inter-arrival times between events follow an exponential distribution with rate RATE_OF_EVENT .
        The popularity of each provider is given by a Zipf distribution  with popularity given by POPULARITY_DISTRIBUTION and truncate according to the NUMBER OF PROVIDER PER TYPE
        """
        for user in self.users:
            user.distance = calculate_decimal_distance(user.current_position, self.point_of_interest)
        #distances = [calculate_decimal_distance(user.current_position, self.point_of_interest) for user in self.users]
        # index = [0 for user in self.users]
        sorted_users = sorted(self.users, key=lambda user: user.distance)

        user = sorted_users[-1]
        self.max_distance = user.distance
        print(user)
        current_time = 0
        print(f"farthest device will make {MIN_REQUESTS_FARTHEST*PERIOD} reqs")
        for i in range(MIN_REQUESTS_FARTHEST*PERIOD):
            size = self.next_size_from_trace(user.id)
            latency = self.next_latency_from_trace(user.id)
            user.number_of_requests = i
            next_request_in_ms = self.custom_math_function(user.number_of_requests, user.distance)
            # print(next_request_in_ms)
            next_request_execution_time = next_request_in_ms + current_time
            current_time += (next_request_in_ms)
            # print(current_time)
            provider = self.providers[0] if self.generate_trace else self.choose_provider_id(user, current_time)
            new_request = Request(
                next_request_execution_time, provider)
            new_request.application_latency = latency
            new_request.resource = Resource(0, size)
            new_request.user_location = user.current_position
            user.requests.append(new_request)

        self.experiment_duration = current_time
        print('experiment duration', self.experiment_duration)
        # sys.exit()
        print(current_time)
        for user in sorted_users[:-1]:
            current_time = 0
            while current_time <= self.experiment_duration:
                size = self.next_size_from_trace(user.id)
                latency = self.next_latency_from_trace(user.id)
                next_request_in_ms = self.custom_math_function(user.number_of_requests, user.distance)
                user.number_of_requests += 1
                # print(next_request_in_ms)
                next_request_execution_time = next_request_in_ms + current_time
                if next_request_execution_time >= self.experiment_duration:
                    break
                current_time += (next_request_in_ms)
                provider = self.providers[0] if self.generate_trace else self.choose_provider_id(user, current_time)
                new_request = Request(
                    next_request_execution_time, provider)
                new_request.application_latency = latency
                new_request.resource = Resource(0, size)
                new_request.user_location = user.current_position
                user.requests.append(new_request)

    def generate_requests_pattern_per_location(self) -> List[Area]:
        subareas = self.divide_square_area()
        for subarea in subareas:
            subarea.periodicity = regular_random.randint(MIN_PERIODICITY_PER_SUBAREA, MAX_PERIODICITY_PER_SUBAREA)
            print(subarea)
        return subareas

    def custom_math_function(self, index, distance, amplitude_percentage=0.25, period=PERIOD):
        scale = 3600000
        distance = distance * scale
        #scaled_distance = (distance - 0) / (self.max_distance - 0)
        result = ((distance * amplitude_percentage) * abs(math.sin((index * math.pi) / period))) + distance
        return result + self.generate_noise(result)

    def generate_noise(self, value, percentage=0.1):
        max = percentage * value
        return regular_random.uniform(-max, +max)

    def next_event_time_from_function(self, position: Tuple[Decimal, Decimal]):
        subarea = self.find_subarea(position, self.popularity[UserCategory.LOCATION.value])
        return subarea.periodicity

    def next_size_from_trace(self, id: int):
        return time_trace_loader.get_size(id)

    def next_event_time_from_trace(self, id: int):
        return time_trace_loader.get_time(id)

    def next_latency_from_trace(self, id: int):
        return time_trace_loader.get_application_latency(id)

    def next_event_time(self, rate: float = RATE_OF_EVENT):
        """
        Generates the time of the next event according to an exponential distribution.

        Args:
            rate (float): The average rate of events per unit of time (ms).

        Returns:
            int: The time of the next event in ms.
        """
        # Generate a random value from a uniform distribution between 0 and 1
        u = regular_random.random()

        # Calculate the time of the next event using the inverse of the cumulative distribution function (CDF) of the exponential distribution
        time = -math.log(1 - u) / rate
        discrete_time = int(time)
        if (discrete_time <= 0):
            return self.next_event_time(rate)
        return int(time)

    # solve time problem = user in s and rest in ms

    def choose_provider_id(self, user: User, request_time: int) -> Provider:
        provider_index = np_random.zipf(a=self.popularity_distribution)
        if provider_index >= len(self.providers):
            return self.choose_provider_id(user, request_time)
        if user.category == UserCategory.TYPE:
            return self.popularity[UserCategory.TYPE.value][user.type - 1][provider_index]
        elif user.category == UserCategory.ID:
            return self.popularity[UserCategory.ID.value][user.id][provider_index]
        elif user.category == UserCategory.LOCATION:
            user_location = user.get_position_at_time(request_time)

            user_subarea = self.find_subarea(user_location, self.popularity[UserCategory.LOCATION.value])
            if (user_subarea == -1):
                print("error in user position")
                print(user_location)
                sys.exit()
            return user_subarea.popularity[provider_index]
        else:
            print(f"Invalid user category {user.category} - cannot choose provider id")
            return

    @staticmethod
    def generate_request_id(provider_id: int, provider_type: ProviderType):
        plain_id = f"{provider_type}/{provider_id}"
        return hashlib.sha256(plain_id.encode())

    def generate_popularity_per_type(self) -> List[List[Provider]]:
        return [regular_random.sample(self.providers, len(self.providers)) for i in range(self.number_of_types)]

    def generate_popularity_per_location(self) -> List[Area]:
        subareas = self.divide_square_area()
        for subarea in subareas:
            subarea.popularity = regular_random.sample(
                self.providers, len(self.providers))
        return subareas

    def generate_popularity_per_user(self) -> List[List[Provider]]:
        return [regular_random.sample(self.providers, len(self.providers)) for i in range(self.number_of_users)]

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
        return -1  # If point does not belong to any

    def random_point_of_interest(self, dimensions: int = AREA_DIMENSIONS) -> Tuple[int, int]:
        x = regular_random.randint(0, dimensions - 1)
        y = regular_random.randint(0, dimensions - 1)
        return x, y
