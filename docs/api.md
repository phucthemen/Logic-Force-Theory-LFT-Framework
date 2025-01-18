# Logic Force Theory (LFT) Framework API Reference

## Core Components

### LogicForceProcessor

The main class for processing logical forces and converting them to quantum states.

#### Initialization
```python
processor = LogicForceProcessor(
    num_qubits: int = 4,
    force_threshold: float = 0.7,
    coherence_check: bool = True
)
```

**Parameters:**
- `num_qubits`: Number of qubits to use in quantum state representation
- `force_threshold`: Threshold for considering logical force significant
- `coherence_check`: Whether to perform quantum coherence preservation

#### Methods

##### calculate_force
```python
def calculate_force(self, input_text: str, rules: Dict[str, List[str]]) -> float
```
Calculates logical force from input text based on defined rules.

**Parameters:**
- `input_text`: Input text to analyze
- `rules`: Dictionary of logical rules

**Returns:**
- Float value representing logical force (0 to 1)

##### generate_quantum_state
```python
def generate_quantum_state(self, force: float) -> np.ndarray
```
Generates quantum state based on logical force.

**Parameters:**
- `force`: Logical force value

**Returns:**
- Numpy array representing quantum state

### QuantumDecisionSystem

Handles quantum-enhanced decision making based on logical forces.

#### Initialization
```python
system = QuantumDecisionSystem(
    logic_rules: Dict[str, List[str]],
    weights: Optional[Dict[str, float]] = None,
    quantum_backend: str = 'default',
    num_qubits: int = 4
)
```

**Parameters:**
- `logic_rules`: Dictionary of logical rules
- `weights`: Optional weights for different rule categories
- `quantum_backend`: Quantum processing backend to use
- `num_qubits`: Number of qubits in the system

#### Methods

##### process
```python
def process(self, input_data: str) -> DecisionResult
```
Process input and make quantum-enhanced decision.

**Parameters:**
- `input_data`: Input string to process

**Returns:**
- `DecisionResult` object containing decision, probability, and quantum state

### AIInterface

Interface for integrating with AI systems.

#### Initialization
```python
interface = AIInterface(
    model_type: str = 'transformer',
    logic_processor: Optional[LogicForceProcessor] = None,
    decision_system: Optional[QuantumDecisionSystem] = None,
    config: Optional[Dict[str, Any]] = None
)
```

**Parameters:**
- `model_type`: Type of AI model to use
- `logic_processor`: Optional LogicForceProcessor instance
- `decision_system`: Optional QuantumDecisionSystem instance
- `config`: Additional configuration options

## Utility Components

### LogicMeasurements

Utility class for measuring aspects of logical forces.

#### Methods

##### measure_logic_impact
```python
@staticmethod
def measure_logic_impact(
    initial_state: np.ndarray,
    final_state: np.ndarray
) -> MeasurementResult
```

**Parameters:**
- `initial_state`: Initial quantum state
- `final_state`: Final quantum state

**Returns:**
- `MeasurementResult` containing value, uncertainty, and metadata

### QuantumAnalytics

Analytics tools for quantum states and measurements.

#### Methods

##### calculate_entropy
```python
@staticmethod
def calculate_entropy(state: np.ndarray) -> float
```

##### measure_coherence
```python
@staticmethod
def measure_coherence(state: np.ndarray) -> float
```

## Data Types

### LogicForceResult
```python
@dataclass
class LogicForceResult:
    force: float
    confidence: float
    state_vector: np.ndarray
```

### DecisionResult
```python
@dataclass
class DecisionResult:
    decision: str
    probability: float
    quantum_state: np.ndarray
```

### MeasurementResult
```python
@dataclass
class MeasurementResult:
    value: float
    uncertainty: float
    metadata: Dict[str, any]
```

## Error Handling

The framework uses standard Python exceptions with additional context:

- `ValueError`: Invalid parameter values
- `TypeError`: Incorrect type of input
- `RuntimeError`: Execution errors in quantum processing

Example error handling:
```python
try:
    result = processor.process(input_text, rules)
except ValueError as e:
    print(f"Invalid input: {e}")
except RuntimeError as e:
    print(f"Processing error: {e}")
```
