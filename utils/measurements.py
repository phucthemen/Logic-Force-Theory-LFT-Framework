import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class MeasurementResult:
    value: float
    uncertainty: float
    metadata: Dict[str, any]

class LogicMeasurements:
    """Utility class for measuring various aspects of logical forces."""
    
    @staticmethod
    def measure_logic_impact(
        initial_state: np.ndarray,
        final_state: np.ndarray
    ) -> MeasurementResult:
        """Measure the impact of logical force transformation."""
        # Calculate fidelity between initial and final states
        fidelity = np.abs(np.vdot(initial_state, final_state)) ** 2
        
        # Calculate uncertainty using quantum state purity
        purity_i = np.abs(np.vdot(initial_state, initial_state))
        purity_f = np.abs(np.vdot(final_state, final_state))
        uncertainty = abs(purity_f - purity_i)
        
        return MeasurementResult(
            value=float(fidelity),
            uncertainty=float(uncertainty),
            metadata={
                'initial_purity': float(purity_i),
                'final_purity': float(purity_f)
            }
        )

class QuantumAnalytics:
    """Analytics tools for quantum states and measurements."""
    
    @staticmethod
    def calculate_entropy(state: np.ndarray) -> float:
        """Calculate von Neumann entropy of a quantum state."""
        probabilities = np.abs(state) ** 2
        # Avoid log(0) issues
        probabilities = probabilities[probabilities > 0]
        return float(-np.sum(probabilities * np.log2(probabilities)))
    
    @staticmethod
    def measure_coherence(state: np.ndarray) -> float:
        """Calculate quantum coherence of the state."""
        # Using l1-norm of coherence
        rho = np.outer(state, state.conj())
        off_diagonal_sum = np.sum(np.abs(rho)) - np.sum(np.abs(np.diag(rho)))
        return float(off_diagonal_sum)
    
    @staticmethod
    def calculate_expectation(
        state: np.ndarray,
        observable: np.ndarray
    ) -> MeasurementResult:
        """Calculate expectation value of an observable."""
        expectation = np.real(state.conj() @ observable @ state)
        # Calculate variance for uncertainty
        variance = np.real(state.conj() @ observable @ observable @ state) - expectation**2
        
        return MeasurementResult(
            value=float(expectation),
            uncertainty=float(np.sqrt(variance)),
            metadata={'variance': float(variance)}
        )

class PerformanceMetrics:
    """Tools for measuring system performance."""
    
    def __init__(self):
        self.history: List[Dict[str, float]] = []
        
    def record_metric(
        self,
        metric_name: str,
        value: float,
        timestamp: Optional[float] = None
    ) -> None:
        """Record a performance metric."""
        if timestamp is None:
            import time
            timestamp = time.time()
            
        self.history.append({
            'metric': metric_name,
            'value': value,
            'timestamp': timestamp
        })
    
    def get_metric_stats(
        self,
        metric_name: str
    ) -> Dict[str, float]:
        """Get statistics for a specific metric."""
        values = [
            entry['value']
            for entry in self.history
            if entry['metric'] == metric_name
        ]
        
        if not values:
            return {}
            
        return {
            'mean': np.mean(values),
            'std': np.std(values),
            'min': np.min(values),
            'max': np.max(values),
            'count': len(values)
        }
    
    def clear_history(self) -> None:
        """Clear metric history."""
        self.history.clear()

def measure_logic_impact(
    initial_state: np.ndarray,
    final_state: np.ndarray
) -> Dict[str, float]:
    """Convenience function for measuring logic impact."""
    analytics = QuantumAnalytics()
    measurements = LogicMeasurements()
    
    impact = measurements.measure_logic_impact(initial_state, final_state)
    coherence_change = (
        analytics.measure_coherence(final_state) -
        analytics.measure_coherence(initial_state)
    )
    
    return {
        'impact': impact.value,
        'uncertainty': impact.uncertainty,
        'coherence_change': coherence_change,
        'final_entropy': analytics.calculate_entropy(final_state)
    }
