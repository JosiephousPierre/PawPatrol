"""
Unit Tests for Stochastic Processes Module
Tests Box-Muller transform, Wiener process, and Euler-Maruyama method
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from simulation.stochastic_processes import (
    box_muller_transform,
    generate_normal_random,
    wiener_increment,
    wiener_process,
    euler_maruyama_step,
    euler_maruyama_simulate,
    apply_stochastic_fluctuation
)

def test_box_muller_statistics():
    """Test that Box-Muller produces correct statistical properties"""
    print("Test: Box-Muller Statistics")
    
    n_samples = 10000
    samples = []
    
    for _ in range(n_samples // 2):
        z0, z1 = box_muller_transform()
        samples.extend([z0, z1])
    
    samples = np.array(samples[:n_samples])
    
    mean = np.mean(samples)
    std = np.std(samples, ddof=1)
    
    print(f"  Sample size: {n_samples}")
    print(f"  Mean: {mean:.6f} (expected: 0.000000)")
    print(f"  Std:  {std:.6f} (expected: 1.000000)")
    
    # Statistical test: mean should be close to 0, std close to 1
    mean_error = abs(mean)
    std_error = abs(std - 1.0)
    
    tolerance = 0.05  # 5% tolerance
    passed = mean_error < tolerance and std_error < tolerance
    
    print(f"  Mean error: {mean_error:.6f}")
    print(f"  Std error:  {std_error:.6f}")
    print(f"  Status: {'PASS ✓' if passed else 'FAIL ✗'}")
    print()
    
    return passed

def test_wiener_increment_properties():
    """Test Wiener increment dW properties"""
    print("Test: Wiener Increment Properties")
    
    dt = 0.01
    sigma = 1.0
    n_samples = 10000
    
    increments = [wiener_increment(dt, sigma) for _ in range(n_samples)]
    increments = np.array(increments)
    
    # dW should have mean 0 and variance dt
    mean = np.mean(increments)
    variance = np.var(increments, ddof=1)
    expected_variance = dt
    
    print(f"  Time step dt: {dt}")
    print(f"  Sigma: {sigma}")
    print(f"  Samples: {n_samples}")
    print(f"  Mean: {mean:.6f} (expected: 0.000000)")
    print(f"  Variance: {variance:.6f} (expected: {expected_variance:.6f})")
    
    tolerance = 0.002  # Tighter tolerance for large sample
    passed = abs(mean) < tolerance and abs(variance - expected_variance) < tolerance
    
    print(f"  Status: {'PASS ✓' if passed else 'FAIL ✗'}")
    print()
    
    return passed

def test_wiener_process_scaling():
    """Test that Wiener process variance scales with time"""
    print("Test: Wiener Process Time Scaling")
    
    T = 1.0
    dt = 0.001
    sigma = 1.0
    n_simulations = 1000
    
    # Run multiple simulations
    final_values = []
    for _ in range(n_simulations):
        W = wiener_process(T, dt, sigma)
        final_values.append(W[-1])
    
    final_values = np.array(final_values)
    
    # Theoretical: Var[W(T)] = sigma² * T
    expected_variance = sigma**2 * T
    observed_variance = np.var(final_values, ddof=1)
    
    print(f"  Simulation time T: {T}")
    print(f"  Time step dt: {dt}")
    print(f"  Sigma: {sigma}")
    print(f"  Simulations: {n_simulations}")
    print(f"  Expected Var[W(T)]: {expected_variance:.6f}")
    print(f"  Observed Var[W(T)]: {observed_variance:.6f}")
    
    relative_error = abs(observed_variance - expected_variance) / expected_variance
    print(f"  Relative error: {relative_error:.4%}")
    
    tolerance = 0.15  # 15% tolerance
    passed = relative_error < tolerance
    
    print(f"  Status: {'PASS ✓' if passed else 'FAIL ✗'}")
    print()
    
    return passed

def test_euler_maruyama_geometric_brownian():
    """Test Euler-Maruyama with Geometric Brownian Motion"""
    print("Test: Euler-Maruyama (Geometric Brownian Motion)")
    
    # GBM: dS = μS dt + σS dW
    # Analytical solution exists for validation
    
    S0 = 100.0
    mu = 0.05
    sigma = 0.2
    T = 1.0
    dt = 0.001
    
    def drift(s, t):
        return mu * s
    
    def diffusion(s, t):
        return sigma * s
    
    # Simulate
    t, S = euler_maruyama_simulate(S0, drift, diffusion, T, dt)
    
    print(f"  Initial S(0): {S[0]:.2f}")
    print(f"  Final S(T):   {S[-1]:.2f}")
    print(f"  Drift μ: {mu}")
    print(f"  Volatility σ: {sigma}")
    
    # Check properties
    all_positive = np.all(S > 0)
    monotonic_time = np.all(np.diff(t) > 0)
    correct_length = len(S) == len(t)
    
    passed = all_positive and monotonic_time and correct_length
    
    print(f"  All values positive: {all_positive}")
    print(f"  Time monotonic: {monotonic_time}")
    print(f"  Correct length: {correct_length}")
    print(f"  Status: {'PASS ✓' if passed else 'FAIL ✗'}")
    print()
    
    return passed

def test_stochastic_fluctuation():
    """Test stochastic fluctuation application"""
    print("Test: Stochastic Fluctuation Application")
    
    value = 100.0
    sigma = 0.5
    dt = 0.01
    n_tests = 1000
    
    results = [apply_stochastic_fluctuation(value, sigma, dt) for _ in range(n_tests)]
    results = np.array(results)
    
    # Should be centered around original value
    mean_result = np.mean(results)
    
    print(f"  Original value: {value:.2f}")
    print(f"  Sigma: {sigma}")
    print(f"  dt: {dt}")
    print(f"  Tests: {n_tests}")
    print(f"  Mean result: {mean_result:.2f}")
    
    # Check all positive (ensure_positive=True by default)
    all_positive = np.all(results >= 0)
    mean_close = abs(mean_result - value) < 2.0  # Within 2 units
    
    passed = all_positive and mean_close
    
    print(f"  All positive: {all_positive}")
    print(f"  Mean close to original: {mean_close}")
    print(f"  Status: {'PASS ✓' if passed else 'FAIL ✗'}")
    print()
    
    return passed

def run_all_tests():
    """Run all tests and report results"""
    print("=" * 70)
    print("STOCHASTIC PROCESSES - UNIT TESTS")
    print("=" * 70)
    print()
    
    tests = [
        ("Box-Muller Statistics", test_box_muller_statistics),
        ("Wiener Increment Properties", test_wiener_increment_properties),
        ("Wiener Process Scaling", test_wiener_process_scaling),
        ("Euler-Maruyama GBM", test_euler_maruyama_geometric_brownian),
        ("Stochastic Fluctuation", test_stochastic_fluctuation)
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"  ERROR in {test_name}: {str(e)}")
            results[test_name] = False
            print()
    
    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {test_name:.<50} {status}")
    
    print()
    total_tests = len(results)
    passed_tests = sum(results.values())
    print(f"  Total: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("\n  🎉 ALL TESTS PASSED!")
    else:
        print(f"\n  ⚠️  {total_tests - passed_tests} test(s) failed")
    
    print("=" * 70)
    
    return passed_tests == total_tests

if __name__ == "__main__":
    run_all_tests()
