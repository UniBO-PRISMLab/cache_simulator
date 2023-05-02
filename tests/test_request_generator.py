import unittest

from ..models.provider import Provider
from ..models.request_generator import RequestGenerator
from ..models.user import User
from ..parameters import NUMBER_OF_PROVIDERS, NUMBER_OF_USERS

users = [User(i) for i in range(NUMBER_OF_USERS)]

# 2. Create providers
providers = [Provider(i) for i in range(NUMBER_OF_PROVIDERS)]
request_generator = RequestGenerator(users=users, providers=providers)


class TestSquareArea(unittest.TestCase):

    def test_divide_area(self):
        area_size = 10
        portions = 4

        subareas = request_generator.divide_square_area(area_size, portions)

        self.assertEqual(len(subareas), 4)
        self.assertEqual(subareas[0].id, 0)
        self.assertEqual(subareas[0].x1, 0)
        self.assertEqual(subareas[0].y1, 0)
        self.assertGreater(subareas[0].x2, 0)
        self.assertGreater(subareas[0].y2, 0)

    def test_get_area_for_point(self):
        area_size = 10
        portions = 4
        subareas = request_generator.divide_square_area(area_size, portions)

        area = request_generator.find_subarea((1, 2), subareas)
        self.assertEqual(area.id, 0)

        area = request_generator.find_subarea((7, 2), subareas)
        self.assertEqual(area.id, 1)

        area = request_generator.find_subarea((3, 9), subareas)
        self.assertEqual(area.id, 2)

        area = request_generator.find_subarea((8, 9), subareas)
        self.assertEqual(area.id, 3)


if __name__ == '__main__':
    unittest.main()
