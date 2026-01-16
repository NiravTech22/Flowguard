from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum

class PortType(Enum):
    INPUT = "input"
    OUTPUT = "output"

@dataclass
class Port:
    name: str
    port_type: PortType
    data_type: str
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class NodeConstraints:
    min_rate_hz: Optional[float] = None
    max_latency_ms: Optional[float] = None
    timeout_ms: Optional[float] = None

@dataclass
class Node:
    """Purely declarative Node representation."""
    id: str
    node_type: str
    ports: List[Port]
    constraints: NodeConstraints = field(default_factory=NodeConstraints)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        # Validate node ID and ports
        if not self.id:
            raise ValueError("Node ID cannot be empty")
        
    @property
    def input_ports(self) -> List[Port]:
        return [p for p in self.ports if p.port_type == PortType.INPUT]

    @property
    def output_ports(self) -> List[Port]:
        return [p for p in self.ports if p.port_type == PortType.OUTPUT]
