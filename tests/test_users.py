import unittest
from models.cache_worker import CacheWorker
from models.edge_node import EdgeNode

from models.user import User
from parameters import AREA_DIMENSIONS, EDGE_NODE_MIN_DISTANCE
from shared.helper import distance, generate_edge_node_position

edge_nodes = [EdgeNode(i) for i in range(5)]


class TestUserMobility(unittest.TestCase):

    def test_get_user_position_in_time(self):
        error_tolerance = 1E-16
        user = User(id=0)
        test_experiment_time = 360000
        predicted_movement = []
        actual_movement = []
        for time in range(test_experiment_time):
            predicted_movement.append(user.get_position_at_time(time+1))
        for time in range(test_experiment_time):
            user.epoch_passed(time+1)
            actual_movement.append(user.get_position())

        self.assertEqual(len(actual_movement), len(predicted_movement))

        for i in range(len(actual_movement)):
            #print(f"actual: {actual_movement[i]} - predicted: {predicted_movement[i]}")
            squared_error = ((actual_movement[i][0] - predicted_movement[i][0]) ** 2,
                             ((actual_movement[i][1] - predicted_movement[i][1]) ** 2))

            self.assertGreater(error_tolerance, squared_error[0])
            self.assertGreater(error_tolerance, squared_error[1])

    def test_user_predicted_and_real_edge(self):
        edge_nodes = [EdgeNode(i) for i in range(10)]
        for index, edge_node in enumerate(edge_nodes):
            edge_position = generate_edge_node_position(AREA_DIMENSIONS, EDGE_NODE_MIN_DISTANCE, edge_nodes[:index])
            edge_node.set_position(edge_position[0], edge_position[1])
        cache_workers = [CacheWorker(i, edge_nodes[i], edge_nodes) for i in range(10)]
        user = User(id=0)
        test_experiment_time = 100000
        predicted_cache_worker = []
        actual_cache_worker = []
        for time in range(test_experiment_time):
            predicted = user.closest_cache_worker_by_index_in_time(cache_workers, time + 1)
            predicted_cache_worker.append(predicted)
        for time in range(test_experiment_time):
            user.epoch_passed(time + 1)
            actual = user.closest_cache_worker_by_id(cache_workers)
            actual_cache_worker.append(actual)

        self.assertEqual(len(actual_cache_worker), len(predicted_cache_worker))
        for i in range(len(actual_cache_worker)):
            self.assertEqual(actual_cache_worker[i], predicted_cache_worker[i])



if __name__ == '__main__':
    unittest.main()
