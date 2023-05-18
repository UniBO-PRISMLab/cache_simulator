from models.edge_node import EdgeNode
from models.enums.order_type import OrderType
from models.provider import Provider


class CachingOrder:
    """
    A class representing a caching order to be executed by a cache worker.

    Attributes
    ----------
    type : OrderType, optional
        The type of the caching order, defaults to OrderType.STANDARD.
    cache_worker_id : int
        The id of the cache worker responsible for executing the caching order.
    execution_time : int
        The epoch time at which the caching order should be executed.
    expiration_time : int
        The epoch time at which the caching order will expire.
    provider : Provider
        The provider from which the data will be fetched and cached.
    request_execution_time : int, optional
        The epoch time at which the user requested the data.
    cooperator_edge_node : EdgeNode, optional
        The EdgeNode that will share the data, only present for cooperative orders.
    is_cooperator_pointer: boolean
        If True, this order is the pointer for a cooperative order, hence, it cannot be converted to cooperative itself.
    """
    def __init__(self, cache_worker_id: int, execution_time, expiration_time, provider: Provider,
                 type=OrderType.STANDARD, cooperator_edge_node: EdgeNode = None, request_execution_time: int = None):
        self.type = type
        self.cache_worker_id = cache_worker_id
        self.execution_time = execution_time
        self.expiration_time = expiration_time
        self.provider = provider
        self.request_execution_time = request_execution_time
        self.cooperator_edge_node = cooperator_edge_node
        self.is_cooperator_pointer = False

    def __str__(self):
        return f"CachingOrder(Type: {self.type}, Cache Worker ID: {self.cache_worker_id}, Execution Time: {self.execution_time}, Expiration Time: {self.expiration_time}, Provider: {self.provider}, Request Execution Time: {self.request_execution_time}, Cooperator Edge Node: {self.cooperator_edge_node}) -- is_cooperator_pointer {self.is_cooperator_pointer}"
