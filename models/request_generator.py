import random
import math
import hashlib
import numpy as np
from typing import List
from models.enums.provider_type import ProviderType
from models.user import User
from parameters import EXPERIMENT_DURATION, POPULARITY_DISTRIBUTION, PROVIDER_DISTRIBUTION, RATE_OF_EVENT, TIME_WINDOW_SIZE, NUMBER_OF_PROVIDERS_PER_TYPE
from models.request import Request


class RequestGenerator:
    """
        Responsible to generate the list of requests for each user
    """
    def __init__(self, users: List[User], provider_distribution=PROVIDER_DISTRIBUTION, time_window=TIME_WINDOW_SIZE, popularity_distribution=POPULARITY_DISTRIBUTION, number_of_providers_per_type=NUMBER_OF_PROVIDERS_PER_TYPE, seed=42):
        np.random.seed(seed=seed)
        random.seed(seed)
        self.number_of_providers_per_type = number_of_providers_per_type
        self.users = users
        self.provider_distribution = provider_distribution
        self.time_window = time_window
        self.generate_request_id()
        pass

    def generate_requests(self):
        """
        Populate the request list of each users with request for the EXPERIMENT_DURATION.
        The inter-arrival times between events follow an exponential distribution with rate RATE_OF_EVENT .
        The popularity of each provider is given by a Zipf distribution  with popularity given by POPULARITY_DISTRIBUTION and truncate according to the NUMBER OF PROVIDER PER TYPE       
        """
        for user in self.users:
            current_time = 0
            while current_time >= EXPERIMENT_DURATION: 
                next_request_execution_time = self.next_request_time() + current_time
                current_time += next_request_execution_time
                if next_request_execution_time >= EXPERIMENT_DURATION:
                    break
                provider_id = self.choose_provider_id()
                provider_type = self.choose_provider_type()
                request_id =  RequestGenerator.generate_request_id(provider_id, provider_type)
                new_request = Request(request_id, next_request_execution_time, provider_type)
                user.requests.append(new_request)

    def choose_provider_type(self) -> ProviderType:
        """
        Chooses a provider type according to the probabilities defined in the PROVIDER_DISTRIBUTION.

        Returns:
            ProviderType: The chosen provider type.
        """
        # Generate a random value from a uniform distribution between 0 and 1
        u = random.random()

        # Initialize cumulative probability
        cumulative_prob = 0

        # Iterate through the provider types and their probabilities
        for provider_type, prob in PROVIDER_DISTRIBUTION.items():
            # Add the probability of the current provider type to the cumulative probability
            cumulative_prob += prob

            # If the cumulative probability exceeds the random value, choose the current provider type
            if u <= cumulative_prob:
                return provider_type

        # If the loop completes without choosing a provider type, return None (or raise an error, depending on your requirements)
        return None

    def next_event_time(self, rate: float = RATE_OF_EVENT):
        """
        Generates the time of the next event according to an exponential distribution.

        Args:
            rate (float): The average rate of events per unit of time (ms).

        Returns:
            float: The time of the next event in ms.
        """
        # Generate a random value from a uniform distribution between 0 and 1
        u = random.random()

        # Calculate the time of the next event using the inverse of the cumulative distribution function (CDF) of the exponential distribution
        time = -math.log(1 - u) / rate

        return time

    def choose_provider_id(self):
        provider = np.random.zipf(a=self.popularity_distribution)
        if provider > self.number_of_providers_per_type:
            return self.choose_provider_id()
        return provider

    @staticmethod
    def generate_request_id(provider_id:int,provider_type:ProviderType):
        return hashlib.sha256(bytes(f"{provider_type}/{provider_id}"))
