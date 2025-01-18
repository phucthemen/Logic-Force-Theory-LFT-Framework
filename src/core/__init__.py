# Initialize components
logic_processor = LogicForceProcessor(num_qubits=4)
decision_system = QuantumDecisionSystem(
    logic_rules={
        "greeting": ["hi", "hello", "hey"],
        "command": ["create", "update", "delete"],
        "query": ["what", "how", "when"]
    }
)
ai_interface = AIInterface(
    model_type='transformer',
    logic_processor=logic_processor,
    decision_system=decision_system
)

# Process a message
response = ai_interface.process_message("Hello, can you create a new document?")
print(f"Response: {response.content}")
print(f"Logic Force: {response.logic_force}")
print(f"Confidence: {response.confidence}")
