from abc import ABC, abstractmethod
from typing import List, Dict, Any
from dataclasses import dataclass
from ..execution.signals import WorkflowExecutionTrace
from ..workflow.graph import WorkflowGraph

@dataclass
class ValidationResult:
    pass_status: bool
    validator_id: str
    message: str
    metrics: Dict[str, Any] = None

class BaseValidator(ABC):
    @abstractmethod
    def validate(self, graph: WorkflowGraph, traces: List[WorkflowExecutionTrace]) -> ValidationResult:
        pass
