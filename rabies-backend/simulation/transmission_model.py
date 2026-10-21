"""
Fractional-Order Stochastic Transmission Model
Implements the complete mathematical model from the research paper

Mathematical Model:
    dI/dt^α = β * p(t) * S(t) * I(t) / N - γ * I(t) + u(t) + σ * dW(t)

Where:
    α = fractional order (memory effects)
    β = transmission rate
    p(t) = contact probability
    γ = recovery/removal rate
    u(t) = vaccination intervention
    σ = stochastic intensity
    dW(t) = Wiener process

This model combines:
    1. Fractional derivatives (memory effects)
    2. Stochastic processes (environmental randomness)
    3. Multi-species transmission (dogs, cats, humans)
    4. Spatial heterogeneity (population density)
    5. Inter-municipality transmission (network effects)

Reference:
    Research paper: "Fractional-Order Stochastic Transmission Model"

IMPORTANT - CAT TRANSMISSION PARAMETERS (October 2026):
    Extensive literature review found NO published studies quantifying:
    - Cat-to-cat transmission rates vs dog-to-dog
    - Dog-to-cat cross-species transmission coefficients
    
    Key Research Findings:
    - Dogs are primary rabies reservoir (>95-99% of human cases) [WHO, 2026]
    - Cats are spillover hosts, NOT maintenance hosts
    - No sustained cat-only epidemics documented
    - 10-day infectious period validated for both species [CDC, Merck Manual]
    
    Parameters 0.7 and 0.4 in this model are MODELING ASSUMPTIONS
    representing conservative estimates for dog-endemic areas.
    These require empirical validation through future research.
    
    See detailed documentation in: TRANSMISSION_PARAMETERS_RESEARCH.md
"""

import numpy as np
from typing import List, Dict, Tuple
from dataclasses import dataclass

try:
    # Try relative imports (when run as module)
    from .fractional_calculus import fractional_derivative, grunwald_letnikov_weights
    from .stochastic_processes import wiener_increment, euler_maruyama_step
except ImportError:
    # Try absolute imports (when run as script)
    from fractional_calculus import fractional_derivative, grunwald_letnikov_weights
    from stochastic_processes import wiener_increment, euler_maruyama_step

# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class Population:
    """
    Population compartments for SI+V+BD model
    
    PHASE 2 UPDATE: Changed from SIRV to SI+V
    - Removed: recovered (rabies is fatal, no recovery in SI model)
    - Added: birth/death tracking for statistics
    """
    susceptible: float
    infected: float
    # recovered: float  # REMOVED in Phase 2 - SI model has no recovery
    vaccinated: float
    total: float
    
    # PHASE 2: Track cumulative statistics
    cumulative_births: float = 0.0
    cumulative_natural_deaths: float = 0.0
    cumulative_rabies_deaths: float = 0.0
    cumulative_vaccinations: float = 0.0
    
    # Track initial state for comparison
    initial_total: float = 0.0
    initial_infected: float = 0.0

@dataclass
class SimulationParameters:
    """
    Parameters for SI+V+BD transmission model
    
    PHASE 2 UPDATE: Added all Phase 1 parameters for births, deaths, and explicit transmission
    """
    # Fractional-order parameter
    alpha: float = 0.95  # α ∈ (0, 1]
    
    # Time step
    dt: float = 0.1  # Time step (0.1 day)
    
    # Contact probability
    contact_probability: float = 0.3  # p - contact probability
    
    # Vaccination
    vaccination_rate: float = 0.0  # u - target vaccination coverage
    
    # Spatial
    use_spatial_heterogeneity: bool = True
    
    # =================================================================
    # PHASE 2: NEW PARAMETERS (from Phase 1)
    # =================================================================
    
    # Birth Rates (Λ)
    lambda_dog: float = 0.00050335  # Midpoint of observed range (0.004167-0.005900 per day)
    lambda_cat: float = 0.0004356  # Updated from demographic data
    lambda_human: float = 0.00003288  # Updated from demographic data
    
    # Natural Mortality (μ)
    mu_dog: float = 0.000397  # Updated from literature
    mu_cat: float = 0.000274  # Updated from demographic data
    mu_human: float = 0.00001699  # Updated from demographic data
    
    # Rabies Mortality (δ)
    delta_dog: float = 0.1
    delta_cat: float = 0.12
    delta_human: float = 0.15
    
    # Stochastic Intensities (σ) - Species-specific
    sigma_1: float = 0.1  # Dogs
    sigma_2: float = 0.08  # Cats
    sigma_3: float = 0.05  # Humans
    
    # Transmission Coefficients (β) - Explicit
    beta_dd: float = 0.15   # Dog-to-dog
    beta_dc: float = 0.06   # Dog-to-cat
    beta_cc: float = 0.105  # Cat-to-cat
    beta_dh: float = 0.0015  # Dog-to-human
    beta_ch: float = 0.00075  # Cat-to-human
    
    # =================================================================
    # LEGACY PARAMETERS (for backward compatibility - NOT USED in Phase 2)
    # =================================================================
    beta: float = 0.15  # Legacy - replaced by explicit beta coefficients
    gamma: float = 0.1  # Legacy - NOT USED (no recovery in SI model)
    sigma: float = 0.1  # Legacy - replaced by sigma_1, sigma_2, sigma_3
    
@dataclass
class MunicipalityState:
    """State of a single municipality"""
    id: str
    name: str
    
    # Populations
    dogs: Population
    cats: Population
    humans: Population
    
    # Geographic
    population_density: float  # ρ (persons/km²)
    
    # Network
    connected_municipalities: List[str]
    
    # History for fractional derivatives
    infected_dogs_history: List[float]
    infected_cats_history: List[float]
    infected_humans_history: List[float]

