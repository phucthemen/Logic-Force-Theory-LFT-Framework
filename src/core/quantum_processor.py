from typing import List, Dict, Optional, Tuple
import numpy as np
from dataclasses import dataclass
from .logic_force import LogicForce

@dataclass
class QuantumDecision:
    """Represents a quantum-enhanced decision"""
    confidence: float
    chosen_action: str
    alternate_actions: Dict[str, float]
    qubits_used: int
    coherence: float

class QuantumProcessor:
    """Handles quantum processing of logical forces"""
    
    def __init__(self, 
                 num_qubits: int = 4,
                 error_threshold: float = 0.01,
                 max_depth: int = 10):
        self.num_qubits = num_qubits
        self.error_threshold = error_threshold
        self.max_depth = max_depth
        self.state = self._initialize_state()
        
    def _initialize_state(self) -> np.ndarray:
        """Initialize quantum system state"""
        dim = 2 ** self.num_qubits
        state = np.zeros(dim)
        state[0] = 1.0  # Start in ground state
        return state
        
    def apply_logic_operation(self, 
                            force: LogicForce,
                            target_qubits: Optional[List[int]] = None) -> None:
        """Apply logical force as quantum operation"""
        if target_qubits is None:
            target_qubits = list(range(min(self.num_qubits, 
                                         int(-np.log2(force.uncertainty)))))
            
        # Create operation matrix
        op_matrix = self._create_logic_operator(force, len(target_qubits))
        
        # Apply operation to specified qubits
        self.state = self._apply_partial_operator(op_matrix, 
                                                target_qubits,
                                                self.state)
                                                
    def _create_logic_operator(self, 
                             force: LogicForce,
                             num_qubits: int) -> np.ndarray:
        """Create quantum operator from logical force"""
        dim = 2 ** num_qubits
        
        # Create base rotation matrix
        theta = force.magnitude * np.pi
        phi = force.direction
        
        # Single qubit rotation matrix
        rotation = np.array([
            [np.cos(theta/2), -np.exp(-1j*phi)*np.sin(theta/2)],
            [np.exp(1j*phi)*np.sin(theta/2), np.cos(theta/2)]
        ])
        
        # Extend to multiple qubits
        operator = rotation
        for _ in range(num_qubits - 1):
            operator = np.kron(operator, rotation)
            
        # Apply coherence damping
        gamma = 1 - force.coherence
        operator = (1 - gamma) * operator + gamma * np.eye(dim)
        
        return operator
        
    def _apply_partial_operator(self,
                              operator: np.ndarray,
                              target_qubits: List[int],
                              state: np.ndarray) -> np.ndarray:
        """Apply operator to specific qubits"""
        # Convert to density matrix
        rho = np.outer(state, state.conj())
        
        # Create full system operator
        full_op = self._extend_to_system(operator, target_qubits)
        
        # Apply operation
        rho_new = full_op @ rho @ full_op.conj().T
        
        # Extract new state (take first eigenvector)
        eigenvals, eigenvecs = np.linalg.eigh(rho_new)
        new_state = eigenvecs[:, -1]
        
        # Ensure proper normalization
        new_state /= np.linalg.norm(new_state)
        
        return new_state
        
    def _extend_to_system(self,
                         operator: np.ndarray,
                         target_qubits: List[int]) -> np.ndarray:
        """Extend operator to full system size"""
        if not target_qubits:
            return np.eye(2 ** self.num_qubits)
            
        # Sort target qubits
        target_qubits = sorted(target_qubits)
        
        # Create full operator
        result = np.eye(1)
        curr_qubit = 0
        
        for sys_qubit in range(self.num_qubits):
            if sys_qubit in target_qubits:
                # Add operator for target qubit
                idx = target_qubits.index(sys_qubit)
                sub_op = operator[idx:idx+1, idx:idx+1]
                result = np.kron(result, sub_op)
                curr_qubit += 1
            else:
                # Add identity for non-target qubit
                result = np.kron(result, np.eye(2))
                
        return result
        
    def make_decision(self,
                     actions: Dict[str, float]) -> QuantumDecision:
        """Make decision based on quantum state"""
        # Calculate probabilities for each action
        probs = self._calculate_action_probabilities(actions)
        
        # Choose action with highest probability
        chosen = max(probs.items(), key=lambda x: x[1])
        
        # Calculate decision confidence
        confidence = self._calculate_confidence(probs)
        
        # Calculate quantum coherence
        coherence = self._calculate_coherence()
        
        return QuantumDecision(
            confidence=confidence,
            chosen_action=chosen[0],
            alternate_actions={k: v for k, v in probs.items() if k != chosen[0]},
            qubits_used=self.num_qubits,
            coherence=coherence
        )
        
    def _calculate_action_probabilities(self,
                                     actions: Dict[str, float]) -> Dict[str, float]:
        """Calculate probability distribution over actions"""
        # Get measurement probabilities
        probs = np.abs(self.state) ** 2
        
        # Map to actions
        action_probs = {}
        chunk_size = len(probs) // len(actions)
        
        for i, (action, weight) in enumerate(actions.items()):
            start = i * chunk_size
            end = (i + 1) * chunk_size
            action_probs[action] = weight * np.sum(probs[start:end])
            
        # Normalize
        total = sum(action_probs.values())
        if total > 0:
            action_probs = {k: v/total for k, v in action_probs.items()}
            
        return action_probs
        
    def _calculate_confidence(self, probs: Dict[str, float]) -> float:
        """Calculate decision confidence"""
        if not probs:
            return 0.0
            
        # Use entropy as confidence measure
        prob_values = list(probs.values())
        entropy_val = -sum(p * np.log2(p) for p in prob_values if p > 0)
        max_entropy = np.log2(len(probs))
        
        if max_entropy == 0:
            return 1.0
            
        # Convert entropy to confidence (1 - normalized entropy)
        confidence = 1.0 - entropy_val / max_entropy
        return confidence
        
    def _calculate_coherence(self) -> float:
        """Calculate quantum coherence of current state"""
        # Use l1-norm of coherence
        rho = np.outer(self.state, self.state.conj())
        coherence = np.sum(np.abs(rho)) - np.sum(np.abs(np.diag(rho)))
        return min(1.0, coherence)
