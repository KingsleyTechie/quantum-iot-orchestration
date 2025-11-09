import numpy as np
from typing import List, Dict, Tuple
from dataclasses import dataclass
from enum import Enum

class ConsensusType(Enum):
    PBFT = "practical_byzantine_fault_tolerance"
    CRDT = "conflict_free_replicated_data_type"
    HYBRID = "hybrid_pbft_crdt"

@dataclass
class ConsensusConfig:
    consensus_type: ConsensusType = ConsensusType.HYBRID
    safety_threshold: float = 0.7
    timeout_ms: float = 100.0

class ConsensusManager:
    def __init__(self, config: ConsensusConfig = None):
        self.config = config or ConsensusConfig()
        
    def practical_byzantine_fault_tolerance(self, nodes: List, proposal: Dict) -> Tuple[bool, float]:
        trust_scores = [node.trust_score for node in nodes]
        avg_trust = np.mean(trust_scores)
        trusted_nodes = [score for score in trust_scores if score >= self.config.safety_threshold]
        consensus_achieved = len(trusted_nodes) >= (2 * len(nodes)) / 3
        return consensus_achieved, avg_trust
    
    def crdt_coordination(self, local_states: List[Dict]) -> Dict:
        merged_state = {}
        for state in local_states:
            for key, value in state.items():
                if key not in merged_state or value['timestamp'] > merged_state[key]['timestamp']:
                    merged_state[key] = value
        return merged_state
    
    def hybrid_consensus(self, nodes: List, proposal: Dict, local_states: List[Dict]) -> Dict:
        pbft_result, avg_trust = self.practical_byzantine_fault_tolerance(nodes, proposal)
        if pbft_result:
            crdt_state = self.crdt_coordination(local_states)
            return {
                'success': True,
                'consensus_type': 'hybrid',
                'avg_trust': avg_trust,
                'merged_state': crdt_state
            }
        return {'success': False, 'consensus_type': 'hybrid'}