# ============================================================================
# PHASE 2: HELPER FUNCTIONS FOR SI+V+BD MODEL
# ============================================================================

def calculate_births(lambda_rate: float, total_population: float, dt: float) -> float:
    """
    Calculate births using recruitment rate Λ
    
    Formula: Births = Λ * N * dt
    
    Args:
        lambda_rate: Birth rate Λ (births per individual per day)
        total_population: Total population N
        dt: Time step
        
    Returns:
        float: Number of births in this time step
        
    Example:
        λ_dog = 0.0001 (1 birth per 10,000 dogs per day)
        N_dog = 1000 dogs
        dt = 0.1 days
        births = 0.0001 * 1000 * 0.1 = 0.01 births
    """
    births = lambda_rate * total_population * dt
    return max(0.0, births)


def calculate_natural_deaths(mu_rate: float, population: float, dt: float) -> float:
    """
    Calculate natural deaths (excluding rabies) using mortality rate μ
    
    Formula: Natural Deaths = μ * Population * dt
    
    Args:
        mu_rate: Natural mortality rate μ (deaths per individual per day)
        population: Current population size
        dt: Time step
        
    Returns:
        float: Number of natural deaths in this time step
        
    Example:
        μ_dog = 0.0001 (1 death per 10,000 dogs per day)
        S_dog = 5000 susceptible dogs
        dt = 0.1 days
        deaths = 0.0001 * 5000 * 0.1 = 0.05 deaths
    """
    deaths = mu_rate * population * dt
    return max(0.0, min(deaths, population))


def calculate_rabies_deaths(delta_rate: float, infected: float, dt: float) -> float:
    """
    Calculate rabies-specific deaths using disease mortality rate δ
    
    Formula: Rabies Deaths = δ * I * dt
    
    Args:
        delta_rate: Rabies mortality rate δ (disease deaths per infected per day)
        infected: Current infected population I
        dt: Time step
        
    Returns:
        float: Number of rabies deaths in this time step
        
    Example:
        δ_dog = 0.1 (average 10-day survival)
        I_dog = 100 infected dogs
        dt = 0.1 days
        deaths = 0.1 * 100 * 0.1 = 1 death
    """
    deaths = delta_rate * infected * dt
    return max(0.0, min(deaths, infected))


def generate_independent_wiener_processes(
    dt: float,
    sigma_values: List[float]
) -> List[float]:
    """
    Generate multiple INDEPENDENT Wiener process increments
    
    This is critical for SI+V+BD model:
    - Dogs get their own independent noise: dW₁
    - Cats get their own independent noise: dW₂
    - Humans get their own independent noise: dW₃
    
    Formula: dW_i ~ N(0, dt) for each species independently
    
    Args:
        dt: Time step
        sigma_values: List of stochastic intensities [σ₁, σ₂, σ₃]
        
    Returns:
        List[float]: Independent Wiener increments [dW₁, dW₂, dW₃]
        
    Example:
        dt = 0.1 days
        sigma_values = [0.1, 0.08, 0.05]  # dog, cat, human
        dW_list = generate_independent_wiener_processes(0.1, [0.1, 0.08, 0.05])
        # Returns: [dW₁, dW₂, dW₃] - all independent random values
    """
    wiener_increments = []
    
    for sigma in sigma_values:
        # Generate independent Wiener increment for this species
        dW = wiener_increment(dt, sigma)
        wiener_increments.append(dW)
    
    return wiener_increments


def calculate_transmission(
    susceptible: float,
    infected: float,
    total_population: float,
    beta_coefficient: float,
    contact_prob: float,
    dt: float
) -> float:
    """
    Calculate new infections using explicit transmission coefficient
    
    Formula: New Infections = β * p * (S * I / N) * dt
    
    Args:
        susceptible: Susceptible population S
        infected: Infected population I
        total_population: Total population N
        beta_coefficient: Explicit transmission coefficient (β_dd, β_dc, etc.)
        contact_prob: Contact probability p
        dt: Time step
        
    Returns:
        float: Number of new infections
        
    Example:
        β_dd = 0.15 (dog-to-dog transmission)
        p = 0.3 (contact probability)
        S = 900, I = 100, N = 1000
        dt = 0.1
        infections = 0.15 * 0.3 * (900 * 100 / 1000) * 0.1 = 0.405 new infections
    """
    if total_population <= 0 or susceptible <= 0 or infected <= 0:
        return 0.0
    
    transmission_rate = beta_coefficient * contact_prob
    new_infections = transmission_rate * (susceptible * infected / total_population) * dt
    
    # Physical constraints
    new_infections = max(0.0, min(new_infections, susceptible))
    
    return new_infections


def calculate_vaccination(
    susceptible: float,
    vaccinated: float,
    total_population: float,
    target_coverage: float,
    daily_capacity: float,
    dt: float
) -> float:
    """
    Calculate vaccination intervention u(t)
    
    Formula: u(t) = min(daily_capacity * dt, susceptible, needed_to_reach_target)
    
    Args:
        susceptible: Current susceptible S
        vaccinated: Current vaccinated V
        total_population: Total population N
        target_coverage: Target vaccination coverage (0-1)
        daily_capacity: Maximum vaccinations per day
        dt: Time step
        
    Returns:
        float: Number of new vaccinations in this step
        
    Example:
        Target: 80% coverage
        Current: 50% vaccinated
        Susceptible: 500
        Capacity: 100 per day
        dt = 0.1
        vaccinations = min(100*0.1, 500, needed) = 10 vaccinations
    """
    if total_population <= 0:
        return 0.0
    
    # Current coverage
    current_coverage = vaccinated / total_population if total_population > 0 else 0.0
    
    # Already at target?
    if current_coverage >= target_coverage:
        return 0.0
    
    # How many vaccinations needed to reach target?
    target_vaccinated = target_coverage * total_population
    needed = target_vaccinated - vaccinated
    
    # Limited by capacity and susceptible available
    max_this_step = daily_capacity * dt
    new_vaccinations = min(max_this_step, susceptible, needed)
    
    return max(0.0, new_vaccinations)

