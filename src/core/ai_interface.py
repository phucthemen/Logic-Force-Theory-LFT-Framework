from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from .logic_force import LogicForceProcessor
from .quantum_processor import QuantumDecisionSystem

@dataclass
class AIResponse:
    content: str
    logic_force: float
    confidence: float
    quantum_state: Optional[List[complex]] = None

class AIInterface:
    def __init__(
        self,
        model_type: str = 'transformer',
        logic_processor: Optional[LogicForceProcessor] = None,
        decision_system: Optional[QuantumDecisionSystem] = None,
        config: Optional[Dict[str, Any]] = None
    ):
        self.model_type = model_type
        self.logic_processor = logic_processor or LogicForceProcessor()
        self.config = config or {}
        
        # Initialize default rules if decision system is not provided
        default_rules = {
            "query": ["what", "how", "why", "when", "where"],
            "command": ["create", "update", "delete", "show", "display"],
            "information": ["tell", "explain", "describe", "elaborate"]
        }
        self.decision_system = decision_system or QuantumDecisionSystem(
            logic_rules=default_rules
        )
        
    def preprocess_input(self, input_text: str) -> str:
        """Preprocess input text before processing."""
        # Basic preprocessing
        text = input_text.strip().lower()
        return text
        
    def enhance_response(self, 
                        base_response: str, 
                        quantum_decision: Dict[str, Any]) -> str:
        """Enhance AI response using quantum decision results."""
        # Modify response based on quantum decision confidence
        confidence = quantum_decision.get('probability', 0.0)
        
        if confidence > 0.8:
            # High confidence - be more assertive
            enhanced = f"With high confidence: {base_response}"
        elif confidence > 0.5:
            # Medium confidence - be more nuanced
            enhanced = f"Based on my analysis: {base_response}"
        else:
            # Low confidence - be more cautious
            enhanced = f"Taking into consideration the complexity: {base_response}"
            
        return enhanced
        
    def process_message(self, input_text: str) -> AIResponse:
        """Process input message and generate enhanced response."""
        # Preprocess input
        processed_input = self.preprocess_input(input_text)
        
        # Get quantum decision
        decision_result = self.decision_system.process(processed_input)
        
        # Generate base response (placeholder - would integrate with actual AI model)
        base_response = f"Response for {decision_result.decision} type input"
        
        # Enhance response
        enhanced_response = self.enhance_response(
            base_response,
            {
                'decision': decision_result.decision,
                'probability': decision_result.probability
            }
        )
        
        # Get logical force analysis
        force_result = self.logic_processor.process(
            processed_input,
            self.decision_system.logic_rules
        )
        
        return AIResponse(
            content=enhanced_response,
            logic_force=force_result.force,
            confidence=force_result.confidence,
            quantum_state=force_result.state_vector.tolist()
        )
        
    def update_rules(self, new_rules: Dict[str, List[str]]) -> None:
        """Update the system's logical rules."""
        self.decision_system.update_rules(new_rules)
        
    def calibrate(self, training_data: List[tuple]) -> None:
        """Calibrate the system using training data."""
        self.decision_system.calibrate(training_data)
