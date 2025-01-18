"""
Logic Force Theory (LFT) Framework
A quantum computing framework for measuring and applying logical forces in AI systems.
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .core.logic_force import LogicForceProcessor
from .core.quantum_processor import QuantumDecisionSystem
from .core.ai_interface import AIInterface
from .utils.measurements import (
    LogicMeasurements,
    QuantumAnalytics,
    PerformanceMetrics,
    measure_logic_impact
)

__all__ = [
    'LogicForceProcessor',
    'QuantumDecisionSystem',
    'AIInterface',
    'LogicMeasurements',
    'QuantumAnalytics',
    'PerformanceMetrics',
    'measure_logic_impact'
]
