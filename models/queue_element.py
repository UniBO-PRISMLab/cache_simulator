from models.cache_worker import CacheWorker
from models.request import Request
from models.user import User


class QueueElement:
    """
    Represents an element in the simulation queue.
    """

    def __init__(self, request: Request, user: User, time_epoch: int, cache_worker: CacheWorker):
        """
        Initialize a new QueueElement object.

        Parameters:
            request (Request): A Request object representing the request to be processed.
            user (User): A User object representing the user who made the request.
            time_epoch (int): An integer representing the time epoch at which the request was made.
            cache_worker (CacheWorker): A CacheWorker object representing the cache worker responsible for processing the request.
        """
        self.request = request
        self.user = user
        self.time_epoch = time_epoch
        self.cache_worker = cache_worker
