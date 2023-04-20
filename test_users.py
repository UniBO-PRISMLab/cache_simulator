import unittest

from models.user import User


class TestUserMobility(unittest.TestCase):

    def test_starting_point(self):
        users = [User(id=i, area_dimension=100, grid_size=10)
                 for i in range(10)]

        for user in users:
            print(f"{user.start_position} -> {user.end_position}")
            user.plot_trajectory()

if __name__ == '__main__':
    unittest.main()
