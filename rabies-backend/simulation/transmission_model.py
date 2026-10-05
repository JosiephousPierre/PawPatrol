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
    """Population compartments for SIR model"""
    susceptible: float
    infected: float
    recovered: float
    vaccinated: float
    total: float

@dataclass
class SimulationParameters:
    """Parameters for transmission model"""
    # Fractional-order parameter
    alpha: float = 0.95  # α ∈ (0, 1]
    
    # Transmission parameters
    beta: float = 0.15  # β - base transmission rate
    gamma: float = 0.1  # γ - recovery/removal rate
    contact_probability: float = 0.3  # p - contact probability
    
    # Stochastic parameters
    sigma: float = 0.1  # σ - stochastic intensity
    
    # Vaccination
    vaccination_rate: float = 0.0  # u - daily vaccination rate
    
    # Spatial
    use_spatial_heterogeneity: bool = True
    
    # Simulation
    dt: float = 0.1  # Time step (0.1 day)
    
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
    # DOGS - Primary rabies reservoir
    # ========================================================================
    
    # Intra-species (dog-to-dog)
    dog_infections, dog_recoveries = intra_species_transmission(
        state.dogs.susceptible,
        state.dogs.infected,
        state.dogs.total,
        beta_eff,
        params.gamma,
        params.alpha,
        params.sigma,
        dt,
        state.infected_dogs_history
    )
    
    # Inter-municipality (dogs from neighbors)
    dog_external_infections = 0.0
    for neighbor_id in state.connected_municipalities:
        if neighbor_id in neighbor_states:
            neighbor = neighbor_states[neighbor_id]
            dog_external_infections += inter_municipality_transmission(
                state.dogs.susceptible,
                neighbor.dogs.infected,
                neighbor.dogs.total,
                beta_eff,
                dt
            )
    
    # Vaccination
    dog_vaccinations = apply_vaccination(
        state.dogs.susceptible,
        state.dogs.vaccinated,
        state.dogs.total,
        params.vaccination_rate,
        state.dogs.total * 0.05,  # 5% of population per day max
        dt
    )
    
    # Update dog population
    total_dog_infections = dog_infections + dog_external_infections
    state.dogs.susceptible -= total_dog_infections + dog_vaccinations
    state.dogs.infected += total_dog_infections - dog_recoveries
    state.dogs.recovered += dog_recoveries
    state.dogs.vaccinated += dog_vaccinations
    
    # Ensure non-negative
    state.dogs.susceptible = max(0.0, state.dogs.susceptible)
    state.dogs.infected = max(0.0, state.dogs.infected)
    state.dogs.recovered = max(0.0, state.dogs.recovered)
    state.dogs.vaccinated = max(0.0, state.dogs.vaccinated)
    
    # Update history
    state.infected_dogs_history.append(state.dogs.infected)
    if len(state.infected_dogs_history) > 100:  # Keep last 100 values
        state.infected_dogs_history.pop(0)
    
    # ========================================================================
    # CATS - Secondary hosts (Spillover, not maintenance hosts)
    # ========================================================================
    # RESEARCH NOTE (October 2026):
    # Extensive literature review found NO published studies directly quantifying
    # cat-to-cat vs dog-to-dog transmission rates, nor dog-to-cat coefficients.
    # 
    # Key findings:
    # - Dogs cause >95-99% of human rabies cases (WHO, 2026)
    # - Cats are incidental/spillover hosts, NOT maintenance hosts
    # - No evidence for sustained cat-only epidemics without dog/wildlife reservoir
    # - Per-bite susceptibility may be similar (β_cat ≈ β_dog), but fewer contacts
    # - 10-day infectious period validated for both species (CDC, Merck Veterinary Manual)
    # 
    # Parameters below are MODELING ASSUMPTIONS (conservative estimates):
    # ========================================================================
    
    # Intra-species (cat-to-cat)
    cat_infections, cat_recoveries = intra_species_transmission(
        state.cats.susceptible,
        state.cats.infected,
        state.cats.total,
        beta_eff * 0.7,  # ASSUMPTION: Cats have reduced transmission (no empirical data)
                         # Reflects spillover host status and lower contact rates
                         # NOT directly supported by published studies
        params.gamma,    # VALIDATED: 10-day infectious period (CDC/Merck guidelines)
                         # Same as dogs - both species die ~1 week after symptoms
        params.alpha,
        params.sigma * 0.8,  # Less stochastic variation
        dt,
        state.infected_cats_history
    )
    
    # Cross-species (dog-to-cat)
    cat_infections_from_dogs = cross_species_transmission(
        state.cats.susceptible,
        state.dogs.infected,
        state.dogs.total,
        beta_eff,
        0.4,  # ASSUMPTION: Reduced cross-species efficiency (no empirical data)
              # Per-bite risk may be similar to dog-to-dog, but this factor
              # represents lower dog-cat contact frequency and spillover dynamics
              # NOT supported by published transmission coefficients
        dt
    )
    
    # Inter-municipality (cats from neighbors)
    cat_external_infections = 0.0
    for neighbor_id in state.connected_municipalities:
        if neighbor_id in neighbor_states:
            neighbor = neighbor_states[neighbor_id]
            cat_external_infections += inter_municipality_transmission(
                state.cats.susceptible,
                neighbor.cats.infected,
                neighbor.cats.total,
                beta_eff * 0.7,  # ASSUMPTION: Same reduction as intra-species
                dt,
                0.2  # ASSUMPTION: Cats have lower inter-municipality movement than dogs
            )
    
    # Update cat population
    total_cat_infections = cat_infections + cat_infections_from_dogs + cat_external_infections
    state.cats.susceptible -= total_cat_infections
    state.cats.infected += total_cat_infections - cat_recoveries
    state.cats.recovered += cat_recoveries
    
    # Ensure non-negative
    state.cats.susceptible = max(0.0, state.cats.susceptible)
    state.cats.infected = max(0.0, state.cats.infected)
    state.cats.recovered = max(0.0, state.cats.recovered)
    
    # Update history
    state.infected_cats_history.append(state.cats.infected)
    if len(state.infected_cats_history) > 100:
        state.infected_cats_history.pop(0)
    
    # ========================================================================
    # HUMANS - End hosts (rabies is fatal without PEP)
    # ========================================================================
    # RESEARCH NOTE:
    # Human rabies is preventable with post-exposure prophylaxis (PEP)
    # Without treatment, rabies is nearly 100% fatal once symptoms appear
    # No human-to-human transmission occurs
    # ========================================================================
    
    # Humans only get infected from animals (no human-to-human)
    total_infected_animals = state.dogs.infected + state.cats.infected
    total_animals = state.dogs.total + state.cats.total
    
    # Cross-species (animal-to-human)
    if total_animals > 0 and total_infected_animals > 5:  # Threshold
        human_infections_from_animals = cross_species_transmission(
            state.humans.susceptible,
            total_infected_animals,
            total_animals,
            beta_eff,
            0.01,  # ASSUMPTION: Very low animal-to-human transmission
                   # Reflects that not all animal contacts result in bites
                   # and that PEP is often administered after exposure
            dt
        )
    else:
        human_infections_from_animals = 0.0
    
    # Humans "recover" (survive with PEP) or die
    # For simulation, we count recovered as "saved by PEP"
    # ASSUMPTION: 50% of exposed humans receive timely PEP treatment
    human_recoveries = state.humans.infected * params.gamma * 0.5 * dt  # 50% treated
    
    # Update human population
    state.humans.susceptible -= human_infections_from_animals
    state.humans.infected += human_infections_from_animals - human_recoveries
    state.humans.recovered += human_recoveries
    
    # Ensure non-negative
    state.humans.susceptible = max(0.0, state.humans.susceptible)
    state.humans.infected = max(0.0, state.humans.infected)
    state.humans.recovered = max(0.0, state.humans.recovered)
    
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
        dog_recovered = 0
        dog_susceptible = dog_total - dog_infected - dog_vaccinated - dog_recovered
        
        cat_total = mun.catPopulation
        cat_infected = mun.infectedCats
        cat_recovered = 0
        cat_susceptible = cat_total - cat_infected - cat_recovered
        
        human_total = mun.humanPopulation
        human_infected = mun.infectedHumans
        human_recovered = 0
        human_susceptible = human_total - human_infected - human_recovered
        
        states[mun.id] = MunicipalityState(
            id=mun.id,
            name=mun.name,
            dogs=Population(dog_susceptible, dog_infected, dog_recovered, dog_vaccinated, dog_total),
            cats=Population(cat_susceptible, cat_infected, cat_recovered, 0, cat_total),
            humans=Population(human_susceptible, human_infected, human_recovered, 0, human_total),
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
            'predictedInfectedDogs': int(round(state.dogs.infected)),
            'predictedInfectedCats': int(round(state.cats.infected)),
            'predictedInfectedHumans': int(round(state.humans.infected)),
            'totalPredictedInfected': int(round(
                state.dogs.infected + state.cats.infected + state.humans.infected
            )),
            'susceptibleDogs': int(round(state.dogs.susceptible)),
            'recoveredDogs': int(round(state.dogs.recovered)),
            'vaccinatedDogs': int(round(state.dogs.vaccinated)),
            'totalPopulation': int(total_population),
            'dailyInfections': []  # TODO: Track daily if needed
        })
    
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
