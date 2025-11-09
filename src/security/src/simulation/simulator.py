import numpy as np
from typing import List, Dict
from ..core.nodes import IoRTNode, NodeType
from ..core.quantum_trust import QuantumTrustEngine
from ..core.consensus import ConsensusManager
from ..core.safety_verifier import NeuralSymbolicSafetyVerifier, SafetyConstraint
from ..security.holographic_storage import HolographicTrustStorage

class IoRTSimulation:
    def __init__(self, num_nodes: int = 300):
        self.num_nodes = num_nodes
        self.nodes = []
        self.quantum_trust = QuantumTrustEngine()
        self.consensus = ConsensusManager()
        self.safety_verifier = NeuralSymbolicSafetyVerifier()
        self.trust_storage = HolographicTrustStorage(num_nodes)
        
        self.setup_network()
        self.apply_quantum_trust()
        
    def setup_network(self):
        np.random.seed(42)
        for i in range(self.num_nodes):
            node_type = np.random.choice(list(NodeType), p=[0.4, 0.3, 0.2, 0.1])
            
            if node_type == NodeType.ROBOT:
                compute = np.random.uniform(200, 800)
                latency = np.random.uniform(1, 15)
                trust = np.random.beta(3, 2)
            elif node_type == NodeType.EDGE_SENSOR:
                compute = np.random.uniform(20, 100)
                latency = np.random.uniform(3, 25)
                trust = np.random.beta(4, 2)
            elif node_type == NodeType.EDGE_COMPUTER:
                compute = np.random.uniform(800, 2000)
                latency = np.random.uniform(2, 12)
                trust = np.random.beta(5, 1)
            else:
                compute = np.random.uniform(2000, 10000)
                latency = np.random.uniform(30, 150)
                trust = np.random.beta(6, 1)
                
            position = (np.random.uniform(0, 500), np.random.uniform(0, 500))
            safety_critical = np.random.random() > 0.5
            
            node = IoRTNode(
                node_id=f"node_{i:05d}",
                node_type=node_type,
                compute_capacity=compute,
                network_latency=latency,
                trust_score=trust,
                position=position,
                safety_critical=safety_critical
            )
            self.nodes.append(node)
            
    def apply_quantum_trust(self):
        positions = np.array([node.position for node in self.nodes])
        initial_trust = np.array([node.trust_score for node in self.nodes])
        quantum_trust = self.quantum_trust.quantum_walk_propagation(
            self.nodes, positions, initial_trust
        )
        for i, node in enumerate(self.nodes):
            node.quantum_trust_score = quantum_trust[i]
            
    def run_consensus_round(self, proposal: Dict) -> Dict:
        participating_nodes = [node for node in self.nodes if node.quantum_trust_score > 0.4]
        if len(participating_nodes) < 3:
            return {'success': False, 'reason': 'Insufficient trusted nodes'}
            
        proposals = []
        for node in participating_nodes:
            node_proposal = proposal.copy()
            node_proposal['node_id'] = node.node_id
            node_proposal['quantum_trust'] = node.quantum_trust_score
            proposals.append(node_proposal)
            
        consensus_result = self.quantum_trust.entanglement_consensus(participating_nodes, proposals)
        trust_levels = [node.quantum_trust_score for node in participating_nodes]
        consensus_quality = np.mean(trust_levels) * len(participating_nodes) / len(self.nodes)
        
        return {
            'success': consensus_quality > 0.5,
            'consensus_result': consensus_result,
            'participating_nodes': len(participating_nodes),
            'consensus_quality': consensus_quality,
            'avg_quantum_trust': np.mean(trust_levels)
        }
        
    def measure_performance_metrics(self) -> Dict:
        latencies = [node.network_latency for node in self.nodes]
        trust_scores = [node.quantum_trust_score for node in self.nodes]
        compute_capacities = [node.compute_capacity for node in self.nodes]
        
        sample_nodes = np.random.choice(self.nodes, size=min(10, len(self.nodes)), replace=False)
        consensus_result, avg_trust = self.consensus.practical_byzantine_fault_tolerance(
            list(sample_nodes), {"task": "performance_measurement"}
        )
        
        safety_critical_nodes = [node for node in self.nodes if node.safety_critical]
        safety_score = np.mean([node.quantum_trust_score for node in safety_critical_nodes]) if safety_critical_nodes else 0.0
        
        return {
            'avg_latency': np.mean(latencies),
            'avg_quantum_trust': np.mean(trust_scores),
            'avg_compute': np.mean(compute_capacities),
            'consensus_success': consensus_result,
            'safety_score': safety_score,
            'network_size': len(self.nodes),
            'safety_critical_count': len(safety_critical_nodes)
        }
