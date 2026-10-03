"""
Stochastic Processes for Rabies Transmission Model
Implements Wiener Process (Brownian Motion) for environmental randomness

Mathematical Background:
    Wiener process W(t) is a continuous-time stochastic process with:
    - W(0) = 0
    - Independent increments
    - W(t) ~ N(0, t) (normally distributed)
    - Continuous paths
    
    Increments: dW(t) = W(t+dt) - W(t) ~ N(0, dt)
    
    In stochastic differential equations:
        dX = μ dt + σ dW(t)
    where:
        μ = drift term
        σ = diffusion coefficient (stochastic intensity)
        dW(t) = Wiener process increment

Reference:
    Research paper: "Fractional-Order Stochastic Transmission Model"
    dI/dt^α = ... + σ * dW(t)
"""

import numpy as np
from typing import Union, Tuple

# ============================================================================
# RANDOM NUMBER GENERATION
# ============================================================================

def box_muller_transform(u1: float = None, u2: float = None) -> Tuple[float, float]:
    """
    Box-Muller transform to generate standard normal random variables
    
    Converts uniform random variables to normal distribution.
    
    Args:
        u1: Uniform random variable in (0, 1), if None generates randomly
        u2: Uniform random variable in (0, 1), if None generates randomly
        
    Returns:
        Tuple[float, float]: Two independent N(0,1) random variables
        
    Formula:
        Z0 = √(-2 ln(U1)) * cos(2π U2)
        Z1 = √(-2 ln(U1)) * sin(2π U2)
    """
    if u1 is None:
        u1 = np.random.uniform(0, 1)
    if u2 is None:
        u2 = np.random.uniform(0, 1)
    
    # Avoid log(0)
    u1 = max(u1, 1e-10)
    
    # Box-Muller transform
    z0 = np.sqrt(-2.0 * np.log(u1)) * np.cos(2.0 * np.pi * u2)
    z1 = np.sqrt(-2.0 * np.log(u1)) * np.sin(2.0 * np.pi * u2)
    
    return z0, z1

def generate_normal_random(mean: float = 0.0, std: float = 1.0, size: int = 1) -> Union[float, np.ndarray]:
    """
    Generate normally distributed random variable(s)
    
    Args:
        mean: Mean of the distribution
        std: Standard deviation
        size: Number of samples to generate
        
    Returns:
        float or np.ndarray: Random sample(s) from N(mean, std²)
    """
    if size == 1:
        z, _ = box_muller_transform()
        return mean + std * z
    else:
        samples = np.zeros(size)
        pairs_needed = (size + 1) // 2
        
        for i in range(pairs_needed):
            z0, z1 = box_muller_transform()
            samples[2*i] = mean + std * z0
            if 2*i + 1 < size:
                samples[2*i + 1] = mean + std * z1
        
        return samples

# ============================================================================
# WIENER PROCESS (BROWNIAN MOTION)
# ============================================================================

def wiener_increment(dt: float, sigma: float = 1.0) -> float:
    """
    Generate a single Wiener process increment dW(t)
    
    For stochastic differential equation:
        dX = μ dt + σ dW(t)
    
    Args:
        dt: Time step
        sigma: Diffusion coefficient (stochastic intensity)
        
    Returns:
        float: Wiener increment dW ~ N(0, dt)
        
    Formula:
        dW(t) = √(dt) * Z
        where Z ~ N(0, 1)
    """
    z = generate_normal_random(mean=0.0, std=1.0)
    return sigma * np.sqrt(dt) * z

def wiener_process(T: float, dt: float, sigma: float = 1.0, W0: float = 0.0) -> np.ndarray:
    """
    Generate a complete Wiener process path W(t) from 0 to T
    
    Args:
        T: Total time period
        dt: Time step
        sigma: Diffusion coefficient
        W0: Initial value (default 0)
        
    Returns:
        np.ndarray: Array of W(t) values at each time step
        
    Properties:
        - W(0) = W0
        - W(t) - W(s) ~ N(0, |t-s|) for t > s
        - Continuous but nowhere differentiable
    """
    n_steps = int(T / dt) + 1
    t_values = np.linspace(0, T, n_steps)
    W = np.zeros(n_steps)
    W[0] = W0
    
    for i in range(1, n_steps):
        dW = wiener_increment(dt, sigma)
        W[i] = W[i-1] + dW
    
    return W

