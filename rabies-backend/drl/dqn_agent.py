"""
DQN Agent Utilities and Helpers
Provides helper functions for DQN training, evaluation, and model management

Author: PAWPATROL Research Team
Date: October 2026
"""

import numpy as np
import torch
from typing import Dict, List, Tuple, Optional
from stable_baselines3 import DQN
from stable_baselines3.common.callbacks import BaseCallback, EvalCallback
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.vec_env import DummyVecEnv
import json
import os
import sys
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from drl.environment import RabiesVaccinationEnv
    from drl.config import DRLConfig, DEFAULT_CONFIG
except ImportError:
    # Fallback for direct script execution
    from environment import RabiesVaccinationEnv
    from config import DRLConfig, DEFAULT_CONFIG


class TrainingCallback(BaseCallback):
    """
    Custom callback for monitoring training progress
    Logs metrics and saves checkpoints during training
    """
    
    def __init__(self, verbose=1, save_freq=10000, save_path="./drl/models"):
        super().__init__(verbose)
        self.save_freq = save_freq
        self.save_path = save_path
        self.episode_rewards = []
        self.episode_lengths = []
        self.current_episode_reward = 0
        self.current_episode_length = 0
        
    def _on_step(self) -> bool:
        """Called at each step"""
        # Track episode metrics
        self.current_episode_reward += self.locals['rewards'][0]
        self.current_episode_length += 1
        
        # Check if episode ended
        if self.locals['dones'][0]:
            self.episode_rewards.append(self.current_episode_reward)
            self.episode_lengths.append(self.current_episode_length)
            
            # Log episode info
            if self.verbose > 0 and len(self.episode_rewards) % 10 == 0:
                avg_reward = np.mean(self.episode_rewards[-100:])
                avg_length = np.mean(self.episode_lengths[-100:])
                print(f"Episode {len(self.episode_rewards)}: "
                      f"Avg Reward (100 ep): {avg_reward:.2f}, "
                      f"Avg Length: {avg_length:.1f}")
            
            # Reset counters
            self.current_episode_reward = 0
            self.current_episode_length = 0
        
        # Save checkpoint
        if self.n_calls % self.save_freq == 0:
            checkpoint_path = os.path.join(
                self.save_path,
                f"dqn_checkpoint_{self.n_calls}"
            )
            self.model.save(checkpoint_path)
            if self.verbose > 0:
                print(f"✅ Saved checkpoint at step {self.n_calls}")
        
        return True
    
    def get_metrics(self) -> Dict:
        """Get training metrics"""
        if not self.episode_rewards:
            return {}
        
        return {
            'total_episodes': len(self.episode_rewards),
            'total_steps': self.n_calls,
            'mean_reward': float(np.mean(self.episode_rewards)),
            'std_reward': float(np.std(self.episode_rewards)),
            'mean_episode_length': float(np.mean(self.episode_lengths)),
            'last_100_mean_reward': float(np.mean(self.episode_rewards[-100:])) if len(self.episode_rewards) >= 100 else float(np.mean(self.episode_rewards)),
        }


def create_dqn_model(
    env: RabiesVaccinationEnv,
    config: DRLConfig = None
) -> DQN:
    """
    Create and configure DQN model
    
    Args:
        env: Training environment
        config: DRL configuration
        
    Returns:
        Configured DQN model
    """
    config = config or DEFAULT_CONFIG
    
    # Create model
    model = DQN(
        policy=config.policy_type,
        env=env,
        learning_rate=config.learning_rate,
        buffer_size=config.buffer_size,
        learning_starts=config.learning_starts,
        batch_size=config.batch_size,
        tau=config.tau,
        gamma=config.gamma,
        train_freq=config.train_freq,
        gradient_steps=config.gradient_steps,
        target_update_interval=config.target_update_interval,
        exploration_fraction=config.exploration_fraction,
        exploration_initial_eps=config.exploration_initial_eps,
        exploration_final_eps=config.exploration_final_eps,
        policy_kwargs=dict(net_arch=config.net_arch),
        tensorboard_log=config.tensorboard_log,
        verbose=1,
        device=config.device
    )
    
    return model


def train_dqn(
    env: RabiesVaccinationEnv,
    config: DRLConfig = None,
    model: DQN = None
) -> Tuple[DQN, Dict]:
    """
    Train DQN model
    
    Args:
        env: Training environment
        config: DRL configuration
        model: Existing model to continue training (optional)
        
    Returns:
        Trained model and training metrics
    """
    config = config or DEFAULT_CONFIG
    
    # Create model if not provided
    if model is None:
        print("Creating new DQN model...")
        model = create_dqn_model(env, config)
    else:
        print("Continuing training with existing model...")
    
    # Create callback
    callback = TrainingCallback(
        verbose=1,
        save_freq=config.save_freq,
        save_path=config.model_save_path
    )
    
    # Train model
    print(f"\nStarting training for {config.total_timesteps:,} timesteps...")
    print(f"This may take 10-15 minutes on CPU...")
    
    # FIXED: Disable log_interval to avoid Python 3.13 compatibility issue
    model.learn(
        total_timesteps=config.total_timesteps,
        callback=callback,
        log_interval=None,  # Disabled to fix Python 3.13 bug
        progress_bar=False
    )
    
    # Get metrics
    metrics = callback.get_metrics()
    
    print("\n✅ Training completed!")
    print(f"Total episodes: {metrics.get('total_episodes', 0)}")
    print(f"Mean reward: {metrics.get('mean_reward', 0):.2f}")
    print(f"Last 100 episodes mean reward: {metrics.get('last_100_mean_reward', 0):.2f}")
    
    return model, metrics


