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
    def __init__(self, edge_node: EdgeNode, cache_nodes: List[EdgeNode], neighbor_edge_nodes=NEIGHBOR_EDGE_NODES, classical_caching=CACHE_NOT_FOUND_RESOURCE):
        self.cooperative_orders: List[CachingOrder] = []
        self.edge_node = edge_node
        self.cache_nodes = self.get_ordered_cache_nodes_by_distance(
            edge_node, cache_nodes, neighbor_edge_nodes)
        self.total_requests = 0
        self.cached_requests = 0
        self.classical_caching = classical_caching

    def get_ordered_cache_nodes_by_distance(self, edge_node: EdgeNode, cache_nodes: List[EdgeNode], neighbor_edge_nodes: int) -> List[EdgeNode]:
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

    def remove_expired_cooperative_orders(self, current_time):
        self.cooperative_orders = [
            order for order in self.cooperative_orders if order.expiration_time <= current_time]

    def request_data(self, request: Request, time_epoch: int):
        self.total_requests += 1
        request.network_latency += network_latency.random_wireless()
        request.resource = self.get_from_cache_node(
            self.edge_node, request.provider.id, time_epoch)
        # 1. check if req exists in local cache
        if self._is_resource(request.resource):
            return request
        # 2. check if request is mapped in a valid caching order
        for order in self.cooperative_orders:
            if self._match(order, request.provider.id):
                request.resource = self.get_from_cache_node(
                    order.cooperator_edge_node, request, time_epoch)
                request.network_latency += network_latency.random_ethernet()
                if self._is_resource(request.resource):
                    return request

        # 3. check if request is cache in N neighbor nodes
        request.resource = self._check_neighbor_nodes(request)
        if self._is_resource(request.resource):
            return request

        # 4. finally, if the cache is not found, grab from the provider
        response = self.perform_request(request, time_epoch)
        if self.classical_caching:
            self._store_data(response.resource)
        return response

    def _is_resource(self, resource):
        if resource != None:
            self.cached_requests += 1
            return True
        return False

    def _check_neighbor_nodes(self, request):
        for cache_node in self.cache_nodes:
            data = self.get_from_cache_node(cache_node, request)
            request.network_latency += network_latency.random_ethernet()
            if data is not None:
                return data
        return

    # why pass the whole resource object + time?
    def _store_data(self, resource: Resource, current_time: int):
        self.edge_node.cache.add_resource(resource, current_time)

    def _match(self, order: CachingOrder, provider_id: str):
        # Check if order matches request request
        return order.provider_id == provider_id

    def get_from_cache_node(self, node: EdgeNode, provider_id: str, time_epoch: int):
        return node.cache.get_resource(provider_id, time_epoch)

    def perform_request(self, request: Request, current_time):
        (size, application_latency) = request.provider.get_latency_and_bytes()
        request.resource = Resource(
            request.provider.id, size, current_time, DEFAULT_EXPIRATION_TIME)
        request.network_latency += network_latency.random_cloud()
        request.application_latency += application_latency
        return request

    def epoch_passed(self, current_time: int):
        # TODO: improve this
        self.remove_expired_cooperative_orders(current_time)
        self.edge_node.cache.epoch_passed()

    def get_cache_hit_rate(self) -> float:
        if self.total_requests == 0:
            return 1.0
        return self.cached_requests / self.total_requests
