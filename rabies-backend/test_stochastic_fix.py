"""
Test to verify Environmental Uncertainty (σ) parameter is working correctly

This test runs the same simulation multiple times with different σ values
and verifies that:
1. σ = 0 produces deterministic results (same every time)
2. σ > 0 produces variable results (different each time)
3. Higher σ produces more variability
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from simulation.transmission_model import run_fractional_stochastic_simulation
import numpy as np


def test_stochastic_intensity():
    """Test that environmental uncertainty parameter affects results"""
    
    print("=" * 70)
    print("TESTING ENVIRONMENTAL UNCERTAINTY (σ) PARAMETER")
    print("=" * 70)
    print()
    
    # Test municipality
    test_municipality = {
        'id': '1',
        'name': 'Maco',
        'latitude': 7.3647,
        'longitude': 125.8583,
        'humanPopulation': 87440,
        'dogPopulation': 3000,
        'catPopulation': 1145,
        'populationDensity': 295.2,
        'infectedDogs': 12,
        'infectedCats': 3,
        'infectedHumans': 0,
        'vaccinatedDogs': 900,
        'riskLevel': 'moderate',
        'connectedMunicipalities': []
    }
    
    # Base settings
    base_settings = {
        'simulationDays': 30,
        'fractionalOrder': 0.95,
        'transmissionRate': 0.15,
        'recoveryRate': 0.1,
        'contactProbability': 0.3,
        'vaccinationRate': 0.0
    }
    
    # Test different σ values
    sigma_values = [0.0, 0.05, 0.10]
    num_runs = 5  # Run each 5 times
    
    print("Running simulations with different σ values...")
    print("Each configuration will be run 5 times to check variability")
    print()
    
    results_by_sigma = {}
    
    for sigma in sigma_values:
        print(f"\n{'='*70}")
        print(f"Testing σ = {sigma} ({'Deterministic' if sigma == 0 else 'Stochastic'})")
        print(f"{'='*70}")
        
        settings = base_settings.copy()
        settings['stochasticIntensity'] = sigma
        
        run_results = []
        
        for run_num in range(num_runs):
            result = run_fractional_stochastic_simulation(
                municipalities=[test_municipality],
                settings=settings
            )
            
            predicted_dogs = result[0].get('predictedInfectedDogs', 0)
            predicted_cats = result[0].get('predictedInfectedCats', 0)
            total_infected = predicted_dogs + predicted_cats
            
            run_results.append(total_infected)
            print(f"  Run {run_num + 1}: {total_infected:.1f} total infected")
        
        results_by_sigma[sigma] = run_results
        
        # Calculate statistics
        mean_val = np.mean(run_results)
        std_val = np.std(run_results)
        min_val = np.min(run_results)
        max_val = np.max(run_results)
        
        print(f"\n  Statistics:")
        print(f"    Mean: {mean_val:.2f}")
        print(f"    Std Dev: {std_val:.2f}")
        print(f"    Range: [{min_val:.1f}, {max_val:.1f}]")
        print(f"    Coefficient of Variation: {(std_val/mean_val*100):.1f}%")
    
    # Verify results
    print(f"\n{'='*70}")
    print("VERIFICATION")
    print(f"{'='*70}")
    
    # Test 1: σ = 0 should have zero variation
    sigma_0_results = results_by_sigma[0.0]
    sigma_0_std = np.std(sigma_0_results)
    
    print(f"\n✓ Test 1: σ = 0 (Deterministic)")
    print(f"  Standard deviation: {sigma_0_std:.6f}")
    if sigma_0_std < 0.01:
        print(f"  ✅ PASS - Results are deterministic (std ≈ 0)")
    else:
        print(f"  ❌ FAIL - Results should be identical for σ = 0")
    
    # Test 2: σ = 0.05 should have some variation
    sigma_005_results = results_by_sigma[0.05]
    sigma_005_std = np.std(sigma_005_results)
    sigma_005_cv = sigma_005_std / np.mean(sigma_005_results) * 100
    
    print(f"\n✓ Test 2: σ = 0.05 (Low Uncertainty)")
    print(f"  Standard deviation: {sigma_005_std:.2f}")
    print(f"  Coefficient of Variation: {sigma_005_cv:.1f}%")
    if sigma_005_std > 0.1:
        print(f"  ✅ PASS - Results show variability (std > 0)")
    else:
        print(f"  ❌ FAIL - σ = 0.05 should produce some variation")
    
    # Test 3: σ = 0.10 should have more variation than σ = 0.05
    sigma_010_results = results_by_sigma[0.10]
    sigma_010_std = np.std(sigma_010_results)
    sigma_010_cv = sigma_010_std / np.mean(sigma_010_results) * 100
    
    print(f"\n✓ Test 3: σ = 0.10 (Moderate Uncertainty)")
    print(f"  Standard deviation: {sigma_010_std:.2f}")
    print(f"  Coefficient of Variation: {sigma_010_cv:.1f}%")
    if sigma_010_std > sigma_005_std:
        print(f"  ✅ PASS - More variability than σ = 0.05")
    else:
        print(f"  ⚠️  WARNING - σ = 0.10 should have more variation than σ = 0.05")
    
    # Final verdict
    print(f"\n{'='*70}")
    print("FINAL RESULT")
    print(f"{'='*70}")
    
    all_pass = (
        sigma_0_std < 0.01 and  # Deterministic
        sigma_005_std > 0.1 and  # Has variation
        sigma_010_std > sigma_005_std  # More variation
    )
    
    if all_pass:
        print("\n✅ ✅ ✅ ALL TESTS PASSED! ✅ ✅ ✅")
        print("\nEnvironmental Uncertainty parameter is working correctly!")
        print("Different σ values produce different levels of variability as expected.")
    else:
        print("\n⚠️  SOME TESTS FAILED")
        print("\nThe stochastic component may not be applied correctly.")
        print("Check the transmission_model.py implementation.")
    
    print()
    print("="*70)
    
    return all_pass


if __name__ == "__main__":
    success = test_stochastic_intensity()
    sys.exit(0 if success else 1)