def generate_correlated_wiener(
    T: float, 
    dt: float, 
    n_processes: int, 
    correlation_matrix: np.ndarray = None,
    sigma: float = 1.0
) -> np.ndarray:
    """
    Generate multiple correlated Wiener processes
    
    Useful for modeling correlated stochastic effects across:
    - Different species (dogs, cats, humans)
    - Different municipalities
    
    Args:
        T: Total time period
        dt: Time step
        n_processes: Number of correlated processes
        correlation_matrix: Correlation matrix (n_processes x n_processes)
                          If None, assumes independent processes
        sigma: Base diffusion coefficient
        
    Returns:
        np.ndarray: Shape (n_processes, n_steps) of correlated Wiener paths
    """
    n_steps = int(T / dt) + 1
    
    # Initialize correlation matrix if not provided
    if correlation_matrix is None:
        correlation_matrix = np.eye(n_processes)
    
    # Cholesky decomposition for correlated random variables
    L = np.linalg.cholesky(correlation_matrix)
    
    # Generate independent Wiener processes
    W_independent = np.zeros((n_processes, n_steps))
    
    for i in range(n_processes):
        W_independent[i] = wiener_process(T, dt, sigma)
    
    # Transform to correlated processes using Cholesky decomposition
    W_correlated = L @ W_independent
    
    return W_correlated

# ============================================================================
# STOCHASTIC DIFFERENTIAL EQUATION SOLVERS
# ============================================================================

def euler_maruyama_step(
    x_current: float,
    drift: float,
    diffusion: float,
    dt: float,
    dW: float = None
) -> float:
    """
    Single step of Euler-Maruyama method for SDE
    
    For SDE: dX = μ(X,t) dt + σ(X,t) dW(t)
    
    Args:
        x_current: Current value X(t)
        drift: Drift term μ(X,t)
        diffusion: Diffusion term σ(X,t)
        dt: Time step
        dW: Wiener increment (if None, generates new one)
        
    Returns:
        float: Next value X(t+dt)
        
    Formula:
        X(t+dt) = X(t) + μ(X,t)*dt + σ(X,t)*dW
    """
    if dW is None:
        dW = wiener_increment(dt)
    
    x_next = x_current + drift * dt + diffusion * dW
    
    return x_next

