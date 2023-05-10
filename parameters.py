import argparse

from models.enums.cache_manager_node import CacheManagerMode
from models.enums.provider_type import ProviderType
from models.enums.user_category import UserCategory

parser = argparse.ArgumentParser(description='Description of your script')

parser.add_argument('--duration', type=int, default=3600000,
                    help='Duration of the experiment in milliseconds (default: 3600000)')
parser.add_argument('--label', type=str, default='baseline',
                    help='Label of the experiment (default: baseline)')
parser.add_argument('--edge-nodes', type=int, default=10, help='Number of edge nodes (default: 10)')
parser.add_argument('--users', type=int, default=500,                    help='Number of users (default: 500)')
parser.add_argument('--user-speed', type=float, default=10,
                    help='Average speed of the users in m/s (default: 10)')
parser.add_argument('--area-dimensions', type=int, default=100000000,
                    help='Area dimensions in square meters (default: 100000000)')
parser.add_argument('--subareas', type=int, default=5, help='Number of subareas (default: 5)')
parser.add_argument('--edge-node-distance', type=int, default=1000,
                    help='Minimum distance between edge nodes in meters (default: 1000)')
parser.add_argument('--user-waypoints', type=int, default=10,
                    help='Number of waypoints for each user (default: 10)')
parser.add_argument('--user-types', type=int, default=1,                    help='Number of user types (default: 1)')
parser.add_argument('--pre-req-time-avg', type=int, default=100,
                    help='Average time between requests for each user in milliseconds (default: 100)')
parser.add_argument('--pre-req-time-std', type=int, default=500,
                    help='Standard deviation of time between requests for each user in milliseconds (default: 500)')
parser.add_argument('--neighbor-edge-nodes', type=int, default=0,
                    help='Number of neighboring edge nodes for each cache worker (default: 0)')
parser.add_argument('--cache-expiration-time', type=int, default=600000,
                    help='Default expiration time for cached resources in milliseconds (default: 600000)')
parser.add_argument('--cache-not-found-resource', type=bool, default=False,
                    help='Whether to cache not found resources (default: False)')
parser.add_argument('--cache-size', type=float, default=4e+9,
                    help='Maximum size of the cache in bytes (default: 4e+9)')
parser.add_argument('--hit-rate', type=float, default=0.2,
                    help='Initial hit rate of the cache (default: 0)')
parser.add_argument('--cache-mode', type=str, default=CacheManagerMode.STANDARD_ONLY,
                    help='Cache manager mode (default: standard_only)')
parser.add_argument('--provider-high', type=float, default=0.333,
                    help='Fraction of high-capacity providers (default: 0.333)')
parser.add_argument('--provider-medium', type=float, default=0.333,
                    help='Fraction of medium-capacity providers (default: 0.333)')
parser.add_argument('--provider-low', type=float, default=0.334,
                    help='Fraction of low-capacity providers (default: 0.334)')
parser.add_argument('--user-distribution-id', type=float, default=0.333,
                    help='Fraction of id-based users (default: 0.333)')
parser.add_argument('--user-distribution-type', type=float, default=0.333,
                    help='Fraction of type-based users (default: 0.333)')
parser.add_argument('--user-distribution-location', type=float, default=0.334,
                    help='Fraction of location-based user (default: 0.334)')
parser.add_argument('--rate_of_event', type=float, default=0.0001, help='Rate of event')
parser.add_argument('--number_of_providers', type=int, default=750, help='Number of providers')
parser.add_argument('--popularity_distribution', type=float, default=1.1, help='Popularity distribution')
parser.add_argument('--cloud_trace_path', type=str, default='./data/network_traces/WAN', help='Cloud trace path')
parser.add_argument('--path_bytes', type=str, default='./data/bytes/', help='Path for bytes')
parser.add_argument('--path_time', type=str, default='./data/waiting-time/', help='Path for waiting time')
parser.add_argument('--write_in_file', type=bool, default=True, help='Write results to file')
parser.add_argument('--replications', type=int, default=2, help='Number of replications to execute of a single experiment (default: 1)')

args = parser.parse_args()

EXPERIMENT_DURATION = args.duration
EXPERIMENT_LABEL = args.label
REPLICATIONS = args.replications
NUMBER_OF_EDGE_NODES = args.edge_nodes
NUMBER_OF_USERS = args.users  # 100
USER_SPEED = args.user_speed  # 1.42  # avg walking speed in m/s
AREA_DIMENSIONS = args.area_dimensions
SUBAREAS = args.subareas
EDGE_NODE_MIN_DISTANCE = args.edge_node_distance
USER_CATEGORY_DISTRIBUTION = {
    UserCategory.ID: args.user_distribution_id,
    UserCategory.TYPE: args.user_distribution_type,
    UserCategory.LOCATION: args.user_distribution_location,
}
USER_WAYPOINTS = args.user_waypoints
# only when user from the category TYPE are deployed
NUMBER_OF_USER_TYPES = args.user_types
DEFAULT_AVG_PRE_REQUEST_TIME = args.pre_req_time_avg
DEFAULT_STD_PRE_REQUEST_TIME = args.pre_req_time_std


# CACHE WORKER METRICS
NEIGHBOR_EDGE_NODES = args.neighbor_edge_nodes
DEFAULT_EXPIRATION_TIME = args.cache_expiration_time  # 1000000  # in ms
CACHE_NOT_FOUND_RESOURCE = args.cache_not_found_resource
CACHE_DEFAULT_SIZE = args.cache_size

# CACHE MANAGER METRICS
HIT_RATE = args.hit_rate
MODE = args.cache_mode

# Request Generator
PROVIDER_DISTRIBUTION = {
    ProviderType.HIGH: args.provider_high,
    ProviderType.MEDIUM: args.provider_medium,
    ProviderType.LOW: args.provider_low,
}

RATE_OF_EVENT = args.rate_of_event
NUMBER_OF_PROVIDERS = args.number_of_providers
POPULARITY_DISTRIBUTION = args.popularity_distribution
CLOUD_TRACE_PATH = args.cloud_trace_path
PATH_BYTES = args.path_bytes
PATH_TIME = args.path_time
WRITE_IN_FILE = args.write_in_file
