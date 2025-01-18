import pytest
import numpy as np
from ..src.core.quantum_processor import QuantumDecisionSystem, DecisionResult

class TestQuantumDecisionSystem:
    @pytest.fixture
    def test_rules(self):
        return {
            "greeting": ["hello", "hi"],
            "command": ["create", "update"]
        }
        
    @pytest.fixture
    def decision_system(self, test_rules):
        return QuantumDecisionSystem(
            logic_rules=test_rules,
            num_qubits=4
        )
        
    def test_initialization(self, decision_system, test_rules):
        assert decision_system.logic_rules == test_rules
        assert decision_system.num_qubits == 4
        assert all(w == 1.0 for w in decision_system.weights.values())
        
    def test_create_quantum_circuit(self, decision_system):
        state = np.zeros(16, dtype=complex)
        state[0] = 1.0  # Basic state
        
        result = decision_system.create_quantum_circuit(state)
        assert isinstance(result, np.ndarray)
        assert len(result) == 16
        assert np.isclose(np.sum(np.abs(result) ** 2), 1.0)
        
    def test_measure_state(self, decision_system):
        state = np.zeros(16, dtype=complex)
        state[0] = 1.0
        
        decision, probability = decision_system.measure_state(state
