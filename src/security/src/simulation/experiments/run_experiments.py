import json
import pandas as pd
from datetime import datetime
from src.simulation.simulator import IoRTSimulation
from src.security.anomaly_detection import FederatedAnomalyDetector

class ExperimentRunner:
    def __init__(self):
        self.results = {}
        
    def run_all_experiments(self) -> Dict:
        print("Starting comprehensive IoRT experiments...")
        
        # Experiment 1: Baseline Performance
        print("Running baseline performance experiment...")
        baseline_results = self.run_baseline_experiment()
        
        # Experiment 2: Security Analysis
        print("Running security analysis experiment...")
        security_results = self.run_security_experiment()
        
        # Experiment 3: Deployment Scenarios
        print("Running deployment scenario validation...")
        deployment_results = self.run_deployment_scenarios()
        
        # Compile all results
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'baseline': baseline_results,
            'security': security_results,
            'deployment': deployment_results,
            'summary': self.generate_summary(baseline_results, security_results, deployment_results)
        }
        
        # Save results
        self.save_results()
        return self.results
    
    def run_baseline_experiment(self) -> Dict:
        simulation = IoRTSimulation(num_nodes=300)
        metrics = simulation.measure_performance_metrics()
        
        # Run multiple consensus rounds
        consensus_results = []
        for i in range(10):
            result = simulation.run_consensus_round({'experiment': f'round_{i}'})
            consensus_results.append(result)
            
        consensus_success_rate = sum(1 for r in consensus_results if r['success']) / len(consensus_results)
        
        return {
            'network_scale': len(simulation.nodes),
            'performance_metrics': metrics,
            'consensus_success_rate': consensus_success_rate,
            'consensus_quality': np.mean([r['consensus_quality'] for r in consensus_results if r['success']])
        }
    
    def run_security_experiment(self) -> Dict:
        simulation = IoRTSimulation(num_nodes=300)
        detector = FederatedAnomalyDetector(simulation.nodes)
        anomaly_detections = detector.detect_anomalies()
        
        # Calculate detection metrics
        true_positives = len([d for d in anomaly_detections if d['is_adversarial']])
        false_positives = len([d for d in anomaly_detections if not d['is_adversarial']])
        actual_adversarials = len([n for n in simulation.nodes if n.is_adversarial])
        
        precision = true_positives / max(1, true_positives + false_positives)
        recall = true_positives / max(1, actual_adversarials)
        f1_score = 2 * precision * recall / max(1, precision + recall) if (precision + recall) > 0 else 0
        
        return {
            'anomaly_detections': len(anomaly_detections),
            'detection_metrics': {
                'precision': precision,
                'recall': recall,
                'f1_score': f1_score,
                'true_positives': true_positives,
                'false_positives': false_positives
            }
        }
    
    def run_deployment_scenarios(self) -> Dict:
        scenarios = {
            'smart_factory': {
                'max_latency': 20.0,
                'min_trust': 0.8,
                'safety_critical_ratio': 0.8
            },
            'drone_swarm': {
                'max_latency': 10.0,
                'min_trust': 0.85,
                'safety_critical_ratio': 0.9
            },
            'smart_city': {
                'max_latency': 50.0,
                'min_trust': 0.7,
                'safety_critical_ratio': 0.6
            }
        }
        
        results = {}
        simulation = IoRTSimulation(num_nodes=300)
        
        for scenario_name, requirements in scenarios.items():
            # Validate scenario requirements
            latency_ok = all(node.network_latency <= requirements['max_latency'] 
                           for node in simulation.nodes if node.safety_critical)
            trust_ok = all(node.quantum_trust_score >= requirements['min_trust'] 
                         for node in simulation.nodes if node.safety_critical)
            
            safety_critical_count = len([n for n in simulation.nodes if n.safety_critical])
            safety_ratio_ok = (safety_critical_count / len(simulation.nodes)) >= requirements['safety_critical_ratio']
            
            consensus_result = simulation.run_consensus_round({'scenario': scenario_name})
            consensus_ok = consensus_result['success'] and consensus_result['consensus_quality'] > 0.7
            
            results[scenario_name] = {
                'feasible': latency_ok and trust_ok and safety_ratio_ok and consensus_ok,
                'requirements_met': {
                    'latency': latency_ok,
                    'trust': trust_ok,
                    'safety_ratio': safety_ratio_ok,
                    'consensus': consensus_ok
                },
                'overall_score': np.mean([latency_ok, trust_ok, safety_ratio_ok, consensus_ok])
            }
            
        return results
    
    def generate_summary(self, baseline, security, deployment) -> Dict:
        return {
            'total_experiments': 3,
            'network_scale': baseline['network_scale'],
            'consensus_success_rate': baseline['consensus_success_rate'],
            'security_f1_score': security['detection_metrics']['f1_score'],
            'feasible_scenarios': sum(1 for scenario in deployment.values() if scenario['feasible']),
            'total_scenarios': len(deployment),
            'experiment_timestamp': datetime.now().isoformat()
        }
    
    def save_results(self):
        # Save to JSON
        with open('experiments/results/experimental_data.json', 'w') as f:
            json.dump(self.results, f, indent=2)
            
        # Save metrics to CSV
        metrics_data = []
        if 'baseline' in self.results:
            metrics_data.append({
                'metric': 'consensus_success_rate',
                'value': self.results['baseline']['consensus_success_rate'],
                'experiment': 'baseline'
            })
            
        if 'security' in self.results:
            metrics_data.append({
                'metric': 'security_f1_score',
                'value': self.results['security']['detection_metrics']['f1_score'],
                'experiment': 'security'
            })
            
        df = pd.DataFrame(metrics_data)
        df.to_csv('experiments/results/performance_metrics.csv', index=False)

if __name__ == "__main__":
    runner = ExperimentRunner()
    results = runner.run_all_experiments()
    print("Experiments completed. Results saved to experiments/results/")
