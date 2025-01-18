from typing import Dict, List, Optional, Tuple
from ..core.logic_force import LogicForceProcessor
from ..core.quantum_processor import QuantumDecisionSystem
from ..core.ai_interface import AIInterface
from ..utils.measurements import PerformanceMetrics

class EnhancedChatbot:
    """
    Example implementation of a chatbot enhanced with Logic Force Theory.
    """
    
    def __init__(
        self,
        base_model: str = "gpt-3",
        logic_force_processor: Optional[LogicForceProcessor] = None,
        confidence_threshold: float = 0.8,
        custom_rules: Optional[Dict[str, List[str]]] = None
    ):
        # Initialize components
        self.base_model = base_model
        self.confidence_threshold = confidence_threshold
        self.metrics = PerformanceMetrics()
        
        # Define default chatbot-specific rules
        self.default_rules = {
            "greeting": ["hi", "hello", "hey", "greetings"],
            "farewell": ["bye", "goodbye", "see you", "farewell"],
            "question": ["what", "how", "why", "when", "where", "can", "could"],
            "command": ["do", "show", "tell", "find", "search", "create"],
            "affirmative": ["yes", "yeah", "sure", "okay", "alright"],
            "negative": ["no", "nope", "not", "don't", "cannot"]
        }
        
        # Combine with custom rules if provided
        self.rules = self.default_rules.copy()
        if custom_rules:
            self.rules.update(custom_rules)
            
        # Initialize LFT components
        self.logic_processor = logic_force_processor or LogicForceProcessor()
        self.decision_system = QuantumDecisionSystem(logic_rules=self.rules)
        self.ai_interface = AIInterface(
            model_type=base_model,
            logic_processor=self.logic_processor,
            decision_system=self.decision_system
        )
        
        # Initialize conversation history
        self.conversation_history: List[Dict[str, str]] = []
        
    def _update_history(self, user_input: str, response: str) -> None:
        """Update conversation history."""
        self.conversation_history.append({
            'user': user_input,
            'bot': response
        })
        
    def _generate_response_template(self, category: str) -> str:
        """Generate response template based on message category."""
        templates = {
            "greeting": "Hello! How can I help you today?",
            "farewell": "Goodbye! Have a great day!",
            "question": "Let me help you find that information.",
            "command": "I'll help you with that task.",
            "affirmative": "Great! Let's proceed.",
            "negative": "I understand. Let me know if you'd like to try something else."
        }
        return templates.get(category, "I understand. How can I help?")
        
    def process_message(self, message: str) -> Tuple[str, Dict[str, float]]:
        """
        Process user message and return enhanced response with metrics.
        """
        # Process through AI interface
        response = self.ai_interface.process_message(message)
        
        # Record metrics
        self.metrics.record_metric('logic_force', response.logic_force)
        self.metrics.record_metric('confidence', response.confidence)
        
        # Generate base response
        base_response = self._generate_response_template(
            self.decision_system.process(message).decision
        )
        
        # Enhance response based on logical force
        if response.confidence > self.confidence_threshold:
            enhanced_response = f"{base_response} {response.content}"
        else:
            enhanced_response = base_response
            
        # Update conversation history
        self._update_history(message, enhanced_response)
        
        # Return response with metrics
        metrics = {
            'logic_force': response.logic_force,
            'confidence': response.confidence,
            'history_length': len(self.conversation_history)
        }
        
        return enhanced_response, metrics
        
    def train(self, training_data: List[Tuple[str, str]]) -> None:
        """Train the chatbot with examples."""
        self.ai_interface.calibrate(training_data)
        
    def get_performance_metrics(self) -> Dict[str, Dict[str, float]]:
        """Get overall performance metrics."""
        return {
            'logic_force': self.metrics.get_metric_stats('logic_force'),
            'confidence': self.metrics.get_metric_stats('confidence')
        }
        
    def clear_history(self) -> None:
        """Clear conversation history and metrics."""
        self.conversation_history.clear()
        self.metrics.clear_history()

def run_example():
    """Run an example chatbot session."""
    # Initialize chatbot
    chatbot = EnhancedChatbot(
        base_model="gpt-3",
        confidence_threshold=0.7
    )
    
    # Example conversation
    messages = [
        "Hello there!",
        "Can you help me find information about quantum computing?",
        "That's great, thank you!",
        "Goodbye!"
    ]
    
    # Process messages
    print("Starting example conversation...")
    for message in messages:
        print(f"\nUser: {message}")
        response, metrics = chatbot.process_message(message)
        print(f"Bot: {response}")
        print(f"Metrics: {metrics}")
        
    # Show overall performance
    print("\nOverall Performance:")
    print(chatbot.get_performance_metrics())

if __name__ == "__main__":
    run_example()
