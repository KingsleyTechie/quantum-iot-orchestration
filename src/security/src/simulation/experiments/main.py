"""
Quantum-IoRT Framework Main Entry Point

Usage:
    python main.py --experiment baseline
    python main.py --experiment security  
    python main.py --experiment all
"""

import argparse
from experiments.run_experiments import ExperimentRunner
from src.simulation.simulator import IoRTSimulation

def main():
    parser = argparse.ArgumentParser(description='Quantum-IoRT Framework')
    parser.add_argument('--experiment', type=str, default='all',
                       choices=['baseline', 'security', 'deployment', 'all'],
                       help='Experiment to run')
    parser.add_argument('--nodes', type=int, default=300,
                       help='Number of nodes in simulation')
    
    args = parser.parse_args()
    
    if args.experiment == 'all':
        runner = ExperimentRunner()
        results = runner.run_all_experiments()
        print("All experiments completed successfully")
    else:
        simulation = IoRTSimulation(num_nodes=args.nodes)
        
        if args.experiment == 'baseline':
            metrics = simulation.measure_performance_metrics()
            print("Baseline Performance Metrics:", metrics)
            
        elif args.experiment == 'security':
            from src.security.anomaly_detection import FederatedAnomalyDetector
            detector = FederatedAnomalyDetector(simulation.nodes)
            detections = detector.detect_anomalies()
            print(f"Security Analysis: Detected {len(detections)} anomalies")

if __name__ == "__main__":
    main()
