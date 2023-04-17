class Resource:
    def __init__(self, resource_id, size, storage_time=None, expiration_time=None):
        self.resource_id = resource_id
        self.size = size
        self.storage_time = storage_time
        self.expiration_time = expiration_time
        self.frequency = 0
        self.last_time_retrieved = None
