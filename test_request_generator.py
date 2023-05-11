# 1. Initialize users
from models.cache_manager import CacheManager
from models.cache_worker import CacheWorker
from models.edge_node import EdgeNode
from models.enums.user_category import UserCategory
from models.provider import Provider
from models.request_generator import RequestGenerator
from models.simulation_queue import SIMULATION_QUEUE
from models.user import User
from parameters import NUMBER_OF_PROVIDERS, NUMBER_OF_USERS
from shared.helper import generate_edge_node_position, pass_time


def test_users_popularity_distribution():
    user_category_distribution = {
        UserCategory.ID: 0,
        UserCategory.TYPE: 0,
        UserCategory.LOCATION: 1,
    }
    users = [User(id=i, category_distribution=user_category_distribution) for i in range(120)]
    providers = [Provider(i) for i in range(100)]
    request_generator = RequestGenerator(users=users, providers=providers,
                                         popularity_distribution=10, experiment_duration=20000)
    users = request_generator.users
    users = request_generator.users
    for user in users:
        print(f"user #{user.id} will make {len(user.requests)}")

    # 4. Initialize Edge Nodes
    edge_nodes = [EdgeNode(i) for i in range(10)]
    for index, edge_node in enumerate(edge_nodes):
        edge_position = generate_edge_node_position(10000, 100, edge_nodes[:index])
        edge_node.set_position(edge_position[0], edge_position[1])

    # 5. Initialize Cache Workers
    cache_workers = [CacheWorker(i, edge_node, edge_nodes) for i, edge_node in enumerate(edge_nodes)]

    cache_manager = CacheManager()
    caching_orders = cache_manager.generate_caching_orders(users, cache_workers)
    for index, cache_worker_orders in enumerate(caching_orders):
        cache_workers[index].add_caching_orders(cache_worker_orders)
    SIMULATION_QUEUE.sort_queue()
    for i, queue_element in enumerate(SIMULATION_QUEUE.queue):
        pass_time(queue_element.time_epoch, queue_element.user, cache_workers, edge_nodes)
        pos = queue_element.user.get_position_at_time(queue_element.time_epoch)
        area = request_generator.find_subarea(pos, request_generator.popularity[UserCategory.LOCATION.value])
        print(f"subarea: {area}")
        print(queue_element.request)
        print()


test_users_popularity_distribution()
