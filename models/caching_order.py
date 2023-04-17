from models.edge_node import EdgeNode
from models.order_type import OrderType


class CachingOrder:
    def __init__(self, edge_node: EdgeNode, execution_time, expiration_time, request_id: str, type=OrderType.STANDARD, cooperator_edge_node: EdgeNode = None):
        self.type = type
        self.edge_node = edge_node
        self.execution_time = execution_time
        self.validity_time = expiration_time
        self.request_id = request_id
        if type == OrderType.COOPERATIVE:
            self.cooperator_edge_node = cooperator_edge_node
