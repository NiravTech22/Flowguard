import torch
from typing import List, Tuple
from ..workflow.graph import WorkflowGraph
from ..execution.signals import WorkflowExecutionTrace
from .features import AggregatedFeatureExtractor
from ..validation.metrics import StabilityMetrics
from ..validation.base import ValidationResult

class ReplayDataGenerator:
    """Generates synthetic training data from validation runs."""
    
    def __init__(self, extractor: AggregatedFeatureExtractor):
        self.extractor = extractor

    def generate_sample(self, graph: WorkflowGraph, traces: List[WorkflowExecutionTrace], stability_score: float) -> Tuple[torch.Tensor, torch.Tensor]:
        features = self.extractor.extract(graph, traces)
        # Failure label is 1.0 if stability score is low
        label = 1.0 if stability_score < 0.7 else 0.0
        
        return torch.from_numpy(features), torch.tensor([label], dtype=torch.float32)
