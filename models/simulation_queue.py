from typing import List

from models.queue_element import QueueElement


class SimulationQueue:
    """
    A singleton class representing the simulation queue 

    Attributes:
    -----------
    queue : List[QueueElement]
        The queue of elements to be processed.

    Methods:
    --------
    add_element(element: QueueElement) -> None:
        Adds a new element to the queue.

    remove_element(element: QueueElement) -> None:
        Removes the specified element from the queue.

    sort_queue() -> None:
        Sorts the queue in ascending order of the time_epoch attribute of each element.
    """

    def __init__(self):
        self.queue: List[QueueElement] = []

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SimulationQueue, cls).__new__(cls)
        return cls.instance

    def add_element(self, element: QueueElement) -> None:
        """
        Adds a new element to the queue.

        Parameters:
        -----------
        element : QueueElement
            The element to be added to the queue.
        """
        self.queue.append(element)

    def remove_element(self, element: QueueElement) -> None:
        """
        Removes the specified element from the queue.

        Parameters:
        -----------
        element : QueueElement
            The element to be removed from the queue.
        """
        self.queue.remove(element)

    def sort_queue(self) -> None:
        """
        Sorts the queue in ascending order of the time_epoch attribute of each element.
        """
        self.queue.sort(key=lambda x: x.time_epoch)

    def reset(self) -> None:
        """
        Empty the queue.
        """
        self.queue: List[QueueElement] = []


SIMULATION_QUEUE: SimulationQueue = SimulationQueue()
