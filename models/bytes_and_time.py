from models.enums.provider_type import ProviderType

import pandas as pd

from parameters import PATH_BYTES, PATH_TIME
from shared.RandomGenerator import np_random


class BytesAndTime:
    labels = [ProviderType.LOW.value,
              ProviderType.MEDIUM.value, ProviderType.HIGH.value]
    bytes = {ProviderType.LOW.value: [],
             ProviderType.MEDIUM.value: [], ProviderType.HIGH.value: []}
    time = {ProviderType.LOW.value: [],
            ProviderType.MEDIUM.value: [], ProviderType.HIGH.value: []}

    def __init__(self):
        # read lines
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
        random_number = np_random.randint(
            0, len(self.bytes[workload.value]) - 1)
        return int(self.bytes[workload.value]['sc-bytes'][random_number])
        # return self.bytes[workload].sample(random_state=self.seed).iloc[0].iloc[0]

    def get_time(self, workload: ProviderType) -> int:
        random_number = np_random.randint(0, len(self.time[workload.value]) - 1)
        return int(self.time[workload.value]['time-taken'][random_number])

    def get_time_and_bytes(self, workload: ProviderType) -> tuple:
        return self.get_time(workload), self.get_bytes(workload)


bytes_and_time = BytesAndTime()
