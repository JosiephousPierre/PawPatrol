"""
DQN Training Script for Rabies Vaccination Optimization
Trains a Deep Q-Network to learn optimal vaccination strategies

Usage:
    python drl/train_dqn.py                    # Default training
    python drl/train_dqn.py --fast             # Fast training (10K steps)
    python drl/train_dqn.py --extended         # Extended training (500K steps)
    python drl/train_dqn.py --timesteps 50000  # Custom timesteps

Author: PAWPATROL Research Team
Date: October 2026
"""

import argparse
import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from drl.environment import RabiesVaccinationEnv
    from drl.dqn_agent import (
        create_dqn_model,
        train_dqn,
        evaluate_dqn,
        compare_with_baseline,
        save_model_with_metadata
    )
    from drl.config import get_config, DRLConfig
except ImportError:
    from environment import RabiesVaccinationEnv
    from dqn_agent import (
        create_dqn_model,
        train_dqn,
        evaluate_dqn,
        compare_with_baseline,
        save_model_with_metadata
    )
    from config import get_config, DRLConfig


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Train DQN for Rabies Vaccination Optimization'
    )
    
    parser.add_argument(
        '--preset',
        type=str,
        default='standard',
        choices=['fast', 'standard', 'extended'],
        help='Training preset: fast (10K), standard (100K), extended (500K)'
    )
    
    parser.add_argument(
        '--timesteps',
        type=int,
        default=None,
        help='Custom number of training timesteps'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default='./drl/models/dqn_rabies_vaccination',
        help='Output path for trained model'
    )
    
    parser.add_argument(
        '--eval-episodes',
        type=int,
        default=10,
        help='Number of episodes for evaluation'
    )
    
    parser.add_argument(
        '--no-comparison',
        action='store_true',
        help='Skip baseline comparison'
    )
    
    parser.add_argument(
        '--continue-training',
        type=str,
        default=None,
        help='Path to existing model to continue training'
    )
    
    return parser.parse_args()


def print_header():
    """Print training header"""
    print("=" * 70)
    print("  PAWPATROL - DQN Training for Vaccination Optimization")
    print("=" * 70)
    print()


def print_config_info(config: DRLConfig):
    """Print configuration information"""
    print("📊 Training Configuration:")
    print(f"  Total Timesteps: {config.total_timesteps:,}")
    print(f"  Learning Rate: {config.learning_rate}")
    print(f"  Batch Size: {config.batch_size}")
    print(f"  Gamma (Discount): {config.gamma}")
    print(f"  Buffer Size: {config.buffer_size:,}")
    print(f"  Network Architecture: {config.net_arch}")
    print()
    
    print("🎮 Environment:")
    print(f"  Simulation Days: {config.simulation_days}")
    print(f"  State Features: {len(config.state_features)}")
    print(f"  Actions: 6 discrete levels [0%, 50%, 70%, 80%, 90%, 95%]")
    print()
    
    print("💰 Reward Weights:")
    print(f"  Infection Penalty: {config.infection_penalty}")
    print(f"  Cost Penalty: {config.cost_penalty}")
    print(f"  Human Infection Penalty: {config.human_infection_penalty}")
    print(f"  Control Bonus: {config.outbreak_control_bonus}")
    print()


def create_dummy_municipalities():
    """Create dummy municipalities for training"""
    return [
        {
            'id': '1',
            'name': 'Maco',
            'humanPopulation': 75033,
            'dogPopulation': 3000,
            'catPopulation': 1500,
            'infectedDogs': 15,
            'infectedCats': 3,
            'infectedHumans': 0,
            'vaccinatedDogs': 900,
            'populationDensity': 295.2,
            'latitude': 7.3667,
            'longitude': 126.0167,
            'riskLevel': 'moderate',
            'connectedMunicipalities': ['2', '3']
        },
        {
            'id': '2',
            'name': 'Mawab',
            'humanPopulation': 36418,
            'dogPopulation': 1500,
            'catPopulation': 750,
            'infectedDogs': 8,
            'infectedCats': 2,
            'infectedHumans': 0,
            'vaccinatedDogs': 450,
            'populationDensity': 212.5,
            'latitude': 7.5167,
            'longitude': 125.9667,
            'riskLevel': 'low',
            'connectedMunicipalities': ['1', '3']
        },
        {
            'id': '3',
            'name': 'Maragusan',
            'humanPopulation': 58367,
            'dogPopulation': 2500,
            'catPopulation': 1200,
            'infectedDogs': 20,
            'infectedCats': 5,
            'infectedHumans': 0,
            'vaccinatedDogs': 750,
            'populationDensity': 48.2,
            'latitude': 7.3,
            'longitude': 126.15,
            'riskLevel': 'high',
            'connectedMunicipalities': ['1', '2']
        }
    ]


