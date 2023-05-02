
from typing import List
from models.resource import Resource
from models.enums.cache_replacement_strategy import CacheReplacementStrategy

# note: I think this is not the right place to add cache hit rate and cache miss rate


class Cache:
    def __init__(self, max_size_bytes: int, replacement_strategy=CacheReplacementStrategy.LRU):
        self.resources: List[Resource] = []
        self.max_size_bytes = max_size_bytes
        self.current_size_bytes = 0
        self.replacement_strategy = replacement_strategy
        self.request_received = 0
        self.cache_hits = 0
        # a cache miss is a cached resource that is not used
        self.cache_misses = 0

    def add_resource(self, resource: Resource, current_time: int = None):
        if current_time != None:
            resource.storage_time = current_time
         # check if there is space is cache
        if self.current_size_bytes + resource.size <= self.max_size_bytes:
            self.resources.append(resource)
            self.current_size_bytes += resource.size
            print(
                f"Resource {resource.provider_id} stored in cache at {current_time} until {resource.expiration_time}.")
        else:
            # check if resource bytes is bigger than the maximum cache size
            if resource.size > self.max_size_bytes:
                print(
                    f'impossible to cache {resource.provider_id} since its size is bigger then the cache size')
                return
            # If cache is full, apply replacement strategy
            if self.replacement_strategy == CacheReplacementStrategy.LRU:
                self._apply_lru_strategy()
                self.add_resource(resource)
            elif self.replacement_strategy == CacheReplacementStrategy.LFU:
                self._apply_lfu_strategy()
                self.add_resource(resource)
            else:
                print(f"Error: Invalid replacement strategy.")
                return

    def add_resource_per_description(self, provider_id: str, size_bytes: int, expiration_time, current_time):
        resource = Resource(provider_id, size_bytes,
                            current_time, expiration_time)
        self.add_resource(resource)

    def _apply_lru_strategy(self):
        # Least Recently Used (LRU)
        if len(self.resources) <= 0:
            print("Cache already empty - not possible to perform LRU")
            return
        self.resources.sort(key=lambda x: x.last_time_retrieved)
        # consider the case that the resource is great than the cache
        resource_to_remove = self.resources.pop(0)
        self.current_size_bytes -= resource_to_remove.size
        # check resource freq and if it 0, increment cache miss
        if resource_to_remove.frequency == 0:
            self.cache_misses += 1
        print(
            f"Resource {resource_to_remove.provider_id} removed from cache due to LRU strategy.")

    def _apply_lfu_strategy(self):
        # Least Frequently Used (LFU)
        if len(self.resources) <= 0:
            print("Cache already empty - not possible to perform LFU")
            return
        # Find the minimum frequency among all resources in the cache
        min_frequency = min(resource.frequency for resource in self.resources)

        # Find all resources with the minimum frequency
        least_frequent_resources = [
            resource.provider_id for resource in self.resources if resource.frequency == min_frequency]
        resource_to_remove = None
        # Iterate through the resources in the cache
        for resource in self.resources:
            # Check if the current resource is one of the least frequent resources
            if resource.provider_id in least_frequent_resources:
                # Compare the storage times of the current resource and the resource to remove
                if resource_to_remove is None or resource.storage_time < resource_to_remove.storage_time:
                    resource_to_remove = resource
        # If a resource to remove is found
        if resource_to_remove is not None:
            # Remove the resource from the cache
            self.resources.remove(resource_to_remove)
            # check resource freq and if it 0, increment cache miss
            if resource_to_remove.frequency == 0:
                self.cache_misses += 1
            self.current_size_bytes -= resource_to_remove.size
            print(
                f"Resource {resource_to_remove.provider_id} removed from cache due to LFU strategy.")

    def remove_expired_resources(self, current_time: int):
        #self.resources = [resource for resource in self.resources if current_time - resource.storage_time <= resource.expiration_time]
        self.resources = [resource for resource in self.resources if current_time <= resource.expiration_time]
        self.current_size_bytes = sum(
            resource.size for resource in self.resources)

    def get_resource(self, provider_id: str, current_time: int):
        self.request_received += 1
        for resource in self.resources:
            if resource.provider_id == provider_id:
                # if current_time - resource.storage_time <= resource.expiration_time:
                #if current_time <= resource.expiration_time:
                resource.frequency += 1
                resource.last_time_retrieved = current_time
                #print(f"Resource {provider_id} retrieved from cache.")
                self.cache_hits += 1
                return resource
        print(f"Resource {provider_id} not found in cache at {current_time}")
        return

    def get_cache_hit_rate(self):
        if self.request_received == 0:
            return 1
        return self.cache_hits / self.request_received

    def get_cache_miss_rate(self):
        if self.request_received == 0:
            return 1
        return self.miss_rate / self.request_received

    def epoch_passed(self, current_time):
        # TODO: optimize this operation
        self.remove_expired_resources(current_time)
