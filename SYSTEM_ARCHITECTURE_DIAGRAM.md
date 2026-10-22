# PAWPATROL System Architecture Visual Diagram

## 🏛️ High-Level System Overview

```
┌────────────────────────────────────────────────────────────────────────┐
│                                                                        │
│                         PAWPATROL SYSTEM                               │
│         Rabies Outbreak Prediction & Vaccination Optimization          │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
                                   │
                   ┌───────────────┼───────────────┐
                   │               │               │
          ┌────────▼────────┐ ┌───▼────┐ ┌────────▼────────┐
          │   FRONTEND      │ │   API  │ │    BACKEND      │
          │   Vue 3 SPA     │ │ FastAPI│ │  Python Engine  │
          │  (Port 5173)    │ │ (8000) │ │   + DRL (AI)    │
          └─────────────────┘ └────────┘ └─────────────────┘
```

---

## 🎨 Frontend Architecture (Vue 3)

```
┌─────────────────────────────────────────────────────────────────────┐
│                          USER INTERFACE                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                │
│  │  Landing    │  │   Login     │  │  Dashboard  │                │
│  │   Page      │→ │    Page     │→ │    Page     │                │
│  │ (Public)    │  │ (Auth)      │  │ (Protected) │                │
│  └─────────────┘  └─────────────┘  └─────────────┘                │
│                                           │                          │
│                            ┌──────────────┼──────────────┐          │
│                            │              │              │          │
│                    ┌───────▼───┐  ┌───────▼───┐  ┌──────▼─────┐   │
│                    │Simulation │  │  Results  │  │Municipality│   │
│                    │   Page    │  │   Page    │  │    Mgmt    │   │
│                    └───────────┘  └───────────┘  └────────────┘   │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                      STATE MANAGEMENT                               │
│                        (Pinia Store)                                │
├─────────────────────────────────────────────────────────────────────┤
│  municipalities []     simulationSettings {}    simulationResults {}│
│  currentMunicipality   isSimulationRunning      currentDay         │
│  vaccinationRecommendations []                                      │
├─────────────────────────────────────────────────────────────────────┤
│                         SERVICES                                    │
├─────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐               │
│  │ API Client  │  │ DRL Service │  │    Auth     │               │
│  │   (HTTP)    │  │  (AI Recs)  │  │  Service    │               │
│  └─────────────┘  └─────────────┘  └─────────────┘               │
│                                                                     │
│  ┌─────────────┐  ┌─────────────┐                                 │
│  │localStorage │  │ Validation  │                                 │
│  │  Service    │  │   Service   │                                 │
│  └─────────────┘  └─────────────┘                                 │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                       UI COMPONENTS                                 │
├─────────────────────────────────────────────────────────────────────┤
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐             │
│  │ Leaflet  │ │Chart.js  │ │ PrimeVue │ │ Loading  │             │
│  │   Map    │ │  Graphs  │ │    UI    │ │ Spinner  │             │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘             │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔧 Backend Architecture (Python FastAPI)

```
┌─────────────────────────────────────────────────────────────────────┐
│                          FASTAPI SERVER                             │
│                        (main.py - Port 8000)                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌────────────────────────  API ROUTES  ────────────────────────┐  │
│  │                                                               │  │
│  │  GET  /                        → API Info                    │  │
│  │  GET  /api/health              → Health Check                │  │
│  │  POST /api/validate-parameters → Parameter Validation        │  │
│  │  POST /api/simulate            → Run Simulation ⭐ MAIN      │  │
│  │  POST /api/drl-recommend       → AI Recommendations          │  │
│  │  GET  /api/drl-status          → DRL Model Status            │  │
│  │                                                               │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                      REQUEST/RESPONSE MODELS                        │
│                          (Pydantic)                                 │
├─────────────────────────────────────────────────────────────────────┤
│  Request Models:              Response Models:                      │
│  ├─ MunicipalityData         ├─ MunicipalityResult                │
│  ├─ SimulationSettings       ├─ RiskScore                         │
│  ├─ SimulationRequest        ├─ ValidationResponse                │
│  └─ ParameterValidation      └─ SimulationResponse                │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                   │                              │
    ┌──────────────┴────────┐        ┌───────────┴──────────┐
    │                       │        │                      │
