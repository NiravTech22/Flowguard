import torch
from invariant.workflow.loader import WorkflowLoader
from invariant.execution.engine import DeterministicEngine, PerturbationModel
from invariant.core.config import ExperimentConfig
from invariant.validation.structural import StructuralValidator
from invariant.validation.temporal import TemporalValidator
from invariant.validation.behavioral import BehavioralValidator
from invariant.validation.metrics import StabilityMetrics
from invariant.ml.features import AggregatedFeatureExtractor
from invariant.ml.supervisor import MLPSupervisor
from invariant.ml.data import ReplayDataGenerator

def test_ml_loop():
    workflow_path = "examples/simple_workflow.yaml"
    graph = WorkflowLoader.from_yaml(workflow_path)
    
    extractor = AggregatedFeatureExtractor()
    supervisor = MLPSupervisor(input_dim=9) # 5 graph + 4 temporal
    generator = ReplayDataGenerator(extractor)
    
    print("Generating training data...")
    samples = []
    
    # Generate samples with different perturbations
    seeds = [42, 43, 44, 45, 46]
    for seed in seeds:
        config = ExperimentConfig({"seed": seed})
        engine = DeterministicEngine(graph, config)
        
        # High latency -> expected failure
        engine.set_perturbation(PerturbationModel(latency_max_ms=150.0, seed=seed))
        traces = [engine.run() for _ in range(3)]
        
        validators = [StructuralValidator(), TemporalValidator(), BehavioralValidator()]
        results = [v.validate(graph, traces) for v in validators]
        score = StabilityMetrics.compute_stability_score(results)
        
        sample = generator.generate_sample(graph, traces, score)
        samples.append(sample)
        print(f"Seed {seed}: Stability Score {score:.2f} -> Target {sample[1].item()}")

    print("\nTraining supervisor...")
    for epoch in range(50):
        total_loss = 0
        for feat, label in samples:
            loss = supervisor.train_step(feat, label)
            total_loss += loss
        if epoch % 10 == 0:
            print(f"Epoch {epoch}, Loss: {total_loss/len(samples):.4f}")
            
    # Prediction
    test_feat = samples[1][0] # Seed 43, which has Target 1.0 (High Risk)
    pred = supervisor.predict(test_feat)
    print(f"\nFinal Prediction for high-risk sample: {pred:.4f}")
    assert pred > 0.5, "Supervisor should predict high failure risk for high latency"
    
    print("\nML loop verification PASSED!")

if __name__ == "__main__":
    test_ml_loop()
