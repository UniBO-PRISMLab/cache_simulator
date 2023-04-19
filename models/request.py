from models.enums.provider_type import ProviderType
from models.resource import Resource


class Request:
    def __init__(self, id, execution_timestamp, provider_type: ProviderType):
        self.id: str = id
        self.provider_type = provider_type
        self.resource: Resource = None
        self.latency = 0
        self.returned_to_client = False
        self.execution_timestamp = execution_timestamp

    def calculate_aoi(self, current_time) -> (float | None):
        """
        Calculates the Age of Information (AoI) if the request was already returned to the client given the current time.

        Args:
            resource_time: The time when the resource was collected.

        Returns:
            float: The Age of Information (AoI) in ms.
        """
        if not self.returned_to_client:
            return
        resource_time = self.resource.storage_time()
        aoi = current_time - resource_time
        return aoi

    def __str__(self):
        return f"Request {self.id} - provider: {self.provider_type} - latency: {self.latency} - created_at: {self.execution_timestamp} "
