"""
Test Sub-Phase 2C: Dog Equations
Verify the dog SI+V+BD equations implementation
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


def test_dog_births():
    """Test that dog births are calculated correctly"""
    print("\n[Test 1] Dog births calculation...")
    
    # Setup
    params = SimulationParameters(
        lambda_dog=0.0002,  # 2 births per 10,000 per day
        mu_dog=0.0001,
        delta_dog=0.1,
        beta_dd=0.15,
        contact_probability=0.3,
        dt=1.0
    )
    
    state = MunicipalityState(
        id="test",
        name="Test City",
        dogs=Population(
            susceptible=9000.0,
            infected=100.0,
            vaccinated=900.0,
            total=10000.0
        ),
        cats=Population(susceptible=5000.0, infected=0.0, vaccinated=0.0, total=5000.0),
        humans=Population(susceptible=100000.0, infected=0.0, vaccinated=0.0, total=100000.0),
        population_density=1000.0,
        connected_municipalities=[],
        infected_dogs_history=[],
        infected_cats_history=[],
        infected_humans_history=[]
    )
    
    initial_total = state.dogs.total
    initial_births = state.dogs.cumulative_births
    
    # Run simulation step
    state = simulate_municipality_step(state, params, {})
    
    # Check births were added
    births_added = state.dogs.cumulative_births - initial_births
    expected_births = 0.0002 * 10000 * 1.0  # λ * N * dt = 2.0
    
    assert abs(births_added - expected_births) < 0.5, \
        f"Expected ~{expected_births} births, got {births_added}"
    
    print(f"   ✅ Births correct: {births_added:.2f} (expected ~{expected_births})")
    print(f"      Initial population: {initial_total:.0f}")
    print(f"      Births added: {births_added:.2f}")


def test_dog_natural_deaths():
    """Test that natural deaths are tracked for all compartments"""
    print("\n[Test 2] Dog natural deaths...")
    
    params = SimulationParameters(
        lambda_dog=0.0,  # No births
        mu_dog=0.0002,   # 2 deaths per 10,000 per day
        delta_dog=0.0,   # No rabies deaths
        beta_dd=0.0,     # No transmission
        dt=1.0
    )
    
    state = MunicipalityState(
        id="test",
        name="Test City",
        dogs=Population(
            susceptible=5000.0,
            infected=2000.0,
            vaccinated=3000.0,
            total=10000.0
        ),
        cats=Population(susceptible=5000.0, infected=0.0, vaccinated=0.0, total=5000.0),
        humans=Population(susceptible=100000.0, infected=0.0, vaccinated=0.0, total=100000.0),
        population_density=1000.0,
        connected_municipalities=[],
        infected_dogs_history=[],
        infected_cats_history=[],
        infected_humans_history=[]
    )
    
    initial_deaths = state.dogs.cumulative_natural_deaths
    
    # Run simulation step
    state = simulate_municipality_step(state, params, {})
    
    # Check natural deaths
    deaths_added = state.dogs.cumulative_natural_deaths - initial_deaths
    
    # Expected: μ * (S + I + V) * dt = 0.0002 * 10000 * 1.0 = 2.0
    expected_deaths = 0.0002 * 10000 * 1.0
    
    assert abs(deaths_added - expected_deaths) < 0.5, \
        f"Expected ~{expected_deaths} natural deaths, got {deaths_added}"
    
    print(f"   ✅ Natural deaths correct: {deaths_added:.2f} (expected ~{expected_deaths})")
    print(f"      Deaths from S: {0.0002 * 5000:.1f}")
    print(f"      Deaths from I: {0.0002 * 2000:.1f}")
    print(f"      Deaths from V: {0.0002 * 3000:.1f}")


def test_dog_rabies_deaths():
    """Test that rabies deaths are calculated correctly"""
    print("\n[Test 3] Dog rabies deaths...")
    
    params = SimulationParameters(
        lambda_dog=0.0,
        mu_dog=0.0,
        delta_dog=0.1,  # 10% die per day (~10 day survival)
        beta_dd=0.0,
        dt=1.0
    )
    
    state = MunicipalityState(
        id="test",
        name="Test City",
        dogs=Population(
            susceptible=9000.0,
            infected=100.0,  # 100 infected dogs
            vaccinated=900.0,
            total=10000.0
        ),
        cats=Population(susceptible=5000.0, infected=0.0, vaccinated=0.0, total=5000.0),
        humans=Population(susceptible=100000.0, infected=0.0, vaccinated=0.0, total=100000.0),
        population_density=1000.0,
        connected_municipalities=[],
        infected_dogs_history=[],
        infected_cats_history=[],
        infected_humans_history=[]
    )
    
    initial_rabies_deaths = state.dogs.cumulative_rabies_deaths
    
    # Run simulation step
    state = simulate_municipality_step(state, params, {})
    
    # Check rabies deaths
    rabies_deaths = state.dogs.cumulative_rabies_deaths - initial_rabies_deaths
    expected_rabies_deaths = 0.1 * 100 * 1.0  # δ * I * dt = 10
    
    assert abs(rabies_deaths - expected_rabies_deaths) < 1.0, \
        f"Expected ~{expected_rabies_deaths} rabies deaths, got {rabies_deaths}"
    
    print(f"   ✅ Rabies deaths correct: {rabies_deaths:.2f} (expected ~{expected_rabies_deaths})")
    print(f"      10% of 100 infected dogs = 10 deaths/day")


def test_dog_vaccination():
    """Test that vaccination moves dogs from S to V"""
    print("\n[Test 4] Dog vaccination...")
    
    params = SimulationParameters(
        lambda_dog=0.0,
        mu_dog=0.0,
        delta_dog=0.0,
        beta_dd=0.0,
        vaccination_rate=0.8,  # Target 80% coverage
        dt=1.0
    )
    
    state = MunicipalityState(
        id="test",
        name="Test City",
        dogs=Population(
            susceptible=9000.0,  # 90% susceptible
            infected=100.0,
            vaccinated=900.0,    # 9% already vaccinated
            total=10000.0
        ),
        cats=Population(susceptible=5000.0, infected=0.0, vaccinated=0.0, total=5000.0),
        humans=Population(susceptible=100000.0, infected=0.0, vaccinated=0.0, total=100000.0),
        population_density=1000.0,
        connected_municipalities=[],
        infected_dogs_history=[],
        infected_cats_history=[],
        infected_humans_history=[]
    )
    
    initial_vaccinations = state.dogs.cumulative_vaccinations
    initial_S = state.dogs.susceptible
    initial_V = state.dogs.vaccinated
    
    # Run simulation step
    state = simulate_municipality_step(state, params, {})
    
    # Check vaccinations
    vaccinations_done = state.dogs.cumulative_vaccinations - initial_vaccinations
    
    # Current coverage: 900/10000 = 9%
    # Target: 80% = 8000
    # Need: 7100 more, but limited by capacity (5% of 10000 = 500/day)
    expected_vaccinations = 500.0
    
    assert abs(vaccinations_done - expected_vaccinations) < 50, \
        f"Expected ~{expected_vaccinations} vaccinations, got {vaccinations_done}"
    
    print(f"   ✅ Vaccination correct: {vaccinations_done:.0f} (expected ~{expected_vaccinations})")
    print(f"      Initial: S={initial_S:.0f}, V={initial_V:.0f} ({initial_V/10000*100:.0f}%)")
    print(f"      After: S={state.dogs.susceptible:.0f}, V={state.dogs.vaccinated:.0f} ({state.dogs.vaccinated/state.dogs.total*100:.0f}%)")
    print(f"      Limited by capacity: 5% of population/day")


def test_dog_transmission():
    """Test that dog-to-dog transmission occurs correctly"""
    print("\n[Test 5] Dog-to-dog transmission...")
    
    params = SimulationParameters(
        lambda_dog=0.0,
        mu_dog=0.0,
        delta_dog=0.0,  # Keep infected alive for now
        beta_dd=0.15,
        contact_probability=0.5,
        sigma_1=0.0,  # No stochastic noise for testing
        dt=1.0
    )
    
    state = MunicipalityState(
        id="test",
        name="Test City",
        dogs=Population(
            susceptible=9900.0,
            infected=100.0,  # 1% infected
            vaccinated=0.0,
            total=10000.0
        ),
        cats=Population(susceptible=5000.0, infected=0.0, vaccinated=0.0, total=5000.0),
        humans=Population(susceptible=100000.0, infected=0.0, vaccinated=0.0, total=100000.0),
        population_density=1000.0,
        connected_municipalities=[],
        infected_dogs_history=[],
        infected_cats_history=[],
        infected_humans_history=[]
    )
    
    initial_S = state.dogs.susceptible
    initial_I = state.dogs.infected
    
    # Run simulation step
    state = simulate_municipality_step(state, params, {})
    
    # Check transmission occurred
    # Expected: β * p * (S * I / N) * dt = 0.15 * 0.5 * (9900 * 100 / 10000) * 1.0 = 7.425
    S_decrease = initial_S - state.dogs.susceptible
    I_increase = state.dogs.infected - initial_I
    
    # S should decrease, I should increase
    assert S_decrease > 5, f"Expected significant S decrease, got {S_decrease:.2f}"
    assert I_increase > 5, f"Expected significant I increase, got {I_increase:.2f}"
    
    # They should be roughly equal (what leaves S enters I)
    assert abs(S_decrease - I_increase) < 1, \
        f"S decrease ({S_decrease:.2f}) should ≈ I increase ({I_increase:.2f})"
    
    print(f"   ✅ Transmission working: {S_decrease:.2f} new infections")
    print(f"      S: {initial_S:.0f} → {state.dogs.susceptible:.0f} (Δ={-S_decrease:.0f})")
    print(f"      I: {initial_I:.0f} → {state.dogs.infected:.0f} (Δ={I_increase:.0f})")


def test_dog_no_recovery():
    """Test that dogs don't recover (SI model, not SIR)"""
    print("\n[Test 6] Dogs don't recover (SI model)...")
    
    params = SimulationParameters(
        lambda_dog=0.0,
        mu_dog=0.0,
        delta_dog=0.0,
        beta_dd=0.0,
        dt=1.0
    )
    
    state = MunicipalityState(
        id="test",
        name="Test City",
        dogs=Population(
            susceptible=9000.0,
            infected=1000.0,
            vaccinated=0.0,
            total=10000.0
        ),
        cats=Population(susceptible=5000.0, infected=0.0, vaccinated=0.0, total=5000.0),
        humans=Population(susceptible=100000.0, infected=0.0, vaccinated=0.0, total=100000.0),
        population_density=1000.0,
        connected_municipalities=[],
        infected_dogs_history=[],
        infected_cats_history=[],
        infected_humans_history=[]
    )
    
    # Run simulation step
    state = simulate_municipality_step(state, params, {})
    
    # Check that Population doesn't have recovered field
    assert not hasattr(state.dogs, 'recovered'), \
        "Dogs should not have recovered field (SI model, not SIR)"
    
    # Verify only S, I, V exist
    assert hasattr(state.dogs, 'susceptible'), "Dogs should have susceptible"
    assert hasattr(state.dogs, 'infected'), "Dogs should have infected"
    assert hasattr(state.dogs, 'vaccinated'), "Dogs should have vaccinated"
    
    print(f"   ✅ No recovery field: Population only has S, I, V compartments")
    print(f"      This is an SI model, not SIR - rabies is fatal")


