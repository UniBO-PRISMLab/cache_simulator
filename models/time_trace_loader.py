import sys
import json
from parameters import NUMBER_OF_USERS

PATH_TIMESTAMP = 'data/most_stable_cs_host_ordered.json'  # 'scripts/timestamps.json'


class TimeTraceLoader:
    def __init__(self, number_of_users=NUMBER_OF_USERS):
        self.index = [0 for _ in range(number_of_users)]
        response_trace = []
        with open(PATH_TIMESTAMP, 'r') as file:

            last_timestamp = None
            zero, not_zero = 0, 0
            for line in file:
                json_object = json.loads(line)
                timestamp = json_object['timegenerated']
                latency = json_object['time-taken']
                size = json_object['sc-bytes']
                if (last_timestamp == None):
                    last_timestamp = timestamp
                else:
                    time_difference = timestamp - last_timestamp
                    if (int(time_difference) == 0):
                        time_difference = 1
                        zero += 1
                    else:
                        not_zero += 1
                    response_trace.append({'interval': int(time_difference), 'time_taken': int(latency), 'size': int(size)})
                    # print(response_trace[-1])
                    last_timestamp = timestamp
        self.response_trace_per_id = self.divide_list_into_parts(response_trace, number_of_users)

        # print(self.time_interval_per_id[0][0])
        # sys.exit()
    # TimeTraceLoader is a singleton

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(TimeTraceLoader, cls).__new__(cls)
        return cls.instance

    def get_time(self, id: int) -> int:
        time_interval = self.response_trace_per_id[id][self.index[id]]['interval']
        self.index[id] = (self.index[id] + 1) % len(self.response_trace_per_id[id])
        return time_interval

    def get_application_latency(self, id: int) -> int:
        time_taken = self.response_trace_per_id[id][self.index[id]]['time_taken']
        return time_taken
    
    def get_size(self, id: int) -> int:
        size = self.response_trace_per_id[id][self.index[id]]['size']
        return size

    def get_trace_length(self, id: int) -> int:
        return len(self.response_trace_per_id[id])

    def divide_list_into_parts(self, input_list, num_parts):
        if num_parts <= 0:
            raise ValueError("Number of parts must be greater than 0.")

        part_size = len(input_list) // num_parts
        if part_size == 0:
            raise ValueError("Number of parts is too large for the input list.")
        divided_parts = [[] for _ in range(num_parts)]
        for i, item in enumerate(input_list):
            part_index = i % num_parts
            divided_parts[part_index].append(item)

        return divided_parts


time_trace_loader = TimeTraceLoader()
