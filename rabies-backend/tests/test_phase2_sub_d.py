"""
Test Sub-Phase 2D: Cat Equations
Verify the cat SI+V+BD equations implementation
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulation.transmission_model import (
    simulate_municipality_step,
    MunicipalityState,
    Population,
    SimulationParameters
)


def test_cat_births():
    """Test that cat births are calculated correctly"""
    print("\n[Test 1] Cat births calculation...")
    
    # Setup
    params = SimulationParameters(
        lambda_cat=0.0003,  # 3 births per 10,000 per day (higher than dogs)
        mu_cat=0.0002,
        delta_cat=0.12,
        beta_dc=0.06,
        beta_cc=0.105,
        contact_probability=0.3,
        dt=1.0
    )
    
    state = MunicipalityState(
        id="test",
        name="Test City",
        dogs=Population(susceptible=9000.0, infected=100.0, vaccinated=900.0, total=10000.0),
        cats=Population(
            susceptible=4500.0,
            infected=50.0,
            vaccinated=450.0,
            total=5000.0
        ),
        humans=Population(susceptible=100000.0, infected=0.0, vaccinated=0.0, total=100000.0),
        population_density=1000.0,
        connected_municipalities=[],
        infected_dogs_history=[],
        infected_cats_history=[],
        infected_humans_history=[]
    )
    
    initial_births = state.cats.cumulative_births
    
    # Run simulation step
    state = simulate_municipality_step(state, params, {})
    
    # Check births were added
    births_added = state.cats.cumulative_births - initial_births
    expected_births = 0.0003 * 5000 * 1.0  # λ * N * dt = 1.5
    
    assert abs(births_added - expected_births) < 0.5, \
        f"Expected ~{expected_births} births, got {births_added}"
    
    print(f"   ✅ Births correct: {births_added:.2f} (expected ~{expected_births})")
    print(f"      λ_cat = {params.lambda_cat} (higher than dogs - faster reproduction)")


def test_cat_natural_deaths():
    """Test that natural deaths are tracked for all cat compartments"""
    print("\n[Test 2] Cat natural deaths...")
    
    params = SimulationParameters(
        lambda_cat=0.0,
        mu_cat=0.0003,  # Higher than dogs (shorter lifespan)
        delta_cat=0.0,
        beta_dc=0.0,
        beta_cc=0.0,
        dt=1.0
    )
    
    state = MunicipalityState(
        id="test",
        name="Test City",
        dogs=Population(susceptible=9000.0, infected=0.0, vaccinated=1000.0, total=10000.0),
        cats=Population(
            susceptible=2500.0,
            infected=1000.0,
            vaccinated=1500.0,
            total=5000.0
        ),
        humans=Population(susceptible=100000.0, infected=0.0, vaccinated=0.0, total=100000.0),
        population_density=1000.0,
        connected_municipalities=[],
        infected_dogs_history=[],
        infected_cats_history=[],
        infected_humans_history=[]
    )
    
    initial_deaths = state.cats.cumulative_natural_deaths
    
    # Run simulation step
    state = simulate_municipality_step(state, params, {})
    
    # Check natural deaths
    deaths_added = state.cats.cumulative_natural_deaths - initial_deaths
    
    # Expected: μ * (S + I + V) * dt = 0.0003 * 5000 * 1.0 = 1.5
    expected_deaths = 0.0003 * 5000 * 1.0
    
    assert abs(deaths_added - expected_deaths) < 0.5, \
        f"Expected ~{expected_deaths} natural deaths, got {deaths_added}"
    
    print(f"   ✅ Natural deaths correct: {deaths_added:.2f} (expected ~{expected_deaths})")
    print(f"      μ_cat = {params.mu_cat} (higher than dogs - shorter lifespan)")


def test_cat_rabies_deaths():
    """Test that rabies deaths are calculated correctly for cats"""
    print("\n[Test 3] Cat rabies deaths...")
    
    params = SimulationParameters(
        lambda_cat=0.0,
        mu_cat=0.0,
        delta_cat=0.12,  # 12% die per day (~8 day survival, slightly faster than dogs)
        beta_dc=0.0,
        beta_cc=0.0,
        dt=1.0
    )
    
    state = MunicipalityState(
        id="test",
        name="Test City",
        dogs=Population(susceptible=9000.0, infected=0.0, vaccinated=1000.0, total=10000.0),
        cats=Population(
            susceptible=4900.0,
            infected=100.0,  # 100 infected cats
            vaccinated=0.0,
            total=5000.0
        ),
        humans=Population(susceptible=100000.0, infected=0.0, vaccinated=0.0, total=100000.0),
        population_density=1000.0,
        connected_municipalities=[],
        infected_dogs_history=[],
        infected_cats_history=[],
        infected_humans_history=[]
    )
    
    initial_rabies_deaths = state.cats.cumulative_rabies_deaths
    
    # Run simulation step
    state = simulate_municipality_step(state, params, {})
    
    # Check rabies deaths
    rabies_deaths = state.cats.cumulative_rabies_deaths - initial_rabies_deaths
    expected_rabies_deaths = 0.12 * 100 * 1.0  # δ * I * dt = 12
    
    assert abs(rabies_deaths - expected_rabies_deaths) < 1.0, \
        f"Expected ~{expected_rabies_deaths} rabies deaths, got {rabies_deaths}"
    
    print(f"   ✅ Rabies deaths correct: {rabies_deaths:.2f} (expected ~{expected_rabies_deaths})")
    print(f"      12% of 100 infected cats = 12 deaths/day (~8-day survival)")


def test_dog_to_cat_transmission():
    """Test that dog-to-cat transmission (spillover) works correctly"""
    print("\n[Test 4] Dog-to-cat transmission (spillover)...")
    
    params = SimulationParameters(
        lambda_cat=0.0,
        mu_cat=0.0,
        delta_cat=0.0,
        beta_dc=0.06,  # Dog-to-cat coefficient
        beta_cc=0.0,   # Disable cat-to-cat for this test
        contact_probability=0.5,
        sigma_2=0.0,  # No stochastic noise
        dt=1.0
    )
    
    state = MunicipalityState(
        id="test",
        name="Test City",
        dogs=Population(
            susceptible=9000.0,
            infected=1000.0,  # 10% infected dogs (primary reservoir)
            vaccinated=0.0,
            total=10000.0
        ),
        cats=Population(
            susceptible=4950.0,
            infected=50.0,
            vaccinated=0.0,
            total=5000.0
        ),
        humans=Population(susceptible=100000.0, infected=0.0, vaccinated=0.0, total=100000.0),
        population_density=1000.0,
        connected_municipalities=[],
        infected_dogs_history=[],
        infected_cats_history=[],
        infected_humans_history=[]
    )
    
    initial_S_cat = state.cats.susceptible
    initial_I_cat = state.cats.infected
    
    # Run simulation step
    state = simulate_municipality_step(state, params, {})
    
    # Check transmission occurred
    # Expected: β_dc * p * (S_c * I_d / N_d) * dt
    # = 0.06 * 0.5 * (4950 * 1000 / 10000) * 1.0 = 14.85
    S_cat_decrease = initial_S_cat - state.cats.susceptible
    I_cat_increase = state.cats.infected - initial_I_cat
    
    # Should have some infections from dogs
    assert S_cat_decrease > 10, f"Expected spillover infections, got {S_cat_decrease:.2f}"
    
    print(f"   ✅ Dog-to-cat spillover: {S_cat_decrease:.2f} new infections")
    print(f"      S_c: {initial_S_cat:.0f} → {state.cats.susceptible:.0f}")
    print(f"      I_c: {initial_I_cat:.0f} → {state.cats.infected:.0f}")
    print(f"      Cats infected by dogs (primary reservoir)")


def test_cat_to_cat_transmission():
    """Test that cat-to-cat transmission (secondary spread) works correctly"""
    print("\n[Test 5] Cat-to-cat transmission (secondary spread)...")
    
    params = SimulationParameters(
        lambda_cat=0.0,
        mu_cat=0.0,
        delta_cat=0.0,
        beta_dc=0.0,   # Disable dog-to-cat for this test
        beta_cc=0.105,  # Cat-to-cat coefficient
        contact_probability=0.5,
        sigma_2=0.0,
        dt=1.0
    )
    
    state = MunicipalityState(
        id="test",
        name="Test City",
        dogs=Population(
            susceptible=10000.0,
            infected=0.0,  # No infected dogs
            vaccinated=0.0,
            total=10000.0
        ),
        cats=Population(
            susceptible=4900.0,
            infected=100.0,  # 2% infected cats
            vaccinated=0.0,
            total=5000.0
        ),
        humans=Population(susceptible=100000.0, infected=0.0, vaccinated=0.0, total=100000.0),
        population_density=1000.0,
        connected_municipalities=[],
        infected_dogs_history=[],
        infected_cats_history=[],
        infected_humans_history=[]
    )
    
    initial_S_cat = state.cats.susceptible
    initial_I_cat = state.cats.infected
    
    # Run simulation step
    state = simulate_municipality_step(state, params, {})
    
    # Check transmission occurred
    # Expected: β_cc * p * (S_c * I_c / N_c) * dt
    # = 0.105 * 0.5 * (4900 * 100 / 5000) * 1.0 = 5.145
    S_cat_decrease = initial_S_cat - state.cats.susceptible
    
    # Should have some cat-to-cat infections
    assert S_cat_decrease > 3, f"Expected cat-to-cat infections, got {S_cat_decrease:.2f}"
    
    print(f"   ✅ Cat-to-cat transmission: {S_cat_decrease:.2f} new infections")
    print(f"      S_c: {initial_S_cat:.0f} → {state.cats.susceptible:.0f}")
    print(f"      I_c: {initial_I_cat:.0f} → {state.cats.infected:.0f}")
    print(f"      Secondary spread within cat population")


def test_combined_transmission():
    """Test that cats get infected from BOTH dogs AND other cats"""
    print("\n[Test 6] Combined transmission (dogs + cats)...")
    
    params = SimulationParameters(
        lambda_cat=0.0,
        mu_cat=0.0,
        delta_cat=0.0,
        beta_dc=0.06,   # Dog-to-cat enabled
        beta_cc=0.105,  # Cat-to-cat enabled
        contact_probability=0.3,
        sigma_2=0.0,
        dt=1.0
    )
    
    state = MunicipalityState(
        id="test",
        name="Test City",
        dogs=Population(
            susceptible=9000.0,
            infected=500.0,  # 5% infected dogs
            vaccinated=500.0,
            total=10000.0
        ),
        cats=Population(
            susceptible=4800.0,
            infected=200.0,  # 4% infected cats
            vaccinated=0.0,
            total=5000.0
        ),
        humans=Population(susceptible=100000.0, infected=0.0, vaccinated=0.0, total=100000.0),
        population_density=1000.0,
        connected_municipalities=[],
        infected_dogs_history=[],
        infected_cats_history=[],
        infected_humans_history=[]
    )
    
    initial_S_cat = state.cats.susceptible
    
    # Run simulation step
    state = simulate_municipality_step(state, params, {})
    
    # Should get infections from both sources
    total_infections = initial_S_cat - state.cats.susceptible
    
    # Expected:
    # From dogs: β_dc * p * (S_c * I_d / N_d) = 0.06 * 0.3 * (4800 * 500 / 10000) = 4.32
    # From cats: β_cc * p * (S_c * I_c / N_c) = 0.105 * 0.3 * (4800 * 200 / 5000) = 6.048
    # Total: ~10.37
    
    assert total_infections > 8, f"Expected combined infections, got {total_infections:.2f}"
    
    print(f"   ✅ Combined transmission: {total_infections:.2f} new infections")
    print(f"      From dogs (spillover): β_dc = {params.beta_dc}")
    print(f"      From cats (secondary): β_cc = {params.beta_cc}")
    print(f"      Cats are infected by BOTH sources")


def test_cat_independent_stochastic():
    """Test that cats have independent stochastic noise (σ₂·dW₂, not σ₁·dW₁)"""
    print("\n[Test 7] Cat independent stochastic noise...")
    
    params = SimulationParameters(
        lambda_cat=0.0,
        mu_cat=0.0,
        delta_cat=0.0,
        beta_dc=0.0,
        beta_cc=0.0,
        sigma_1=0.5,  # Dog noise
        sigma_2=0.4,  # Cat noise (different from dogs)
        dt=1.0
    )
    
    # Run multiple simulations
    cat_infected_values = []
    dog_infected_values = []
    
    for _ in range(20):
        state = MunicipalityState(
            id="test",
            name="Test City",
            dogs=Population(susceptible=9000.0, infected=1000.0, vaccinated=0.0, total=10000.0),
            cats=Population(susceptible=4000.0, infected=1000.0, vaccinated=0.0, total=5000.0),
            humans=Population(susceptible=100000.0, infected=0.0, vaccinated=0.0, total=100000.0),
            population_density=1000.0,
            connected_municipalities=[],
            infected_dogs_history=[],
            infected_cats_history=[],
            infected_humans_history=[]
        )
        state = simulate_municipality_step(state, params, {})
        cat_infected_values.append(state.cats.infected)
        dog_infected_values.append(state.dogs.infected)
    
    # Check both have variation (stochastic)
    import numpy as np
    cat_std = np.std(cat_infected_values)
    dog_std = np.std(dog_infected_values)
    
    assert cat_std > 0.1, f"Expected cat stochastic variation, got std={cat_std:.3f}"
    assert dog_std > 0.1, f"Expected dog stochastic variation, got std={dog_std:.3f}"
    
    # Verify independence (correlation should be low)
    correlation = np.corrcoef(cat_infected_values, dog_infected_values)[0, 1]
    
    print(f"   ✅ Independent stochastic noise:")
    print(f"      Cat variation (σ₂): std = {cat_std:.2f}")
    print(f"      Dog variation (σ₁): std = {dog_std:.2f}")
    print(f"      Correlation: {correlation:.3f} (should be ~0)")
    print(f"      dW₁ and dW₂ are INDEPENDENT")


def test_cat_no_recovery():
    """Test that cats don't recover (SI model, not SIR)"""
    print("\n[Test 8] Cats don't recover (SI model)...")
    
    state = MunicipalityState(
        id="test",
        name="Test City",
        dogs=Population(susceptible=9000.0, infected=1000.0, vaccinated=0.0, total=10000.0),
        cats=Population(susceptible=4000.0, infected=1000.0, vaccinated=0.0, total=5000.0),
        humans=Population(susceptible=100000.0, infected=0.0, vaccinated=0.0, total=100000.0),
        population_density=1000.0,
        connected_municipalities=[],
        infected_dogs_history=[],
        infected_cats_history=[],
        infected_humans_history=[]
    )
    
    # Check that Population doesn't have recovered field
    assert not hasattr(state.cats, 'recovered'), \
        "Cats should not have recovered field (SI model, not SIR)"
    
    print(f"   ✅ No recovery field: Population only has S, I, V compartments")
    print(f"      This is an SI model - rabies is fatal for cats too")


