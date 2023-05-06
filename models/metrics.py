

import csv
from datetime import datetime
import os
import statistics
from typing import List
from models.cache_worker import CacheWorker
from models.provider import Provider
from models.request import Request
from parameters import *


class MetricsCalculator:
    def __init__(self, write_in_file: bool = WRITE_IN_FILE):
        self.write_in_file = write_in_file
        self.metrics = {
            "latency": {
                "total": [],
                "application": [],
                "network": []
            },
            "aoi": []
        }
        self.to_store = {
            "aoi": None,
            "std_aoi": None,
            "total_latency": None,
            "std_total_latency": None,
            "number_of_requests_to_provider": None,
            "hit_rate": None,
        }
        self.experiment_start_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.experiment_dir_path = os.path.join("experiments", self.experiment_start_time)
        os.makedirs(self.experiment_dir_path)

    def write_parameter_file(self):
        # Define the header row
        header_row = ['EXPERIMENT_DURATION', 'EXPERIMENT_TYPE', 'NUMBER_OF_EDGE_NODES', 'NUMBER_OF_USERS',
                      'USER_SPEED', 'NUMBER_OF_PROVIDERS', 'AREA_DIMENSIONS', 'SUBAREAS', 'EDGE_NODE_MIN_DISTANCE',
                      'USER_WAYPOINTS', 'NUMBER_OF_USER_TYPES',
                      'DEFAULT_AVG_PRE_REQUEST_TIME', 'DEFAULT_STD_PRE_REQUEST_TIME', 'NEIGHBOR_EDGE_NODES',
                      'DEFAULT_EXPIRATION_TIME', 'CACHE_NOT_FOUND_RESOURCE', 'CACHE_DEFAULT_SIZE', 'HIT_RATE',
                      'MODE', 'PROVIDER_DISTRIBUTION', 'RATE_OF_EVENT', 'POPULARITY_DISTRIBUTION',
                      'NUMBER_OF_PROVIDERS', 'CLOUD_TRACE_PATH', 'USER_CATEGORY_DISTRIBUTION']

        # Define the values to store
        values_row = [EXPERIMENT_DURATION, EXPERIMENT_TYPE, NUMBER_OF_EDGE_NODES, NUMBER_OF_USERS, USER_SPEED,
                      NUMBER_OF_PROVIDERS, AREA_DIMENSIONS, SUBAREAS, EDGE_NODE_MIN_DISTANCE, USER_WAYPOINTS,
                      NUMBER_OF_USER_TYPES, DEFAULT_AVG_PRE_REQUEST_TIME, DEFAULT_STD_PRE_REQUEST_TIME,
                      NEIGHBOR_EDGE_NODES, DEFAULT_EXPIRATION_TIME, CACHE_NOT_FOUND_RESOURCE, CACHE_DEFAULT_SIZE,
                      HIT_RATE, MODE, PROVIDER_DISTRIBUTION, RATE_OF_EVENT, POPULARITY_DISTRIBUTION,
                      NUMBER_OF_PROVIDERS, CLOUD_TRACE_PATH, USER_CATEGORY_DISTRIBUTION]

        # Store the header row and values in a dictionary
        self.metrics['file_header'] = dict(zip(header_row, values_row))
        file_path = f'{self.experiment_dir_path}/parameters.csv'
        file_exists = os.path.isfile(file_path)
        # If write_in_file is True, write the header row and values to a CSV file
        if self.write_in_file and not file_exists:
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(header_row)
                writer.writerow(values_row)

    def calculate_cache_worker_metrics(self, cache_workers: List[CacheWorker]):
        acc_total_requests = 0
        acc_cached_requests = 0
        hit_rates = []
        for cache_worker in cache_workers:
            acc_total_requests += cache_worker.total_requests
            acc_cached_requests += cache_worker.cached_requests
            hit_rate = cache_worker.get_cache_hit_rate()
            hit_rates.append(hit_rate)
            print(
                f"Cache Worker #{cache_worker.id} received {cache_worker.total_requests} requests and its hit rate was {hit_rate}")
        hit_rate = acc_cached_requests/acc_total_requests
        self.to_store["hit_rate"] = hit_rate
        print(f"total requests: {acc_total_requests}")
        print(f"Average Hit Rate: {acc_cached_requests/acc_total_requests}")
        print(f"Standard Deviation of Hit Rate: {statistics.stdev(hit_rates)}")

    def add_request(self, response: Request, current_time_epoch):
        self.metrics["latency"]["application"].append(response.application_latency)
        self.metrics["latency"]["network"].append(response.network_latency)
        self.metrics["latency"]["total"].append(response.get_total_latency())
        self.metrics["aoi"].append(response.calculate_aoi(current_time_epoch))

    def calculate_latency_metrics(self):

        latency_metrics = self.metrics["latency"]

        avg_latency = statistics.mean(latency_metrics["total"])
        std_latency = statistics.stdev(latency_metrics["total"])
        self.to_store["total_latency"] = avg_latency
        self.to_store["std_total_latency"] = std_latency
        self.to_store["aoi"] = statistics.mean(self.metrics["aoi"])
        self.to_store["std_aoi"] = statistics.stdev(self.metrics["aoi"])
        print(f"average latency: {avg_latency}")
        print(f"std latency: {std_latency}")

    def calculate_requests_to_providers(self, providers: List[Provider]):
        providers_requests = 0
        for provider in providers:
            providers_requests += provider.number_of_requests
        self.to_store["number_of_requests_to_provider"] = providers_requests
        print(f"number of requests to providers: {providers_requests}")

    def calculate_metrics(self, cache_workers: List[CacheWorker], providers: List[Provider]):
        self.calculate_latency_metrics()
        self.calculate_requests_to_providers(providers)
        self.calculate_cache_worker_metrics(cache_workers)
        if self.write_in_file:
            self.write_parameter_file()
            file_path = os.path.join(self.experiment_dir_path, "data.csv")
            file_exists = os.path.isfile(file_path)
            with open(file_path, "a", newline="") as csv_file:
                headers = list(self.to_store.keys())
                writer = csv.DictWriter(csv_file, fieldnames=headers)
                if not file_exists or os.stat(file_path).st_size == 0:
                    writer.writeheader()
                writer.writerow(self.to_store)
