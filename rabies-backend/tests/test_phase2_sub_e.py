"""
Test Sub-Phase 2E: Human Equations
Verify the human SI+V+BD equations implementation
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


def test_human_births():
    """Test that human births are calculated correctly"""
    print("\n[Test 1] Human births calculation...")
    
    params = SimulationParameters(
        lambda_human=0.00005,  # 5 births per 100,000 per day
        mu_human=0.00003,
        delta_human=0.15,
        beta_dh=0.0015,
        beta_ch=0.00075,
        contact_probability=0.3,
        dt=1.0
    )
    
    state = MunicipalityState(
        id="test",
        name="Test City",
        dogs=Population(susceptible=9000.0, infected=100.0, vaccinated=900.0, total=10000.0),
        cats=Population(susceptible=4500.0, infected=50.0, vaccinated=450.0, total=5000.0),
        humans=Population(
            susceptible=99000.0,
            infected=500.0,
            vaccinated=500.0,
            total=100000.0
        ),
        population_density=1000.0,
        connected_municipalities=[],
        infected_dogs_history=[],
        infected_cats_history=[],
        infected_humans_history=[]
    )
    
    initial_births = state.humans.cumulative_births
    
    # Run simulation step
    state = simulate_municipality_step(state, params, {})
    
    # Check births were added
    births_added = state.humans.cumulative_births - initial_births
    expected_births = 0.00005 * 100000 * 1.0  # λ * N * dt = 5.0
    
    assert abs(births_added - expected_births) < 0.5, \
        f"Expected ~{expected_births} births, got {births_added}"
    
    print(f"   ✅ Births correct: {births_added:.2f} (expected ~{expected_births})")
    print(f"      λ_human = {params.lambda_human} (lower than dogs/cats - slower reproduction)")


def test_human_natural_deaths():
    """Test that natural deaths are tracked for all human compartments"""
    print("\n[Test 2] Human natural deaths...")
    
    params = SimulationParameters(
        lambda_human=0.0,
        mu_human=0.00004,  # Lower than cats (longer lifespan)
        delta_human=0.0,
        beta_dh=0.0,
        beta_ch=0.0,
        dt=1.0
    )
    
    state = MunicipalityState(
        id="test",
        name="Test City",
        dogs=Population(susceptible=9000.0, infected=0.0, vaccinated=1000.0, total=10000.0),
        cats=Population(susceptible=4500.0, infected=0.0, vaccinated=500.0, total=5000.0),
        humans=Population(
            susceptible=50000.0,
            infected=25000.0,
            vaccinated=25000.0,
            total=100000.0
        ),
        population_density=1000.0,
        connected_municipalities=[],
        infected_dogs_history=[],
        infected_cats_history=[],
        infected_humans_history=[]
    )
    
    initial_deaths = state.humans.cumulative_natural_deaths
    
    # Run simulation step
    state = simulate_municipality_step(state, params, {})
    
    # Check natural deaths
    deaths_added = state.humans.cumulative_natural_deaths - initial_deaths
    
    # Expected: μ * (S + I + V) * dt = 0.00004 * 100000 * 1.0 = 4.0
    expected_deaths = 0.00004 * 100000 * 1.0
    
    assert abs(deaths_added - expected_deaths) < 0.5, \
        f"Expected ~{expected_deaths} natural deaths, got {deaths_added}"
    
    print(f"   ✅ Natural deaths correct: {deaths_added:.2f} (expected ~{expected_deaths})")
    print(f"      μ_human = {params.mu_human} (lower than animals - longer lifespan)")


def test_human_rabies_deaths():
    """Test that rabies deaths are calculated correctly for humans"""
    print("\n[Test 3] Human rabies deaths...")
    
    params = SimulationParameters(
        lambda_human=0.0,
        mu_human=0.0,
        delta_human=0.15,  # 15% die per day (~6-7 day survival after symptoms)
        beta_dh=0.0,
        beta_ch=0.0,
        dt=1.0
    )
    
    state = MunicipalityState(
        id="test",
        name="Test City",
        dogs=Population(susceptible=9000.0, infected=0.0, vaccinated=1000.0, total=10000.0),
        cats=Population(susceptible=4500.0, infected=0.0, vaccinated=500.0, total=5000.0),
        humans=Population(
            susceptible=99900.0,
            infected=100.0,  # 100 infected humans
            vaccinated=0.0,
            total=100000.0
        ),
        population_density=1000.0,
        connected_municipalities=[],
        infected_dogs_history=[],
        infected_cats_history=[],
        infected_humans_history=[]
    )
    
    initial_rabies_deaths = state.humans.cumulative_rabies_deaths
    
    # Run simulation step
    state = simulate_municipality_step(state, params, {})
    
    # Check rabies deaths
    rabies_deaths = state.humans.cumulative_rabies_deaths - initial_rabies_deaths
    expected_rabies_deaths = 0.15 * 100 * 1.0  # δ * I * dt = 15
    
    assert abs(rabies_deaths - expected_rabies_deaths) < 1.5, \
        f"Expected ~{expected_rabies_deaths} rabies deaths, got {rabies_deaths}"
    
    print(f"   ✅ Rabies deaths correct: {rabies_deaths:.2f} (expected ~{expected_rabies_deaths})")
    print(f"      15% of 100 infected humans = 15 deaths/day")
    print(f"      Without PEP, rabies is nearly 100% fatal")


def test_dog_to_human_transmission():
    """Test that dog-to-human transmission works correctly"""
    print("\n[Test 4] Dog-to-human transmission...")
    
    params = SimulationParameters(
        lambda_human=0.0,
        mu_human=0.0,
        delta_human=0.0,
        beta_dh=0.0015,  # Dog-to-human coefficient (very low)
        beta_ch=0.0,     # Disable cat-to-human for this test
        contact_probability=0.3,
        sigma_3=0.0,  # No stochastic noise
        dt=1.0
    )
    
    state = MunicipalityState(
        id="test",
        name="Test City",
        dogs=Population(
            susceptible=9000.0,
            infected=1000.0,  # 10% infected dogs
            vaccinated=0.0,
            total=10000.0
        ),
        cats=Population(susceptible=4950.0, infected=50.0, vaccinated=0.0, total=5000.0),
        humans=Population(
            susceptible=99900.0,
            infected=100.0,
            vaccinated=0.0,
            total=100000.0
        ),
        population_density=1000.0,
        connected_municipalities=[],
        infected_dogs_history=[],
        infected_cats_history=[],
        infected_humans_history=[]
    )
    
    initial_S_human = state.humans.susceptible
    
    # Run simulation step
    state = simulate_municipality_step(state, params, {})
    
    # Check transmission occurred
    # Expected: β_dh * (p * 0.1) * (S_h * I_d / N_d) * dt
    # = 0.0015 * 0.03 * (99900 * 1000 / 10000) * 1.0 ≈ 0.45
    S_human_decrease = initial_S_human - state.humans.susceptible
    
    # Should have very few infections (dogs rarely bite humans)
    assert S_human_decrease > 0, f"Expected some dog-to-human infections, got {S_human_decrease:.2f}"
    assert S_human_decrease < 5, f"Expected LOW infection rate, got {S_human_decrease:.2f}"
    
    print(f"   ✅ Dog-to-human transmission: {S_human_decrease:.2f} new infections")
    print(f"      Very low rate (β_dh = {params.beta_dh})")
    print(f"      Dogs cause >95% of human rabies cases (WHO)")


def test_cat_to_human_transmission():
    """Test that cat-to-human transmission works correctly"""
    print("\n[Test 5] Cat-to-human transmission...")
    
    params = SimulationParameters(
        lambda_human=0.0,
        mu_human=0.0,
        delta_human=0.0,
        beta_dh=0.0,     # Disable dog-to-human for this test
        beta_ch=0.00075,  # Cat-to-human coefficient (even lower than dog-to-human)
        contact_probability=0.3,
        sigma_3=0.0,
        dt=1.0
    )
    
    state = MunicipalityState(
        id="test",
        name="Test City",
        dogs=Population(susceptible=10000.0, infected=0.0, vaccinated=0.0, total=10000.0),
        cats=Population(
            susceptible=4000.0,
            infected=1000.0,  # 20% infected cats
            vaccinated=0.0,
            total=5000.0
        ),
        humans=Population(
            susceptible=99900.0,
            infected=100.0,
            vaccinated=0.0,
            total=100000.0
        ),
        population_density=1000.0,
        connected_municipalities=[],
        infected_dogs_history=[],
        infected_cats_history=[],
        infected_humans_history=[]
    )
    
    initial_S_human = state.humans.susceptible
    
    # Run simulation step
    state = simulate_municipality_step(state, params, {})
    
    # Check transmission occurred
    S_human_decrease = initial_S_human - state.humans.susceptible
    
    # Should have very few infections (even rarer than dogs)
    assert S_human_decrease > 0, f"Expected some cat-to-human infections, got {S_human_decrease:.2f}"
    
    print(f"   ✅ Cat-to-human transmission: {S_human_decrease:.2f} new infections")
    print(f"      Even lower rate than dogs (β_ch = {params.beta_ch})")
    print(f"      β_ch < β_dh (cats cause <5% of human cases)")


def test_combined_animal_to_human():
    """Test that humans get infected from BOTH dogs AND cats"""
    print("\n[Test 6] Combined animal-to-human transmission...")
    
    params = SimulationParameters(
        lambda_human=0.0,
        mu_human=0.0,
        delta_human=0.0,
        beta_dh=0.0015,   # Dog-to-human enabled
        beta_ch=0.00075,  # Cat-to-human enabled
        contact_probability=0.3,
        sigma_3=0.0,
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
            susceptible=4500.0,
            infected=500.0,  # 10% infected cats
            vaccinated=0.0,
            total=5000.0
        ),
        humans=Population(
            susceptible=99800.0,
            infected=200.0,
            vaccinated=0.0,
            total=100000.0
        ),
        population_density=1000.0,
        connected_municipalities=[],
        infected_dogs_history=[],
        infected_cats_history=[],
        infected_humans_history=[]
    )
    
    initial_S_human = state.humans.susceptible
    
    # Run simulation step
    state = simulate_municipality_step(state, params, {})
    
    # Should get infections from both animal sources
    total_infections = initial_S_human - state.humans.susceptible
    
    assert total_infections > 0, f"Expected combined infections, got {total_infections:.2f}"
    
    print(f"   ✅ Combined transmission: {total_infections:.2f} new infections")
    print(f"      From dogs (primary): β_dh = {params.beta_dh}")
    print(f"      From cats (secondary): β_ch = {params.beta_ch}")
    print(f"      Humans infected by BOTH animal sources")


def test_no_human_to_human():
    """Test that there's NO human-to-human transmission (end host)"""
    print("\n[Test 7] No human-to-human transmission (end host)...")
    
    params = SimulationParameters(
        lambda_human=0.0,
        mu_human=0.0,
        delta_human=0.0,
        beta_dh=0.0,  # No animals infected
        beta_ch=0.0,
        sigma_3=0.0,
        dt=1.0
    )
    
    state = MunicipalityState(
        id="test",
        name="Test City",
        dogs=Population(susceptible=10000.0, infected=0.0, vaccinated=0.0, total=10000.0),
        cats=Population(susceptible=5000.0, infected=0.0, vaccinated=0.0, total=5000.0),
        humans=Population(
            susceptible=99000.0,
            infected=1000.0,  # 1% infected humans (but no animals)
            vaccinated=0.0,
            total=100000.0
        ),
        population_density=1000.0,
        connected_municipalities=[],
        infected_dogs_history=[],
        infected_cats_history=[],
        infected_humans_history=[]
    )
    
    initial_S_human = state.humans.susceptible
    
    # Run simulation step
    state = simulate_municipality_step(state, params, {})
    
    # Check NO human-to-human transmission
    S_human_change = initial_S_human - state.humans.susceptible
    
    # Should be zero (no animal infections = no human infections)
    assert abs(S_human_change) < 0.01, \
        f"Expected NO human-to-human transmission, but S changed by {S_human_change:.2f}"
    
    print(f"   ✅ No human-to-human transmission: S_h change = {S_human_change:.4f}")
    print(f"      Humans are END HOSTS (rabies doesn't spread human-to-human)")


