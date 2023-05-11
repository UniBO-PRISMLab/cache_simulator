# Distributed Edge Computing Simulation
This is a simulation of a distributed edge computing system, built using Python. The goal of the simulation is to evaluate the performance of different caching strategies in the context of a distributed edge computing system.

### Requirements
- Python 3.x
- Numpy
### Running the simulation
To run the simulation, simply run the simulator.py file:

```console
$ python simulator.py [-h] [--duration DURATION] [--label LABEL] [--edge-nodes EDGE_NODES] [--users USERS] [--user-speed USER_SPEED] [--area-dimensions AREA_DIMENSIONS]
                    [--subareas SUBAREAS] [--edge-node-distance EDGE_NODE_DISTANCE] [--user-waypoints USER_WAYPOINTS] [--user-types USER_TYPES]
                    [--pre-req-time-avg PRE_REQ_TIME_AVG] [--pre-req-time-std PRE_REQ_TIME_STD] [--neighbor-edge-nodes NEIGHBOR_EDGE_NODES]
                    [--cache-expiration-time CACHE_EXPIRATION_TIME] [--cache-not-found-resource CACHE_NOT_FOUND_RESOURCE] [--cache-size CACHE_SIZE] [--accuracy ACCURACY]
                    [--cache-mode CACHE_MODE] [--provider-high PROVIDER_HIGH] [--provider-medium PROVIDER_MEDIUM] [--provider-low PROVIDER_LOW]
                    [--user-distribution-id USER_DISTRIBUTION_ID] [--user-distribution-type USER_DISTRIBUTION_TYPE] [--user-distribution-location USER_DISTRIBUTION_LOCATION]
                    [--rate-of-event RATE_OF_EVENT] [--number-of-providers NUMBER_OF_PROVIDERS] [--popularity-distribution POPULARITY_DISTRIBUTION]
                    [--cloud-trace-path CLOUD_TRACE_PATH] [--path-bytes PATH_BYTES] [--path-time PATH_TIME] [--write-in-file WRITE_IN_FILE] [--replications REPLICATIONS]
```
The simulation takes several input parameters, including the number of edge nodes, the number of cache nodes, which can be configured using the cli. The complete list of parameters is: 
``` console
usage: simulator.py 

Description of your script

options:
  -h, --help            show this help message and exit
  --duration DURATION   Duration of the experiment in milliseconds (default: 3600000)
  --label LABEL         Label of the experiment (default: baseline)
  --edge-nodes EDGE_NODES
                        Number of edge nodes (default: 10)
  --users USERS         Number of users (default: 500)
  --user-speed USER_SPEED
                        Average speed of the users in m/s (default: 10)
  --area-dimensions AREA_DIMENSIONS
                        Area dimensions in square meters (default: 100000000)
  --subareas SUBAREAS   Number of subareas (default: 5)
  --edge-node-distance EDGE_NODE_DISTANCE
                        Minimum distance between edge nodes in meters (default: 1000)
  --user-waypoints USER_WAYPOINTS
                        Number of waypoints for each user (default: 10)
  --user-types USER_TYPES
                        Number of user types (default: 5)
  --pre-req-time-avg PRE_REQ_TIME_AVG
                        Average time between requests for each user in milliseconds (default: 100)
  --pre-req-time-std PRE_REQ_TIME_STD
                        Standard deviation of time between requests for each user in milliseconds (default: 500
  --neighbor-edge-nodes NEIGHBOR_EDGE_NODES
                        Number of neighboring edge nodes for each cache worker (default: 0)
  --cache-expiration-time CACHE_EXPIRATION_TIME
                        Default expiration time for cached resources in milliseconds (default: 600000)
  --cache-not-found-resource CACHE_NOT_FOUND_RESOURCE
                        Whether to cache not found resources (default: False)
  --cache-size CACHE_SIZE
                        Maximum size of the cache in bytes (default: 4e+9)
  --accuracy ACCURACY   Initial hit rate of the cache (default: 0)
  --cache-mode CACHE_MODE
                        Cache manager mode (default: standard)
  --provider-high PROVIDER_HIGH
                        Fraction of high-capacity providers (default: 0.333)
  --provider-medium PROVIDER_MEDIUM
                        Fraction of medium-capacity providers (default: 0.333)
  --provider-low PROVIDER_LOW
                        Fraction of low-capacity providers (default: 0.334)
  --user-distribution-id USER_DISTRIBUTION_ID
                        Fraction of id-based users (default: 0.333)
  --user-distribution-type USER_DISTRIBUTION_TYPE
                        Fraction of type-based users (default: 0.333)
  --user-distribution-location USER_DISTRIBUTION_LOCATION
                        Fraction of location-based user (default: 0.334)
  --rate-of-event RATE_OF_EVENT
                        Rate of event
  --number-of-providers NUMBER_OF_PROVIDERS
                        Number of providers
  --popularity-distribution POPULARITY_DISTRIBUTION
                        Popularity distribution
  --cloud-trace-path CLOUD_TRACE_PATH
                        Cloud trace path
  --path-bytes PATH_BYTES
                        Path for bytes
  --path-time PATH_TIME
                        Path for waiting time
  --write-in-file WRITE_IN_FILE
                        Write results to file
  --replications REPLICATIONS
                        Number of replications to execute of a single experiment (default: 1)
 ```

### Output
The simulation outputs several metrics, including the number of requests served, the number of requests served from the cache, and the average latency . These metrics are printed to the console at the end of the simulation and written in a file.


### Contributing
Contributions to the simulation are welcome! If you'd like to contribute, please fork the repository and submit a pull request.
