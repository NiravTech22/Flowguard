import sys
import os
# Add the current directory to path so we can import invariant
sys.path.append(os.getcwd())

from invariant.workflow.loader import WorkflowLoader
from invariant.execution.engine import DeterministicEngine, PerturbationModel
from invariant.core.config import ExperimentConfig

def test_determinism():
    workflow_path = "examples/simple_workflow.yaml"
    graph = WorkflowLoader.from_yaml(workflow_path)
    
    # Run 1
    t0 = 1000.0
    config1 = ExperimentConfig({"seed": 42}, timestamp=t0)
    engine1 = DeterministicEngine(graph, config1)
    engine1.set_perturbation(PerturbationModel(latency_max_ms=50.0, seed=42))
    trace1 = engine1.run()
    
    # Run 2 (Same seed and same timestamp)
    config2 = ExperimentConfig({"seed": 42}, timestamp=t0)
    engine2 = DeterministicEngine(graph, config2)
    engine2.set_perturbation(PerturbationModel(latency_max_ms=50.0, seed=42))
    trace2 = engine2.run()
    
    # Compare latencies
    l1 = trace1.get_node_latencies()
    l2 = trace2.get_node_latencies()
    
    print(f"Run 1 Latencies: {l1}")
    print(f"Run 2 Latencies: {l2}")
    
    for node_id in l1:
        assert l1[node_id] == l2[node_id], f"Determinism failed for node {node_id}"
    
    print("Determinism test PASSED!")

if __name__ == "__main__":
    test_determinism()
