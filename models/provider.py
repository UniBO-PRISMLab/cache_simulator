from models.bytes_and_time import bytes_and_time
from models.enums.provider_type import ProviderType
import random
import string
import os

from parameters import CLOUD_TRACE_PATH, PROVIDER_DISTRIBUTION

class Provider:
    def __init__(
            self, index: int, provider_type: ProviderType = None, provider_distribution=PROVIDER_DISTRIBUTION,
            path=CLOUD_TRACE_PATH):
        self.index = index
        self.path = path
        self.id = self.generate_random_string()
        self.provider_distribution = provider_distribution
        self.network_trace = self.assign_random_cloud_trace()
        self.number_of_requests = 0
        self.provider_type = provider_type if provider_type != None else self.choose_random_provider_type()

    def assign_random_cloud_trace(self) -> string:
        # Get a list of all subdirectories in the path
        subdirs = [d for d in os.listdir(self.path) if os.path.isdir(os.path.join(self.path, d))]

        # Choose a random subdirectory
        random_subdir = random.choice(subdirs)

        # Get a list of all files in the chosen subdirectory
        files = [f for f in os.listdir(os.path.join(self.path, random_subdir))
                 if os.path.isfile(os.path.join(self.path, random_subdir, f))]

        # Choose a random file
        random_file = random.choice(files)

        # Return the relative path to the chosen file
        return os.path.join(random_subdir, random_file)

    def choose_random_provider_type(self) -> ProviderType:
        """
        Chooses a random provider type according to the probabilities defined in the PROVIDER_DISTRIBUTION.

        Returns:
            ProviderType: The chosen provider type.
        """
        # Generate a random value from a uniform distribution between 0 and 1
        u = random.random()

        # Initialize cumulative probability
        cumulative_prob = 0

        # Iterate through the provider types and their probabilities
        for provider_type, prob in self.provider_distribution.items():
            # Add the probability of the current provider type to the cumulative probability
            cumulative_prob += prob

            # If the cumulative probability exceeds the random value, choose the current provider type
            if u <= cumulative_prob:
                return provider_type

        # If the loop completes without choosing a provider type, return None (or raise an error, depending on your requirements)
        return None

    def generate_random_string(self, length: int = 32) -> str:
        """
        Generates a random string of the specified length.

        Args:
            length (int): The desired length of the random string.

        Returns:
            str: The random string.
        """
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))

    def get_latency(self):
        return bytes_and_time.get_time(self.provider_type)

    def get_bytes(self):
        return bytes_and_time.get_bytes(self.provider_type)

    def get_latency_and_bytes(self):
        self.number_of_requests += 1
        return (self.get_latency(), self.get_bytes())

    def __str__(self):
        if self.provider_type != None:
            return f"Provider {self.id} of type {self.provider_type.value}"
