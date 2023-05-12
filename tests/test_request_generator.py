import unittest

from models.enums.user_category import UserCategory

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

    def test_users_popularity_distribution(self):
        user_category_distribution = {
            UserCategory.ID:1,
            UserCategory.TYPE: 0,
            UserCategory.LOCATION: 0,
        }
        users = [User(category_distribution=user_category_distribution) for i in range(2)]
        providers = [Provider(i) for i in range(1000)]
        request_generator = RequestGenerator(users, providers, 10, 100000)
        users = request_generator.users
        for user in users:
            for request in user.requests:
                print(request)
        
        
        pass 

if __name__ == '__main__':
    unittest.main()
