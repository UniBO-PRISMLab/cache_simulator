import random
from models.cache_worker import CacheWorker
from shared.helper import generate_edge_node_position
from models.edge_node import EdgeNode
from models.request_generator import RequestGenerator
from models.user import User

from parameters import AREA_DIMENSIONS, EDGE_NODE_MIN_DISTANCE, EXPERIMENT_DURATION, EXPERIMENT_TYPE, NUMBER_OF_EDGE_NODES, NUMBER_OF_USERS


# 1. Initialize users
users = [User(i) for i in range(NUMBER_OF_USERS)]
# 2. Assign requests to users for the experiment duration
request_generator = RequestGenerator(users)
users = request_generator.users
# 3. Initialize Edge Nodes
edge_nodes = [EdgeNode(i) for i in range(NUMBER_OF_EDGE_NODES)]
for index, edge_node in enumerate(edge_nodes):
    edge_position = generate_edge_node_position(
        AREA_DIMENSIONS, EDGE_NODE_MIN_DISTANCE, edge_nodes[:index])
    edge_node.set_position(edge_position[0], edge_position[1])


# 4. Initialize Cache Workers
if EXPERIMENT_TYPE != "baseline":
    cache_workers = [CacheWorker(edge_node, edge_nodes)
                     for edge_node in edge_nodes]


for time_epoch in range(EXPERIMENT_DURATION):
    # every time epoch loop all users
    for user in users:
        # check if there is a request in the given time_epoch
        if user.check_request(time_epoch):
            # if yes, get the request and the closest edge node
            request = user.get_request()
            closest_cache_worker = user.closest_cache_worker(
                edge_nodes, time_epoch)
            closest_cache_worker.request_data(request, time_epoch)
    
    if time_epoch % 1000 == 0:
        print(f'{time_epoch/1000}s epoch passed from {EXPERIMENT_DURATION/1000}')
