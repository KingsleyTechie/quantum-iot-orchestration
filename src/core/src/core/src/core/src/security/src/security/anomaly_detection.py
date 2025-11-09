import torch
import torch.nn as nn
from typing import List, Dict
import numpy as np

class FederatedAnomalyDetector:
    def __init__(self, nodes: List):
        self.nodes = nodes
        self.global_model = self._create_detection_model()
        self.detection_history = []
        
    def _create_detection_model(self) -> nn.Module:
        return nn.Sequential(
            nn.Linear(7, 32),
            nn.Tanh(),
            nn.Linear(32, 16),
            nn.Tanh(),
            nn.Linear(16, 8),
            nn.Tanh(),
            nn.Linear(8, 1),
            nn.Sigmoid()
        )
    
    def extract_quantum_features(self, node) -> torch.Tensor:
        features = [
            node.quantum_trust_score,
            node.trust_score,
            node.network_latency / 100.0,
            node.compute_capacity / 1000.0,
            node.behavioral_profile['quantum_entanglement'],
            node.behavioral_profile['anomaly_score'],
            1.0 if node.safety_critical else 0.0
        ]
        return torch.tensor(features, dtype=torch.float32)
    
    def detect_anomalies(self) -> List[Dict]:
        detections = []
        for node in self.nodes:
            features = self.extract_quantum_features(node)
            with torch.no_grad():
                anomaly_prob = self.global_model(features.unsqueeze(0)).item()
            node.behavioral_profile['anomaly_score'] = anomaly_prob
            
            if anomaly_prob > 0.7:
                detection = {
                    'node_id': node.node_id,
                    'anomaly_score': anomaly_prob,
                    'quantum_trust': node.quantum_trust_score,
                    'regular_trust': node.trust_score,
                    'is_adversarial': node.is_adversarial
                }
                detections.append(detection)
        
        self.detection_history.extend(detections)
        return detections
