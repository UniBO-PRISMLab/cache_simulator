import numpy as np
import random

good_seeds = [ 62505, 1037184, 222556, 175639 , 247986, 306166, 342810, 438166, 478767, 536727, 596506, 644578, 676658, 686266, 757626, 767979, 793834, 811813, 855207, 890460, 890939, 931361, 953584, 975241, 1001473, 1009105, 1053646, 1069554, 1095984, 1103844]
class RandomGenerator:
    def __init__(self, replication = 0):
        self.seed = good_seeds[replication]
        np.random.seed(seed=self.seed)
        # read lines
        random.seed(self.seed)
        self.random: random = random
        self.np_random: random = np.random


random_generator = RandomGenerator()
regular_random = random_generator.random
np_random = random_generator.np_random
#from shared.RandomGenerator import regular_random
