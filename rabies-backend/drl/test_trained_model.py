"""
Test Trained DRL Model Across All Infection Scenarios
Verifies that the model handles 0% to 90% infection rates properly
"""

import numpy as np
from stable_baselines3 import DQN
from environment import RabiesVaccinationEnv
from config import DEFAULT_CONFIG

def test_model_on_scenarios():
    """Test trained model across diverse infection scenarios"""
    
    print("=" * 80)
    print("  Testing Trained DRL Model - Comprehensive Scenario Coverage")
    print("=" * 80)
    print()
    
    # Load model
    model_path = "./drl/models/dqn_rabies_vaccination"
    print(f"📂 Loading model from: {model_path}.zip")
    
    try:
        model = DQN.load(model_path)
        print("✅ Model loaded successfully")
    except FileNotFoundError:
        print("❌ Model not found. Please train the model first:")
        print("   python drl/train_dqn.py")
        return
    
    print()
    
    # Create test scenarios
    vaccination_levels = [0.0, 0.5, 0.7, 0.8, 0.9, 0.95]
    
    scenarios = [
        {"name": "Very Low Infection", "infection_rate": 0.02, "expected_action": [0, 1, 2]},
        {"name": "Low Infection", "infection_rate": 0.08, "expected_action": [1, 2]},
        {"name": "Moderate Infection", "infection_rate": 0.15, "expected_action": [2, 3]},
        {"name": "High Infection", "infection_rate": 0.30, "expected_action": [3, 4]},
        {"name": "Very High Infection", "infection_rate": 0.50, "expected_action": [4, 5]},
        {"name": "Critical Infection", "infection_rate": 0.80, "expected_action": [5]},
    ]
    
    print("Testing model across infection scenarios:")
    print("-" * 80)
    print(f"{'Scenario':<25} {'Infection':<12} {'Recommended':<15} {'Action':<8} {'Status':<10}")
    print("-" * 80)
    
    all_passed = True
    
    for scenario in scenarios:
        infection_rate = scenario["infection_rate"]
        expected_actions = scenario["expected_action"]
        
        # Create observation with this infection rate
        # observation = [infection_rate, vaccination_coverage, neighbor_risk, 
        #                population_density, risk_level_numeric, day_normalized]
        
        vaccination_coverage = 0.3  # 30% current coverage
        neighbor_risk = 0.0
        population_density = 0.6
        
        # Risk level based on infection rate
        if infection_rate >= 0.50:
            risk_level_numeric = 1.0  # critical
        elif infection_rate >= 0.20:
            risk_level_numeric = 0.75  # high
        elif infection_rate >= 0.05:
            risk_level_numeric = 0.5  # moderate
        else:
            risk_level_numeric = 0.25  # low
        
        day_normalized = 0.0
        
        observation = np.array([
            infection_rate,
            vaccination_coverage,
            neighbor_risk,
            population_density,
            risk_level_numeric,
            day_normalized
        ], dtype=np.float32)
        
        # Get model prediction
        action, _ = model.predict(observation, deterministic=True)
        action = int(action)
        vaccination_pct = vaccination_levels[action]
        
        # Check if action is expected
        passed = action in expected_actions
        status = "✅ PASS" if passed else "❌ FAIL"
        
        if not passed:
            all_passed = False
        
        print(f"{scenario['name']:<25} {infection_rate*100:>5.1f}% {vaccination_pct*100:>5.0f}%  {action:<8} {status:<10}")
    
    print("-" * 80)
    print()
    
    if all_passed:
        print("🎉 All tests PASSED! Model handles all scenarios correctly.")
    else:
        print("⚠️  Some tests FAILED. Model may need more training or different hyperparameters.")
    
    print()
    
    # Additional Q-value analysis for critical scenario
    print("=" * 80)
    print("  Detailed Analysis: Critical Infection Scenario (80%)")
    print("=" * 80)
    print()
    
    critical_obs = np.array([0.80, 0.0, 0.0, 0.6, 1.0, 0.0], dtype=np.float32)
    
    # Get Q-values
    import torch
    obs_tensor = torch.as_tensor(critical_obs).reshape(1, -1).to(model.device)
    with torch.no_grad():
        q_values = model.q_net(obs_tensor).cpu().numpy().flatten()
    
    print("State Vector:")
    print(f"  Infection Rate: {critical_obs[0]*100:.1f}%")
    print(f"  Vaccination Coverage: {critical_obs[1]*100:.1f}%")
    print(f"  Risk Level: Critical")
    print()
    
    print("Q-Values (expected utility) for each action:")
    print("-" * 60)
    print(f"{'Action':<10} {'Vaccination':<15} {'Q-Value':<15} {'Selection':<10}")
    print("-" * 60)
    
    best_action = np.argmax(q_values)
    
    for i, (vacc_pct, q_val) in enumerate(zip(vaccination_levels, q_values)):
        selection = "← CHOSEN" if i == best_action else ""
        print(f"{i:<10} {vacc_pct*100:>5.0f}% {q_val:>12.2f}  {selection:<10}")
    
    print("-" * 60)
    print()
    
    if best_action >= 4:  # 90% or 95%
        print("✅ Model correctly chooses high vaccination (90-95%) for critical scenario!")
    else:
        print("❌ Model should choose higher vaccination for 80% infection rate!")
    
    print()
    print("=" * 80)


if __name__ == "__main__":
    test_model_on_scenarios()