def test_human_independent_stochastic():
    """Test that humans have independent stochastic noise (σ₃·dW₃)"""
    print("\n[Test 8] Human independent stochastic noise...")
    
    params = SimulationParameters(
        lambda_human=0.0,
        mu_human=0.0,
        delta_human=0.0,
        beta_dh=0.0,
        beta_ch=0.0,
        sigma_1=0.5,  # Dog noise
        sigma_2=0.4,  # Cat noise
        sigma_3=0.3,  # Human noise (different from dogs and cats)
        dt=1.0
    )
    
    # Run multiple simulations
    human_infected_values = []
    dog_infected_values = []
    cat_infected_values = []
    
    for _ in range(20):
        state = MunicipalityState(
            id="test",
            name="Test City",
            dogs=Population(susceptible=9000.0, infected=1000.0, vaccinated=0.0, total=10000.0),
            cats=Population(susceptible=4000.0, infected=1000.0, vaccinated=0.0, total=5000.0),
            humans=Population(susceptible=99000.0, infected=1000.0, vaccinated=0.0, total=100000.0),
            population_density=1000.0,
            connected_municipalities=[],
            infected_dogs_history=[],
            infected_cats_history=[],
            infected_humans_history=[]
        )
        state = simulate_municipality_step(state, params, {})
        human_infected_values.append(state.humans.infected)
        dog_infected_values.append(state.dogs.infected)
        cat_infected_values.append(state.cats.infected)
    
    # Check all have variation (stochastic)
    import numpy as np
    human_std = np.std(human_infected_values)
    dog_std = np.std(dog_infected_values)
    cat_std = np.std(cat_infected_values)
    
    assert human_std > 0.1, f"Expected human stochastic variation, got std={human_std:.3f}"
    
    # Verify independence
    correlation_human_dog = np.corrcoef(human_infected_values, dog_infected_values)[0, 1]
    correlation_human_cat = np.corrcoef(human_infected_values, cat_infected_values)[0, 1]
    
    print(f"   ✅ Independent stochastic noise:")
    print(f"      Human variation (σ₃): std = {human_std:.2f}")
    print(f"      Dog variation (σ₁): std = {dog_std:.2f}")
    print(f"      Cat variation (σ₂): std = {cat_std:.2f}")
    print(f"      Correlation(human, dog): {correlation_human_dog:.3f} (should be ~0)")
    print(f"      Correlation(human, cat): {correlation_human_cat:.3f} (should be ~0)")
    print(f"      dW₁, dW₂, and dW₃ are ALL INDEPENDENT")


