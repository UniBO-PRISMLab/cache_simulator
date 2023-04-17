import random
import numpy as np
import pandas as pd

PATH_NETWORK = './data/network_traces'


class NetworkLatency:
    def __init__(self, seed=42):
        self.seed = seed
        np.random.seed(seed=seed)
        random.seed(seed)

        self.wireless = pd.read_csv(
            f'{PATH_NETWORK}/LAN/filtered_ping_wireless.csv')
        self.ethernet = pd.read_csv(
            f'{PATH_NETWORK}/LAN/filtered_ping_ethernet.csv')
        return

    # NetworkLatency is a singleton
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(NetworkLatency, cls).__new__(cls)
        return cls.instance

    def random_wireless(self) -> float:
        random_number = random.randint(0, len(self.wireless))
        return self.wireless['remote_avg'][random_number]

    def random_ethernet(self) -> float:
        random_number = random.randint(0, len(self.ethernet))
        return self.ethernet['remote_avg'][random_number]

    def random_cloud(self) -> int:
        ''' NOT IMPLEMENTED
        '''
        return 10


network_latency = NetworkLatency()
