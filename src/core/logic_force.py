from dataclasses import dataclass
from typing import Dict, List, Optional, Union
import numpy as np
from scipy.stats import entropy

@dataclass
class LogicForce:
    """Represents a quantum of logical force"""
    magnitude: float  # 0-1
    coherence: float  # 0-1
    direction: float  # 0-2π
    uncertainty: float  # 0-1

@dataclass
class LogicRule:
    """Defines a logical rule with patterns and weights"""
    patterns: List[str]
    weight: float
    context: Optional[str] = None

class LogicForceProcessor:
    """Core processor for logical force calculations"""
    
    def __init__(self, 
                 force_threshold: float = 0.5,
                 coherence_threshold: float = 0.7,
                 quantum_enabled: bool = True):
        self.force_threshold = force_threshold
        self.coherence_threshold = coherence_threshold
        self.quantum_enabled = quantum_enabled
        self._rules: Dict[str, LogicRule] = {}
        
    def add_rule(self, 
                 rule_id: str, 
                 patterns: List[str], 
                 weight: float,
                 context: Optional[str] = None) -> None:
        """Add a new logical rule"""
        if not 0 <= weight <= 1:
            raise ValueError("Weight must be between 0 and 1")
        self._rules[rule_id] = LogicRule(patterns, weight, context)
        
    def calculate_force(self, 
                       input_text: str,
                       context: Optional[str] = None) -> LogicForce:
        """Calculate logical force from input text"""
        words = input_text.lower().split()
        matches = self._find_pattern_matches(words)
        
        if not matches:
            return LogicForce(0.0, 1.0, 0.0, 1.0)
            
        # Calculate base magnitude
        magnitude = self._calculate_magnitude(matches)
        
        # Calculate coherence based on pattern consistency
        coherence = self._calculate_coherence(matches)
        
        # Calculate direction based on context alignment
        direction = self._calculate_direction(matches, context)
        
        # Calculate uncertainty based on pattern coverage
        uncertainty = self._calculate_uncertainty(matches, words)
        
        return LogicForce(magnitude, coherence, direction, uncertainty)
    
    def _find_pattern_matches(self, words: List[str]) -> Dict[str, List[str]]:
        """Find matching patterns in input words"""
        matches = {}
        for rule_id, rule in self._rules.items():
            matched_patterns = [
                pattern for pattern in rule.patterns 
                if any(self._pattern_matches(pattern, word) for word in words)
            ]
            if matched_patterns:
                matches[rule_id] = matched_patterns
        return matches
    
    def _pattern_matches(self, pattern: str, word: str) -> bool:
        """Check if word matches pattern, supporting wildcards"""
        if pattern.endswith('*'):
            return word.startswith(pattern[:-1])
        return pattern == word
    
    def _calculate_magnitude(self, matches: Dict[str, List[str]]) -> float:
        """Calculate force magnitude from matches"""
        total_weight = sum(self._rules[rule_id].weight * len(patterns)
                          for rule_id, patterns in matches.items())
        return min(1.0, total_weight / len(self._rules))
    
    def _calculate_coherence(self, matches: Dict[str, List[str]]) -> float:
        """Calculate force coherence from pattern consistency"""
        if not matches:
            return 1.0
            
        # Calculate entropy of pattern distribution
        pattern_counts = [len(patterns) for patterns in matches.values()]
        if len(pattern_counts) == 1:
            return 1.0
            
        # Normalize pattern counts to probabilities
        total_patterns = sum(pattern_counts)
        probabilities = [count / total_patterns for count in pattern_counts]
        
        # Calculate normalized entropy (0-1)
        max_entropy = np.log(len(pattern_counts))
        if max_entropy == 0:
            return 1.0
            
        normalized_entropy = entropy(probabilities) / max_entropy
        return 1.0 - normalized_entropy
    
    def _calculate_direction(self, 
                           matches: Dict[str, List[str]], 
                           context: Optional[str]) -> float:
        """Calculate force direction based on context alignment"""
        if not context:
            return 0.0
            
        # Count context-aligned rules
        aligned_rules = sum(
            1 for rule_id in matches
            if self._rules[rule_id].context == context
        )
        
        if not aligned_rules:
            return np.pi  # Opposite direction for no alignment
            
        # Calculate direction based on alignment ratio
        alignment_ratio = aligned_rules / len(matches)
        return 2 * np.pi * alignment_ratio
    
    def _calculate_uncertainty(self, 
                             matches: Dict[str, List[str]], 
                             words: List[str]) -> float:
        """Calculate force uncertainty based on pattern coverage"""
        if not words:
            return 1.0
            
        # Count unique matched words
        matched_words = set()
        for patterns in matches.values():
            for pattern in patterns:
                if pattern.endswith('*'):
                    matched_words.update(
                        word for word in words 
                        if word.startswith(pattern[:-1])
                    )
                else:
                    matched_words.add(pattern)
                    
        # Calculate coverage ratio
        coverage = len(matched_words) / len(words)
        return 1.0 - coverage

    def to_quantum_state(self, force: LogicForce) -> np.ndarray:
        """Convert logical force to quantum state"""
        if not self.quantum_enabled:
            raise RuntimeError("Quantum processing is disabled")
            
        # Calculate number of required qubits
        magnitude_qubits = max(1, int(-np.log2(force.uncertainty)))
        
        # Create quantum state vector
        dim = 2 ** magnitude_qubits
        state = np.zeros(dim, dtype=np.complex128)
        
        # Encode force properties into quantum state
        angle = force.direction
        for i in range(dim):
            # Amplitude based on magnitude and coherence
            amplitude = np.sqrt(force.magnitude * force.coherence)
            
            # Phase based on direction
            phase = angle * i / (dim - 1) if dim > 1 else angle
            
            state[i] = amplitude * np.exp(1j * phase)
            
        # Normalize state
        state /= np.linalg.norm(state)
        
        return state

    def apply_force(self, 
                   target_state: np.ndarray, 
                   force: LogicForce) -> np.ndarray:
        """Apply logical force to quantum state"""
        if not self.quantum_enabled:
            raise RuntimeError("Quantum processing is disabled")
            
        force_state = self.to_quantum_state(force)
        
        # Ensure compatible dimensions
        if force_state.shape != target_state.shape:
            raise ValueError("Incompatible quantum states")
            
        # Apply force through quantum operation
        # Here we use a simple weighted superposition
        alpha = force.magnitude
        result_state = alpha * force_state + (1 - alpha) * target_state
        
        # Normalize result
        result_state /= np.linalg.norm(result_state)
        
        return result_state
