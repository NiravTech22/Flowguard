import click
import os
import yaml
from .workflow.loader import WorkflowLoader
from .execution.engine import DeterministicEngine, PerturbationModel
from .core.config import ExperimentConfig
from .validation.structural import StructuralValidator
from .validation.temporal import TemporalValidator
from .validation.behavioral import BehavioralValidator
from .validation.metrics import StabilityMetrics
from .reporting.generator import ReportGenerator

@click.group()
def main():
    """Invariant: Control-Theoretic ML for Robotics Workflows."""
    pass

@main.command()
@click.argument('workflow_path')
@click.option('--runs', default=5, help='Number of validation runs')
@click.option('--seed', default=42, help='Random seed')
@click.option('--latency-max', default=20.0, help='Max injected latency (ms)')
def validate(workflow_path, runs, seed, latency_max):
    """Run validation pipeline on a workflow."""
    if not os.path.exists(workflow_path):
        click.echo(f"Error: Workflow file not found at {workflow_path}")
        return

    click.echo(f"Loading workflow: {workflow_path}")
    graph = WorkflowLoader.from_yaml(workflow_path)
    
    config = ExperimentConfig({"workflow": workflow_path, "runs": runs, "seed": seed})
    engine = DeterministicEngine(graph, config)
    
    # Apply perturbations
    model = PerturbationModel(latency_max_ms=latency_max, jitter_ms=5.0, seed=seed)
    engine.set_perturbation(model)
    
    click.echo(f"Executing {runs} deterministic runs...")
    traces = []
    for _ in range(runs):
        traces.append(engine.run())
        
    click.echo("Running validation passes...")
    validators = [StructuralValidator(), TemporalValidator(), BehavioralValidator()]
    results = [v.validate(graph, traces) for v in validators]
    
    score = StabilityMetrics.compute_stability_score(results)
    
    click.echo(f"Stability Score: {score:.2f}")
    
    # Generate report
    reporter = ReportGenerator()
    md_report = reporter.generate_markdown(results, score, config.to_dict())
    
    report_path = "stability_report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(md_report)
        
    click.echo(f"Report generated: {report_path}")

if __name__ == "__main__":
    main()
