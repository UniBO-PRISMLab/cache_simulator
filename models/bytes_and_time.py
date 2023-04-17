from models.provider_type import ProviderType

import pandas as pd
import numpy as np
import random


PATH_BYTES = './data/bytes/'
PATH_TIME = './data/waiting-time/'


class BytesAndTime:
    labels = [ProviderType.LOW, ProviderType.MEDIUM, ProviderType.HIGH]
    bytes = {ProviderType.LOW: [],
             ProviderType.MEDIUM: [], ProviderType.HIGH: []}
    time = {ProviderType.LOW: [], ProviderType.MEDIUM: [], ProviderType.HIGH: []}

    def __init__(self, seed=42):
        self.seed = seed
        np.random.seed(seed=seed)
        # read lines
        random.seed(seed)
        # pd.random.seed(seed)
        for label in self.labels:
            self.bytes[label] = pd.read_csv(
                f'{PATH_BYTES}{label}.csv', usecols=['sc-bytes'])
            self.time[label] = pd.read_csv(
                f'{PATH_TIME}{label}.csv',  usecols=['time-taken'])
        return

    # BytesAndTime is a singleton
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(BytesAndTime, cls).__new__(cls)
        return cls.instance

    def get_bytes(self, workload: ProviderType) -> int:
        random_number = np.random.randint(0, len(self.bytes[workload]))
        return int(self.bytes[workload]['sc-bytes'][random_number])
        # return self.bytes[workload].sample(random_state=self.seed).iloc[0].iloc[0]

    def get_time(self, workload: ProviderType) -> int:
        random_number = random.randint(0, len(self.time[workload]))
        return int(self.time[workload]['time-taken'][random_number])

    def get_time_and_bytes(self, workload: ProviderType)-> tuple:
        return self.get_time(workload), self.get_bytes(workload)


bytes_and_time = BytesAndTime()
