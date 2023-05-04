import random
import numpy as np
import pandas as pd

PATH_NETWORK = './data/network_traces'


class NetworkLatency:
    def __init__(self, seed=42):
        self.seed = seed
        np.random.seed(seed=seed)
        random.seed(seed)
        self.cloud = {}
        self.wireless = pd.read_csv(f'{PATH_NETWORK}/LAN/filtered_ping_wireless.csv')
        self.ethernet = pd.read_csv(f'{PATH_NETWORK}/LAN/filtered_ping_ethernet.csv')
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

    def random_cloud(self, trace_file) -> int:
        if not trace_file in self.cloud:
            file_content = pd.read_csv(f'{PATH_NETWORK}/WAN/{trace_file}', delimiter="	")
            self.cloud[trace_file] = file_content["latency_value[ms]"]
        random_number = random.randint(0, len(self.cloud[trace_file]))
        return self.cloud[trace_file][random_number]


network_latency = NetworkLatency()