def test_dog_stochastic_noise():
    """Test that stochastic term affects infected dogs"""
    print("\n[Test 7] Stochastic noise in infected dogs...")
    
    params = SimulationParameters(
        lambda_dog=0.0,
        mu_dog=0.0,
        delta_dog=0.0,
        beta_dd=0.0,  # No transmission
        sigma_1=0.5,  # Strong stochastic noise
        dt=1.0
    )
    
    state = MunicipalityState(
        id="test",
        name="Test City",
        dogs=Population(
            susceptible=9000.0,
            infected=1000.0,
            vaccinated=0.0,
            total=10000.0
        ),
        cats=Population(susceptible=5000.0, infected=0.0, vaccinated=0.0, total=5000.0),
        humans=Population(susceptible=100000.0, infected=0.0, vaccinated=0.0, total=100000.0),
        population_density=1000.0,
        connected_municipalities=[],
        infected_dogs_history=[],
        infected_cats_history=[],
        infected_humans_history=[]
    )
    
    initial_I = state.dogs.infected
    
    # Run multiple times to see stochastic variation
    infected_values = []
    for _ in range(10):
        state_copy = MunicipalityState(
            id="test",
            name="Test City",
            dogs=Population(susceptible=9000.0, infected=1000.0, vaccinated=0.0, total=10000.0),
            cats=Population(susceptible=5000.0, infected=0.0, vaccinated=0.0, total=5000.0),
            humans=Population(susceptible=100000.0, infected=0.0, vaccinated=0.0, total=100000.0),
            population_density=1000.0,
            connected_municipalities=[],
            infected_dogs_history=[],
            infected_cats_history=[],
            infected_humans_history=[]
        )
        state_copy = simulate_municipality_step(state_copy, params, {})
        infected_values.append(state_copy.dogs.infected)
    
    # Check that infected values vary (stochastic)
    import numpy as np
    std_dev = np.std(infected_values)
    
    assert std_dev > 0.1, f"Expected stochastic variation, but std_dev = {std_dev:.3f}"
    
    print(f"   ✅ Stochastic variation present: std_dev = {std_dev:.2f}")
    print(f"      Initial I: {initial_I:.0f}")
    print(f"      After 10 runs: min={min(infected_values):.0f}, max={max(infected_values):.0f}")
    print(f"      This reflects random environmental fluctuations (σ₁·dW₁)")