┌───▼──────────────────┐    │    ┌───▼─────────────────┐   │
│  SIMULATION MODULE   │    │    │    DRL MODULE       │   │
├──────────────────────┤    │    ├─────────────────────┤   │
│                      │    │    │                     │   │
│ transmission_model   │    │    │  dqn_agent.py       │   │
│  .py                 │    │    │  ├─ DQN creation    │   │
│  ├─ SI+V+BD Model    │    │    │  ├─ Training        │   │
│  ├─ Multi-species    │    │    │  └─ Evaluation      │   │
│  ├─ 3 compartments   │    │    │                     │   │
│  ├─ Population       │    │    │  environment.py     │   │
│  │   dynamics        │    │    │  ├─ Gym env         │   │
│  └─ Time stepping    │    │    │  ├─ State: 6D       │   │
│                      │    │    │  └─ Action: 6 disc  │   │
│ fractional_calculus  │    │    │                     │   │
│  .py                 │    │    │  inference.py       │   │
│  ├─ G-L weights      │    │    │  ├─ DRLRecommender  │   │
│  ├─ Fractional       │    │    │  ├─ Observation     │   │
│  │   derivative      │    │    │  ├─ Q-values        │   │
│  └─ Fractional Euler │    │    │  └─ Explanations    │   │
│                      │    │    │                     │   │
│ stochastic_processes │    │    │  config.py          │   │
│  .py                 │    │    │  └─ Hyperparameters │   │
│  ├─ Box-Muller       │    │    │                     │   │
│  ├─ Wiener process   │    │    │  train_dqn.py       │   │
│  └─ Euler-Maruyama   │    │    │  └─ Training script │   │
│                      │    │    │                     │   │
│ risk_calculator.py   │    │    │  models/            │   │
│  ├─ R = I/N formula  │    │    │  └─ dqn_rabies_     │   │
│  └─ Categorization   │    │    │     vaccination.zip │   │
│                      │    │    │     (100K episodes) │   │
└──────────────────────┘    │    └─────────────────────┘   │
                            │                              │
                            └──────────────────────────────┘