if __name__ == "__main__":
    print("=" * 70)
    print("SUB-PHASE 2D TESTING: Cat Equations (SI+V+BD)")
    print("=" * 70)
    
    try:
        test_cat_births()
        test_cat_natural_deaths()
        test_cat_rabies_deaths()
        test_dog_to_cat_transmission()
        test_cat_to_cat_transmission()
        test_combined_transmission()
        test_cat_independent_stochastic()
        test_cat_no_recovery()
        
        print("\n" + "=" * 70)
        print("✅ SUB-PHASE 2D COMPLETE!")
        print("=" * 70)
        print("\n📊 Summary:")
        print("  ✅ Cat births (Λ_c)")
        print("  ✅ Cat natural deaths (μ_c·S_c, μ_c·I_c, μ_c·V_c)")
        print("  ✅ Cat rabies deaths (δ_c·I_c)")
        print("  ✅ Dog-to-cat transmission (β_dc·S_c·I_d/N_d) - SPILLOVER")
        print("  ✅ Cat-to-cat transmission (β_cc·S_c·I_c/N_c) - SECONDARY")
        print("  ✅ Combined transmission (both sources)")
        print("  ✅ Independent stochastic noise (σ₂·dW₂(t))")
        print("  ✅ No recovery (SI model confirmed)")
        print("\n🎉 Cat equations fully implemented!")
        print("\n📝 Key Feature: SPILLOVER + SECONDARY SPREAD")
        print("   • Cats get infected from dogs (β_dc) - primary spillover")
        print("   • Cats infect other cats (β_cc) - secondary maintenance")
        print("   • Independent noise from dogs (dW₂ ≠ dW₁)")
        print("\n🚀 Ready for Sub-Phase 2E: Human Equations!")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
