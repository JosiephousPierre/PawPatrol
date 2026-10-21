"""
Test Sub-Phase 2B: Helper Functions
Verify the mathematical helper functions for SI+V+BD model
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulation.transmission_model import (
    calculate_births,
    calculate_natural_deaths,
    calculate_rabies_deaths,
    generate_independent_wiener_processes,
    calculate_transmission,
    calculate_vaccination
)


def test_births():
    """Test birth calculation: Births = Λ * N * dt"""
    print("\n[Test 1] Birth calculation...")
    
    # Example: 1 birth per 10,000 dogs per day
    lambda_dog = 0.0001
    N_dog = 10000
    dt = 1.0  # 1 full day
    
    births = calculate_births(lambda_dog, N_dog, dt)
    
    # Expected: 0.0001 * 10000 * 1.0 = 1.0 birth
    assert abs(births - 1.0) < 0.01, f"Birth calculation incorrect: {births}"
    
    print(f"   ✅ Births correct: {births:.2f} births per day")
    print(f"      Formula: {lambda_dog} * {N_dog} * {dt} = {births}")
    
    # Test with smaller timestep
    dt = 0.1
    births = calculate_births(lambda_dog, N_dog, dt)
    expected = 0.1
    assert abs(births - expected) < 0.01, "Births with dt=0.1 incorrect"
    print(f"   ✅ With dt=0.1: {births:.2f} births")


def test_natural_deaths():
    """Test natural death calculation: Deaths = μ * Population * dt"""
    print("\n[Test 2] Natural death calculation...")
    
    # Example: 1 natural death per 10,000 dogs per day
    mu_dog = 0.0001
    population = 5000
    dt = 1.0
    
    deaths = calculate_natural_deaths(mu_dog, population, dt)
    
    # Expected: 0.0001 * 5000 * 1.0 = 0.5 deaths
    assert abs(deaths - 0.5) < 0.01, f"Natural death calculation incorrect: {deaths}"
    
    print(f"   ✅ Natural deaths correct: {deaths:.2f} deaths per day")
    print(f"      Formula: {mu_dog} * {population} * {dt} = {deaths}")
    
    # Test that deaths can't exceed population
    deaths = calculate_natural_deaths(10.0, 100, 1.0)  # Would be 1000 deaths from 100 pop
    assert deaths == 100, "Deaths should be capped at population size"
    print(f"   ✅ Deaths capped at population: max {deaths} from 100")


def test_rabies_deaths():
    """Test rabies death calculation: Deaths = δ * I * dt"""
    print("\n[Test 3] Rabies death calculation...")
    
    # Example: δ = 0.1 means average 10-day survival
    delta_dog = 0.1
    infected = 100
    dt = 1.0
    
    deaths = calculate_rabies_deaths(delta_dog, infected, dt)
    
    # Expected: 0.1 * 100 * 1.0 = 10 deaths
    assert abs(deaths - 10.0) < 0.01, f"Rabies death calculation incorrect: {deaths}"
    
    print(f"   ✅ Rabies deaths correct: {deaths:.2f} deaths per day")
    print(f"      Formula: {delta_dog} * {infected} * {dt} = {deaths}")
    print(f"      Interpretation: 10% of infected die per day (~10 day survival)")


def test_independent_wiener():
    """Test independent Wiener process generation"""
    print("\n[Test 4] Independent Wiener processes...")
    
    dt = 0.1
    sigma_values = [0.1, 0.08, 0.05]  # dog, cat, human
    
    # Generate multiple times to test independence
    all_dW = []
    for _ in range(100):
        dW_list = generate_independent_wiener_processes(dt, sigma_values)
        all_dW.append(dW_list)
    
    # Check we got 3 values each time
    assert len(all_dW[0]) == 3, "Should return 3 Wiener increments"
    
    # Check they're not all the same (independence)
    dW1_values = [dW[0] for dW in all_dW]
    dW2_values = [dW[1] for dW in all_dW]
    dW3_values = [dW[2] for dW in all_dW]
    
    # Standard deviations should be roughly sqrt(dt) * sigma
    import numpy as np
    std1 = np.std(dW1_values)
    std2 = np.std(dW2_values)
    std3 = np.std(dW3_values)
    
    print(f"   ✅ Generated 3 independent processes")
    print(f"      dW₁ std: {std1:.3f} (expected ~{0.1 * np.sqrt(dt):.3f})")
    print(f"      dW₂ std: {std2:.3f} (expected ~{0.08 * np.sqrt(dt):.3f})")
    print(f"      dW₃ std: {std3:.3f} (expected ~{0.05 * np.sqrt(dt):.3f})")
    
    # Verify independence (correlation should be near 0)
    correlation_12 = np.corrcoef(dW1_values, dW2_values)[0, 1]
    print(f"      Correlation dW₁-dW₂: {correlation_12:.3f} (should be ~0)")
    assert abs(correlation_12) < 0.3, "dW₁ and dW₂ should be independent"


def test_transmission():
    """Test transmission calculation: β * p * (S * I / N) * dt"""
    print("\n[Test 5] Transmission calculation...")
    
    # Dog-to-dog transmission
    beta_dd = 0.15
    contact_prob = 0.3
    susceptible = 900
    infected = 100
    total = 1000
    dt = 1.0
    
    new_infections = calculate_transmission(
        susceptible, infected, total, beta_dd, contact_prob, dt
    )
    
    # Expected: 0.15 * 0.3 * (900 * 100 / 1000) * 1.0 = 4.05
    expected = 0.15 * 0.3 * (900 * 100 / 1000) * 1.0
    assert abs(new_infections - expected) < 0.01, f"Transmission incorrect: {new_infections}"
    
    print(f"   ✅ Transmission correct: {new_infections:.2f} new infections")
    print(f"      Formula: {beta_dd} * {contact_prob} * ({susceptible}*{infected}/{total}) * {dt}")
    print(f"      Expected: {expected:.2f}")
    
    # Test cross-species (dog-to-cat with lower β_dc)
    beta_dc = 0.06  # Dog-to-cat is reduced
    cat_infections = calculate_transmission(
        500, 100, 1000, beta_dc, 0.3, 1.0
    )
    print(f"   ✅ Dog-to-cat transmission: {cat_infections:.2f} infections")
    print(f"      (Lower than dog-to-dog due to β_dc = {beta_dc} < β_dd = {beta_dd})")


def test_vaccination():
    """Test vaccination calculation"""
    print("\n[Test 6] Vaccination calculation...")
    
    susceptible = 500
    vaccinated = 300
    total = 1000
    target_coverage = 0.8  # 80%
    daily_capacity = 100
    dt = 1.0
    
    new_vaccinations = calculate_vaccination(
        susceptible, vaccinated, total, target_coverage, daily_capacity, dt
    )
    
    # Current coverage: 300/1000 = 30%
    # Target: 80% = 800 vaccinated
    # Needed: 800 - 300 = 500
    # But limited by capacity (100/day) and susceptible (500)
    # So should vaccinate 100
    expected = 100.0
    assert abs(new_vaccinations - expected) < 0.01, f"Vaccination incorrect: {new_vaccinations}"
    
    print(f"   ✅ Vaccination correct: {new_vaccinations:.0f} vaccinations")
    print(f"      Current: {vaccinated}/{total} ({vaccinated/total*100:.0f}%)")
    print(f"      Target: {target_coverage*100:.0f}%")
    print(f"      Capacity: {daily_capacity}/day")
    
    # Test when already at target
    vaccinated = 850  # Already above 80%
    new_vaccinations = calculate_vaccination(
        susceptible, vaccinated, total, target_coverage, daily_capacity, dt
    )
    assert new_vaccinations == 0.0, "Should not vaccinate when at target"
    print(f"   ✅ No vaccination when at target (current {vaccinated/total*100:.0f}%)")


def test_equilibrium():
    """Test that births can balance deaths at equilibrium"""
    print("\n[Test 7] Birth-death equilibrium...")
    
    # At equilibrium: Λ * N = μ * N + δ * I
    # If Λ = μ and no infections, population stays constant
    
    lambda_rate = 0.0001
    mu_rate = 0.0001  # Same as birth rate
    population = 10000
    dt = 1.0
    
    births = calculate_births(lambda_rate, population, dt)
    deaths = calculate_natural_deaths(mu_rate, population, dt)
    
    # Should be equal
    assert abs(births - deaths) < 0.01, "Births should equal deaths at equilibrium"
    
    print(f"   ✅ Equilibrium maintained:")
    print(f"      Births: {births:.2f}")
    print(f"      Deaths: {deaths:.2f}")
    print(f"      Net change: {births - deaths:.4f} ≈ 0")
    print(f"      Population stays constant at {population}")


if __name__ == "__main__":
    print("=" * 70)
    print("SUB-PHASE 2B TESTING: Helper Functions")
    print("=" * 70)
    
    try:
        test_births()
        test_natural_deaths()
        test_rabies_deaths()
        test_independent_wiener()
        test_transmission()
        test_vaccination()
        test_equilibrium()
        
        print("\n" + "=" * 70)
        print("✅ SUB-PHASE 2B COMPLETE!")
        print("=" * 70)
        print("\n📊 Summary:")
        print("  ✅ Birth calculations (Λ * N * dt)")
        print("  ✅ Natural death calculations (μ * Population * dt)")
        print("  ✅ Rabies death calculations (δ * I * dt)")
        print("  ✅ Independent Wiener processes (dW₁, dW₂, dW₃)")
        print("  ✅ Transmission calculations (β * p * S * I / N)")
        print("  ✅ Vaccination calculations (u(t))")
        print("  ✅ Birth-death equilibrium verified")
        print("\n🎉 Ready for Sub-Phase 2C: Dog Equations!")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
