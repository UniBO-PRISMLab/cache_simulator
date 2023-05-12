import uuid

from models.provider import Provider
from models.resource import Resource


class Request:
    def __init__(self, execution_time: int, provider: Provider): #,cache_worker: int):
        #self.id: str = uuid.uuid4()
        self.provider = provider
        self.resource: Resource = None
        self.network_latency = 0
        self.application_latency = 0
        self.execution_time = execution_time
        #self.cache_worker = cache_worker

    def calculate_aoi(self, current_time):
        """
        Calculates the Age of Information (AoI) if the request was already returned to the client given the current time.

        Args:
            resource_time: The time when the resource was collected.

        Returns:
            float: The Age of Information (AoI) in ms.
        """
        resource_time = self.resource.creation_time
        aoi = current_time - resource_time
        return aoi

    def get_total_latency(self):
        return self.network_latency + self.application_latency

    def __str__(self):
        return f"Request - {self.provider} - latency: {self.get_total_latency()} - created_at: {self.execution_time} "
