"""
Fractional Calculus Implementation
Grünwald-Letnikov Method for Fractional Derivatives

Mathematical Background:
    Fractional derivative of order α captures memory effects in the system.
    
    D^α f(t) ≈ (1/h^α) Σ_{k=0}^{n} w_k^(α) f(t - kh)
    
    where w_k^(α) are Grünwald-Letnikov weights:
        w_0^(α) = 1
        w_k^(α) = w_{k-1}^(α) * (1 - (1+α)/k) for k ≥ 1

Reference:
    Research paper: "Fractional-Order Stochastic Transmission Model"
"""

import numpy as np
from typing import Callable

def grunwald_letnikov_weights(alpha: float, n: int) -> np.ndarray:
    """
    Calculate Grünwald-Letnikov weights for fractional derivative
    
    Args:
        alpha: Fractional order (α) ∈ (0, 1]
        n: Number of weights to calculate
        
    Returns:
        np.ndarray: Array of G-L weights [w_0, w_1, ..., w_{n-1}]
        
    Formula:
        w_0 = 1
        w_k = w_{k-1} * (1 - (1+α)/k) for k ≥ 1
    """
    weights = np.zeros(n)
    weights[0] = 1.0
    
    for k in range(1, n):
        weights[k] = weights[k-1] * (1.0 - (1.0 + alpha) / k)
    
    return weights

def fractional_derivative(f_values: np.ndarray, alpha: float, h: float) -> float:
    """
    Compute fractional derivative using Grünwald-Letnikov approximation
    
    Args:
        f_values: Array of function values [f(t), f(t-h), f(t-2h), ...]
        alpha: Fractional order
        h: Time step
        
    Returns:
        float: Approximation of D^α f(t)
        
    Formula:
        D^α f(t) ≈ (1/h^α) Σ w_k f(t - kh)
    """
    n = len(f_values)
    weights = grunwald_letnikov_weights(alpha, n)
    
    # Compute weighted sum
    derivative = np.sum(weights * f_values) / (h ** alpha)
    
    return derivative

def fractional_euler_step(
    y_current: float,
    f_derivative: Callable,
    t: float,
    h: float,
    alpha: float,
    history: np.ndarray
) -> float:
    """
    Perform one step of fractional Euler method
    
    For equation: D^α y = f(y, t)
    
    Args:
        y_current: Current value y(t)
        f_derivative: Function f(y, t) defining the derivative
        t: Current time
        h: Time step
        alpha: Fractional order
        history: Previous values [y(t), y(t-h), y(t-2h), ...]
        
    Returns:
        float: Next value y(t+h)
    """
    # Calculate fractional derivative of current state
    D_alpha_y = fractional_derivative(history, alpha, h)
    
    # Euler step: y(t+h) = y(t) + h^α * (f(y,t) - D_alpha_y)
    f_val = f_derivative(y_current, t)
    y_next = y_current + (h ** alpha) * (f_val - D_alpha_y)
    
    return y_next

# ============================================================================
# TESTING / VALIDATION FUNCTIONS
# ============================================================================

def test_fractional_derivative():
    """
    Test fractional derivative against known results
    """
    # For α=1, should give standard derivative
    # For f(t) = t^2, f'(t) = 2t
    
    t = 1.0
    h = 0.01
    alpha = 1.0
    
    # Generate function values around t
    n = 100
    t_values = np.array([t - k*h for k in range(n)])
    f_values = t_values ** 2
    
    # Compute fractional derivative
    result = fractional_derivative(f_values, alpha, h)
    
    # Expected: 2*t = 2.0
    expected = 2.0 * t
    
    error = abs(result - expected)
    print(f"Test: D^{alpha} (t^2) at t={t}")
    print(f"Result: {result:.4f}")
    print(f"Expected: {expected:.4f}")
    print(f"Error: {error:.4f}")
    
    return error < 0.1  # Tolerance

if __name__ == "__main__":
    print("="*60)
    print("Fractional Calculus Module - Test")
    print("="*60)
    
    # Test Grünwald-Letnikov weights
    alpha = 0.5
    n = 10
    weights = grunwald_letnikov_weights(alpha, n)
    print(f"\nG-L Weights for α={alpha}:")
    print(weights)
    
    # Test fractional derivative
    print("\n" + "="*60)
    test_passed = test_fractional_derivative()
    print(f"\nTest Result: {'PASSED' if test_passed else 'FAILED'}")
    print("="*60)
