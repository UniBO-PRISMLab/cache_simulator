import sys
from typing import List

from models.resource import Resource
from models.request import Request
from models.enums.order_type import OrderType
from models.edge_node import EdgeNode
from models.caching_order import CachingOrder
from parameters import CACHE_NOT_FOUND_RESOURCE, DEFAULT_EXPIRATION_TIME, NEIGHBOR_EDGE_NODES
from shared.helper import calculate_distance
from models.network_latency import network_latency


class CacheWorker:
    """
    A CacheWorker represents a caching server in the network.

    Attributes
    ----------
    id : int
        The identifier of the CacheWorker.
    cooperative_orders : List[CachingOrder]
        The list of cooperative orders this CacheWorker has.
    edge_node : EdgeNode
        The EdgeNode that is responsible for this CacheWorker.
    cache_nodes : List[EdgeNode]
        The list of cache nodes sorted by distance from the EdgeNode.
    total_requests : int
        The total number of requests this CacheWorker has received.
    cached_requests : int
        The number of requests that have been cached by this CacheWorker.
    classical_caching : int
        The maximum number of resources that can be cached by this CacheWorker using classical caching.
    neighbor_resources : int
        The amount of resources that this CacheWorker can request from its neighbors.
    pending_orders : List[CachingOrder]
        The list of pending orders this CacheWorker has.

    Methods
    -------
    get_ordered_cache_nodes_by_distance(edge_node: EdgeNode, cache_nodes: List[EdgeNode],
                                          neighbor_edge_nodes=NEIGHBOR_EDGE_NODES) -> List[EdgeNode]:
        Orders the cache nodes by distance from the given EdgeNode.

    check_cooperative_order(order: CachingOrder) -> bool:
        Checks if the given order is cooperative and adds it to the list of cooperative orders if it is.

    check_pending_orders(current_time: int, global_order_list: List[CachingOrder]) -> None:
        Checks if there are any pending orders that can be executed and executes them.

    execute_order(order: CachingOrder) -> None:
        Executes the given order.

    request_resource(request: Request, current_time: int, global_order_list: List[CachingOrder]) -> Union[str, None]:
        Attempts to cache the given request and returns the status message.

    get_cooperative_caching_info() -> Tuple[int, int, List[Tuple[int, int, int]]]:
        Returns the information about the cooperative orders.

    get_classical_caching_info() -> Tuple[int, int]:
        Returns the information about the classical caching.
    """

    def __init__(
            self, id: int, edge_node: EdgeNode, cache_nodes: List[EdgeNode],
            neighbor_edge_nodes=NEIGHBOR_EDGE_NODES, classical_caching=CACHE_NOT_FOUND_RESOURCE):
        self.id = id
        self.cooperative_orders: List[CachingOrder] = []
        self.edge_node = edge_node
        self.cache_nodes = self.get_ordered_cache_nodes_by_distance(edge_node, cache_nodes, neighbor_edge_nodes)
        self.total_requests = 0
        self.cached_requests = 0
        self.classical_caching = classical_caching
        self.neighbor_resources = 0
        self.pending_orders: List[CachingOrder] = []

    def get_ordered_cache_nodes_by_distance(
            self, edge_node: EdgeNode, cache_nodes: List[EdgeNode],
            neighbor_edge_nodes: int) -> List[EdgeNode]:
        """
        Returns a list of N CacheNode objects sorted by their distance from the passed EdgeNode object.

        Args:
        - edge_node (EdgeNode): The EdgeNode object for which the cache nodes need to be sorted by distance.
        - cache_nodes (List[EdgeNode]): The list of EdgeNode objects.
        - neighbor_edge_nodes (int): the list size

        Returns:
        - List[EdgeNode]: The list of EdgeNode objects sorted by their distance from the passed EdgeNode object.
        """
        if neighbor_edge_nodes <= 0:
            return []
        # Calculate distances from the edge_node to each cache_node
        distances = {}
        for cache_node in cache_nodes:
            if (cache_node.id != self.edge_node.id):
                distance = calculate_distance(edge_node.get_position(), cache_node.get_position())
                distances[cache_node] = distance
        # Sort the cache_nodes by distance in ascending order
        ordered_cache_nodes = sorted(distances.keys(), key=lambda x: distances[x])
        limit_index = neighbor_edge_nodes
        return ordered_cache_nodes[:limit_index]

    def add_caching_orders(self, orders: List[CachingOrder]):
        """
        Add a list of CachingOrders to the cache worker. The orders are separated into two lists: 
        cooperative orders and standard orders. The standard orders are sorted by execution time.

        Parameters:
        -----------
        orders : List[CachingOrder]
        The list of orders to be added to the cache worker.
        """
        for order in orders:
            if order.type == OrderType.STANDARD:
                self.pending_orders.append(order)
            else:
                self.cooperative_orders.append(order)
        self.pending_orders = sorted(
            self.pending_orders, key=lambda x: x.execution_time)

    def remove_expired_cooperative_orders(self, current_time):
        """
        Removes expired cooperative orders from the cache worker.

        Parameters:
        -----------
        current_time : int
            The current time in epoch format.
        """
        self.cooperative_orders = [
            order for order in self.cooperative_orders if order.expiration_time > current_time]

    def request_data(self, request: Request, time_epoch: int):
        """
        Retrieves the requested data from the cache, if available. Otherwise, retrieves it from the provider.

        Parameters:
        -----------
        request : Request
            The request to be processed.
        time_epoch : int
            The current epoch time.

        Returns:
        --------
        Request
            The processed request, containing the retrieved resource and the network latency.
        """
        self.total_requests += 1
        request.network_latency += network_latency.random_wireless()
        request.resource = self.get_from_cache_node(self.edge_node, request.provider.id, time_epoch)
        # 1. check if req exists in local cache
        if self._is_resource(request.resource):
            return request
        # 2. check if request is mapped in a valid caching order
        for order in self.cooperative_orders:
            if self._match(order, request.provider.id):
                request.resource = self.get_from_cache_node(order.cooperator_edge_node, request.provider.id, time_epoch)
                request.network_latency += network_latency.random_ethernet()
                if self._is_resource(request.resource):
                    return request

        # 3. check if request is cache in N neighbor nodes
        request.resource = self._check_neighbor_nodes(request, time_epoch)
        if self._is_resource(request.resource):
            self.neighbor_resources += 1
            return request

        # 4. finally, if the cache is not found, grab from the provider
        response = self.perform_request(request, time_epoch)
        if self.classical_caching:
            self._store_data(response.resource, time_epoch)
        return response

    def _is_resource(self, resource):
        """
        Checks if the given resource is not None and increments the number of cached requests if it is not.

        Parameters:
        -----------
        resource : any
            The resource to be checked.

        Returns:
        --------
        bool
            True if the resource is not None, False otherwise.
        """
        if resource != None:
            self.cached_requests += 1
            return True
        return False

    def _check_neighbor_nodes(self, request, time_epoch):
        """
        Searches for the requested data in the cache of neighboring CacheWorkers.

        Parameters:
        -----------
        request : Request
            The request for the data.
        time_epoch : int
            The current time in epoch format.

        Returns:
        --------
        The requested data, if found in any of the neighboring CacheWorkers' caches. Returns None otherwise.
        """
        for cache_node in self.cache_nodes:
            # print(f"neighbor #{cache_node.id} of {self.edge_node.id} cached resources: {len(cache_node.cache.resources)}")
            data = self.get_from_cache_node(cache_node, request.provider.id, time_epoch)
            request.network_latency += network_latency.random_ethernet()
            if data is not None:
                return data
        return

    # why pass the whole resource object + time?
    def _store_data(self, resource: Resource, current_time: int):
        """
        Stores a resource in the cache.

        Parameters:
        -----------
        resource : Resource
            The resource to store.
        current_time : int
            The current time in epoch format.
        """
        self.edge_node.cache.add_resource(resource, current_time)

    def _match(self, order: CachingOrder, provider_id: str):
        """    
        Parameters:
        -----------
        order : CachingOrder
            The CachingOrder to be checked for a match with the provider ID.
        provider_id : str
            The provider ID to be matched with the CachingOrder.

        Returns:
        --------
        bool
            True if the provider ID of the CachingOrder matches the given provider ID, False otherwise.
        """
        return order.provider.id == provider_id

    def get_from_cache_node(self, node: EdgeNode, provider_id: str, time_epoch: int):
        """
        Retrieves the resource associated with the specified provider ID and time epoch from the cache of the given EdgeNode.

        Parameters:
        -----------
        node : EdgeNode
            The EdgeNode whose cache will be searched for the specified resource.
        provider_id : str
            The ID of the provider whose resource is being searched for.
        time_epoch : int
            The time epoch of the resource being searched for.

        Returns:
        --------
        Resource or None
            Returns the resource associated with the specified provider ID and time epoch if found in the cache, 
            otherwise returns None.
        """
        return node.cache.get_resource(provider_id, time_epoch)

    def perform_request(self, request: Request, current_time):
        """
        Simulates sending a request to the provider and returning the corresponding response as a Request object.

        Args:
            request (Request): the Request object to be sent.
            current_time (int): the current time in epoch format.

        Returns:
            Request: the updated Request object containing the response data.
        """
        (application_latency, size) = request.provider.get_latency_and_bytes()
        request.network_latency += network_latency.random_cloud(request.provider.network_trace)
        resource_creation_time = current_time - (request.network_latency/2)
        request.resource = Resource(request.provider.id, size, current_time,
                                    DEFAULT_EXPIRATION_TIME, resource_creation_time)
        request.application_latency += application_latency
        return request

    def _store_pending_order(self, order: CachingOrder, current_time: int):
        """
        Performs a Caching Order.It Simulates sending a request to the provider and stores in cache the corresponding response as a Request object.

        Parameters:
        -----------
            order (CachingOrder): the CachingOrder object to be stored.
            current_time (int): the current time in epoch format.

        Returns:
            None.
        """
        (application_latency, size) = order.provider.get_latency_and_bytes()
        cloud_latency = network_latency.random_cloud(order.provider.network_trace)
        resource_creation_time = (current_time) - (cloud_latency/2)
        new_resource = Resource(order.provider.id, size, order.execution_time,
                                order.expiration_time, resource_creation_time)
        self._store_data(new_resource, order.execution_time)

    def epoch_passed(self, current_time: int):
        """
        Checks for pending caching orders that are ready to be executed, and remove expired cooperative orders.

        Parameters:
        -----------
            current_time (int): the current time epoch.

        Returns:
        --------
            None
        """
        self.remove_expired_cooperative_orders(current_time)

        orders_to_be_removed = []
        for pending_resource in self.pending_orders:
            if pending_resource.execution_time >= current_time:
                break

            self._store_pending_order(pending_resource, current_time)
            orders_to_be_removed.append(pending_resource)
        for order in orders_to_be_removed:
            self.pending_orders.remove(order)

    def get_cache_hit_rate(self) -> float:
        if self.total_requests == 0:
            return 1.0
        return self.cached_requests / self.total_requests