# ============================================================================
# TRANSMISSION DYNAMICS
# ============================================================================

def calculate_transmission_rate(
    beta: float,
    contact_prob: float,
    population_density: float,
    use_spatial: bool = True
) -> float:
    """
    Calculate effective transmission rate with spatial heterogeneity
    
    Formula:
        β_eff = β * p(t) * f(ρ)
    
    where:
        β = base transmission rate
        p(t) = contact probability
        f(ρ) = spatial heterogeneity factor based on density ρ
    
    Args:
        beta: Base transmission rate
        contact_prob: Contact probability
        population_density: ρ (persons/km²)
        use_spatial: Apply spatial heterogeneity
        
    Returns:
        float: Effective transmission rate
    """
    beta_eff = beta * contact_prob
    
    if use_spatial and population_density > 0:
        # Spatial heterogeneity: higher density = higher transmission
        # f(ρ) = 1 + (ρ / ρ_ref) * factor
        rho_ref = 200.0  # Reference density (persons/km²)
        spatial_factor = 0.2  # Scaling factor
        f_rho = 1.0 + (population_density / rho_ref) * spatial_factor
        beta_eff *= f_rho
    
    return beta_eff

def intra_species_transmission(
    susceptible: float,
    infected: float,
    total_population: float,
    beta_eff: float,
    gamma: float,
    alpha: float,
    sigma: float,
    dt: float,
    infected_history: List[float]
) -> Tuple[float, float]:
    """
    Calculate new infections within a single species
    
    Fractional-order stochastic SIR:
        dS/dt^α = -β_eff * S * I / N
        dI/dt^α = β_eff * S * I / N - γ * I + σ * dW(t)
        dR/dt^α = γ * I
    
    Args:
        susceptible: S(t)
        infected: I(t)
        total_population: N
        beta_eff: Effective transmission rate
        gamma: Recovery rate
        alpha: Fractional order
        sigma: Stochastic intensity
        dt: Time step
        infected_history: Past infected values for fractional derivative
        
    Returns:
        Tuple[float, float]: (new_infections, new_recoveries)
    """
    if total_population <= 0 or susceptible <= 0:
        return 0.0, 0.0
    
    # Apply stochastic fluctuation to transmission rate
    # This makes environmental uncertainty (σ) affect the infection dynamics
    dW = wiener_increment(dt, sigma)
    stochastic_multiplier = 1.0 + dW  # Fluctuate around 1.0
    
    # Ensure positive multiplier (minimum 10% of base rate)
    stochastic_multiplier = max(0.1, stochastic_multiplier)
    
    # Standard transmission term WITH stochastic component applied
    transmission_term = beta_eff * susceptible * infected / total_population
    transmission_term *= stochastic_multiplier  # ✅ Apply environmental uncertainty
    
    # Recovery term
    recovery_term = gamma * infected
    
    # Fractional derivative of infected
    if len(infected_history) > 1:
        D_alpha_I = fractional_derivative(
            np.array(infected_history),
            alpha,
            dt
        )
    else:
        D_alpha_I = 0.0
    
    # Calculate new infections and recoveries (now includes stochastic effect)
    new_infections = max(0.0, transmission_term * dt)
    new_recoveries = max(0.0, recovery_term * dt)
    
    # Ensure physical constraints
    new_infections = min(new_infections, susceptible)
    new_recoveries = min(new_recoveries, infected)
    
    return new_infections, new_recoveries

def cross_species_transmission(
    susceptible_target: float,
    infected_source: float,
    total_source: float,
    beta_eff: float,
    cross_species_factor: float,
    dt: float
) -> float:
    """
    Calculate cross-species transmission (e.g., dog to cat, dog to human)
    
    Rate is reduced compared to intra-species transmission.
    
    Args:
        susceptible_target: Susceptible in target species
        infected_source: Infected in source species
        total_source: Total population of source species
        beta_eff: Effective transmission rate
        cross_species_factor: Reduction factor (0-1)
        dt: Time step
        
    Returns:
        float: New infections in target species from source
    """
    if total_source <= 0 or susceptible_target <= 0:
        return 0.0
    
    # Cross-species transmission with reduced rate
    transmission_rate = beta_eff * cross_species_factor
    transmission = transmission_rate * susceptible_target * infected_source / total_source
    new_infections = transmission * dt
    
    # Ensure physical constraints
    new_infections = max(0.0, min(new_infections, susceptible_target))
    
    return new_infections

def inter_municipality_transmission(
    susceptible_local: float,
    infected_neighbor: float,
    total_neighbor: float,
    beta_eff: float,
    dt: float,
    reduction_factor: float = 0.3
) -> float:
    """
    Calculate inter-municipality transmission (spatial spread)
    
    Transmission between connected municipalities is reduced.
    
    Args:
        susceptible_local: Susceptible in local municipality
        infected_neighbor: Infected in neighboring municipality
        total_neighbor: Total population in neighbor
        beta_eff: Effective transmission rate
        dt: Time step
        reduction_factor: Spatial reduction (default 0.3)
        
    Returns:
        float: New infections from neighbor
    """
    if total_neighbor <= 0 or susceptible_local <= 0:
        return 0.0
    
    # Inter-municipality transmission with spatial reduction
    transmission_rate = beta_eff * reduction_factor
    transmission = transmission_rate * susceptible_local * infected_neighbor / total_neighbor
    new_infections = transmission * dt
    
    # Ensure physical constraints
    new_infections = max(0.0, min(new_infections, susceptible_local))
    
    return new_infections