def evaluate_dqn(
    model: DQN,
    env: RabiesVaccinationEnv,
    n_eval_episodes: int = 10
) -> Dict:
    """
    Evaluate trained DQN model
    
    Args:
        model: Trained DQN model
        env: Evaluation environment
        n_eval_episodes: Number of episodes to evaluate
        
    Returns:
        Evaluation metrics
    """
    print(f"\nEvaluating model on {n_eval_episodes} episodes...")
    
    mean_reward, std_reward = evaluate_policy(
        model,
        env,
        n_eval_episodes=n_eval_episodes,
        deterministic=True
    )
    
    metrics = {
        'mean_reward': float(mean_reward),
        'std_reward': float(std_reward),
        'n_episodes': n_eval_episodes,
        'success_rate': None  # Can be calculated based on reward threshold
    }
    
    # Calculate success rate (reward > 0 means controlled outbreak)
    episode_rewards = []
    for _ in range(n_eval_episodes):
        obs, _ = env.reset()
        episode_reward = 0
        done = False
        
        while not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, _ = env.step(action)
            episode_reward += reward
            done = terminated or truncated
        
        episode_rewards.append(episode_reward)
    
    success_count = sum(1 for r in episode_rewards if r > 0)
    metrics['success_rate'] = success_count / n_eval_episodes
    metrics['episode_rewards'] = episode_rewards
    
    print(f"Mean reward: {mean_reward:.2f} ± {std_reward:.2f}")
    print(f"Success rate: {metrics['success_rate']*100:.1f}%")
    
    return metrics


def save_model_with_metadata(
    model: DQN,
    save_path: str,
    config: DRLConfig,
    training_metrics: Dict,
    eval_metrics: Dict = None
):
    """
    Save model with metadata
    
    Args:
        model: Trained DQN model
        save_path: Path to save model
        config: Configuration used
        training_metrics: Training metrics
        eval_metrics: Evaluation metrics (optional)
    """
    # Save model
    model.save(save_path)
    print(f"✅ Model saved to: {save_path}.zip")
    
    # Save metadata
    metadata = {
        'model_type': 'DQN',
        'version': '1.0',
        'created_at': datetime.now().isoformat(),
        'config': {
            'learning_rate': config.learning_rate,
            'total_timesteps': config.total_timesteps,
            'batch_size': config.batch_size,
            'gamma': config.gamma,
            'net_arch': config.net_arch,
        },
        'training_metrics': training_metrics,
        'eval_metrics': eval_metrics or {},
    }
    
    metadata_path = f"{save_path}_metadata.json"
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"✅ Metadata saved to: {metadata_path}")


def load_model_with_metadata(
    model_path: str
) -> Tuple[DQN, Dict]:
    """
    Load model with metadata
    
    Args:
        model_path: Path to model (without .zip extension)
        
    Returns:
        Loaded model and metadata
    """
    # Load model
    model = DQN.load(model_path)
    print(f"✅ Model loaded from: {model_path}.zip")
    
    # Load metadata
    metadata_path = f"{model_path}_metadata.json"
    if os.path.exists(metadata_path):
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        print(f"✅ Metadata loaded from: {metadata_path}")
    else:
        metadata = {}
        print(f"⚠️  No metadata found")
    
    return model, metadata


