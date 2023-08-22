class TraceElement:
    """
    Represents an element in the trace generated.
    """

    def __init__(
            self, timestamp: int, edge_node: int, edge_node_location, provider: str, bytes: int, user_id: int,
            user_location, execution_time: int, subarea: int):
        """
        Initialize a new TraceElement object.

        Parameters:
            timestamp (int): The timestamp of the trace element.
            edge_node (int): The ID of the edge node associated with the trace element.
            provider (str): The hash of the data provider for the trace element.
            bytes (int): The size of the data in bytes for the trace element.
            user_id (int): The ID of the user associated with the trace element.
            execution_time (int): The execution time of the operation for the trace element.
        """
        self.timestamp = timestamp
        self.edge_node = edge_node
        self.edge_node_location = edge_node_location
        self.provider = provider
        self.bytes = bytes
        self.user_id = user_id
        formatted_tuple = tuple(str(x) for x in user_location)
        formatted_output = f"({', '.join(formatted_tuple)})"
        self.user_location = formatted_output
        self.execution_time = execution_time
        self.subarea = subarea