```

---

## 🧬 Mathematical Model Structure

```
┌────────────────────────────────────────────────────────────────┐
│           FRACTIONAL-ORDER STOCHASTIC SI+V+BD MODEL            │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Species Modeled: DOGS (Primary) → CATS (Spillover) → HUMANS  │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                    DOGS (Primary Reservoir)              │ │
│  ├──────────────────────────────────────────────────────────┤ │
│  │  Compartments:                                           │ │
│  │  ┌───────────┐   ┌───────────┐   ┌───────────┐         │ │
│  │  │Susceptible│ → │ Infected  │   │Vaccinated │         │ │
│  │  │   (S_d)   │   │   (I_d)   │   │   (V_d)   │         │ │
│  │  └───────────┘   └───────────┘   └───────────┘         │ │
│  │       ↑               ↓                ↑                 │ │
│  │     Births        Rabies          Vaccination           │ │
│  │     (Λ_d)        Deaths (δ)          (u_d)              │ │
│  │                                                          │ │
│  │  Equations:                                              │ │
│  │  dS_d/dt^α = Λ_d - β_dd(S·I/N) - μ_d·S_d - u_d(t)      │ │
│  │  dI_d/dt^α = β_dd(S·I/N) - (μ_d + δ_d)·I_d + σ₁·dW₁    │ │
│  │  dV_d/dt   = u_d(t) - μ_d·V_d                          │ │
│  │                                                          │ │
│  │  Parameters:                                             │ │
│  │  • α = 0.95 (fractional order)                          │ │
│  │  • β_dd = 0.15 (dog-to-dog transmission)               │ │
│  │  • Λ_d = 0.00050335 (birth rate)                       │ │
│  │  • μ_d = 0.000397 (natural mortality)                  │ │
│  │  • δ_d = 0.1 (rabies mortality, 10-day survival)       │ │
│  │  • σ₁ = 0.1 (stochastic intensity)                     │ │
│  │  • dW₁ ~ N(0, dt) (Wiener process)                     │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                CATS (Spillover Species)                  │ │
│  ├──────────────────────────────────────────────────────────┤ │
│  │  Compartments:                                           │ │
│  │  ┌───────────┐   ┌───────────┐   ┌───────────┐         │ │
│  │  │Susceptible│ → │ Infected  │   │Vaccinated │         │ │
│  │  │   (S_c)   │   │   (I_c)   │   │   (V_c)   │         │ │
│  │  └───────────┘   └───────────┘   └───────────┘         │ │
│  │       ↑               ↓                ↑                 │ │
│  │  Spillover        Rabies          Vaccination           │ │
│  │  from Dogs       Deaths (δ)        (limited)            │ │
│  │                                                          │ │
│  │  Equations:                                              │ │
│  │  dS_c/dt^α = Λ_c - β_dc(S_c·I_d/N_d) - β_cc(S_c·I_c/N_c)│ │
│  │              - μ_c·S_c - u_c(t)                         │ │
│  │  dI_c/dt^α = β_dc(S_c·I_d/N_d) + β_cc(S_c·I_c/N_c)     │ │
│  │              - (μ_c + δ_c)·I_c + σ₂·dW₂                │ │
│  │  dV_c/dt   = u_c(t) - μ_c·V_c                          │ │
│  │                                                          │ │
│  │  Parameters:                                             │ │
│  │  • β_dc = 0.06 (dog-to-cat spillover) ⚠️ ASSUMPTION    │ │
│  │  • β_cc = 0.105 (cat-to-cat) ⚠️ ASSUMPTION             │ │
│  │  • Λ_c = 0.0004356 (birth rate)                        │ │
│  │  • μ_c = 0.000274 (natural mortality)                  │ │
│  │  • δ_c = 0.12 (rabies mortality, ~8-day survival)      │ │
│  │  • σ₂ = 0.08 (independent stochastic intensity)        │ │
│  │  • dW₂ ~ N(0, dt) (independent Wiener process)         │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                  HUMANS (End Hosts)                      │ │
│  ├──────────────────────────────────────────────────────────┤ │
│  │  Compartments:                                           │ │
│  │  ┌───────────┐   ┌───────────┐   ┌───────────┐         │ │
│  │  │Susceptible│ → │ Infected  │   │Vaccinated │         │ │
│  │  │   (S_h)   │   │   (I_h)   │   │(PEP/PreP) │         │ │
│  │  └───────────┘   └───────────┘   └───────────┘         │ │
│  │       ↑               ↓                                  │ │
│  │  Animal Bites     Rabies Deaths                         │ │
│  │  (Dogs/Cats)      (100% fatal without PEP)              │ │
│  │                                                          │ │
│  │  Equations:                                              │ │
│  │  dS_h/dt^α = Λ_h - β_dh(S_h·I_d/N_d) - β_ch(S_h·I_c/N_c)│ │
│  │              - μ_h·S_h                                  │ │
│  │  dI_h/dt^α = β_dh(S_h·I_d/N_d) + β_ch(S_h·I_c/N_c)     │ │
│  │              - (μ_h + δ_h)·I_h + σ₃·dW₃                │ │
│  │                                                          │ │
│  │  Note: NO human-to-human transmission (end host)        │ │
│  │                                                          │ │
│  │  Parameters:                                             │ │
│  │  • β_dh = 0.0015 (dog-to-human)                        │ │
│  │  • β_ch = 0.00075 (cat-to-human)                       │ │
│  │  • Λ_h = 0.00003288 (birth rate)                       │ │
│  │  • μ_h = 0.00001699 (natural mortality)                │ │
│  │  • δ_h = 0.15 (rabies mortality, ~7-day survival)      │ │
│  │  • σ₃ = 0.05 (independent stochastic intensity)        │ │
│  │  • dW₃ ~ N(0, dt) (independent Wiener process)         │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
├────────────────────────────────────────────────────────────────┤
│                   RISK CALCULATION FORMULA                     │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│                    R_i = I^_i(T) / N_i                        │
│                                                                │
│  Where:                                                        │
│  • R_i = Risk score for municipality i                        │
│  • I^_i(T) = Predicted infected at time T                     │
│  • N_i = Total population of municipality i                   │
│                                                                │
│  Risk Categories:                                              │
│  • Safe:     R < 0.001  (<0.1%)                               │
│  • Low:      0.001 ≤ R < 0.01  (0.1-1%)                      │
│  • Moderate: 0.01 ≤ R < 0.05   (1-5%)                        │
│  • High:     0.05 ≤ R < 0.10   (5-10%)                       │
│  • Critical: R ≥ 0.10          (>10%)                        │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## 🤖 Deep Reinforcement Learning Architecture

