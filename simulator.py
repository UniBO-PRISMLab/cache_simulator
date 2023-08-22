import datetime
from models.cache_manager import CacheManager
from models.cache_worker import CacheWorker
from models.enums.user_category import UserCategory
from models.metrics import MetricsCalculator
from models.provider import Provider
from models.simulation_queue import SIMULATION_QUEUE
from shared.helper import generate_edge_node_position, pass_time, write_objects_to_csv
from models.edge_node import EdgeNode
from models.request_generator import RequestGenerator
from models.user import User


from parameters import AREA_DIMENSIONS, CACHE_NOT_FOUND_RESOURCE, EDGE_NODE_MIN_DISTANCE, ACCURACY, GENERATE_TRACE, MODE, NEIGHBOR_EDGE_NODES, NUMBER_OF_EDGE_NODES, NUMBER_OF_PROVIDERS, NUMBER_OF_USERS, REPLICATIONS, USER_CATEGORY_DISTRIBUTION, WRITE_IN_FILE


print(f"starting experiment with {ACCURACY} accuracy")
print(
    f"Cache resources not found is {CACHE_NOT_FOUND_RESOURCE} and neighbor nodes are {NEIGHBOR_EDGE_NODES}. Mode is {MODE.value}")
print(
    f"user distributions: id - {USER_CATEGORY_DISTRIBUTION[UserCategory.ID]}, location  - {USER_CATEGORY_DISTRIBUTION[UserCategory.LOCATION]}, type - {USER_CATEGORY_DISTRIBUTION[UserCategory.TYPE]}")
if WRITE_IN_FILE:
    print("*** WILL WRITE RESULTS INTO FILES ***")
metrics_calculator = MetricsCalculator()

for i in range(REPLICATIONS):
    # 0. reset everything before the simulation
    metrics_calculator.reset()
    SIMULATION_QUEUE.reset()
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
    cache_workers = [CacheWorker(i, edge_node, edge_nodes) for i, edge_node in enumerate(edge_nodes)]
    now = datetime.datetime.now()
    print(f"{now} - All cache workers created")

    cache_manager = CacheManager()
    caching_orders = cache_manager.generate_caching_orders(users, cache_workers)
    now = datetime.datetime.now()
    print(f"{now} - Caching orders created")
    for index, cache_worker_orders in enumerate(caching_orders):
        cache_workers[index].add_caching_orders(cache_worker_orders)

    SIMULATION_QUEUE.sort_queue()
    now = datetime.datetime.now()
    print(f"{now} - Simulation Queue sorted")
    total_number_of_requests = len(SIMULATION_QUEUE.queue)
    for i, queue_element in enumerate(SIMULATION_QUEUE.queue):
        pass_time(queue_element.time_epoch, queue_element.user, cache_workers, edge_nodes)
        response = queue_element.cache_worker.request_data(queue_element.request, queue_element.time_epoch)
        metrics_calculator.add_request(response, queue_element.time_epoch)
        if i % 10000 == 0:
            print(f'{i} requests made from {total_number_of_requests}')

    metrics_calculator.calculate_metrics(cache_workers, providers)
