from models.enums.cache_manager_node import CacheManagerMode
from models.enums.provider_type import ProviderType
from models.enums.user_category import UserCategory

# one hour?
EXPERIMENT_DURATION = 3600000
EXPERIMENT_TYPE = "Normal"  # baseline, normal, proactive, cooperative, etc
NUMBER_OF_EDGE_NODES = 8
NUMBER_OF_USERS = 2  # 100
USER_SPEED = 1.42  # avg walking speed in m/s
NUMBER_OF_PROVIDERS = 5
AREA_DIMENSIONS = 1000
SUBAREAS = 5
EDGE_NODE_MIN_DISTANCE = 100
USER_CATEGORY_DISTRIBUTION = {
    UserCategory.ID: 0,
    UserCategory.TYPE: 0,
    UserCategory.LOCATION: 1,
}
USER_WAYPOINTS = 10
# only when user from the category TYPE are deployed
NUMBER_OF_USER_TYPES = 10
DEFAULT_AVG_PRE_REQUEST_TIME = 100
DEFAULT_STD_PRE_REQUEST_TIME = 50


# CACHE WORKER METRICS
NEIGHBOR_EDGE_NODES = 0
DEFAULT_EXPIRATION_TIME = 1000000  # in ms
CACHE_NOT_FOUND_RESOURCE = False
CACHE_DEFAULT_SIZE = 4e+9

# CACHE MANAGER METRICS
HIT_RATE = 1
TIME_WINDOW_SIZE = 600000  # 10min in ms
MODE = CacheManagerMode.STANDARD_ONLY

# Request Generator
PROVIDER_DISTRIBUTION = {
    ProviderType.HIGH: 0.333,
    ProviderType.MEDIUM: 0.333,
    ProviderType.LOW: 0.334,
}
RATE_OF_EVENT = 0.0001  # one event per 10 seconds according to a poisson distribution
NUMBER_OF_PROVIDERS = 500
POPULARITY_DISTRIBUTION = 1.5