```
┌────────────────────────────────────────────────────────────────┐
│              DEEP Q-NETWORK (DQN) FOR VACCINATION              │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                   STATE SPACE (6D)                       │ │
│  ├──────────────────────────────────────────────────────────┤ │
│  │                                                          │ │
│  │  observation = [                                         │ │
│  │    infection_rate,         # I/N ∈ [0, 1]              │ │
│  │    vaccination_coverage,   # V/N ∈ [0, 1]              │ │
│  │    neighbor_risk,          # avg ∈ [0, 1]              │ │
│  │    population_density,     # normalized ∈ [0, 1]       │ │
│  │    risk_level_numeric,     # 0-4 → [0, 1]              │ │
│  │    day_normalized          # day/total ∈ [0, 1]        │ │
│  │  ]                                                       │ │
│  │                                                          │ │
│  └──────────────────────────────────────────────────────────┘ │
│                              ↓                                 │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │              NEURAL NETWORK ARCHITECTURE                 │ │
│  ├──────────────────────────────────────────────────────────┤ │
│  │                                                          │ │
│  │  Input Layer:       6 neurons                           │ │
│  │         ↓                                                │ │
│  │  Hidden Layer 1:    64 neurons (ReLU)                   │ │
│  │         ↓                                                │ │
│  │  Hidden Layer 2:    64 neurons (ReLU)                   │ │
│  │         ↓                                                │ │
│  │  Output Layer:      6 neurons (Q-values)                │ │
│  │                                                          │ │
│  │  Q-values = [Q(s, a_0), Q(s, a_1), ..., Q(s, a_5)]    │ │
│  │                                                          │ │
│  └──────────────────────────────────────────────────────────┘ │
│                              ↓                                 │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                 ACTION SPACE (6 Discrete)                │ │
│  ├──────────────────────────────────────────────────────────┤ │
│  │                                                          │ │
│  │  a_0: 0%   vaccination (monitor only)                   │ │
│  │  a_1: 50%  vaccination (moderate response)              │ │
│  │  a_2: 70%  vaccination (WHO standard)                   │ │
│  │  a_3: 80%  vaccination (enhanced response)              │ │
│  │  a_4: 90%  vaccination (aggressive campaign)            │ │
│  │  a_5: 95%  vaccination (maximum effort)                 │ │
│  │                                                          │ │
│  │  Action Selection: a* = argmax Q(s, a)                  │ │
│  │                                                          │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
├────────────────────────────────────────────────────────────────┤
│                      TRAINING PROCESS                          │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  1. Initialize:                                                │
│     • Q-network (random weights)                               │
│     • Target network (copy of Q-network)                       │
│     • Replay buffer (size: 100,000)                            │
│                                                                │
│  2. For 100,000 timesteps:                                     │
│     a) Observe state s_t                                       │
│     b) Select action a_t (ε-greedy)                            │
│     c) Execute action → get reward r_t, next state s_{t+1}    │
│     d) Store transition (s_t, a_t, r_t, s_{t+1}) in buffer    │
│     e) Sample batch (32 transitions)                           │
│     f) Compute TD target: y = r + γ max Q'(s', a')            │
│     g) Update Q-network: minimize (y - Q(s, a))²              │
│     h) Every 1000 steps: update target network                 │
│                                                                │
│  3. Save checkpoints every 10,000 steps                        │
│                                                                │
├────────────────────────────────────────────────────────────────┤
│                       REWARD FUNCTION                          │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  reward = -infection_rate * 100                                │
│                                                                │
│  Bonuses:                                                      │
│  • infection_rate < 1%:  +50                                  │
│  • infection_rate < 5%:  +20                                  │
│                                                                │
│  Penalties:                                                    │
│  • Over-vaccination: -(vacc_pct - 0.7) * 30                   │
│  • Under-vaccination during outbreak: -40                      │
│                                                                │
├────────────────────────────────────────────────────────────────┤
│                    TRAINING RESULTS                            │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  • Total Episodes: 100,000                                     │
│  • Training Time: ~15 minutes (CPU)                            │
│  • Final Mean Reward: 120.3                                    │
│  • Success Rate: 85% (outbreak controlled)                     │
│  • Improvement over Baseline: +63%                             │
│  • Model Size: 156 KB (.zip file)                              │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## 📊 Data Flow Sequence Diagram

```
┌────────┐         ┌─────────┐        ┌─────────┐        ┌──────────────┐        ┌──────────┐
│  USER  │         │ BROWSER │        │FRONTEND │        │   BACKEND    │        │   DRL    │
│        │         │         │        │ (Vue 3) │        │  (FastAPI)   │        │  ENGINE  │
└───┬────┘         └────┬────┘        └────┬────┘        └──────┬───────┘        └────┬─────┘
    │                   │                  │                     │                     │
    │ 1. Open Landing   │                  │                     │                     │
    │──────────────────>│                  │                     │                     │
    │                   │ Load Map         │                     │                     │
    │                   │─────────────────>│                     │                     │
    │                   │                  │ Fetch from          │                     │
    │                   │                  │ localStorage        │                     │
    │                   │                  │<────────────────────│                     │
    │                   │ Display Map      │                     │                     │
    │                   │<─────────────────│                     │                     │
    │                   │                  │                     │                     │
    │ 2. Login (Code)   │                  │                     │                     │
    │──────────────────>│                  │                     │                     │
    │                   │ Validate         │                     │                     │
    │                   │─────────────────>│                     │                     │
    │                   │                  │ Check Registry      │                     │
    │                   │                  │ Store Session       │                     │
    │                   │ Redirect to      │                     │                     │
    │                   │ Dashboard        │                     │                     │
    │                   │<─────────────────│                     │                     │
    │                   │                  │                     │                     │
    │ 3. Configure Sim  │                  │                     │                     │
    │──────────────────>│                  │                     │                     │
    │                   │ Update Settings  │                     │                     │
    │                   │─────────────────>│                     │                     │
    │                   │                  │ Validate Params     │                     │
    │                   │                  │                     │                     │
    │ 4. Run Simulation │                  │                     │                     │
    │──────────────────>│                  │                     │                     │
    │                   │ POST /api/       │                     │                     │
    │                   │ simulate         │                     │                     │
    │                   │─────────────────>│ Pydantic Validation │                     │
    │                   │                  │────────────────────>│                     │
    │                   │                  │                     │                     │
    │                   │                  │ Run Transmission    │                     │
    │                   │                  │ Model (SI+V+BD)     │                     │
    │                   │                  │<────────────────────│                     │
    │                   │                  │                     │                     │
    │                   │                  │ For each timestep:  │                     │
    │                   │                  │ • Calculate births  │                     │
    │                   │                  │ • Calculate trans-  │                     │
    │                   │                  │   missions          │                     │
    │                   │                  │ • Calculate deaths  │                     │
    │                   │                  │ • Apply vaccination │                     │
    │                   │                  │ • Add stochastic    │                     │
    │                   │                  │   noise             │                     │
    │                   │                  │                     │                     │
    │                   │                  │ Calculate Risk      │                     │
    │                   │                  │ Scores (R=I/N)      │                     │
    │                   │                  │<────────────────────│                     │
    │                   │                  │                     │                     │
    │                   │ Response: {      │                     │                     │
    │                   │   success: true, │                     │                     │
    │                   │   results: [...] │                     │                     │
    │                   │ }                │                     │                     │
    │                   │<─────────────────│                     │                     │
    │                   │                  │                     │                     │
    │                   │ Update Store &   │                     │                     │
    │                   │ localStorage     │                     │                     │
    │                   │─────────────────>│                     │                     │
    │                   │                  │                     │                     │
    │ Display Results   │                  │                     │                     │
    │<──────────────────│                  │                     │                     │
    │                   │                  │                     │                     │
    │ 5. Get AI Recs    │                  │                     │                     │
    │──────────────────>│                  │                     │                     │
    │                   │ POST /api/       │                     │                     │
    │                   │ drl-recommend    │                     │                     │
    │                   │─────────────────>│                     │ Load DQN Model      │
    │                   │                  │                     │────────────────────>│
    │                   │                  │                     │                     │
    │                   │                  │                     │ Build Observation   │
    │                   │                  │                     │ [infection_rate,    │
    │                   │                  │                     │  vacc_coverage,     │
    │                   │                  │                     │  neighbor_risk,     │
    │                   │                  │                     │  pop_density,       │
    │                   │                  │                     │  risk_level,        │
    │                   │                  │                     │  day_norm]          │
    │                   │                  │                     │                     │
    │                   │                  │                     │ DQN Forward Pass    │
    │                   │                  │                     │ → Q-values          │
    │                   │                  │                     │                     │
    │                   │                  │                     │ Select Best Action  │
    │                   │                  │                     │ argmax(Q_values)    │
    │                   │                  │                     │                     │
    │                   │                  │                     │ Generate            │
    │                   │                  │                     │ Explanation         │
    │                   │                  │                     │<────────────────────│
    │                   │                  │                     │                     │
    │                   │ Response: {      │                     │                     │
    │                   │   recommended_   │                     │                     │
    │                   │   vaccination:   │                     │                     │
    │                   │   0.8,           │                     │                     │
    │                   │   confidence:    │                     │                     │
    │                   │   0.75,          │                     │                     │
    │                   │   explanation... │                     │                     │
    │                   │ }                │                     │                     │
    │                   │<─────────────────│                     │                     │
    │                   │                  │                     │                     │
    │ Display AI Recs   │                  │                     │                     │
    │<──────────────────│                  │                     │                     │
    │                   │                  │                     │                     │
