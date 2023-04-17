import time
from typing import List

from models.resource import Resource
from models.request import Request
from models.order_type import OrderType
from edge_node import EdgeNode
from models.caching_order import CachingOrder
from models.bytes_and_time import bytes_and_time
from parameters import DEFAULT_EXPIRATION_TIME
from shared.helper import calculate_distance


class CacheWorker:
    def __init__(self, edge_node: EdgeNode, cache_nodes: List[EdgeNode], neighbor_edge_nodes=0, classical_caching=False):
        self.cooperative_orders: List[CachingOrder] = []
        self.edge_node = edge_node
        self.cache_nodes = self.get_ordered_cache_nodes_by_distance(
            edge_node, cache_nodes, neighbor_edge_nodes)
        self.total_requests = 0
        self.cached_requests = 0
        self.classical_caching = classical_caching

    def get_ordered_cache_nodes_by_distance(edge_node: EdgeNode, cache_nodes: List[EdgeNode], neighbor_edge_nodes: int) -> List[EdgeNode]:
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
            distance = calculate_distance(
                edge_node.get_position(), cache_node.get_position())
            distances[cache_node] = distance

        # Sort the cache_nodes by distance in ascending order
        ordered_cache_nodes = sorted(
            distances.keys(), key=lambda x: distances[x])
        limit_index = neighbor_edge_nodes - 1
        return ordered_cache_nodes[:limit_index]

    def add_caching_orders(self, orders: List[CachingOrder]):
        for order in orders:
            if order.type == OrderType.STANDARD:
                print('get data from provider at order time')
            else:
                self.cooperative_orders.append(order)

    def remove_expired_cooperative_orders(self):
        current_time = self.get_current_time()
        self.cooperative_orders = [
            order for order in self.cooperative_orders if order.expiration_time <= current_time]

    def request_data(self, request: Request):
        self.total_requests += 1
        request.resource = self.get_from_cache_node(self.edge_node, request.id)
        # 1. check if req exists in local cache
        if self._is_resource(request.resource):
            return request
        # 2. check if request is mapped in a valid caching order
        for order in self.cooperative_orders:
            if self._match(order, request.id):
                request.resource = self.get_from_cache_node(
                    order.cooperator_edge_node, request)
                if self._is_resource(request.resource):
                    return request

        # 3. check if request is cache in N neighbor nodes
        request.resource = self._check_neighbor_nodes(request)
        if self._is_resource(request.resource):
            return request

        # 4. finally, if the cache is not found, grab from the provider
        resource = self.perform_request(request)
        if self.classical_caching:
            self._store_data(resource)
        return resource

    def _is_resource(self, resource):
        if resource != None:
            self.cached_requests += 1
            return True
        return False

    def _check_neighbor_nodes(self, request):
        for cache_node in self.cache_nodes:
            data = self.get_from_cache_node(cache_node, request)
            if data is not None:
                return data
        return

    def _store_data(self, resource: Resource):
        self.edge_node.cache.add_resource(
            resource.id, resource.size, resource.expiration_time)

    def get_current_time(self):
        # Get current time
        pass

    def _match(self, order: CachingOrder, request_id: str):
        # Check if order matches request request
        return order.request_id == request_id

    def get_from_cache_node(self, node: EdgeNode, request: str):
        return node.cache.get_resource(request)

    def perform_request(self, request: Request):
        (size, latency) = bytes_and_time.get_time_and_bytes(request.provider)
        request.resource = Resource(request.id, size, time.time(), DEFAULT_EXPIRATION_TIME)
        request.latency += latency
        return request
