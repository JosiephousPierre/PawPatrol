"""
Test Sub-Phase 2A: Data Structure Updates
Verify that Population and SimulationParameters have been updated correctly
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulation.transmission_model import Population, SimulationParameters


def test_population_structure():
    """Test that Population class has correct fields for SI+V+BD model"""
    print("\n[Test 1] Population structure...")
    
    pop = Population(
        susceptible=1000,
        infected=10,
        vaccinated=200,
        total=1210
    )
    
    # Check SI+V fields exist
    assert hasattr(pop, 'susceptible'), "Missing susceptible"
    assert hasattr(pop, 'infected'), "Missing infected"
    assert hasattr(pop, 'vaccinated'), "Missing vaccinated"
    assert hasattr(pop, 'total'), "Missing total"
    
    # Check tracking fields exist
    assert hasattr(pop, 'cumulative_births'), "Missing cumulative_births"
    assert hasattr(pop, 'cumulative_natural_deaths'), "Missing cumulative_natural_deaths"
    assert hasattr(pop, 'cumulative_rabies_deaths'), "Missing cumulative_rabies_deaths"
    assert hasattr(pop, 'cumulative_vaccinations'), "Missing cumulative_vaccinations"
    
    # Check defaults
    assert pop.cumulative_births == 0.0, "Birth tracking not initialized"
    assert pop.cumulative_natural_deaths == 0.0, "Natural death tracking not initialized"
    
    print("   ✅ Population structure correct!")
    print(f"      S={pop.susceptible}, I={pop.infected}, V={pop.vaccinated}")
    print(f"      Tracking: births={pop.cumulative_births}, deaths={pop.cumulative_natural_deaths}")


def test_simulation_parameters():
    """Test that SimulationParameters has Phase 1 parameters"""
    print("\n[Test 2] SimulationParameters...")
    
    params = SimulationParameters()
    
    # Check birth rates
    assert hasattr(params, 'lambda_dog'), "Missing lambda_dog"
    assert hasattr(params, 'lambda_cat'), "Missing lambda_cat"
    assert hasattr(params, 'lambda_human'), "Missing lambda_human"
    assert params.lambda_dog == 0.0001, "lambda_dog default incorrect"
    
    # Check natural mortality
    assert hasattr(params, 'mu_dog'), "Missing mu_dog"
    assert hasattr(params, 'mu_cat'), "Missing mu_cat"
    assert hasattr(params, 'mu_human'), "Missing mu_human"
    assert params.mu_dog == 0.0001, "mu_dog default incorrect"
    
    # Check rabies mortality
    assert hasattr(params, 'delta_dog'), "Missing delta_dog"
    assert hasattr(params, 'delta_cat'), "Missing delta_cat"
    assert hasattr(params, 'delta_human'), "Missing delta_human"
    assert params.delta_dog == 0.1, "delta_dog default incorrect"
    
    # Check stochastic intensities
    assert hasattr(params, 'sigma_1'), "Missing sigma_1"
    assert hasattr(params, 'sigma_2'), "Missing sigma_2"
    assert hasattr(params, 'sigma_3'), "Missing sigma_3"
    assert params.sigma_1 == 0.1, "sigma_1 default incorrect"
    
    # Check transmission coefficients
    assert hasattr(params, 'beta_dd'), "Missing beta_dd"
    assert hasattr(params, 'beta_dc'), "Missing beta_dc"
    assert hasattr(params, 'beta_cc'), "Missing beta_cc"
    assert hasattr(params, 'beta_dh'), "Missing beta_dh"
    assert hasattr(params, 'beta_ch'), "Missing beta_ch"
    assert params.beta_dd == 0.15, "beta_dd default incorrect"
    assert params.beta_dc == 0.06, "beta_dc default incorrect"
    
    print("   ✅ SimulationParameters complete!")
    print(f"      Birth rates: λ_d={params.lambda_dog}, λ_c={params.lambda_cat}")
    print(f"      Mortality: μ_d={params.mu_dog}, δ_d={params.delta_dog}")
    print(f"      Stochastic: σ₁={params.sigma_1}, σ₂={params.sigma_2}, σ₃={params.sigma_3}")
    print(f"      Transmission: β_dd={params.beta_dd}, β_dc={params.beta_dc}, β_cc={params.beta_cc}")


def test_custom_parameters():
    """Test creating parameters with custom values"""
    print("\n[Test 3] Custom parameter values...")
    
    params = SimulationParameters(
        lambda_dog=0.0002,
        mu_dog=0.0003,
        delta_dog=0.15,
        sigma_1=0.12,
        beta_dd=0.18
    )
    
    assert params.lambda_dog == 0.0002, "Custom lambda_dog not set"
    assert params.mu_dog == 0.0003, "Custom mu_dog not set"
    assert params.delta_dog == 0.15, "Custom delta_dog not set"
    assert params.sigma_1 == 0.12, "Custom sigma_1 not set"
    assert params.beta_dd == 0.18, "Custom beta_dd not set"
    
    print("   ✅ Custom parameters work!")
    print(f"      Custom values accepted: λ={params.lambda_dog}, β_dd={params.beta_dd}")


if __name__ == "__main__":
    print("=" * 70)
    print("SUB-PHASE 2A TESTING: Data Structure Updates")
    print("=" * 70)
    
    try:
        test_population_structure()
        test_simulation_parameters()
        test_custom_parameters()
        
        print("\n" + "=" * 70)
        print("✅ SUB-PHASE 2A COMPLETE!")
        print("=" * 70)
        print("\n📊 Summary:")
        print("  ✅ Population class updated (SI+V model)")
        print("  ✅ Birth/death tracking added")
        print("  ✅ SimulationParameters has all 14 new parameters")
        print("  ✅ Default values correct")
        print("  ✅ Custom values work")
        print("\n🎉 Ready for Sub-Phase 2B: Helper Functions!")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
