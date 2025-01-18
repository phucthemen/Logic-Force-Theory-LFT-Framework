import pytest
import numpy as np
from ..src.core.logic_force import LogicForceProcessor, LogicForceResult

class TestLogicForceProcessor:
    @pytest.fixture
    def processor(self):
        return LogicForceProcessor(num_qubits=4)
        
    @pytest.fixture
    def test_rules(self):
        return {
            "greeting": ["hello", "hi"],
            "command": ["create", "update"]
        }
        
    def test_initialization(self, processor):
        assert processor.num_qubits == 4
        assert processor.state_space == 16  # 2^4
        assert processor.force_threshold == 0.7
        
    def test_calculate_force(self, processor, test_rules):
        force = processor.calculate_force("hello world", test_rules)
        assert 0 <= force <= 1
        assert force > 0  # Should detect "hello"
        
    def test_generate_quantum_state(self, processor):
        state = processor.generate_quantum_state(0.5)
        assert isinstance(state, np.ndarray)
        assert len(state) == processor.state_space
        assert np.isclose(np.sum(np.abs(state) ** 2), 1.0)  # Normalized
        
    def test_coherence_check(self, processor):
        # Create un-normalized state
        state = np.array([0.5, 0.5, 0.5, 0.5])
        checked_state = processor.apply_coherence_check(state)
        assert np.isclose(np.sum(np.abs(checked_state) ** 2), 1.0)
        
    def test_process(self, processor, test_rules):
        result = processor.process("hello create something", test_rules)
        assert isinstance(result, LogicForceResult)
        assert 0 <= result.force <= 1
        assert 0 <= result.confidence <= 1
        assert isinstance(result.state_vector, np.ndarray)
        
    def test_empty_input(self, processor, test_rules):
        result = processor.process("", test_rules)
        assert result.force == 0
        
    def test_force_threshold(self):
        processor = LogicForceProcessor(force_threshold=0.5)
        assert processor.force_threshold == 0.5
        
    @pytest.mark.parametrize("input_text,expected_force", [
        ("hello world", 0.5),  # Single match
        ("hello create", 1.0),  # Multiple matches
        ("random text", 0.0),   # No matches
    ])
    def test_various_inputs(self, processor, test_rules, input_text, expected_force):
        result = processor.process(input_text, test_rules)
        assert np.isclose(result.force, expected_force, atol=0.1)