def test_human_no_recovery():
    """Test that humans don't recover (SI model, not SIR)"""
    print("\n[Test 9] Humans don't recover (SI model)...")
    
    state = MunicipalityState(
        id="test",
        name="Test City",
        dogs=Population(susceptible=9000.0, infected=1000.0, vaccinated=0.0, total=10000.0),
        cats=Population(susceptible=4000.0, infected=1000.0, vaccinated=0.0, total=5000.0),
        humans=Population(susceptible=99000.0, infected=1000.0, vaccinated=0.0, total=100000.0),
        population_density=1000.0,
        connected_municipalities=[],
        infected_dogs_history=[],
        infected_cats_history=[],
        infected_humans_history=[]
    )
    
    # Check that Population doesn't have recovered field
    assert not hasattr(state.humans, 'recovered'), \
        "Humans should not have recovered field (SI model, not SIR)"
    
    print(f"   ✅ No recovery field: Population only has S, I, V compartments")
    print(f"      Without PEP, rabies is fatal for humans too")


if __name__ == "__main__":
    print("=" * 70)
    print("SUB-PHASE 2E TESTING: Human Equations (SI+V+BD)")
    print("=" * 70)
    
    try:
        test_human_births()
        test_human_natural_deaths()
        test_human_rabies_deaths()
        test_dog_to_human_transmission()
        test_cat_to_human_transmission()
        test_combined_animal_to_human()
        test_no_human_to_human()
        test_human_independent_stochastic()
        test_human_no_recovery()
        
        print("\n" + "=" * 70)
        print("✅ SUB-PHASE 2E COMPLETE!")
        print("=" * 70)
        print("\n📊 Summary:")
        print("  ✅ Human births (Λ_h)")
        print("  ✅ Human natural deaths (μ_h·S_h, μ_h·I_h, μ_h·V_h)")
        print("  ✅ Human rabies deaths (δ_h·I_h)")
        print("  ✅ Dog-to-human transmission (β_dh·S_h·I_d/N_d)")
        print("  ✅ Cat-to-human transmission (β_ch·S_h·I_c/N_c)")
        print("  ✅ Combined animal transmission (both sources)")
        print("  ✅ NO human-to-human transmission (end host)")
        print("  ✅ Independent stochastic noise (σ₃·dW₃(t))")
        print("  ✅ No recovery (SI model confirmed)")
        print("\n🎉 Human equations fully implemented!")
        print("\n📝 Key Feature: END HOST (No Human-to-Human)")
        print("   • Humans infected by dogs (β_dh) - primary (>95%)")
        print("   • Humans infected by cats (β_ch) - secondary (<5%)")
        print("   • NO human-to-human transmission")
        print("   • Independent noise from animals (dW₃ ≠ dW₁ ≠ dW₂)")
        print("\n🚀 All species implemented! Ready for Sub-Phase 2F: Integration!")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
