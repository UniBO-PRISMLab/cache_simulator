import pandas as pd
import numpy as np
import random

PATH_BYTES = './data/bytes/'
PATH_TIME = './data/waiting-time/'


class BytesAndTime:
    labels = ['low', 'medium', 'high']
    bytes = {'low': [], 'medium': [], 'high': []}
    time = {'low': [], 'medium': [], 'high': []}

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

    def get_bytes(self, workload):
        random_number = np.random.randint(0, len(self.bytes[workload]))
        return self.bytes[workload]['sc-bytes'][random_number]
        # return self.bytes[workload].sample(random_state=self.seed).iloc[0].iloc[0]

    def get_time(self, workload):
        random_number = random.randint(0, len(self.time[workload]))
        return self.time[workload]['time-taken'][random_number]
    
    def get_time_and_bytes(self, workload):
        data = {
            'time': self.get_time(workload),
            'bytes': self.get_bytes(workload)
        }
        return data
