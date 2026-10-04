"""
DRL Configuration Settings
Centralized configuration for Deep Q-Network training and inference
"""

from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class DRLConfig:
    """Configuration for DRL training and inference"""
    
    # =========================================================================
    # MODEL ARCHITECTURE
    # =========================================================================
    policy_type: str = "MlpPolicy"  # Multi-Layer Perceptron
    net_arch: list = None  # [64, 64] - will be set in __post_init__
    activation_fn: str = "relu"  # Activation function
    
    # =========================================================================
    # TRAINING HYPERPARAMETERS
    # =========================================================================
    learning_rate: float = 1e-3  # 0.001
    buffer_size: int = 100000  # Replay buffer size
    learning_starts: int = 1000  # Steps before training starts
    batch_size: int = 64  # Mini-batch size
    tau: float = 1.0  # Target network soft update
    gamma: float = 0.99  # Discount factor for future rewards
    train_freq: int = 4  # Update every 4 steps
    gradient_steps: int = 1  # Gradient steps per update
    target_update_interval: int = 1000  # Update target network every N steps
    
    # =========================================================================
    # EXPLORATION (EPSILON-GREEDY)
    # =========================================================================
    exploration_fraction: float = 0.1  # 10% of training for exploration
    exploration_initial_eps: float = 1.0  # Start with 100% random
    exploration_final_eps: float = 0.05  # End with 5% random
    
    # =========================================================================
    # TRAINING DURATION
    # =========================================================================
    total_timesteps: int = 100000  # Total training steps
    eval_episodes: int = 10  # Episodes for evaluation
    
    # =========================================================================
    # ENVIRONMENT SETTINGS
    # =========================================================================
    simulation_days: int = 30  # Days per episode
    max_steps_per_episode: int = 30  # Max steps (one per day)
    
    # =========================================================================
    # REWARD FUNCTION WEIGHTS
    # =========================================================================
    infection_penalty: float = 1.0  # Weight for infections
    cost_penalty: float = 0.01  # Weight for vaccination cost
    human_infection_penalty: float = 1000.0  # Heavy penalty for human cases
    outbreak_control_bonus: float = 50.0  # Bonus for stopping outbreak
    
    # =========================================================================
    # STATE SPACE CONFIGURATION
    # =========================================================================
    state_features: list = None  # Will be set in __post_init__
    normalize_state: bool = True  # Normalize state values to [0, 1]
    
    # =========================================================================
    # ACTION SPACE CONFIGURATION
    # =========================================================================
    action_type: str = "continuous"  # "continuous" or "discrete"
    discrete_actions: list = None  # [0.0, 0.25, 0.5, 0.75, 0.85, 0.95]
    action_min: float = 0.0  # Min vaccination %
    action_max: float = 1.0  # Max vaccination %
    
    # =========================================================================
    # MODEL SAVING & LOGGING
    # =========================================================================
    model_save_path: str = "./drl/models/dqn_rabies_vaccination"
    tensorboard_log: str = "./drl/logs/tensorboard"
    save_freq: int = 10000  # Save model every N steps
    log_interval: int = 100  # Log progress every N steps
    
    # =========================================================================
    # DEVICE SETTINGS
    # =========================================================================
    device: str = "auto"  # "cuda", "cpu", or "auto"
    
    def __post_init__(self):
        """Initialize default lists"""
        if self.net_arch is None:
            self.net_arch = [64, 64]  # 2 hidden layers with 64 neurons each
        
        if self.state_features is None:
            self.state_features = [
                'infection_rate',
                'vaccination_coverage', 
                'neighbor_risk',
                'population_density',
                'risk_level_numeric',
                'day_normalized'
            ]
        
        if self.discrete_actions is None:
            self.discrete_actions = [0.0, 0.25, 0.5, 0.75, 0.85, 0.95]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary"""
        return {
            'learning_rate': self.learning_rate,
            'buffer_size': self.buffer_size,
            'learning_starts': self.learning_starts,
            'batch_size': self.batch_size,
            'gamma': self.gamma,
            'train_freq': self.train_freq,
            'gradient_steps': self.gradient_steps,
            'target_update_interval': self.target_update_interval,
            'exploration_fraction': self.exploration_fraction,
            'exploration_initial_eps': self.exploration_initial_eps,
            'exploration_final_eps': self.exploration_final_eps,
        }


# =============================================================================
# DEFAULT CONFIGURATION INSTANCE
# =============================================================================

DEFAULT_CONFIG = DRLConfig()


# =============================================================================
# CONFIGURATION PRESETS
# =============================================================================

# Fast training (for testing)
FAST_CONFIG = DRLConfig(
    total_timesteps=10000,
    buffer_size=10000,
    learning_starts=500,
)

# Standard training (recommended)
STANDARD_CONFIG = DRLConfig(
    total_timesteps=100000,
    buffer_size=100000,
    learning_starts=1000,
)

# Extended training (for best performance)
EXTENDED_CONFIG = DRLConfig(
    total_timesteps=500000,
    buffer_size=200000,
    learning_starts=5000,
    batch_size=128,
)


def get_config(preset: str = "standard") -> DRLConfig:
    """
    Get configuration preset
    
    Args:
        preset: "fast", "standard", or "extended"
        
    Returns:
        DRLConfig instance
    """
    configs = {
        "fast": FAST_CONFIG,
        "standard": STANDARD_CONFIG,
        "extended": EXTENDED_CONFIG,
    }
    
    return configs.get(preset.lower(), STANDARD_CONFIG)


# =============================================================================
# TESTING
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("DRL Configuration")
    print("=" * 70)
    
    config = DEFAULT_CONFIG
    
    print("\n📊 Model Architecture:")
    print(f"  Policy: {config.policy_type}")
    print(f"  Network: {config.net_arch}")
    print(f"  Activation: {config.activation_fn}")
    
    print("\n⚙️ Training Settings:")
    print(f"  Total Timesteps: {config.total_timesteps:,}")
    print(f"  Learning Rate: {config.learning_rate}")
    print(f"  Batch Size: {config.batch_size}")
    print(f"  Gamma (Discount): {config.gamma}")
    
    print("\n🔍 Exploration:")
    print(f"  Initial Epsilon: {config.exploration_initial_eps}")
    print(f"  Final Epsilon: {config.exploration_final_eps}")
    print(f"  Exploration Fraction: {config.exploration_fraction}")
    
    print("\n🎮 Environment:")
    print(f"  Simulation Days: {config.simulation_days}")
    print(f"  State Features: {len(config.state_features)}")
    print(f"  Features: {', '.join(config.state_features)}")
    
    print("\n💰 Reward Weights:")
    print(f"  Infection Penalty: {config.infection_penalty}")
    print(f"  Cost Penalty: {config.cost_penalty}")
    print(f"  Human Infection Penalty: {config.human_infection_penalty}")
    print(f"  Outbreak Control Bonus: {config.outbreak_control_bonus}")
    
    print("\n" + "=" * 70)
    print("Configuration loaded successfully!")
    print("=" * 70)
