from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional, Set
from datetime import datetime, timezone
import enum

class DependencyStatus(str, enum.Enum):
    PENDING = "PENDING"
    FULFILLED = "FULFILLED"
    BLOCKED = "BLOCKED"

class DependencyNode(BaseModel):
    node_id: str
    status: str = "ACTIVE"
    depends_on: List[str] = Field(default_factory=list)

class DependencyEngine:
    def __init__(self):
        self.nodes: Dict[str, DependencyNode] = {}
        
    def add_node(self, node: DependencyNode) -> DependencyNode:
        self.nodes[node.node_id] = node
        return node
        
    def check_blocked(self, node_id: str) -> bool:
        if node_id not in self.nodes:
            raise ValueError("Node not found")
            
        node = self.nodes[node_id]
        for dep_id in node.depends_on:
            if dep_id not in self.nodes:
                continue
            if self.nodes[dep_id].status == "DELAYED" or self.nodes[dep_id].status == "BLOCKED":
                return True
        return False
        
    def get_critical_path(self, target_node_id: str) -> List[str]:
        # simplified traversal
        path = []
        current = target_node_id
        while current in self.nodes:
            path.append(current)
            if not self.nodes[current].depends_on:
                break
            current = self.nodes[current].depends_on[0] # Just following first for simple critical path
        return path[::-1]
