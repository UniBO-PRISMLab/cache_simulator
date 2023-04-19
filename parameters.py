from models.enums.cache_manager_node import CacheManagerMode
from models.enums.provider_type import ProviderType

# one hour? 
EXPERIMENT_DURATION = 3600000
EXPERIMENT_TYPE = "Normal" #baseline, normal, proactive, cooperative, etc
NUMBER_OF_EDGE_NODES = 8
NUMBER_OF_USERS = 2#100
USER_SPEED = 1.42 # avg walking speed in m/s 
NUMBER_OF_PROVIDERS = 50
AREA_DIMENSIONS = 1000
GRID_SIZE = 10
CACHE_SIZE = 1024
EDGE_NODE_MIN_DISTANCE=100


#CACHE WORKER METRICS
NEIGHBOR_EDGE_NODES = 1
DEFAULT_EXPIRATION_TIME = 1000000 #in ms
CACHE_NOT_FOUND_RESOURCE = False
CLEAN_CACHING_ORDERS_TIME_INTERNAL = 100 #not utilized
CACHE_DEFAULT_SIZE = 4e+9

# CACHE MANAGER METRICS
HIT_RATE = 0.5
TIME_WINDOW_SIZE = 600000 #10min in ms
MODE = CacheManagerMode.STANDARD_ONLY

#Request Generator
PROVIDER_DISTRIBUTION = {
    ProviderType.HIGH: 0.33,
    ProviderType.MEDIUM: 0.33,
    ProviderType.LOW: 0.33,
}
RATE_OF_EVENT = 0.0001 #one event per 10 seconds according to a poisson distribution
NUMBER_OF_PROVIDERS_PER_TYPE = 50
POPULARITY_DISTRIBUTION = 1.5