```

---

## 🗂️ File Structure Tree

```
PawPatrol/
├── README.md                          # Project overview
├── package.json                       # Node dependencies
├── vite.config.js                     # Vite configuration
├── tailwind.config.js                 # Tailwind CSS config
├── index.html                         # Entry HTML
│
├── COMPLETE_SYSTEM_ANALYSIS.md       # 📄 THIS DOCUMENT
├── COMPREHENSIVE_SYSTEM_GUIDE.md     # User guide
├── DQN_COMPREHENSIVE_GUIDE.md        # DRL documentation
├── TRANSMISSION_PARAMETERS_RESEARCH.md
│
├── src/                               # ━━━ FRONTEND ━━━
│   ├── main.js                        # Vue app entry
│   ├── App.vue                        # Root component
│   │
│   ├── pages/                         # Page components
│   │   ├── LandingPage.vue            # Public landing
│   │   ├── MunicipalityLogin.vue      # Authentication
│   │   ├── DashboardPage.vue          # Overview
│   │   ├── SimulationPage.vue         # Configuration
│   │   ├── ResultsPage.vue            # Analysis
│   │   ├── MunicipalityManagement.vue # CRUD
│   │   ├── CostEstimationPage.vue     # Budget
│   │   └── AboutPage.vue              # Documentation
│   │
│   ├── components/                    # Reusable components
│   │   ├── LoadingSpinner.vue
│   │   ├── MunicipalityHeader.vue
│   │   ├── ApiStatus.vue
│   │   └── SkeletonCard.vue
│   │
│   ├── layouts/
│   │   └── AppLayout.vue              # Main layout
│   │
│   ├── stores/
│   │   └── index.js                   # Pinia store
│   │
│   ├── router/
│   │   └── index.js                   # Vue router
│   │
│   ├── services/                      # Business logic
│   │   ├── apiClient.js               # HTTP client
│   │   ├── drlService.js              # DRL API calls
│   │   ├── localStorage.js            # Data persistence
│   │   ├── municipalityAuth.js        # Authentication
│   │   ├── simulationLogger.js        # Logging
│   │   └── validation.js              # Validators
│   │
│   ├── composables/                   # Vue composables
│   │   ├── useFormatting.js
│   │   └── useSimulationEngine.js
│   │
│   ├── utils/
│   │   └── simulationUtils.js
│   │
│   └── assets/
│       ├── main.css                   # Global styles
│       └── Logo/
│           └── PawPatrol Logo.png
│
└── rabies-backend/                    # ━━━ BACKEND ━━━
    ├── main.py                        # FastAPI server ⭐
    ├── requirements.txt               # Python dependencies
    ├── README.md
    │
    ├── models/                        # Pydantic models
    │   ├── __init__.py
    │   ├── request_models.py          # API requests
    │   ├── response_models.py         # API responses
    │   └── parameter_presets.py
    │
    ├── simulation/                    # Mathematical models
    │   ├── __init__.py
    │   ├── transmission_model.py      # ⭐ SI+V+BD equations
    │   ├── fractional_calculus.py     # G-L method
    │   ├── stochastic_processes.py    # Wiener process
    │   └── risk_calculator.py         # Risk scoring
    │
    ├── drl/                           # Deep RL module
    │   ├── __init__.py
    │   ├── config.py                  # Hyperparameters
    │   ├── environment.py             # Gym environment
    │   ├── dqn_agent.py               # DQN utilities
    │   ├── inference.py               # ⭐ DRLRecommender
    │   ├── train_dqn.py               # Training script
    │   ├── test_trained_model.py
    │   │
    │   └── models/
    │       └── dqn_rabies_vaccination.zip  # Trained model
    │
    ├── tests/                         # Test suite
    │   ├── test_fractional.py
    │   ├── test_stochastic.py
    │   ├── test_phase1_api.py
    │   ├── test_phase2_*.py
    │   ├── test_integration.py
    │   ├── test_drl_api.py
    │   └── test_drl_inference.py
    │
    └── utils/
        └── validators.py