if __name__ == "__main__":
    print("=" * 70)
    print("SUB-PHASE 2C TESTING: Dog Equations (SI+V+BD)")
    print("=" * 70)
    
    try:
        test_dog_births()
        test_dog_natural_deaths()
        test_dog_rabies_deaths()
        test_dog_vaccination()
        test_dog_transmission()
        test_dog_no_recovery()
        test_dog_stochastic_noise()
        
        print("\n" + "=" * 70)
        print("✅ SUB-PHASE 2C COMPLETE!")
        print("=" * 70)
        print("\n📊 Summary:")
        print("  ✅ Dog births (Λ_d)")
        print("  ✅ Dog natural deaths (μ_d·S_d, μ_d·I_d, μ_d·V_d)")
        print("  ✅ Dog rabies deaths (δ_d·I_d)")
        print("  ✅ Dog vaccination (u_d(t): S → V)")
        print("  ✅ Dog transmission (β_dd·S_d·I_d/N_d)")
        print("  ✅ No recovery (SI model confirmed)")
        print("  ✅ Stochastic noise (σ₁·dW₁(t))")
        print("\n🎉 Dog equations fully implemented!")
        print("\n📝 Model: SI+V+BD (Susceptible-Infected-Vaccinated + Births-Deaths)")
        print("   • S_d: Susceptible dogs (can get infected or vaccinated)")
        print("   • I_d: Infected dogs (fatal disease, no recovery)")
        print("   • V_d: Vaccinated dogs (protected)")
        print("\n🚀 Ready for Sub-Phase 2D: Cat Equations!")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