def euler_maruyama_simulate(
    x0: float,
    drift_fn: callable,
    diffusion_fn: callable,
    T: float,
    dt: float,
    t0: float = 0.0
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Simulate SDE using Euler-Maruyama method
    
    For SDE: dX = μ(X,t) dt + σ(X,t) dW(t)
    
    Args:
        x0: Initial condition X(t0)
        drift_fn: Function μ(x, t) returning drift
        diffusion_fn: Function σ(x, t) returning diffusion coefficient
        T: Total simulation time
        dt: Time step
        t0: Initial time
        
    Returns:
        Tuple[np.ndarray, np.ndarray]: (time_array, solution_array)
        
    Example:
        # Geometric Brownian Motion: dS = μS dt + σS dW
        def drift(s, t): return mu * s
        def diffusion(s, t): return sigma * s
        t, S = euler_maruyama_simulate(S0, drift, diffusion, T, dt)
    """
    n_steps = int((T - t0) / dt) + 1
    t_values = np.linspace(t0, T, n_steps)
    x_values = np.zeros(n_steps)
    x_values[0] = x0
    
    for i in range(1, n_steps):
        t = t_values[i-1]
        x = x_values[i-1]
        
        # Evaluate drift and diffusion at current state
        mu_current = drift_fn(x, t)
        sigma_current = diffusion_fn(x, t)
        
        # Generate Wiener increment
        dW = wiener_increment(dt)
        
        # Euler-Maruyama step
        x_values[i] = euler_maruyama_step(x, mu_current, sigma_current, dt, dW)
    
    return t_values, x_values

# ============================================================================
# STOCHASTIC TRANSMISSION MODEL INTEGRATION
# ============================================================================

def apply_stochastic_fluctuation(
    value: float,
    sigma: float,
    dt: float,
    ensure_positive: bool = True
) -> float:
    """
    Apply stochastic fluctuation to a value
    
    Used in transmission model to add environmental randomness:
        X_new = X + σ * dW(t)
    
    Args:
        value: Current value
        sigma: Stochastic intensity
        dt: Time step
        ensure_positive: If True, ensures result ≥ 0 (for populations)
        
    Returns:
        float: Value with stochastic fluctuation applied
    """
    dW = wiener_increment(dt, sigma)
    fluctuated_value = value + dW
    
    if ensure_positive:
        fluctuated_value = max(0.0, fluctuated_value)
    
    return fluctuated_value

def stochastic_transmission_rate(
    base_rate: float,
    sigma: float,
    dt: float,
    min_rate: float = 0.0,
    max_rate: float = 1.0
) -> float:
    """
    Calculate transmission rate with stochastic fluctuation
    
    Models environmental uncertainty in disease transmission:
        β(t) = β_base + σ * dW(t)
    
    Args:
        base_rate: Base transmission rate β
        sigma: Stochastic intensity
        dt: Time step
        min_rate: Minimum allowed rate
        max_rate: Maximum allowed rate
        
    Returns:
        float: Transmission rate with stochastic component
    """
    dW = wiener_increment(dt, sigma)
    rate = base_rate + dW
    
    # Clamp to valid range
    rate = np.clip(rate, min_rate, max_rate)
    
    return rate

# ============================================================================
# TESTING / VALIDATION FUNCTIONS
# ============================================================================

def test_box_muller():
    """Test Box-Muller transform produces normal distribution"""
    print("Testing Box-Muller Transform...")
    
    samples = 10000
    z_values = []
    
    for _ in range(samples // 2):
        z0, z1 = box_muller_transform()
        z_values.extend([z0, z1])
    
    z_values = np.array(z_values[:samples])
    
    mean = np.mean(z_values)
    std = np.std(z_values)
    
    print(f"  Mean: {mean:.4f} (expected: 0.0000)")
    print(f"  Std:  {std:.4f} (expected: 1.0000)")
    
    # Check if approximately normal
    is_normal = abs(mean) < 0.05 and abs(std - 1.0) < 0.05
    print(f"  Result: {'PASS' if is_normal else 'FAIL'}")
    
    return is_normal

def test_wiener_process():
    """Test Wiener process properties"""
    print("\nTesting Wiener Process...")
    
    T = 1.0
    dt = 0.001
    sigma = 1.0
    
    # Generate Wiener process
    W = wiener_process(T, dt, sigma)
    
    # Check initial condition
    assert W[0] == 0.0, "W(0) should be 0"
    print(f"  W(0) = {W[0]:.4f} ✓")
    
    # Check variance scales with time
    # E[W(T)²] = σ² * T
    expected_var = sigma**2 * T
    n_simulations = 1000
    final_values = [wiener_process(T, dt, sigma)[-1] for _ in range(n_simulations)]
    observed_var = np.var(final_values)
    
    print(f"  Expected Var[W(T)]: {expected_var:.4f}")
    print(f"  Observed Var[W(T)]: {observed_var:.4f}")
    
    # Allow 20% tolerance
    is_valid = abs(observed_var - expected_var) / expected_var < 0.2
    print(f"  Result: {'PASS' if is_valid else 'FAIL'}")
    
    return is_valid

def test_euler_maruyama():
    """Test Euler-Maruyama for known SDE"""
    print("\nTesting Euler-Maruyama Method...")
    
    # Test with Geometric Brownian Motion
    # dS = μS dt + σS dW
    # Solution: S(t) = S(0) * exp((μ - σ²/2)t + σW(t))
    
    S0 = 100.0
    mu = 0.05
    sigma = 0.2
    T = 1.0
    dt = 0.001
    
    def drift(s, t):
        return mu * s
    
    def diffusion(s, t):
        return sigma * s
    
    t, S = euler_maruyama_simulate(S0, drift, diffusion, T, dt)
    
    print(f"  Initial value S(0): {S[0]:.2f}")
    print(f"  Final value S(T):   {S[-1]:.2f}")
    print(f"  Mean drift: {mu:.2f}")
    print(f"  Volatility: {sigma:.2f}")
    
    # Check S stays positive (required for Geometric BM)
    all_positive = np.all(S > 0)
    print(f"  All positive: {all_positive}")
    print(f"  Result: {'PASS' if all_positive else 'FAIL'}")
    
    return all_positive

# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Stochastic Processes Module - Tests")
    print("=" * 60)
    
    # Run all tests
    test1 = test_box_muller()
    test2 = test_wiener_process()
    test3 = test_euler_maruyama()
    
    print("\n" + "=" * 60)
    all_passed = test1 and test2 and test3
    print(f"Overall Result: {'ALL TESTS PASSED ✓' if all_passed else 'SOME TESTS FAILED ✗'}")
    print("=" * 60)