# ============================================================================
# VACCINATION INTERVENTION
# ============================================================================

def apply_vaccination(
    susceptible: float,
    vaccinated: float,
    total_population: float,
    target_coverage: float,
    daily_rate: float,
    dt: float
) -> float:
    """
    Apply vaccination intervention u(t)
    
    Args:
        susceptible: Current susceptible
        vaccinated: Current vaccinated
        total_population: Total population
        target_coverage: Target vaccination coverage (0-1)
        daily_rate: Maximum daily vaccination rate
        dt: Time step
        
    Returns:
        float: Number of new vaccinations in this time step
    """
    if total_population <= 0:
        return 0.0
    
    # Current coverage
    current_coverage = vaccinated / total_population
    
    # If already at target, no more vaccination
    if current_coverage >= target_coverage:
        return 0.0
    
    # Maximum vaccinations this step
    max_vaccinations = daily_rate * dt
    
    # Actual vaccinations (limited by susceptible available)
    new_vaccinations = min(max_vaccinations, susceptible)
    
    return new_vaccinations

# ============================================================================
# MAIN SIMULATION ENGINE
# ============================================================================

def simulate_municipality_step(
    state: MunicipalityState,
    params: SimulationParameters,
    neighbor_states: Dict[str, MunicipalityState]
) -> MunicipalityState:
    """
    Simulate one time step for a single municipality
    
    Updates all species (dogs, cats, humans) with:
    - Intra-species transmission
    - Cross-species transmission
    - Inter-municipality transmission
    - Vaccination
    - Recovery
    
    Args:
        state: Current municipality state
        params: Simulation parameters
        neighbor_states: States of connected municipalities
        
    Returns:
        MunicipalityState: Updated state
    """
    dt = params.dt
    
    # Calculate effective transmission rate for this municipality
    beta_eff = calculate_transmission_rate(
        params.beta,
        params.contact_probability,
        state.population_density,
        params.use_spatial_heterogeneity
    )
    
    # ========================================================================
    # DOGS - Primary rabies reservoir (SI+V+BD Model)
    # ========================================================================
    # Equations from Formulas.docx:
    # dS_d/dt^α = Λ_d - β_dd(S_d·I_d)/N_d - μ_d·S_d - u_d(t)
    # dI_d/dt^α = β_dd(S_d·I_d)/N_d - (μ_d + δ_d)·I_d + σ₁·dW₁(t)
    # dV_d/dt = u_d(t) - μ_d·V_d
    # ========================================================================
    
    # Current populations
    S_dog = state.dogs.susceptible
    I_dog = state.dogs.infected
    V_dog = state.dogs.vaccinated
    N_dog = state.dogs.total
    
    # Generate independent Wiener processes for all species (dogs, cats, humans)
    sigma_values = [params.sigma_1, params.sigma_2, params.sigma_3]
    dW1, dW2, dW3 = generate_independent_wiener_processes(dt, sigma_values)
    
    # --- SUSCEPTIBLE DOGS: dS_d/dt^α = Λ_d - β_dd(S_d·I_d)/N_d - μ_d·S_d - u_d(t) ---
    
    # Births: Λ_d
    dog_births = calculate_births(params.lambda_dog, N_dog, dt)
    
    # Infections: β_dd(S_d·I_d)/N_d (intra-species dog-to-dog)
    dog_infections_intra = calculate_transmission(
        S_dog, I_dog, N_dog,
        params.beta_dd,
        params.contact_probability,
        dt
    )
    
    # Inter-municipality infections (dogs from neighbors)
    dog_infections_external = 0.0
    for neighbor_id in state.connected_municipalities:
        if neighbor_id in neighbor_states:
            neighbor = neighbor_states[neighbor_id]
            dog_infections_external += calculate_transmission(
                S_dog,
                neighbor.dogs.infected,
                neighbor.dogs.total,
                params.beta_dd,
                params.contact_probability * 0.3,  # Reduced for inter-municipality
                dt
            )
    
    # Total new infections
    dog_infections_total = dog_infections_intra + dog_infections_external
    
    # Natural deaths from susceptible: μ_d·S_d
    dog_natural_deaths_S = calculate_natural_deaths(params.mu_dog, S_dog, dt)
    
    # Vaccination: u_d(t)
    dog_vaccinations = calculate_vaccination(
        S_dog, V_dog, N_dog,
        params.vaccination_rate,
        state.dogs.total * 0.05,  # 5% of population per day max capacity
        dt
    )
    
    # Update susceptible: S_d(t+dt) = S_d(t) + Λ_d - β_dd(S·I/N) - μ_d·S_d - u_d(t)
    S_dog_new = S_dog + dog_births - dog_infections_total - dog_natural_deaths_S - dog_vaccinations
    
    # --- INFECTED DOGS: dI_d/dt^α = β_dd(S_d·I_d)/N_d - (μ_d + δ_d)·I_d + σ₁·dW₁(t) ---
    
    # Natural deaths from infected: μ_d·I_d
    dog_natural_deaths_I = calculate_natural_deaths(params.mu_dog, I_dog, dt)
    
    # Rabies deaths: δ_d·I_d
    dog_rabies_deaths = calculate_rabies_deaths(params.delta_dog, I_dog, dt)
    
    # Stochastic term: σ₁·dW₁(t)
    dog_stochastic_term = dW1  # Already includes σ₁
    
    # Update infected: I_d(t+dt) = I_d(t) + β_dd(S·I/N) - (μ_d + δ_d)·I_d + σ₁·dW₁
    I_dog_new = I_dog + dog_infections_total - dog_natural_deaths_I - dog_rabies_deaths + dog_stochastic_term
    
    # --- VACCINATED DOGS: dV_d/dt = u_d(t) - μ_d·V_d ---
    
    # Natural deaths from vaccinated: μ_d·V_d
    dog_natural_deaths_V = calculate_natural_deaths(params.mu_dog, V_dog, dt)
    
    # Update vaccinated: V_d(t+dt) = V_d(t) + u_d(t) - μ_d·V_d
    V_dog_new = V_dog + dog_vaccinations - dog_natural_deaths_V
    
    # --- Update dog population ---
    state.dogs.susceptible = max(0.0, S_dog_new)
    state.dogs.infected = max(0.0, I_dog_new)
    state.dogs.vaccinated = max(0.0, V_dog_new)
    
    # Update total population: N_d = S_d + I_d + V_d
    state.dogs.total = state.dogs.susceptible + state.dogs.infected + state.dogs.vaccinated
    
    # Track cumulative statistics
    state.dogs.cumulative_births += dog_births
    state.dogs.cumulative_natural_deaths += (dog_natural_deaths_S + dog_natural_deaths_I + dog_natural_deaths_V)
    state.dogs.cumulative_rabies_deaths += dog_rabies_deaths
    state.dogs.cumulative_vaccinations += dog_vaccinations
    
    # Update history
    state.infected_dogs_history.append(state.dogs.infected)
    if len(state.infected_dogs_history) > 100:  # Keep last 100 values
        state.infected_dogs_history.pop(0)
    
    # ========================================================================
    # CATS - Secondary hosts (SI+V+BD Model)
    # ========================================================================
    # Equations from Formulas.docx:
    # dS_c/dt^α = Λ_c - β_dc(S_c·I_d)/N_d - β_cc(S_c·I_c)/N_c - μ_c·S_c - u_c(t)
    # dI_c/dt^α = β_dc(S_c·I_d)/N_d + β_cc(S_c·I_c)/N_c - (μ_c + δ_c)·I_c + σ₂·dW₂(t)
    # dV_c/dt = u_c(t) - μ_c·V_c
    # ========================================================================
    # RESEARCH NOTE: Cats are spillover hosts, not maintenance hosts.
    # They get infected primarily from dogs (β_dc) with secondary cat-to-cat spread (β_cc).
    # ========================================================================
    
    # Current populations
    S_cat = state.cats.susceptible
    I_cat = state.cats.infected
    V_cat = state.cats.vaccinated
    N_cat = state.cats.total
    
    # Note: dW2 already generated above for all species
    
    # --- SUSCEPTIBLE CATS: dS_c/dt^α = Λ_c - β_dc(S_c·I_d)/N_d - β_cc(S_c·I_c)/N_c - μ_c·S_c - u_c(t) ---
    
    # Births: Λ_c
    cat_births = calculate_births(params.lambda_cat, N_cat, dt)
    
    # Dog-to-cat transmission: β_dc(S_c·I_d)/N_d (cross-species from primary reservoir)
    cat_infections_from_dogs = calculate_transmission(
        S_cat, I_dog, N_dog,
        params.beta_dc,
        params.contact_probability,
        dt
    )
    
    # Cat-to-cat transmission: β_cc(S_c·I_c)/N_c (intra-species secondary spread)
    cat_infections_intra = calculate_transmission(
        S_cat, I_cat, N_cat,
        params.beta_cc,
        params.contact_probability,
        dt
    )
    
    # Inter-municipality infections (cats from neighbors)
    cat_infections_external = 0.0
    for neighbor_id in state.connected_municipalities:
        if neighbor_id in neighbor_states:
            neighbor = neighbor_states[neighbor_id]
            cat_infections_external += calculate_transmission(
                S_cat,
                neighbor.cats.infected,
                neighbor.cats.total,
                params.beta_cc,
                params.contact_probability * 0.2,  # Cats have lower inter-municipality movement
                dt
            )
    
    # Total new infections
    cat_infections_total = cat_infections_from_dogs + cat_infections_intra + cat_infections_external
    
    # Natural deaths from susceptible: μ_c·S_c
    cat_natural_deaths_S = calculate_natural_deaths(params.mu_cat, S_cat, dt)
    
    # Vaccination: u_c(t) - Note: cats typically have lower vaccination rates than dogs
    cat_vaccinations = calculate_vaccination(
        S_cat, V_cat, N_cat,
        params.vaccination_rate * 0.5,  # Cats: 50% of dog vaccination rate (harder to reach)
        state.cats.total * 0.03,  # 3% of population per day max capacity (lower than dogs)
        dt
    )
    
    # Update susceptible: S_c(t+dt) = S_c(t) + Λ_c - β_dc(S_c·I_d)/N_d - β_cc(S_c·I_c)/N_c - μ_c·S_c - u_c(t)
    S_cat_new = S_cat + cat_births - cat_infections_total - cat_natural_deaths_S - cat_vaccinations
    
    # --- INFECTED CATS: dI_c/dt^α = β_dc(S_c·I_d)/N_d + β_cc(S_c·I_c)/N_c - (μ_c + δ_c)·I_c + σ₂·dW₂(t) ---
    
    # Natural deaths from infected: μ_c·I_c
    cat_natural_deaths_I = calculate_natural_deaths(params.mu_cat, I_cat, dt)
    
    # Rabies deaths: δ_c·I_c
    cat_rabies_deaths = calculate_rabies_deaths(params.delta_cat, I_cat, dt)
    
    # Stochastic term: σ₂·dW₂(t) - Independent from dog noise
    cat_stochastic_term = dW2  # Already includes σ₂
    
    # Update infected: I_c(t+dt) = I_c(t) + infections - (μ_c + δ_c)·I_c + σ₂·dW₂
    I_cat_new = I_cat + cat_infections_total - cat_natural_deaths_I - cat_rabies_deaths + cat_stochastic_term
    
    # --- VACCINATED CATS: dV_c/dt = u_c(t) - μ_c·V_c ---
    
    # Natural deaths from vaccinated: μ_c·V_c
    cat_natural_deaths_V = calculate_natural_deaths(params.mu_cat, V_cat, dt)
    
    # Update vaccinated: V_c(t+dt) = V_c(t) + u_c(t) - μ_c·V_c
    V_cat_new = V_cat + cat_vaccinations - cat_natural_deaths_V
    
    # --- Update cat population ---
    state.cats.susceptible = max(0.0, S_cat_new)
    state.cats.infected = max(0.0, I_cat_new)
    state.cats.vaccinated = max(0.0, V_cat_new)
    
    # Update total population: N_c = S_c + I_c + V_c
    state.cats.total = state.cats.susceptible + state.cats.infected + state.cats.vaccinated
    
    # Track cumulative statistics
    state.cats.cumulative_births += cat_births
    state.cats.cumulative_natural_deaths += (cat_natural_deaths_S + cat_natural_deaths_I + cat_natural_deaths_V)
    state.cats.cumulative_rabies_deaths += cat_rabies_deaths
    state.cats.cumulative_vaccinations += cat_vaccinations
    
    # Update history
    state.infected_cats_history.append(state.cats.infected)
    if len(state.infected_cats_history) > 100:
        state.infected_cats_history.pop(0)
    
    # ========================================================================
    # HUMANS - End hosts (SI+V+BD Model)
    # ========================================================================
    # Equations from Formulas.docx:
    # dS_h/dt^α = Λ_h - β_dh(S_h·I_d)/N_d - β_ch(S_h·I_c)/N_c - μ_h·S_h
    # dI_h/dt^α = β_dh(S_h·I_d)/N_d + β_ch(S_h·I_c)/N_c - (μ_h + δ_h)·I_h + σ₃·dW₃(t)
    # ========================================================================
    # RESEARCH NOTE: 
    # - Humans are END HOSTS (no human-to-human transmission)
    # - Get infected from animal bites (dogs > cats)
    # - Rabies is nearly 100% fatal without PEP (post-exposure prophylaxis)
    # - No pre-exposure vaccination compartment (PEP is reactive, not proactive)
    # ========================================================================
    
    # Current populations
    S_human = state.humans.susceptible
    I_human = state.humans.infected
    V_human = state.humans.vaccinated
    N_human = state.humans.total
    
    # Note: dW3 already generated above for all species
    
    # --- SUSCEPTIBLE HUMANS: dS_h/dt^α = Λ_h - β_dh(S_h·I_d)/N_d - β_ch(S_h·I_c)/N_c - μ_h·S_h ---
    
    # Births: Λ_h
    human_births = calculate_births(params.lambda_human, N_human, dt)
    
    # Dog-to-human transmission: β_dh(S_h·I_d)/N_d (primary source of human rabies)
    human_infections_from_dogs = calculate_transmission(
        S_human, I_dog, N_dog,
        params.beta_dh,
        params.contact_probability * 0.1,  # Very low - not all contacts are bites
        dt
    )
    
    # Cat-to-human transmission: β_ch(S_h·I_c)/N_c (secondary source)
    human_infections_from_cats = calculate_transmission(
        S_human, I_cat, N_cat,
        params.beta_ch,
        params.contact_probability * 0.1,  # Very low - not all contacts are bites
        dt
    )
    
    # Total new infections (NO human-to-human transmission - end host)
    human_infections_total = human_infections_from_dogs + human_infections_from_cats
    
    # Natural deaths from susceptible: μ_h·S_h
    human_natural_deaths_S = calculate_natural_deaths(params.mu_human, S_human, dt)
    
    # Note: No vaccination for humans in the traditional sense
    # PEP (post-exposure prophylaxis) is reactive, not proactive
    # For now, we can include a small vaccination rate for high-risk individuals
    human_vaccinations = calculate_vaccination(
        S_human, V_human, N_human,
        params.vaccination_rate * 0.01,  # Very low - only high-risk individuals (vets, etc.)
        state.humans.total * 0.001,  # 0.1% of population per day max capacity
        dt
    )
    
    # Update susceptible: S_h(t+dt) = S_h(t) + Λ_h - β_dh(S_h·I_d)/N_d - β_ch(S_h·I_c)/N_c - μ_h·S_h - u_h(t)
    S_human_new = S_human + human_births - human_infections_total - human_natural_deaths_S - human_vaccinations
    
    # --- INFECTED HUMANS: dI_h/dt^α = β_dh(S_h·I_d)/N_d + β_ch(S_h·I_c)/N_c - (μ_h + δ_h)·I_h + σ₃·dW₃(t) ---
    
    # Natural deaths from infected: μ_h·I_h
    human_natural_deaths_I = calculate_natural_deaths(params.mu_human, I_human, dt)
    
    # Rabies deaths: δ_h·I_h
    # Note: δ_h is very high because without PEP, rabies is nearly 100% fatal
    human_rabies_deaths = calculate_rabies_deaths(params.delta_human, I_human, dt)
    
    # Stochastic term: σ₃·dW₃(t) - Independent from dogs and cats
    human_stochastic_term = dW3  # Already includes σ₃
    
    # Update infected: I_h(t+dt) = I_h(t) + infections - (μ_h + δ_h)·I_h + σ₃·dW₃
    I_human_new = I_human + human_infections_total - human_natural_deaths_I - human_rabies_deaths + human_stochastic_term
    
    # --- VACCINATED HUMANS: dV_h/dt = u_h(t) - μ_h·V_h ---
    # Note: This represents pre-exposure prophylaxis for high-risk individuals
    
    # Natural deaths from vaccinated: μ_h·V_h
    human_natural_deaths_V = calculate_natural_deaths(params.mu_human, V_human, dt)
    
    # Update vaccinated: V_h(t+dt) = V_h(t) + u_h(t) - μ_h·V_h
    V_human_new = V_human + human_vaccinations - human_natural_deaths_V
    
    # --- Update human population ---
    state.humans.susceptible = max(0.0, S_human_new)
    state.humans.infected = max(0.0, I_human_new)
    state.humans.vaccinated = max(0.0, V_human_new)
    
    # Update total population: N_h = S_h + I_h + V_h
    state.humans.total = state.humans.susceptible + state.humans.infected + state.humans.vaccinated
    
    # Track cumulative statistics
    state.humans.cumulative_births += human_births
    state.humans.cumulative_natural_deaths += (human_natural_deaths_S + human_natural_deaths_I + human_natural_deaths_V)
    state.humans.cumulative_rabies_deaths += human_rabies_deaths
    state.humans.cumulative_vaccinations += human_vaccinations
    
    # Update history
    state.infected_humans_history.append(state.humans.infected)
    if len(state.infected_humans_history) > 100:
        state.infected_humans_history.pop(0)
    
    return state

