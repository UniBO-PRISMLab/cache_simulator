
from typing import List

from models.cache_worker import CacheWorker
from models.caching_order import CachingOrder
from models.queue_element import QueueElement
from models.request import Request
from models.simulation_queue import SIMULATION_QUEUE
from models.user import User
from parameters import DEFAULT_AVG_PRE_REQUEST_TIME, DEFAULT_STD_PRE_REQUEST_TIME, HIT_RATE, DEFAULT_EXPIRATION_TIME
from shared.RandomGenerator import regular_random



class CacheManager:
    def __init__(self, hit_rate=HIT_RATE, average_pre_request_time=DEFAULT_AVG_PRE_REQUEST_TIME,
                 std_pre_request_time=DEFAULT_STD_PRE_REQUEST_TIME, default_expiration_time=DEFAULT_EXPIRATION_TIME):
        self.hit_rate = hit_rate
        self.average_pre_request_time = average_pre_request_time
        self.std_pre_request_time = std_pre_request_time
        self.default_expiration_time = default_expiration_time
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
                    print(f"add element at {request.execution_time} to the queue. Now it has {len(SIMULATION_QUEUE.queue)} requests")
                    random_number = regular_random.random()
                    if random_number <= self.hit_rate:
                        requests_per_cache_worker[closest_cache_worker].append(request)

        for i in range(len(requests_per_cache_worker)):
            requests_per_cache_worker[i] = sorted(requests_per_cache_worker[i], key=lambda x: x.execution_time)

        # 2. according to a target_hit_rate, define the subset of resources to cache
        caching_orders_per_cache_worker: List[List[CachingOrder]] = [[] for cache_worker in cache_workers]
        for index, requests in enumerate(requests_per_cache_worker):
            for request in requests:
                random_pre_fetch_time = self.get_pre_fetch_time()
                execution_time = 0 if request.execution_time - random_pre_fetch_time < 0 else request.execution_time - random_pre_fetch_time
                expiration_time = random_pre_fetch_time + request.execution_time + self.default_expiration_time
                #print(f"request: {request.execution_time} - order: {execution_time} to {expiration_time}")

                new_caching_order = CachingOrder(
                    cache_worker_id=cache_workers[index].id, execution_time=execution_time,
                    expiration_time=expiration_time, provider=request.provider)

                if not self.check_redundant_cache_order(request, caching_orders_per_cache_worker[index]):
                    caching_orders_per_cache_worker[index].append(new_caching_order)

            caching_orders_per_cache_worker[index] = sorted(
                caching_orders_per_cache_worker[index],
                key=lambda x: x.execution_time)

        # TODO: for cooperative: check all cache workers and detect when there is significant overlap, then swap standard for coop
        return caching_orders_per_cache_worker

    def get_pre_fetch_time(self):
        random_pre_fetch_time = regular_random.gauss(
            self.average_pre_request_time, self.std_pre_request_time)
        return int(random_pre_fetch_time) if int(random_pre_fetch_time) > 0 else 1

    def check_redundant_cache_order(self, request: Request, caching_orders: List[CachingOrder]):
        # TODO: just check the ones that make sense looking at the execution time (that should be ordered)
        for caching_order in caching_orders:
            if request.provider.id == caching_order.provider.id and request.execution_time > caching_order.execution_time and request.execution_time < caching_order.expiration_time:
                return True
        return False
