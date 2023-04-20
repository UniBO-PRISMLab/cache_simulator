from models.bytes_and_time import bytes_and_time
from models.enums.provider_type import ProviderType
import random
import string

from parameters import PROVIDER_DISTRIBUTION


class Provider:
    def __init__(self, index: int, provider_type: ProviderType = None, provider_distribution=PROVIDER_DISTRIBUTION,):
        self.index = index
        self.id = self.generate_random_string()
        self.provider_distribution = provider_distribution

        self.provider_type = provider_type if provider_type != None else self.choose_random_provider_type()

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
        return (self.get_provider_latency, self.get_provider_bytes)

    def __str__(self):
        if self.provider_type != None:
            return f"Provider {self.id} of type {self.provider_type.value}"
