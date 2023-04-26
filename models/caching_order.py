from models.enums.order_type import OrderType
from models.provider import Provider


class CachingOrder:
    def __init__(self, cache_worker_id: int, execution_time, expiration_time, provider: Provider, type=OrderType.STANDARD, cooperator_cache_worker: int = None):
        self.type = type
        self.cache_worker_id = cache_worker_id
        self.execution_time = execution_time
        self.expiration_time = expiration_time
        self.provider = provider
        if type == OrderType.COOPERATIVE:
            self.cooperator_cache_worker = cooperator_cache_worker
