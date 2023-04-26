
from typing import List

import numpy as np
from models.cache_worker import CacheWorker
from models.caching_order import CachingOrder
from models.user import User
from parameters import DEFAULT_AVG_PRE_REQUEST_TIME, DEFAULT_STD_PRE_REQUEST_TIME, HIT_RATE, DEFAULT_EXPIRATION_TIME
import random


class CacheManager:
    def __init__(self, hit_rate=HIT_RATE):
        self.hit_rate = hit_rate
        return

    def epoch_passed(self, current_time):
        if current_time % self.time_window_size != 0:
            return
        return self.generate_caching_orders()

    def generate_caching_orders(self, users: List[User], cache_workers: List[CacheWorker]):
        # 1. get all users order and separate orders per edge_node
        requests_per_cache_worker = [[] for cache_worker in cache_workers]
        for user in users:
            for request in user.requests:
                closest_cache_worker = user.closest_cache_worker_by_index(
                    cache_workers, request.execution_time)
                requests_per_cache_worker[closest_cache_worker].append(request)

        for i in range(len(requests_per_cache_worker)):
            requests_per_cache_worker[i] = sorted(
                requests_per_cache_worker[i], key=lambda x: x.execution_time)

        # 2. according to a target_hit_rate, define the subset of resources to cache
        caching_orders_per_cache_worker: List[List[CachingOrder]] = [[]
                                                                     for cache_worker in cache_workers]
        for index, requests in enumerate(requests_per_cache_worker):
            for request in requests:
                random_number = random.random()
                if random_number <= self.hit_rate:
                    random_pre_fetch_time = random.gauss(
                        DEFAULT_AVG_PRE_REQUEST_TIME, DEFAULT_STD_PRE_REQUEST_TIME)
                    execution_time = 0 if request.execution_time - \
                        random_pre_fetch_time < 0 else request.execution_time - random_pre_fetch_time
                    new_caching_order = CachingOrder(
                        cache_workers[index].id, execution_time, request.execution_time + DEFAULT_EXPIRATION_TIME, request.provider)
                    if not self.check_redundant_cache_order(new_caching_order, caching_orders_per_cache_worker[index]):
                        caching_orders_per_cache_worker[index].append(
                            new_caching_order)
            caching_orders_per_cache_worker[index] = sorted(
                caching_orders_per_cache_worker[index], key=lambda x: x.execution_time)

        # TODO: for cooperative: check all cache workers and detect when there is significant overlap, then swap standard for coop
        return caching_orders_per_cache_worker

    def check_redundant_cache_order(self, new_cache_order: CachingOrder, caching_orders: List[CachingOrder]):
        for caching_order in caching_orders:
            if new_cache_order.provider.id == caching_order.provider.id and new_cache_order.execution_time >= caching_order.execution_time and new_cache_order.execution_time <= caching_order.expiration_time:
                return True
        return False
