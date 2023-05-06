import datetime
import sys
import numpy as np
from models.cache_manager import CacheManager
from models.cache_worker import CacheWorker
from models.metrics import MetricsCalculator
from models.provider import Provider
from shared.helper import generate_edge_node_position, pass_time
from models.edge_node import EdgeNode
from models.request_generator import RequestGenerator
from models.user import User

from parameters import AREA_DIMENSIONS, EDGE_NODE_MIN_DISTANCE, EXPERIMENT_DURATION, EXPERIMENT_TYPE, NUMBER_OF_EDGE_NODES, NUMBER_OF_PROVIDERS, NUMBER_OF_USERS

# 1. Initialize users
users = [User(i) for i in range(NUMBER_OF_USERS)]
now = datetime.datetime.now()
print(f"{now} - All users created")
# 2. Create providers
providers = [Provider(i) for i in range(NUMBER_OF_PROVIDERS)]
now = datetime.datetime.now()
print(f"{now} - All providers created")

# 3. Assign requests to providers to each users (according to user category) for the experiment duration
request_generator = RequestGenerator(users, providers)
users = request_generator.users
for user in users:
    print(f"user #{user.id} will make {len(user.requests)}")
now = datetime.datetime.now()
print(f"{now} - All requests assigned")

# 4. Initialize Edge Nodes
edge_nodes = [EdgeNode(i) for i in range(NUMBER_OF_EDGE_NODES)]
for index, edge_node in enumerate(edge_nodes):
    edge_position = generate_edge_node_position(AREA_DIMENSIONS, EDGE_NODE_MIN_DISTANCE, edge_nodes[:index])
    edge_node.set_position(edge_position[0], edge_position[1])
now = datetime.datetime.now()
print(f"{now} - All edge nodes created")

# 5. Initialize Cache Workers
if EXPERIMENT_TYPE != "baseline":
    cache_workers = [CacheWorker(i, edge_node, edge_nodes) for i, edge_node in enumerate(edge_nodes)]
    now = datetime.datetime.now()
    print(f"{now} - All cache workers created")

    cache_manager = CacheManager()
    caching_orders = cache_manager.generate_caching_orders(users, cache_workers)
    now = datetime.datetime.now()
    print(f"{now} - Caching orders created")
    for index, cache_worker_orders in enumerate(caching_orders):
        cache_workers[index].add_caching_orders(cache_worker_orders)

metrics_calculator = MetricsCalculator()
# Start experiment TODO: make a queue of requests and only look those. No need to loop all user in all time epochs
for time_epoch in range(EXPERIMENT_DURATION):
    # every time epoch loop all users
    for user in users:
        # check if there is a request in the given time_epoch
        if user.check_request(time_epoch):
            # perform the time epoch operations in the other classes
            pass_time(time_epoch, user, cache_workers, edge_nodes)
            # get the request and the closest edge node
            request = user.get_request()
            closest_cache_worker = user.closest_cache_worker(cache_workers)
            response = closest_cache_worker.request_data(request, time_epoch)
            metrics_calculator.add_request(response, time_epoch)
    if time_epoch % 60000 == 0:
        print(f'{time_epoch//1000}s passed from {EXPERIMENT_DURATION//1000}')

metrics_calculator.calculate_metrics(cache_workers, providers)