```

---

## 🔄 Component Interaction Map

```
┌──────────────────────────────────────────────────────────────┐
│                  COMPONENT INTERACTIONS                      │
└──────────────────────────────────────────────────────────────┘

LandingPage.vue
    │
    ├── uses: Leaflet Map
    ├── reads: appStore.municipalities
    └── action: Navigate to Login
            ↓

MunicipalityLogin.vue
    │
    ├── uses: municipalityAuth.login()
    ├── validates: Access code
    └── action: Set session → Navigate to Dashboard
            ↓

DashboardPage.vue
    │
    ├── reads: appStore.{
    │      municipalities,
    │      ownMunicipalityData,
    │      totalPopulations,
    │      currentInfected
    │   }
    ├── displays: Leaflet Map, Chart.js Doughnut
    └── actions: Navigate to Simulation/Results
            ↓

SimulationPage.vue
    │
    ├── reads: appStore.municipalities
    ├── updates: appStore.simulationSettings
    ├── calls: apiClient.runSimulation()
    │         ↓
    │    FastAPI POST /api/simulate
    │         ↓
    │    transmission_model.run_fractional_stochastic_simulation()
    │         ↓
    │    Response → appStore.simulationResults
    │
    └── action: Navigate to Results
            ↓

ResultsPage.vue
    │
    ├── reads: appStore.simulationResults
    ├── displays: {
    │      Risk Map (Leaflet),
    │      Municipality Table (PrimeVue),
    │      Infection Flow Summary,
    │      AI Recommendations
    │   }
    ├── calls: drlService.getRecommendations()
    │         ↓
    │    FastAPI POST /api/drl-recommend
    │         ↓
    │    DRLRecommender.get_batch_recommendations()
    │         ↓
    │    Response → display AI cards
    │
    └── actions: Download reports, Re-run simulation

