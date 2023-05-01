import numpy as np
from models.cache_manager import CacheManager
from models.cache_worker import CacheWorker
from models.provider import Provider
from shared.helper import generate_edge_node_position, pass_time
from models.edge_node import EdgeNode
from models.request_generator import RequestGenerator
from models.user import User

from parameters import AREA_DIMENSIONS, EDGE_NODE_MIN_DISTANCE, EXPERIMENT_DURATION, EXPERIMENT_TYPE, NUMBER_OF_EDGE_NODES, NUMBER_OF_PROVIDERS, NUMBER_OF_USERS

# 1. Initialize users
users = [User(i) for i in range(NUMBER_OF_USERS)]

# 2. Create providers
providers = [Provider(i) for i in range(NUMBER_OF_PROVIDERS)]


# 3. Assign requests to providers to each users (according to user category) for the experiment duration
request_generator = RequestGenerator(users, providers)
users = request_generator.users
for user in users:
    print(f"user #{user.id} will make {len(user.requests)}")
# 4. Initialize Edge Nodes
edge_nodes = [EdgeNode(i) for i in range(NUMBER_OF_EDGE_NODES)]
for index, edge_node in enumerate(edge_nodes):
    edge_position = generate_edge_node_position(
        AREA_DIMENSIONS, EDGE_NODE_MIN_DISTANCE, edge_nodes[:index])
    edge_node.set_position(edge_position[0], edge_position[1])

# 5. Initialize Cache Workers
if EXPERIMENT_TYPE != "baseline":
    cache_workers = [CacheWorker(i, edge_node, edge_nodes)
                     for i, edge_node in enumerate(edge_nodes)]

    cache_manager = CacheManager()
    caching_orders = cache_manager.generate_caching_orders(
        users, cache_workers)
    for index, cache_worker_orders in enumerate(caching_orders):
        cache_workers[index].add_caching_orders(cache_worker_orders)


# Start experiment
for time_epoch in range(EXPERIMENT_DURATION):
    # every time epoch loop all users
    for user in users:
        # check if there is a request in the given time_epoch
        if user.check_request(time_epoch):
            # perform the time epoch operations in the other classes
            pass_time(time_epoch, users, cache_workers, edge_nodes)
            # get the request and the closest edge node
            request = user.get_request()
            closest_cache_worker = user.closest_cache_worker(
                cache_workers, time_epoch)
            closest_cache_worker.request_data(request, time_epoch)

    if time_epoch % 60000 == 0:
        print(f'{time_epoch//1000}s passed from {EXPERIMENT_DURATION//1000}')

acc = 0
for cache_worker in cache_workers:
    acc += cache_worker.total_requests
    print(f"Cache Worker #{cache_worker.id} received {cache_worker.total_requests} requests and its hit rate was {cache_worker.get_cache_hit_rate()}" )
print(f"total requests: {acc}")