from enum import Enum

class CacheReplacementStrategy(Enum):
    LFU = "LFU"
    LRU = "LRU"