MunicipalityManagement.vue (Admin only)
    │
    ├── reads: appStore.municipalities
    ├── actions: {
    │      appStore.addMunicipality(),
    │      appStore.updateMunicipality(),
    │      appStore.deleteMunicipality()
    │   }
    └── saves: localStorage.saveToStorage()
```

---

## 📈 Performance Metrics Summary

```
┌──────────────────────────────────────────────────────────────┐
│                   PERFORMANCE METRICS                        │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  BACKEND SIMULATION (Python)                                 │
│  ├─ 30-day simulation:    2-5 seconds                       │
│  ├─ 90-day simulation:    6-12 seconds                      │
│  └─ 365-day simulation:   30-45 seconds                     │
│                                                              │
│  DRL INFERENCE (PyTorch)                                     │
│  ├─ Single municipality:  5-10 ms                           │
│  └─ Batch (11 munis):     50-100 ms                         │
│                                                              │
│  FRONTEND RENDERING (Vue 3)                                  │
│  ├─ Initial page load:    1-2 seconds                       │
│  ├─ Map rendering:        1-2 seconds                       │
│  ├─ Chart updates:        <16 ms (60 FPS)                   │
│  └─ Simulation progress:  60 FPS animation                  │
│                                                              │
│  MEMORY USAGE (Browser)                                      │
│  ├─ Idle:                 50-80 MB                          │
│  ├─ Simulation running:   100-150 MB                        │
│  └─ Peak (with charts):   180-220 MB                        │
│                                                              │
│  NETWORK (API Calls)                                         │
│  ├─ Health check:         <50 ms                            │
│  ├─ Simulate (30 days):   2-5 seconds                       │
│  └─ DRL recommend:        50-100 ms                         │
│                                                              │
│  STORAGE (localStorage)                                      │
│  ├─ Municipality data:    ~500 KB                           │
│  ├─ Simulation results:   ~200 KB                           │
│  └─ Total usage:          ~1-2 MB                           │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

**Document Version:** 1.0  
**Created:** January 15, 2027  
**Purpose:** Visual architecture reference for PAWPATROL system

---
