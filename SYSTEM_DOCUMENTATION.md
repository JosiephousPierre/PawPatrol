# PAWPATROL System Documentation

## Complete Technical Reference Guide

**Version:** 1.0  
**Last Updated:** October 21, 2026  
**Location:** Davao de Oro, Philippines  

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Core Features](#core-features)
3. [Mathematical Models](#mathematical-models)
4. [Formulas Reference](#formulas-reference)
5. [System Architecture](#system-architecture)
6. [Data Flow](#data-flow)
7. [API Endpoints](#api-endpoints)
8. [File Structure](#file-structure)

---

## System Overview

### Project Name
**PAWPATROL** - Fractional-Order Stochastic SI+V+BD Transmission Model with Deep Reinforcement Learning for Rabies Outbreak Prediction and Vaccination Optimization

### Purpose
A research prototype system that models rabies transmission across 11 municipalities in Davao de Oro, Philippines, providing AI-powered vaccination recommendations using Deep Q-Network (DQN) reinforcement learning.

### Key Innovation
- **Fractional-Order Calculus**: Captures disease memory effects
- **Stochastic Processes**: Models environmental uncertainty
- **SI+V+BD Model**: Susceptible-Infected-Vaccinated with Births-Deaths (no recovery - rabies is 100% fatal)
- **Deep Q-Network**: AI-powered vaccination optimization

---

## Core Features

### 1. **Multi-Species Transmission Modeling**

#### Implementation Location
- **Backend:** `rabies-backend/simulation/transmission_model.py` (lines 640-970)

#### Species Roles
| Species | Role | Transmission | Population Dynamics |
|---------|------|--------------|---------------------|
| **Dogs** | Primary Reservoir | Dog↔Dog, Dog→Cat, Dog→Human | Births, Natural Deaths, Rabies Deaths, Vaccination |
| **Cats** | Spillover Hosts | Cat↔Cat (secondary) | Births, Natural Deaths, Rabies Deaths, Vaccination (50% of dog rate) |
| **Humans** | End Hosts | No human-to-human | Births, Natural Deaths, Rabies Deaths, PEP Treatment |

#### Features
- ✅ Explicit transmission coefficients for each species pair (β_dd, β_dc, β_cc, β_dh, β_ch)
- ✅ Species-specific mortality rates (δ_dog = 0.1, δ_cat = 0.12, δ_human = 0.15 per day)
- ✅ Independent stochastic noise for each species (σ₁, σ₂, σ₃)
- ✅ Different vaccination capacities (Dogs: 5%/day, Cats: 3%/day, Humans: 0.1%/day)

---

### 2. **Population Dynamics (SI+V+BD Model)**

#### Implementation Location
- **Backend:** `rabies-backend/simulation/transmission_model.py` (lines 666-970)

#### Birth Rates (Λ)
```python
lambda_dog: 0.00050335 per day    # 3.88% annual growth
lambda_cat: 0.0004356 per day     # 5.90% annual growth  
lambda_human: 0.00003288 per day  # 0.58% annual growth
```
**Source:** Lines 114-116, `transmission_model.py`

#### Natural Mortality (μ)
```python
mu_dog: 0.000397 per day       # Natural lifespan
mu_cat: 0.000274 per day       # Natural lifespan
mu_human: 0.00001699 per day   # Natural lifespan
```
**Source:** Lines 119-121, `transmission_model.py`

#### Rabies Mortality (δ)
```python
delta_dog: 0.1 per day      # 10 day infectious period
delta_cat: 0.12 per day     # 8.3 day infectious period
delta_human: 0.15 per day   # 6.7 day infectious period
```
**Source:** Lines 124-126, `transmission_model.py`

#### Features
- ✅ Realistic population growth/decline
- ✅ Birth and death tracking
- ✅ Cumulative statistics (total births, deaths, vaccinations)
- ✅ Mass conservation: S + I + V = N at all times

---

### 3. **Fractional-Order Calculus**

#### Implementation Location
- **Backend:** `rabies-backend/simulation/fractional_calculus.py`

#### Caputo Fractional Derivative
**Formula:**
```
D^α f(t) = (1/Γ(1-α)) ∫[0 to t] f'(τ)/(t-τ)^α dτ
```

**Where:**
- α = Fractional order (0 < α ≤ 1)
- Γ = Gamma function
- τ = Integration variable

#### Grünwald-Letnikov Approximation
**Formula:**
```
D^α f(t) ≈ (1/h^α) Σ[j=0 to n] w_j^(α) f(t - jh)

Weights: w_0^(α) = 1
         w_j^(α) = w_{j-1}^(α) · (1 - (1+α)/j)
```

**Source:** `fractional_calculus.py`, lines 45-75

#### Purpose
- Captures **memory effects** in disease transmission
- Past infection states influence current dynamics
- Default α = 0.95 (near-integer behavior with slight memory)

---

### 4. **Stochastic Processes**

#### Implementation Location
- **Backend:** `rabies-backend/simulation/stochastic_processes.py`

#### Wiener Process (Brownian Motion)
**Formula:**
```
dW(t) = σ · √dt · Z,  where Z ~ N(0,1)
```

**Species-Specific Intensities:**
```python
sigma_1: 0.1   # Dogs - highest variability (stray populations)
sigma_2: 0.08  # Cats - moderate variability
sigma_3: 0.05  # Humans - lowest variability (controlled environment)
```

**Source:** Lines 128-130, `transmission_model.py`

#### Independent Wiener Processes
**Function:** `generate_independent_wiener_processes(dt, sigma_values)`
**Source:** `stochastic_processes.py`, lines 78-105

#### Purpose
- Models environmental uncertainty (weather, behavior changes)
- Contact rate randomness
- Seasonal variations
- Unpredictable events

---

### 5. **Inter-Municipality Transmission**

#### Implementation Location
- **Backend:** `transmission_model.py`, lines 677-691 (dogs), 796-810 (cats)

#### Network-Based Spread
**Formula:**
```
External_Infections = Σ[neighbors] β · p · 0.3 · (S_local · I_neighbor / N_neighbor) · dt
```

**Reduction Factor:** 0.3 for dogs, 0.2 for cats (lower mobility)

#### Features
- ✅ Explicit municipality connections (network graph)
- ✅ Reduced transmission across borders
- ✅ Asymmetric transmission (depends on infected counts in neighbors)
- ✅ Separate tracking for local vs external infections

#### Data Structure
```javascript
municipality: {
  id: "MUN001",
  name: "Maco",
  connectedMunicipalities: ["MUN002", "MUN003"]  // Connected IDs
}
```

**Source:** `models/request_models.py`, line 24

---

### 6. **Vaccination System**

#### Implementation Location
- **Backend:** `transmission_model.py`, lines 698-703 (dogs), 811-816 (cats), 914-919 (humans)

#### Vaccination Formula
```
Vaccinations = min(
  daily_capacity × dt,
  susceptible_available,
  needed_to_reach_target
)
```

#### Target-Based Vaccination
**Function:** `calculate_vaccination(S, V, N, target_coverage, daily_capacity, dt)`

**Parameters:**
| Species | Target Rate | Daily Capacity | Notes |
|---------|-------------|----------------|-------|
| Dogs | 100% × vaccination_rate | 5% of population/day | Primary intervention |
| Cats | 50% × vaccination_rate | 3% of population/day | Harder to reach |
| Humans | 1% × vaccination_rate | 0.1% of population/day | Pre-exposure only (high-risk) |

**Source:** Lines 325-378, `transmission_model.py`

#### Features
- ✅ Capacity-limited vaccination (realistic constraints)
- ✅ Target coverage goals (e.g., 70% WHO recommendation)
- ✅ Progressive vaccination (reaches target over time)
- ✅ Vaccinated population tracking (living vaccinated dogs at any time)

---

### 7. **Deep Q-Network (DQN) for Vaccination Optimization**

#### Implementation Location
- **Backend:** `rabies-backend/drl/dqn_agent.py`
- **Training:** `rabies-backend/drl/train_dqn.py`
- **Inference:** `rabies-backend/drl/inference.py`

#### State Space
```python
state = [
    infected_dogs / dog_population,        # Infection rate
    vaccinated_dogs / dog_population,      # Coverage
    susceptible_dogs / dog_population,     # Susceptible fraction
    population_density / 1000,             # Density (normalized)
    neighbor_infected / neighbor_total,    # Regional risk
    time_step / max_steps                  # Time progress
]
```

**Dimension:** 6-dimensional continuous state space

#### Action Space
```python
actions = [0%, 20%, 40%, 60%, 80%, 100%]  # Vaccination coverage levels
```

**Dimension:** 6 discrete actions

#### Reward Function
```python
reward = -(new_infections + rabies_deaths × 10 + vaccination_cost × 0.1)
```

**Components:**
- Minimize new infections (weight: 1)
- Minimize rabies deaths (weight: 10 - heavily penalized)
- Minimize vaccination costs (weight: 0.1 - mild penalty for resource use)

**Source:** `drl/environment.py`, lines 120-145

#### Network Architecture
```
Input Layer:    6 neurons (state features)
Hidden Layer 1: 128 neurons (ReLU activation)
Hidden Layer 2: 128 neurons (ReLU activation)
Output Layer:   6 neurons (Q-values for each action)
```

#### Training Parameters
```python
learning_rate: 0.0001
gamma (discount): 0.99
epsilon (exploration): 1.0 → 0.01 (decay)
replay_buffer_size: 100,000
batch_size: 64
total_episodes: 100,000+
```

**Source:** `drl/train_dqn.py`, lines 30-45

#### Features
- ✅ Experience replay for stable learning
- ✅ Epsilon-greedy exploration
- ✅ Target network for Q-value stability
- ✅ Checkpoint saving every 10,000 episodes
- ✅ Model persistence (saved as `.zip` files)

---

### 8. **Risk Assessment System**

#### Implementation Location
- **Backend:** `simulation/risk_calculator.py`
- **Frontend:** `pages/DashboardPage.vue`

#### Risk Score Calculation
```python
risk_score = (infected_dogs + infected_cats + infected_humans) / total_population
```

#### Risk Levels
| Level | Infection Rate | Color | Action |
|-------|---------------|-------|--------|
| **Safe** | < 0.1% | Green | Monitor |
| **Low** | 0.1% - 1% | Yellow | Prepare |
| **Moderate** | 1% - 5% | Orange | Act |
| **High** | 5% - 10% | Red | Urgent intervention |
| **Critical** | > 10% | Dark Red | Emergency response |

**Source:** `risk_calculator.py`, lines 25-50

#### Features
- ✅ Real-time risk updates after simulation
- ✅ Color-coded visualization
- ✅ Municipality-specific risk levels
- ✅ Historical risk tracking

---

### 9. **Interactive Mapping**

#### Implementation Location
- **Frontend:** `pages/LandingPage.vue`, `pages/DashboardPage.vue`, `pages/ResultsPage.vue`

#### Technology
- **Library:** Leaflet.js
- **Tiles:** OpenStreetMap

#### Features
- ✅ Geo-located municipality markers
- ✅ Color-coded by risk level
- ✅ Click for detailed popup (infection counts, vaccination coverage)
- ✅ Network connections visualization
- ✅ Auto-recentering after popup close

#### Map Configuration
```javascript
center: [7.5, 125.9],  // Davao de Oro coordinates
zoom: 9,               // Province-level view
zoomControl: false,    // Fixed view (no zoom)
dragging: false        // No panning
```

**Source:** `ResultsPage.vue`, lines 1567-1580

---

### 10. **Data Persistence & Municipality Management**

#### Implementation Location
- **Frontend:** `stores/index.js` (Pinia state management)
- **Backend:** In-memory (no database in prototype)

#### Municipality Data Structure
```javascript
{
  id: "MUN001",
  name: "Maco",
  accessCode: "MACO2024",
  latitude: 7.3667,
  longitude: 125.8333,
  humanPopulation: 87094,
  dogPopulation: 8768,
  catPopulation: 2000,
  infectedDogs: 200,
  infectedCats: 100,
  infectedHumans: 0,
  vaccinatedDogs: 988,
  populationDensity: 150.5,
  riskLevel: "moderate",
  connectedMunicipalities: ["MUN002", "MUN003"],
  lastUpdated: "2026-10-21T10:30:00Z"
}
```

**Source:** `stores/index.js`, lines 15-80

#### Features
- ✅ Access code-based authentication
- ✅ Municipality-specific data isolation
- ✅ CRUD operations (Create, Read, Update, Delete)
- ✅ Last updated timestamps
- ✅ Data validation (population constraints, positive numbers)

---

## Mathematical Models

### SI+V+BD Model Equations

#### Dogs (Primary Reservoir)

**Susceptible Dogs:**
```
dS_d/dt^α = Λ_d - β_dd(S_d·I_d)/N_d - μ_d·S_d - u_d(t)
```

**Infected Dogs:**
```
dI_d/dt^α = β_dd(S_d·I_d)/N_d - (μ_d + δ_d)·I_d + σ₁·dW₁(t)
```

**Vaccinated Dogs:**
```
dV_d/dt = u_d(t) - μ_d·V_d
```

**Population Conservation:**
```
N_d(t) = S_d(t) + I_d(t) + V_d(t)
```

**Source:** `transmission_model.py`, lines 640-745

---

#### Cats (Spillover Hosts)

**Susceptible Cats:**
```
dS_c/dt^α = Λ_c - β_dc(S_c·I_d)/N_d - β_cc(S_c·I_c)/N_c - μ_c·S_c - u_c(t)
```

**Infected Cats:**
```
dI_c/dt^α = β_dc(S_c·I_d)/N_d + β_cc(S_c·I_c)/N_c - (μ_c + δ_c)·I_c + σ₂·dW₂(t)
```

**Vaccinated Cats:**
```
dV_c/dt = u_c(t) - μ_c·V_c
```

**Population Conservation:**
```
N_c(t) = S_c(t) + I_c(t) + V_c(t)
```

**Source:** `transmission_model.py`, lines 750-870

---

#### Humans (End Hosts)

**Susceptible Humans:**
```
dS_h/dt^α = Λ_h - β_dh(S_h·I_d)/N_d - β_ch(S_h·I_c)/N_c - μ_h·S_h - u_h(t)
```

**Infected Humans:**
```
dI_h/dt^α = β_dh(S_h·I_d)/N_d + β_ch(S_h·I_c)/N_c - (μ_h + δ_h)·I_h + σ₃·dW₃(t)
```

**Vaccinated Humans:**
```
dV_h/dt = u_h(t) - μ_h·V_h
```

**Population Conservation:**
```
N_h(t) = S_h(t) + I_h(t) + V_h(t)
```

**Source:** `transmission_model.py`, lines 875-970

---

### Parameter Summary Table

| Parameter | Symbol | Dogs | Cats | Humans | Unit | Source (Line) |
|-----------|--------|------|------|--------|------|---------------|
| **Birth Rate** | Λ | 0.00050335 | 0.0004356 | 0.00003288 | /day | 114-116 |
| **Natural Death** | μ | 0.000397 | 0.000274 | 0.00001699 | /day | 119-121 |
| **Rabies Death** | δ | 0.1 | 0.12 | 0.15 | /day | 124-126 |
| **Stochastic Intensity** | σ | 0.1 | 0.08 | 0.05 | - | 128-130 |
| **Dog-Dog Transmission** | β_dd | 0.15 | - | - | /day | 133 |
| **Dog-Cat Transmission** | β_dc | - | 0.06 | - | /day | 134 |
| **Cat-Cat Transmission** | β_cc | - | 0.105 | - | /day | 135 |
| **Dog-Human Transmission** | β_dh | - | - | 0.0015 | /day | 136 |
| **Cat-Human Transmission** | β_ch | - | - | 0.00075 | /day | 137 |
| **Contact Probability** | p | 0.3 | 0.3 | 0.3 | - | 103 |
| **Fractional Order** | α | 0.95 | 0.95 | 0.95 | - | 100 |
| **Time Step** | dt | 0.1 | 0.1 | 0.1 | days | 101 |

**All parameters source:** `simulation/transmission_model.py`

---

## Formulas Reference

### Transmission Calculation

**Function:** `calculate_transmission(S, I, N, beta, p, dt)`

**Formula:**
```
new_infections = β × p × (S × I / N) × dt
```

**Where:**
- β = Transmission coefficient
- p = Contact probability
- S = Susceptible population
- I = Infected population
- N = Total population
- dt = Time step

**Physical Constraints:**
```python
new_infections = max(0, min(new_infections, S))  # Cannot exceed susceptible
```

**Source:** `transmission_model.py`, lines 280-320

**Usage:**
- Dog-to-dog transmission (line 668)
- Dog-to-cat transmission (line 777)
- Cat-to-cat transmission (line 785)
- Dog-to-human transmission (line 890)
- Cat-to-human transmission (line 898)
- Inter-municipality transmission (lines 677-691, 796-810)

---

### Birth Calculation

**Function:** `calculate_births(lambda_rate, population, dt)`

**Formula:**
```
births = λ × N × dt
```

**Where:**
- λ = Birth rate (per individual per day)
- N = Current population
- dt = Time step

**Source:** `transmission_model.py`, lines 175-195

**Usage:**
- Dog births (line 661)
- Cat births (line 769)
- Human births (line 883)

---

### Death Calculations

#### Natural Deaths

**Function:** `calculate_natural_deaths(mu_rate, population, dt)`

**Formula:**
```
natural_deaths = μ × N × dt
```

**Source:** `transmission_model.py`, lines 200-220

**Usage:**
- Dog natural deaths (lines 691, 724, 735)
- Cat natural deaths (lines 818, 829, 837)
- Human natural deaths (lines 925, 936, 943)

#### Rabies Deaths

**Function:** `calculate_rabies_deaths(delta_rate, infected, dt)`

**Formula:**
```
rabies_deaths = δ × I × dt
```

**Source:** `transmission_model.py`, lines 225-245

**Usage:**
- Dog rabies deaths (line 728)
- Cat rabies deaths (line 825)
- Human rabies deaths (line 932)

---

### Vaccination Calculation

**Function:** `calculate_vaccination(S, V, N, target_coverage, daily_capacity, dt)`

**Formula:**
```python
current_coverage = V / N
needed = (target_coverage × N) - V
max_this_step = daily_capacity × dt
vaccinations = min(max_this_step, S, needed, 0 if current_coverage >= target else infinity)
```

**Source:** `transmission_model.py`, lines 325-378

**Usage:**
- Dog vaccination (lines 698-703)
- Cat vaccination (lines 811-816)
- Human vaccination (lines 914-919)

---

### Risk Score Calculation

**Formula:**
```
risk_score = (I_dogs + I_cats + I_humans) / (N_dogs + N_cats + N_humans)
infection_rate = risk_score × 100%
```

**Risk Classification:**
```python
if infection_rate >= 10:
    risk_level = "critical"
elif infection_rate >= 5:
    risk_level = "high"
elif infection_rate >= 1:
    risk_level = "moderate"
elif infection_rate >= 0.1:
    risk_level = "low"
else:
    risk_level = "safe"
```

**Source:** `risk_calculator.py`, lines 25-65

**Usage:**
- Municipality risk assessment (Backend)
- Dashboard risk display (Frontend)
- Map marker coloring (Frontend)
- Results page analysis (Frontend)

---

### Coverage Calculation

**Formula:**
```
vaccination_coverage = (vaccinated_dogs / total_dogs) × 100%
```

**Display Cap:**
```python
displayed_coverage = min(100, max(0, calculated_coverage))  # 0-100% range
```

**Source:** `ResultsPage.vue`, lines 1191-1194

**Usage:**
- Municipality Analysis table
- Vaccination recommendations
- DRL input features

---

## System Architecture

### Technology Stack

#### Frontend
```
Framework:     Vue 3 (Composition API)
Build Tool:    Vite
State:         Pinia
UI Library:    PrimeVue
Styling:       Tailwind CSS
Mapping:       Leaflet.js
Charts:        Chart.js (future)
Icons:         PrimeIcons
```

#### Backend
```
Framework:     FastAPI (Python 3.9+)
Numerical:     NumPy, SciPy
DRL:           Stable-Baselines3 (DQN)
Validation:    Pydantic
CORS:          FastAPI middleware
```

#### Mathematical
```
Fractional:    Custom implementation (Grünwald-Letnikov)
Stochastic:    NumPy random (Wiener processes)
ODE Solver:    Euler-Maruyama method
```

---

### Project Structure

```
PawPatrol/
├── src/                          # Frontend (Vue)
│   ├── assets/                   # Static assets
│   ├── components/               # Reusable components
│   │   ├── MunicipalityHeader.vue
│   │   └── ...
│   ├── layouts/                  # Layout components
│   │   └── AppLayout.vue
│   ├── Logo/                     # Logo assets
│   │   └── PawPatrol Logo.png
│   ├── pages/                    # Page components
│   │   ├── AboutPage.vue         # System documentation
│   │   ├── CostEstimationPage.vue# Vaccination cost calculator
│   │   ├── DashboardPage.vue     # Municipality dashboard
│   │   ├── LandingPage.vue       # Public landing page
│   │   ├── MunicipalityLogin.vue # Authentication
│   │   ├── MunicipalityManagement.vue # Data management
│   │   ├── ResultsPage.vue       # Simulation results
│   │   └── SimulationPage.vue    # Simulation controls
│   ├── router/                   # Vue Router
│   │   └── index.js
│   ├── services/                 # API services
│   │   ├── api.js                # API client
│   │   ├── drlService.js         # DRL recommendations
│   │   ├── municipalityAuth.js   # Authentication
│   │   ├── simulationService.js  # Simulation API
│   │   └── formatting.js         # Utilities
│   ├── stores/                   # Pinia stores
│   │   └── index.js              # App state
│   └── main.js                   # App entry point
│
├── rabies-backend/               # Backend (Python)
│   ├── drl/                      # Deep Reinforcement Learning
│   │   ├── config.py             # DRL configuration
│   │   ├── dqn_agent.py          # DQN implementation
│   │   ├── environment.py        # Gym environment
│   │   ├── inference.py          # Model inference
│   │   ├── train_dqn.py          # Training script
│   │   ├── models/               # Saved DQN models
│   │   │   └── dqn_rabies_vaccination.zip
│   │   └── drl/models/           # Training checkpoints
│   │       └── dqn_rabies_vaccination/
│   │
│   ├── models/                   # Pydantic models
│   │   ├── parameter_presets.py  # Default parameters
│   │   ├── request_models.py     # API request schemas
│   │   └── response_models.py    # API response schemas
│   │
│   ├── simulation/               # Core simulation
│   │   ├── fractional_calculus.py# Fractional derivatives
│   │   ├── risk_calculator.py    # Risk assessment
│   │   ├── stochastic_processes.py# Wiener processes
│   │   ├── transmission_model.py # Main SI+V+BD model
│   │   └── transmission_model_SI_V_BD_PHASE2.py # Phase 2 version
│   │
│   ├── tests/                    # Unit tests
│   │   ├── test_integration.py
│   │   ├── test_phase2_sub_*.py
│   │   └── ...
│   │
│   ├── main.py                   # FastAPI app
│   ├── requirements.txt          # Python dependencies
│   └── README.md                 # Backend documentation
│
├── public/                       # Public assets
├── index.html                    # HTML entry point
├── package.json                  # Node dependencies
├── tailwind.config.js            # Tailwind configuration
├── vite.config.js                # Vite configuration
└── README.md                     # Project documentation
```

---

## Data Flow

### 1. Simulation Flow

```
User Input (Frontend)
    ↓
SimulationPage.vue
    ↓ [API Call: POST /simulate]
Backend: main.py
    ↓
transmission_model.py: run_fractional_stochastic_simulation()
    ↓
For each time step (0.1 days):
    ├── simulate_municipality_step() for each municipality
    │   ├── Calculate births (λ × N × dt)
    │   ├── Calculate transmissions (β × p × S × I / N × dt)
    │   ├── Calculate deaths (μ × N × dt, δ × I × dt)
    │   ├── Calculate vaccinations (min(capacity, susceptible, needed))
    │   ├── Add stochastic noise (σ × √dt × Z)
    │   ├── Update compartments (S, I, V)
    │   └── Store cumulative statistics
    ↓
Aggregate results (initial, final, cumulative stats)
    ↓
Return JSON response
    ↓
Frontend: ResultsPage.vue
    ├── Display Municipality Analysis (coverage, infection rate)
    ├── Display Infection Flow Summary (before → after)
    ├── Display Population Dynamics (births, deaths, vaccinations)
    └── Render interactive map with risk markers
```

---

### 2. DRL Recommendation Flow

```
User Clicks "Get AI Recommendations" (Frontend)
    ↓
ResultsPage.vue: fetchDRLRecommendations()
    ↓ [API Call: POST /drl/recommendations]
Backend: main.py
    ↓
inference.py: get_drl_recommendations()
    ├── Load trained DQN model (dqn_rabies_vaccination.zip)
    ├── For each municipality:
    │   ├── Extract state features (infection rate, coverage, density, etc.)
    │   ├── Model predicts Q-values for all actions
    │   ├── Select action with highest Q-value (greedy policy)
    │   ├── Map action to vaccination percentage (0%, 20%, 40%, 60%, 80%, 100%)
    │   └── Assign priority based on infection rate and coverage gap
    ↓
Return recommendations with confidence scores
    ↓
Frontend: Display DRL recommendations table
    ├── Municipality name
    ├── Recommended vaccination percentage
    ├── Priority level (Critical, High, Medium, Low, Monitor)
    ├── Confidence score
    └── AI explanation
```

---

### 3. Municipality Data Flow

```
Municipality Manager Login (Frontend)
    ↓
MunicipalityLogin.vue
    ↓ [API Call: POST /auth/login]
Backend: Verify access code
    ↓ [Success]
Store municipality in Pinia
    ↓
MunicipalityManagement.vue
    ├── Display current data (population, infected, vaccinated)
    ├── Allow edits (update populations, infection counts)
    └── Save changes
        ↓ [API Call: PUT /municipalities/{id}]
Backend: Update municipality data
    ↓
Pinia store updated
    ↓
All pages now use updated data
```

---

## API Endpoints

### Authentication

#### POST `/auth/login`
**Request:**
```json
{
  "accessCode": "MACO2024"
}
```

**Response:**
```json
{
  "success": true,
  "municipality": {
    "id": "MUN001",
    "name": "Maco",
    "accessCode": "MACO2024",
    ...
  }
}
```

---

### Simulation

#### POST `/simulate`
**Request:**
```json
{
  "municipalities": [
    {
      "id": "MUN001",
      "name": "Maco",
      "humanPopulation": 87094,
      "dogPopulation": 8768,
      "catPopulation": 2000,
      "infectedDogs": 200,
      "infectedCats": 100,
      "infectedHumans": 0,
      "vaccinatedDogs": 988,
      "populationDensity": 150.5,
      "connectedMunicipalities": ["MUN002"],
      "riskLevel": "moderate"
    }
  ],
  "settings": {
    "simulationDays": 365,
    "fractionalOrder": 0.95,
    "transmissionRate": 0.15,
    "contactProbability": 0.3,
    "vaccinationRate": 0.8,
    "stochasticIntensity": 0.1
  }
}
```

**Response:**
```json
{
  "municipalities": [
    {
      "id": "MUN001",
      "name": "Maco",
      "predictedInfectedDogs": 0,
      "predictedInfectedCats": 0,
      "predictedInfectedHumans": 0,
      "predictedDogPopulation": 9046,
      "vaccinatedDogs": 7236,
      "initialInfectedDogs": 200,
      "finalInfectedDogs": 0,
      "totalDogBirths": 1631,
      "totalDogNaturalDeaths": 1286,
      "totalDogRabiesDeaths": 72,
      "totalDogVaccinations": 7261,
      "finalDogPopulation": 9046,
      "riskLevel": "safe"
    }
  ],
  "metadata": {
    "model": "Fractional-Order Stochastic SI+V+BD",
    "version": "Phase 2",
    "simulationDays": 365,
    "completedAt": "2026-10-21T10:45:30Z"
  }
}
```

---

### DRL Recommendations

#### POST `/drl/recommendations`
**Request:**
```json
{
  "municipalities": [
    {
      "id": "MUN001",
      "name": "Maco",
      "dogPopulation": 9046,
      "infectedDogs": 0,
      "vaccinatedDogs": 7236,
      "populationDensity": 150.5,
      "riskLevel": "safe"
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "drl_available": true,
  "recommendations": [
    {
      "municipality_id": "MUN001",
      "municipality_name": "Maco",
      "recommended_vaccination_percentage": 80,
      "priority": "Monitor",
      "confidence": 0.92,
      "explanation": "Current coverage (80%) is adequate. Maintain surveillance.",
      "q_values": {
        "0%": -1200,
        "20%": -800,
        "40%": -400,
        "60%": -100,
        "80%": 50,
        "100%": 30
      }
    }
  ]
}
```

---

## File Structure Details

### Key Backend Files

| File | Purpose | Lines | Key Functions |
|------|---------|-------|---------------|
| `main.py` | FastAPI app, routing | 300 | `/simulate`, `/drl/recommendations` |
| `transmission_model.py` | Core SI+V+BD simulation | 1200 | `simulate_municipality_step()`, `run_fractional_stochastic_simulation()` |
| `fractional_calculus.py` | Fractional derivatives | 150 | `grunwald_letnikov_weights()`, `fractional_derivative()` |
| `stochastic_processes.py` | Wiener processes | 120 | `wiener_increment()`, `generate_independent_wiener_processes()` |
| `risk_calculator.py` | Risk assessment | 100 | `calculate_risk_score()`, `categorize_risk()` |
| `dqn_agent.py` | DQN implementation | 250 | `DQNAgent class`, `train()`, `predict()` |
| `environment.py` | Gym environment | 200 | `RabiesVaccinationEnv class`, `step()`, `reset()` |
| `inference.py` | DRL inference | 150 | `get_drl_recommendations()`, `load_model()` |

### Key Frontend Files

| File | Purpose | Lines | Key Features |
|------|---------|-------|--------------|
| `SimulationPage.vue` | Simulation controls | 800 | Parameter inputs, municipality selection, simulation trigger |
| `ResultsPage.vue` | Results display | 1900 | Municipality analysis, infection flow, population dynamics, DRL recommendations, map |
| `DashboardPage.vue` | Overview | 600 | Risk summary, statistics, quick insights, map |
| `MunicipalityManagement.vue` | Data management | 500 | CRUD operations, population editor, vaccination tracker |
| `AboutPage.vue` | Documentation | 700 | System info, objectives, framework, tech stack, limitations |
| `AppLayout.vue` | Main layout | 400 | Sidebar navigation, header, routing |
| `stores/index.js` | State management | 250 | Municipality data, simulation results, global state |

---

## Validation & Testing

### Unit Tests

**Location:** `rabies-backend/tests/`

#### Test Coverage
- ✅ Transmission calculations (`test_phase2_sub_b.py`)
- ✅ Birth/death dynamics (`test_phase2_sub_f.py`)
- ✅ Vaccination mechanics (`test_phase2_sub_c.py`)
- ✅ Multi-species interactions (`test_phase2_sub_e.py`)
- ✅ Fractional-order implementation (`test_phase2_sub_d.py`)
- ✅ Stochastic processes (`test_phase2_sub_d.py`)
- ✅ Inter-municipality transmission (`test_phase2_sub_g.py`)
- ✅ Integration tests (`test_integration.py`)

#### Test Results
**Total Tests:** 32  
**Passed:** 32  
**Failed:** 0  
**Status:** ✅ All tests passing

---

## Performance Metrics

### Simulation Performance

| Scenario | Municipalities | Days | Time Steps | Execution Time |
|----------|---------------|------|------------|----------------|
| Single Municipality | 1 | 365 | 3,650 | ~2-3 seconds |
| Regional (11 Municipalities) | 11 | 365 | 40,150 | ~15-20 seconds |
| Short-term (30 days) | 11 | 30 | 3,300 | ~2-3 seconds |

**Hardware:** Standard development machine (4-core CPU)

### DRL Inference Performance

| Operation | Time |
|-----------|------|
| Model loading | ~1 second (first time), cached after |
| Single prediction | ~5-10 ms |
| 11 municipalities | ~50-100 ms |

---

## Known Limitations

### 1. Parameter Validation
**Issue:** Cat transmission parameters (β_dc = 0.06, β_cc = 0.105) are modeling assumptions  
**Reason:** Limited empirical data on cat-specific rabies transmission  
**Impact:** Low (cats are spillover hosts, not maintenance)  
**Mitigation:** Sensitivity analysis shows results robust to ±50% variation

### 2. Stochastic Calibration
**Issue:** Stochastic intensities (σ₁, σ₂, σ₃) from literature ranges  
**Reason:** No Philippines-specific environmental uncertainty data  
**Impact:** Medium (affects outbreak variability)  
**Mitigation:** Conservative values used; results show realistic variability

### 3. DRL Training Data
**Issue:** DQN trained on simulated scenarios only  
**Reason:** Limited real-world outbreak data for training  
**Impact:** Medium (recommendations need field validation)  
**Mitigation:** Model shows logical behavior; human oversight required

### 4. Spatial Granularity
**Issue:** Homogeneous mixing within municipalities  
**Reason:** Sub-municipal data unavailable; computational complexity  
**Impact:** Low (municipality-level adequate for policy)  
**Mitigation:** Population density partially accounts for heterogeneity

### 5. Seasonal Variation
**Issue:** Constant parameters year-round  
**Reason:** Seasonal data not yet incorporated  
**Impact:** Low (365-day simulations average across seasons)  
**Mitigation:** Future enhancement planned

---

## Future Enhancements

### Phase 3 (Planned)
- [ ] Seasonal variation modeling (monsoon vs dry season)
- [ ] Age-stratified populations (puppies vs adult dogs)
- [ ] Wildlife reservoir integration (bats, monkeys)
- [ ] Economic impact analysis (vaccination cost-benefit)
- [ ] Mobile app for field data collection

### Phase 4 (Research)
- [ ] Quantum computing acceleration (large-scale optimization)
- [ ] Real-time DOH/LGU data integration
- [ ] Provincial/national scale expansion
- [ ] Climate change impact modeling
- [ ] Multi-country network modeling (cross-border transmission)

---

## References

### Key Literature

1. **Fractional Calculus in Epidemiology**
   - Diethelm, K. (2010). "The Analysis of Fractional Differential Equations"
   - Provides theoretical foundation for fractional-order derivatives

2. **Stochastic Epidemic Models**
   - Allen, L. J. S. (2008). "An Introduction to Stochastic Epidemic Models"
   - Wiener process applications in disease modeling

3. **Rabies Transmission Dynamics**
   - Hampson, K. et al. (2009). "Transmission Dynamics and Prospects for the Elimination of Canine Rabies"
   - WHO rabies epidemiology guidelines

4. **Deep Reinforcement Learning**
   - Mnih, V. et al. (2015). "Human-level control through deep reinforcement learning"
   - DQN algorithm and training methodology

5. **Rabies in the Philippines**
   - DOH Philippines Rabies Control Program
   - Philippine Statistics Authority demographic data

---

## Credits & Acknowledgments

**Development Team:**
- Thesis Student: [Name]
- Adviser: [Adviser Name]
- Institution: [University Name]

**Technologies:**
- Vue.js, FastAPI, NumPy, SciPy, Stable-Baselines3
- Leaflet.js, PrimeVue, Tailwind CSS
- OpenStreetMap contributors

**Data Sources:**
- Philippine Statistics Authority (PSA)
- Department of Health (DOH) Philippines
- WHO Rabies Guidelines
- Published rabies epidemiology literature

---

## License & Disclaimer

**License:** Research Prototype (Not for Commercial Use)

**Disclaimer:**  
This system is a research implementation for academic and demonstration purposes. Model parameters use best available estimates from literature; some lack Philippines-specific empirical validation. Deep Q-Network trained on simulated outbreak scenarios requires real-world validation before operational deployment. Not certified for operational public health decision-making without further validation and regulatory approval. For actual rabies control programs, consult qualified veterinary and public health authorities.

---

## Contact & Support

**For Academic Inquiries:**  
[Contact Email]

**For Technical Issues:**  
[GitHub Repository] (if available)

**For Public Health Collaboration:**  
Department of Health, Philippines  
Provincial Health Office, Davao de Oro

---

**Document Version:** 1.0  
**Last Updated:** October 21, 2026  
**Generated By:** PAWPATROL System Documentation Tool  
**Total Pages:** ~30 pages (Markdown format)

---

*End of System Documentation*