def compare_with_baseline(
    dqn_model: DQN,
    env: RabiesVaccinationEnv,
    n_episodes: int = 10
) -> Dict:
    """
    Compare DQN with rule-based baseline
    
    Args:
        dqn_model: Trained DQN model
        env: Environment
        n_episodes: Number of episodes to compare
        
    Returns:
        Comparison metrics
    """
    print(f"\nComparing DQN vs Rule-Based on {n_episodes} episodes...")
    
    dqn_rewards = []
    baseline_rewards = []
    
    for episode in range(n_episodes):
        # DQN policy
        obs, _ = env.reset()
        dqn_reward = 0
        done = False
        
        while not done:
            action, _ = dqn_model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, _ = env.step(action)
            dqn_reward += reward
            done = terminated or truncated
        
        dqn_rewards.append(dqn_reward)
        
        # Rule-based policy (simple: always vaccinate 70% = action 2)
        obs, _ = env.reset()
        baseline_reward = 0
        done = False
        
        while not done:
            action = 2  # 70% vaccination (action index 2)
            obs, reward, terminated, truncated, _ = env.step(action)
            baseline_reward += reward
            done = terminated or truncated
        
        baseline_rewards.append(baseline_reward)
    
    # Calculate metrics
    dqn_mean = np.mean(dqn_rewards)
    baseline_mean = np.mean(baseline_rewards)
    improvement = ((dqn_mean - baseline_mean) / abs(baseline_mean)) * 100 if baseline_mean != 0 else 0
    
    metrics = {
        'dqn_mean_reward': float(dqn_mean),
        'dqn_std_reward': float(np.std(dqn_rewards)),
        'baseline_mean_reward': float(baseline_mean),
        'baseline_std_reward': float(np.std(baseline_rewards)),
        'improvement_percent': float(improvement),
        'dqn_better': dqn_mean > baseline_mean
    }
    
    print(f"\n📊 Comparison Results:")
    print(f"   DQN Mean Reward: {dqn_mean:.2f} ± {np.std(dqn_rewards):.2f}")
    print(f"   Baseline Mean Reward: {baseline_mean:.2f} ± {np.std(baseline_rewards):.2f}")
    print(f"   Improvement: {improvement:+.1f}%")
    print(f"   DQN is {'BETTER' if metrics['dqn_better'] else 'WORSE'} than baseline")
    
    return metrics


def get_q_values(
    model: DQN,
    observation: np.ndarray
) -> np.ndarray:
    """
    Get Q-values for a given observation
    
    Args:
        model: Trained DQN model
        observation: State observation
        
    Returns:
        Q-values for all actions
    """
    # Get Q-values from model
    obs_tensor = torch.as_tensor(observation).reshape(1, -1).to(model.device)
    with torch.no_grad():
        q_values = model.q_net(obs_tensor)
    
    return q_values.cpu().numpy().flatten()


def explain_decision(
    model: DQN,
    observation: np.ndarray,
    vaccination_levels: List[float] = None,
    feature_names: List[str] = None
) -> Dict:
    """
    Explain DQN's decision for interpretability
    
    Args:
        model: Trained DQN model
        observation: State observation
        vaccination_levels: List of vaccination percentages for each action
        feature_names: Names of state features
        
    Returns:
        Explanation dictionary
    """
    if feature_names is None:
        feature_names = [
            'infection_rate',
            'vaccination_coverage',
            'neighbor_risk',
            'population_density',
            'risk_level',
            'day_progress'
        ]
    
    if vaccination_levels is None:
        vaccination_levels = [0.0, 0.5, 0.7, 0.8, 0.9, 0.95]
    
    # Get action and Q-values
    action, _ = model.predict(observation, deterministic=True)
    q_values = get_q_values(model, observation)
    
    # Get confidence (difference between best and second-best Q-value)
    sorted_q = np.sort(q_values)[::-1]
    confidence = (sorted_q[0] - sorted_q[1]) if len(sorted_q) > 1 else sorted_q[0]
    
    # Map Q-values to vaccination percentages
    q_values_dict = {
        f"{int(vaccination_levels[i]*100)}%": float(q_values[i])
        for i in range(min(len(vaccination_levels), len(q_values)))
    }
    
    explanation = {
        'recommended_action': int(action),
        'recommended_vaccination_pct': float(vaccination_levels[action] * 100),
        'confidence': float(confidence),
        'best_q_value': float(q_values[action]) if action < len(q_values) else 0.0,
        'all_q_values': q_values_dict,
        'state_features': {
            name: float(val) 
            for name, val in zip(feature_names, observation)
        }
    }
    
    return explanation


# =============================================================================
# TESTING
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("DQN Agent Utilities - Test")
    print("=" * 70)
    
    # Create environment
    print("\n[1/3] Creating environment...")
    env = RabiesVaccinationEnv()
    print("   ✅ Environment created")
    
    # Create model
    print("\n[2/3] Creating DQN model...")
    model = create_dqn_model(env)
    print("   ✅ Model created")
    print(f"   Policy: {model.policy}")
    print(f"   Learning rate: {model.learning_rate}")
    print(f"   Buffer size: {model.buffer_size}")
    
    # Test prediction
    print("\n[3/3] Testing prediction...")
    obs, _ = env.reset()
    action, _ = model.predict(obs, deterministic=True)
    vacc_pct = env.discrete_vaccination_levels[action]
    print(f"   ✅ Observation: {obs}")
    print(f"   ✅ Predicted action: {action} ({vacc_pct*100:.0f}% vaccination)")
    
    # Test explanation
    print("\n[4/4] Testing decision explanation...")
    explanation = explain_decision(model, obs, env.discrete_vaccination_levels)
    print(f"   ✅ Recommended vaccination: {explanation['recommended_vaccination_pct']:.1f}%")
    print(f"   ✅ Confidence: {explanation['confidence']:.3f}")
    print(f"   ✅ State features:")
    for name, value in explanation['state_features'].items():
        print(f"      - {name}: {value:.3f}")
    
    print("\n" + "=" * 70)
    print("✅ DQN Agent utilities test completed!")
    print("=" * 70)