def main():
    """Main training function"""
    # Parse arguments
    args = parse_args()
    
    # Print header
    print_header()
    
    # Load configuration
    print("⚙️  Loading configuration...")
    config = get_config(args.preset)
    
    # Override timesteps if specified
    if args.timesteps is not None:
        config.total_timesteps = args.timesteps
        print(f"  Custom timesteps: {args.timesteps:,}")
    
    print_config_info(config)
    
    # Create environment
    print("🎮 Creating training environment...")
    municipalities = create_dummy_municipalities()
    env = RabiesVaccinationEnv(
        municipalities_data=municipalities,
        config=config,
        single_municipality_mode=True
    )
    print(f"  ✅ Environment created")
    print(f"  Observation space: {env.observation_space}")
    print(f"  Action space: {env.action_space}")
    print()
    
    # Create or load model
    model = None
    if args.continue_training:
        print(f"📂 Loading existing model from {args.continue_training}...")
        from stable_baselines3 import DQN
        model = DQN.load(args.continue_training, env=env)
        print("  ✅ Model loaded, continuing training")
    else:
        print("🤖 Creating new DQN model...")
        model = create_dqn_model(env, config)
        print("  ✅ Model created")
    
    print()
    print("=" * 70)
    print("  🚀 STARTING TRAINING")
    print("=" * 70)
    print()
    
    # Estimate time
    if config.total_timesteps <= 10000:
        est_time = "~2-5 minutes"
    elif config.total_timesteps <= 100000:
        est_time = "~10-15 minutes"
    else:
        est_time = "~45-60 minutes"
    
    print(f"⏱️  Estimated time: {est_time}")
    print(f"📊 Progress will be logged every {config.log_interval} steps")
    print()
    print("Training started at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print()
    
    # Train model
    try:
        model, training_metrics = train_dqn(env, config, model)
    except KeyboardInterrupt:
        print("\n\n⚠️  Training interrupted by user")
        print("Saving current model state...")
        model.save(args.output + "_interrupted")
        print(f"Model saved to: {args.output}_interrupted.zip")
        return
    
    print()
    print("Training completed at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print()
    
    # Evaluate model
    print("=" * 70)
    print("  📊 EVALUATING MODEL")
    print("=" * 70)
    print()
    
    eval_metrics = evaluate_dqn(model, env, n_eval_episodes=args.eval_episodes)
    
    print()
    print("Evaluation Results:")
    print(f"  Mean Reward: {eval_metrics['mean_reward']:.2f} ± {eval_metrics['std_reward']:.2f}")
    print(f"  Success Rate: {eval_metrics['success_rate']*100:.1f}%")
    print()
    
    # Compare with baseline
    if not args.no_comparison:
        print("=" * 70)
        print("  🔬 COMPARING WITH BASELINE")
        print("=" * 70)
        print()
        
        comparison = compare_with_baseline(model, env, n_episodes=args.eval_episodes)
        
        print()
    
    # Save model
    print("=" * 70)
    print("  💾 SAVING MODEL")
    print("=" * 70)
    print()
    
    save_model_with_metadata(
        model=model,
        save_path=args.output,
        config=config,
        training_metrics=training_metrics,
        eval_metrics=eval_metrics
    )
    
    print()
    
    # Final summary
    print("=" * 70)
    print("  ✅ TRAINING COMPLETE!")
    print("=" * 70)
    print()
    print("📊 Summary:")
    print(f"  Total Episodes: {training_metrics.get('total_episodes', 'N/A')}")
    print(f"  Total Steps: {training_metrics.get('total_steps', 'N/A'):,}")
    print(f"  Mean Reward: {training_metrics.get('mean_reward', 0):.2f}")
    print(f"  Last 100 Episodes: {training_metrics.get('last_100_mean_reward', 0):.2f}")
    print(f"  Evaluation Success Rate: {eval_metrics['success_rate']*100:.1f}%")
    
    if not args.no_comparison:
        improvement = comparison.get('improvement_percent', 0)
        print(f"  Improvement vs Baseline: {improvement:+.1f}%")
        if comparison.get('dqn_better'):
            print("  🏆 DQN outperforms rule-based baseline!")
        else:
            print("  ⚠️  DQN needs more training")
    
    print()
    print(f"📁 Model saved to: {args.output}.zip")
    print(f"📁 Metadata saved to: {args.output}_metadata.json")
    print()
    
    # Next steps
    print("🎯 Next Steps:")
    print("  1. View training logs: tensorboard --logdir=./drl/logs/tensorboard")
    print(f"  2. Load model: model = DQN.load('{args.output}')")
    print("  3. Use for inference: action, _ = model.predict(observation)")
    print()
    print("=" * 70)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print()
        print("=" * 70)
        print("  ❌ ERROR DURING TRAINING")
        print("=" * 70)
        print()
        print(f"Error: {e}")
        print()
        print("Troubleshooting:")
        print("  1. Check that all dependencies are installed: pip install -r requirements.txt")
        print("  2. Verify environment works: python drl/environment.py")
        print("  3. Check available memory (training needs ~2-4 GB RAM)")
        print()
        import traceback
        print("Full traceback:")
        traceback.print_exc()
        sys.exit(1)
