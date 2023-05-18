
from typing import List

from models.cache_worker import CacheWorker
from models.caching_order import CachingOrder
from models.enums.cache_manager_node import CacheManagerMode
from models.enums.order_type import OrderType
from models.queue_element import QueueElement
from models.request import Request
from models.simulation_queue import SIMULATION_QUEUE
from models.user import User
from parameters import DEFAULT_AVG_PRE_REQUEST_TIME, DEFAULT_STD_PRE_REQUEST_TIME, ACCURACY, DEFAULT_EXPIRATION_TIME, MODE
from shared.RandomGenerator import regular_random


class CacheManager:
    def __init__(
            self, accuracy=ACCURACY, average_pre_request_time=DEFAULT_AVG_PRE_REQUEST_TIME,
            std_pre_request_time=DEFAULT_STD_PRE_REQUEST_TIME, default_expiration_time=DEFAULT_EXPIRATION_TIME,
            mode=MODE):
        self.accuracy = accuracy
        self.average_pre_request_time = average_pre_request_time
        self.std_pre_request_time = std_pre_request_time
        self.default_expiration_time = default_expiration_time
        self.mode = mode
        return

    def epoch_passed(self, current_time):
        if current_time % self.time_window_size != 0:
            return
        return self.generate_caching_orders()

    def generate_caching_orders(self, users: List[User], cache_workers: List[CacheWorker]):
        """
        Generate a List of caching orders according to the accuracy. 
        *** ALSO GENERATES QUEUE ELEMENTS AND ADDS THOSE TO THE SIMULATION QUEUE ***

        Parameters:
        -----------
        users : List[User]
            The users with a list a requests.
        cache_workers : List[CacheWorker]
            A list of cache workers involved in the simulation.
        """
        # 1. get all users order and separate orders per edge_node
        requests_per_cache_worker = [[] for cache_worker in cache_workers]
        for user in users:
            for request in user.requests:
                closest_cache_worker = user.closest_cache_worker_by_index_in_time(cache_workers, request.execution_time)
                queueElement = QueueElement(request, user, request.execution_time, cache_workers[closest_cache_worker])
                SIMULATION_QUEUE.add_element(queueElement)
                random_number = regular_random.random()
                if random_number <= self.accuracy:
                    requests_per_cache_worker[closest_cache_worker].append(request)

        for i in range(len(requests_per_cache_worker)):
            requests_per_cache_worker[i] = sorted(requests_per_cache_worker[i], key=lambda x: x.execution_time)

        # 2. according to a target_accuracy, define the subset of resources to cache
        caching_orders_per_cache_worker: List[List[CachingOrder]] = [[] for cache_worker in cache_workers]
        for index, requests in enumerate(requests_per_cache_worker):
            for request in requests:
                random_pre_fetch_time = self.get_pre_fetch_time()
                execution_time = 0 if request.execution_time - random_pre_fetch_time < 0 else request.execution_time - random_pre_fetch_time
                expiration_time = random_pre_fetch_time + request.execution_time + self.default_expiration_time
                #print(f"request: {request.execution_time} - order: {execution_time} to {expiration_time}")

                new_caching_order = CachingOrder(
                    cache_worker_id=cache_workers[index].id, execution_time=execution_time,
                    expiration_time=expiration_time, provider=request.provider,
                    request_execution_time=request.execution_time)               
                caching_orders_per_cache_worker[index].append(new_caching_order)

            caching_orders_per_cache_worker[index] = sorted(
                caching_orders_per_cache_worker[index],
                key=lambda x: x.execution_time)

        if self.mode == CacheManagerMode.COOPERATIVE:
            for cache_worker_index in range(len(caching_orders_per_cache_worker)):
                for order in caching_orders_per_cache_worker[cache_worker_index]:
                    order = self.check_cooperative_cache_order(
                        order, caching_orders_per_cache_worker, cache_worker_index, cache_workers)

        for index in range(len(caching_orders_per_cache_worker)):
            clean_cache_worker_orders = []
            for order in caching_orders_per_cache_worker[index]:
                if not self.check_redundant_cache_order(order, clean_cache_worker_orders):
                    clean_cache_worker_orders.append(order)
            caching_orders_per_cache_worker[index] = clean_cache_worker_orders

        return caching_orders_per_cache_worker

    def check_cooperative_cache_order(
            self, target_order: CachingOrder, caching_orders_per_cache_worker: List[List[CachingOrder]],
            cache_worker_index: int, cache_workers: List[CacheWorker]):
        """
        Checks if a given caching order can be fulfilled cooperatively by any other cache worker. If so, the order is updated
        to a cooperative order, indicating the cooperating cache worker.

        Parameters:
        -----------
        target_order : CachingOrder
            The caching order to be checked.
        caching_orders_per_cache_worker : List[List[CachingOrder]]
            The list of caching orders of all cache workers. Each list contains the caching orders of a single cache worker.
        cache_worker_index : int
            The index of the cache worker that will try to execute the target_order.
        cache_workers : List[CacheWorker]
            The list of all cache workers.

        Returns:
        --------
        CachingOrder
            modified version of target_order if it can be cooperative, unmodified order otherwise.
        """
        if (target_order.is_cooperator_pointer):
            return target_order
        for i, cache_worker_orders in enumerate(caching_orders_per_cache_worker):
            if i != cache_worker_index:
                for order in cache_worker_orders:
                    if order.execution_time >= target_order.request_execution_time:
                        break
                    if order.provider.id == target_order.provider.id and target_order.request_execution_time > order.execution_time and target_order.request_execution_time < order.expiration_time and order.type == OrderType.STANDARD:
                        target_order.type = OrderType.COOPERATIVE
                        target_order.cooperator_edge_node = cache_workers[i].edge_node
                        target_order.expiration_time = order.expiration_time if target_order.expiration_time > order.expiration_time else target_order.expiration_time
                        order.is_cooperator_pointer = True
                        return target_order
        return target_order

    def get_pre_fetch_time(self):
        random_pre_fetch_time = regular_random.gauss(
            self.average_pre_request_time, self.std_pre_request_time)
        return int(random_pre_fetch_time) if int(random_pre_fetch_time) > 0 else 1

    def check_redundant_cache_order(self, order: CachingOrder, caching_orders: List[CachingOrder]):
        for caching_order in caching_orders:
            if order.provider.id == caching_order.provider.id and order.request_execution_time > caching_order.execution_time and order.request_execution_time < caching_order.expiration_time and not order.is_cooperator_pointer:
                return True
        return False
