import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from .logic_force import LogicForceProcessor

@dataclass
class DecisionResult:
    decision: str
    probability: float
    quantum_state: np.ndarray

class QuantumDecisionSystem:
    def __init__(
        self,
        logic_rules: Dict[str, List[str]],
        weights: Optional[Dict[str, float]] = None,
        quantum_backend: str = 'default',
        num_qubits: int = 4
    ):
        self.logic_rules = logic_rules
        self.weights = weights or {category: 1.0 for category in logic_rules}
        self.quantum_backend = quantum_backend
        self.num_qubits = num_qubits
        self.processor = LogicForceProcessor(num_qubits=num_qubits)
        
    def create_quantum_circuit(self, state: np.ndarray) -> np.ndarray:
        """Create a quantum circuit for decision making."""
        # Apply quantum operations
        # Here we're using a simple rotation based on the state
        angle = np.angle(state[np.argmax(np.abs(state))])
        rotation_matrix = np.array([
            [np.cos(angle), -np.sin(angle)],
            [np.sin(angle), np.cos(angle)]
        ])
        
        # Apply rotation to each qubit pair
        final_state = state.copy()
        for i in range(0, self.num_qubits - 1, 2):
            slice_indices = slice(2**i, 2**(i+2))
            final_state[slice_indices] = rotation_matrix @ final_state[slice_indices]
            
        return final_state
    
    def measure_state(self, state: np.ndarray) -> Tuple[str, float]:
        """Measure the quantum state to make a decision."""
        probabilities = np.abs(state) ** 2
        
        # Map state indices to decisions
        decision_map = {
            category: i * (len(state) // len(self.logic_rules))
            for i, category in enumerate(self.logic_rules)
        }
        
        # Find the most probable decision
        max_prob_index = np.argmax(probabilities)
        decision = min(
            decision_map.items(),
            key=lambda x: abs(x[1] - max_prob_index)
        )[0]
        
        return decision, probabilities[max_prob_index]
    
    def process(self, input_data: str) -> DecisionResult:
        """Process input and make quantum-enhanced decision."""
        # Get logical force and quantum state
        force_result = self.processor.process(input_data, self.logic_rules)
        
        # Create and execute quantum circuit
        evolved_state = self.create_quantum_circuit(force_result.state_vector)
        
        # Measure results
        decision, probability = self.measure_state(evolved_state)
        
        return DecisionResult(
            decision=decision,
            probability=probability,
            quantum_state=evolved_state
        )
        
    def update_rules(self, new_rules: Dict[str, List[str]]) -> None:
        """Update logical rules for decision making."""
        self.logic_rules.update(new_rules)
        # Update weights if necessary
        for category in new_rules:
            if category not in self.weights:
                self.weights[category] = 1.0
                
    def calibrate(self, training_data: List[Tuple[str, str]]) -> None:
        """Calibrate the decision system using training data."""
        # Update weights based on training examples
        successes = {category: 0 for category in self.logic_rules}
        totals = {category: 0 for category in self.logic_rules}
        
        for input_text, expected_category in training_data:
            result = self.process(input_text)
            totals[expected_category] += 1
            if result.decision == expected_category:
                successes[expected_category] += 1
        
        # Update weights based on success rates
        for category in self.weights:
            if totals[category] > 0:
                self.weights[category] = successes[category] / totals[category]