def run_fractional_stochastic_simulation(
    municipalities: List[Dict],
    settings: Dict
) -> List[Dict]:
    """
    Run complete fractional-order stochastic simulation
    
    This is the MAIN ENTRY POINT called by the FastAPI endpoint.
    
    Args:
        municipalities: List of municipality data from frontend
        settings: Simulation settings
        
    Returns:
        List[Dict]: Updated municipalities with simulation results
    """
    print(f"[DEBUG] run_fractional_stochastic_simulation called with {len(municipalities)} municipalities")
    
    # Convert global parameters (used as defaults)
    global_params = SimulationParameters(
        alpha=settings.fractionalOrder,
        beta=settings.transmissionRate,
        gamma=settings.recoveryRate,
        contact_probability=settings.contactProbability,
        sigma=settings.stochasticIntensity,
        vaccination_rate=settings.vaccinationRate,
        dt=0.1  # 0.1 day time step
    )
    
    simulation_days = settings.simulationDays
    n_steps = int(simulation_days / global_params.dt)
    
    # Initialize municipality states with custom parameters
    states = {}
    municipality_params = {}  # Store custom parameters for each municipality
    
    for mun in municipalities:
        # Create municipality-specific parameters (use custom if available, otherwise global)
        custom_params = SimulationParameters(
            alpha=global_params.alpha,  # Fractional order remains global
            beta=getattr(mun, 'customTransmissionRate', global_params.beta),
            gamma=global_params.gamma,  # Recovery rate remains global  
            contact_probability=global_params.contact_probability,
            sigma=getattr(mun, 'customEnvironmentalFactor', global_params.sigma),
            vaccination_rate=getattr(mun, 'customVaccinationRate', global_params.vaccination_rate),
            dt=global_params.dt
        )
        
        # Store contact multiplier for this municipality
        contact_multiplier = getattr(mun, 'customContactMultiplier', 1.0)
        custom_params.contact_probability *= contact_multiplier
        
        municipality_params[mun.id] = custom_params
        
        print(f"🏙️ {mun.name}: Custom params = {getattr(mun, 'hasCustomParameters', False)}")
        if getattr(mun, 'hasCustomParameters', False):
            print(f"   📊 Transmission: {custom_params.beta:.4f}, Vaccination: {custom_params.vaccination_rate:.3f}")
        
        # Create population compartments
        dog_total = mun.dogPopulation
        dog_infected = mun.infectedDogs
        dog_vaccinated = mun.vaccinatedDogs
        dog_susceptible = dog_total - dog_infected - dog_vaccinated
        
        cat_total = mun.catPopulation
        cat_infected = mun.infectedCats
        cat_susceptible = cat_total - cat_infected
        
        human_total = mun.humanPopulation
        human_infected = mun.infectedHumans
        human_susceptible = human_total - human_infected
        
        states[mun.id] = MunicipalityState(
            id=mun.id,
            name=mun.name,
            dogs=Population(
                susceptible=dog_susceptible, 
                infected=dog_infected, 
                vaccinated=dog_vaccinated, 
                total=dog_total,
                initial_total=dog_total,
                initial_infected=dog_infected
            ),
            cats=Population(
                susceptible=cat_susceptible, 
                infected=cat_infected, 
                vaccinated=0, 
                total=cat_total,
                initial_total=cat_total,
                initial_infected=cat_infected
            ),
            humans=Population(
                susceptible=human_susceptible, 
                infected=human_infected, 
                vaccinated=0, 
                total=human_total,
                initial_total=human_total,
                initial_infected=human_infected
            ),
            population_density=mun.populationDensity,
            connected_municipalities=mun.connectedMunicipalities,
            infected_dogs_history=[dog_infected],
            infected_cats_history=[cat_infected],
            infected_humans_history=[human_infected]
        )
    
    # Run simulation
    for step in range(n_steps):
        # Update all municipalities
        new_states = {}
        for mun_id, state in states.items():
            # Use municipality-specific parameters for this municipality
            mun_params = municipality_params[mun_id]
            new_states[mun_id] = simulate_municipality_step(
                state,
                mun_params,  # Use custom parameters for each municipality
                states  # Pass all states for inter-municipality transmission
            )
        states = new_states
    
    # Convert back to dictionary format
    results = []
    for mun_id, state in states.items():
        # Calculate total population
        total_population = (
            state.dogs.total +
            state.cats.total +
            state.humans.total
        )
        
        results.append({
            'id': state.id,
            'name': state.name,
            # Predictions (final state after simulation)
            'predictedInfectedDogs': int(round(state.dogs.infected)),
            'predictedInfectedCats': int(round(state.cats.infected)),
            'predictedInfectedHumans': int(round(state.humans.infected)),
            'totalPredictedInfected': int(round(
                state.dogs.infected + state.cats.infected + state.humans.infected
            )),
            # Population totals
            'predictedDogPopulation': int(round(state.dogs.total)),
            'predictedCatPopulation': int(round(state.cats.total)),
            'predictedHumanPopulation': int(round(state.humans.total)),
            'totalPopulation': int(total_population),
            # Compartments
            'susceptibleDogs': int(round(state.dogs.susceptible)),
            'vaccinatedDogs': int(round(state.dogs.vaccinated)),
            # Phase 2: Cumulative Statistics (NEW) - Using response model field names
            'totalDogBirths': int(round(state.dogs.cumulative_births)),
            'totalDogNaturalDeaths': int(round(state.dogs.cumulative_natural_deaths)),
            'totalDogRabiesDeaths': int(round(state.dogs.cumulative_rabies_deaths)),
            'totalDogVaccinations': int(round(state.dogs.cumulative_vaccinations)),
            'totalCatBirths': int(round(state.cats.cumulative_births)),
            'totalCatNaturalDeaths': int(round(state.cats.cumulative_natural_deaths)),
            'totalCatRabiesDeaths': int(round(state.cats.cumulative_rabies_deaths)),
            'totalCatVaccinations': int(round(state.cats.cumulative_vaccinations)),
            'totalHumanBirths': int(round(state.humans.cumulative_births)),
            'totalHumanNaturalDeaths': int(round(state.humans.cumulative_natural_deaths)),
            'totalHumanRabiesDeaths': int(round(state.humans.cumulative_rabies_deaths)),
            'totalHumanVaccinations': int(round(state.humans.cumulative_vaccinations)),
            # Population tracking - FIXED: Use stored initial values
            'initialDogPopulation': int(round(state.dogs.initial_total)),
            'initialCatPopulation': int(round(state.cats.initial_total)),
            'initialHumanPopulation': int(round(state.humans.initial_total)),
            'finalDogPopulation': int(round(state.dogs.total)),
            'finalCatPopulation': int(round(state.cats.total)),
            'finalHumanPopulation': int(round(state.humans.total)),
            # Initial and final infections for change tracking
            'initialInfectedDogs': int(round(state.dogs.initial_infected)),
            'initialInfectedCats': int(round(state.cats.initial_infected)),
            'initialInfectedHumans': int(round(state.humans.initial_infected)),
            'finalInfectedDogs': int(round(state.dogs.infected)),
            'finalInfectedCats': int(round(state.cats.infected)),
            'finalInfectedHumans': int(round(state.humans.infected)),
            # Legacy
            'dailyInfections': []  # TODO: Track daily if needed
        })
        
        # DEBUG: Print first municipality's cumulative stats
        if len(results) == 1:
            print(f"[DEBUG transmission_model.py] First municipality cumulative stats:")
            print(f"  totalDogBirths: {results[0].get('totalDogBirths', 'KEY_MISSING')}")
            print(f"  totalDogNaturalDeaths: {results[0].get('totalDogNaturalDeaths', 'KEY_MISSING')}")
            print(f"  totalHumanVaccinations: {results[0].get('totalHumanVaccinations', 'KEY_MISSING')}")
    
    return results

