from dataclasses import dataclass
from typing import Tuple, Dict, Optional
from enum import Enum

class NodeType(Enum):
    ROBOT = "robot"
    EDGE_SENSOR = "edge_sensor"
    EDGE_COMPUTER = "edge_computer"
    CLOUD = "cloud"

class SafetyLevel(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class IoRTNode:
    node_id: str
    node_type: NodeType
    compute_capacity: float
    network_latency: float
    trust_score: float
    position: Tuple[float, float]
    safety_critical: bool = False
    quantum_trust_score: float = 0.0
    is_adversarial: bool = False
    behavioral_profile: Dict = None
    safety_envelope: Dict = None
    
    def __post_init__(self):
        self.trust_score = max(0.0, min(1.0, self.trust_score))
        if self.behavioral_profile is None:
            self.behavioral_profile = self._default_behavioral_profile()
        if self.safety_envelope is None:
            self.safety_envelope = self._default_safety_envelope()
        self.quantum_trust_score = self.trust_score
    
    def _default_behavioral_profile(self) -> Dict:
        return {
            'response_time_mean': self.network_latency,
            'response_time_std': self.network_latency * 0.1,
            'trust_consistency': 0.9,
            'anomaly_score': 0.0,
            'quantum_entanglement': 1.0
        }
    
    def _default_safety_envelope(self) -> Dict:
        return {
            'max_latency': 50.0,
            'min_trust': 0.6,
            'max_compute_load': 0.8,
            'quantum_safety_threshold': 0.7,
            'entanglement_required': 0.5
        }
