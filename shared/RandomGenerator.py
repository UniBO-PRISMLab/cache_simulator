import numpy as np
import random


class RandomGenerator:
    def __init__(self, seed=42):
        self.seed = seed
        np.random.seed(seed=seed)
        # read lines
        random.seed(seed)
        self.random: random = random
        self.np_random: random = np.random


random_generator = RandomGenerator()
regular_random = random_generator.random
np_random = random_generator.np_random
#from shared.RandomGenerator import regular_random