# ============================================================================
# TESTING / VALIDATION
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("Transmission Model - Test")
    print("=" * 70)
    
    # Create test municipality
    test_mun = {
        'id': '1',
        'name': 'Test City',
        'humanPopulation': 10000,
        'dogPopulation': 1000,
        'catPopulation': 500,
        'infectedDogs': 10,
        'infectedCats': 2,
        'infectedHumans': 0,
        'vaccinatedDogs': 300,
        'populationDensity': 200.0,
        'latitude': 7.0,
        'longitude': 125.0,
        'riskLevel': 'moderate',
        'connectedMunicipalities': []
    }
    
    test_settings = {
        'simulationDays': 10,
        'fractionalOrder': 0.95,
        'transmissionRate': 0.15,
        'recoveryRate': 0.1,
        'contactProbability': 0.3,
        'stochasticIntensity': 0.1,
        'vaccinationRate': 0.8
    }
    
    print("\nRunning test simulation...")
    print(f"Initial infected dogs: {test_mun['infectedDogs']}")
    print(f"Simulation days: {test_settings['simulationDays']}")
    
    results = run_fractional_stochastic_simulation([test_mun], test_settings)
    
    print("\nResults:")
    for r in results:
        print(f"  Municipality: {r['name']}")
        print(f"  Predicted infected dogs: {r['predictedInfectedDogs']}")
        print(f"  Predicted infected cats: {r['predictedInfectedCats']}")
        print(f"  Predicted infected humans: {r['predictedInfectedHumans']}")
        print(f"  Total predicted infected: {r['totalPredictedInfected']}")
    
    print("\n" + "=" * 70)
    print("Test completed successfully!")
    print("=" * 70)
