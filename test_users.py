import unittest
from models.edge_node import EdgeNode

from models.user import User
from shared.helper import distance, generate_edge_node_position

edge_nodes = [EdgeNode(i) for i in range(5)]


class TestUserMobility(unittest.TestCase):

    def test_starting_point(self):
        user = User(id=0, area_dimension=100)

    def test_closest_edge_node(self):
        area_dimension = 100
        edge_nodes = [EdgeNode(i) for i in range(2)]
        for index, edge_node in enumerate(edge_nodes):
            edge_position = generate_edge_node_position(
                area_dimension, 5, edge_nodes[:index])
            edge_node.set_position(edge_position[0], edge_position[1])
            print(edge_node)
        user = User(id=0, area_dimension=area_dimension)
        closest_edge = None

        for i in range(600):
            user.move()
            if closest_edge != user.get_closest_edge_node(edge_nodes):
                closest_edge = user.get_closest_edge_node(edge_nodes)
                print(f"edge: {closest_edge} - user: {user.get_position()}")
                for edge in edge_nodes:
                    print(
                        f"edge: {edge} - distance: {distance(edge.get_position(), user.get_position())}")
                print("\n")


if __name__ == '__main__':
    unittest.main()
