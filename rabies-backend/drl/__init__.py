"""
Deep Reinforcement Learning (DRL) Module for PAWPATROL
Adaptive Rabies Vaccination Optimization using Deep Q-Network (DQN)

This module implements the AI-powered vaccination decision system that learns
optimal vaccination strategies through reinforcement learning.

Components:
- environment.py: Gymnasium environment wrapping the transmission model
- dqn_agent.py: Deep Q-Network implementation and utilities
- train_dqn.py: Training script for the DQN agent
- inference.py: Trained model inference for vaccination recommendations

Author: PAWPATROL Research Team
Date: October 2026
"""

__version__ = "1.0.0"
__author__ = "PAWPATROL Research Team"

# Import components
try:
    from .environment import RabiesVaccinationEnv
    from .inference import DRLRecommender, get_recommender
    from .config import DRLConfig, DEFAULT_CONFIG, get_config
    
    __all__ = [
        'RabiesVaccinationEnv',
        'DRLRecommender',
        'get_recommender',
        'DRLConfig',
        'DEFAULT_CONFIG',
        'get_config'
    ]
except ImportError as e:
    print(f"Warning: Could not import DRL components: {e}")
    __all__ = []

