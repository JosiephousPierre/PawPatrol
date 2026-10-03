# 🔍 DEEP CODE ANALYSIS - PAWPATROL System

## **Complete Understanding of the Codebase**

---

## **1. SYSTEM ARCHITECTURE**

### **Technology Stack:**
```
Frontend:
├── Vue 3 (Composition API)
├── Vue Router 4 (Routing)
├── Pinia (State Management)
├── PrimeVue 3.46 (UI Component Library)
├── Tailwind CSS 3.4 (Styling)
├── Chart.js 4.4 + Vue-ChartJS (Charts)
├── Leaflet 1.9.4 (Maps)
└── Vite 5 (Build Tool)

Backend (NEW):
├── Python 3.x
├── FastAPI 0.104 (Web Framework)
├── NumPy 1.26 (Numerical Computing)
├── SciPy 1.11 (Scientific Computing)
├── Pydantic 2.5 (Data Validation)
└── Uvicorn 0.24 (ASGI Server)
```

---

## **2. PROJECT STRUCTURE**

### **Frontend Structure:**
```
src/
├── main.js                    ← App entry point, plugins, global components
├── App.vue                    ← Root component, Toast
│
├── router/
│   └── index.js               ← All routes (7 routes: landing, dashboard, etc.)
│
├── stores/
│   └── index.js               ← Pinia store (state management)
│                                 - municipalities, settings, results
│                                 - Computed properties
│                                 - CRUD actions
│
├── services/
│   ├── localStorage.js        ← Data persistence (11 municipalities)
│   ├── simulationLogger.js    ← Simulation event logging
│   └── validation.js          ← Input validation utilities
│
├── composables/
│   ├── useSimulationEngine.js      ← Main simulation logic (current)
│   ├── useAdaptiveVaccination.js   ← Rule-based vaccination system
│   └── useFormatting.js            ← Formatting utilities
│
├── utils/
│   └── simulationUtils.js     ← Utility functions (risk calc, predictions, cost)
│
├── layouts/
│   └── AppLayout.vue          ← Main layout (sidebar navigation, top bar)
│
├── pages/
│   ├── LandingPage.vue              ← Landing/welcome screen
│   ├── DashboardPage.vue            ← Dashboard with stats, charts
│   ├── MunicipalityManagement.vue   ← CRUD for municipalities
│   ├── SimulationPage.vue           ← Simulation controls, parameters
│   ├── ResultsPage.vue              ← Simulation results, maps
│   ├── PredictiveAnalysisPage.vue   ← Future predictions
│   ├── CostEstimationPage.vue       ← Intervention cost calculations
│   └── AboutPage.vue                ← About/info page
│
├── components/
│   ├── LoadingSpinner.vue     ← Loading indicator
│   └── SkeletonCard.vue       ← Skeleton loading UI
│
└── assets/
    └── main.css               ← Global styles, Tailwind, animations
```

### **Backend Structure (NEW):**
```
rabies-backend/
├── main.py                    ← FastAPI app, endpoints
├── requirements.txt           ← Dependencies
│
├── models/
│   ├── request_models.py      ← API request schemas (Pydantic)
│   └── response_models.py     ← API response schemas
│
├── simulation/
│   ├── fractional_calculus.py      ← Grünwald-Letnikov method (✅ DONE)
│   ├── stochastic_processes.py     ← Wiener process (TODO)
│   ├── transmission_model.py       ← Paper's SIR model (TODO)
│   └── risk_calculator.py          ← R_i = I^_i(T) / N_i (TODO)
│
├── utils/
│   └── validators.py          ← Input validation (TODO)
│
└── tests/
    ├── test_fractional.py     ← Unit tests (TODO)
    ├── test_stochastic.py
    └── test_simulation.py
```

---

## **3. DATA FLOW ARCHITECTURE**

### **Current System (Frontend Only):**
```
┌─────────────────────────────────────────────────────────────┐
│                         USER                                │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                    VUE ROUTER                               │
│  Routes: /, /dashboard, /municipalities, /simulation, etc.  │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                   PAGES (Components)                        │
│  - Dashboard, Municipalities, Simulation, Results, etc.     │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                  PINIA STORE (State)                        │
│  - municipalities[]       (reactive state)                  │
│  - simulationSettings{}   (reactive state)                  │
│  - simulationResults{}    (reactive state)                  │
│  - Computed properties    (derived state)                   │
│  - Actions (CRUD, save)   (mutations)                       │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                 COMPOSABLES (Business Logic)                │
│  useSimulationEngine  → runs simulation locally             │
│  useAdaptiveVaccination → vaccination recommendations       │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│           SERVICES & UTILS (Helper Functions)               │
│  localStorage.js   → persist to browser storage             │
│  simulationUtils.js → risk scores, predictions, costs       │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                  BROWSER localStorage                       │
│  Keys: pawpatrol_municipalities, pawpatrol_settings, etc.   │
└─────────────────────────────────────────────────────────────┘
```

### **New System (With Python Backend):**
```
┌─────────────────────────────────────────────────────────────┐
│                         USER                                │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                    VUE FRONTEND                             │
│  Same UI, but simulation calls backend API                  │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP POST /api/simulate
                           │ { municipalities, settings }
┌──────────────────────────▼──────────────────────────────────┐
│              PYTHON BACKEND (FastAPI)                       │
│  main.py → receives request                                 │
│          → validates parameters                             │
│          → calls simulation engine                          │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│        FRACTIONAL-ORDER STOCHASTIC MODEL                    │
│  fractional_calculus.py  → D^α f(t)                         │
│  stochastic_processes.py → dW(t), Brownian motion           │
│  transmission_model.py   → dI/dt^α = β*p*S*I/N - γ*I + σ*dW│
│  risk_calculator.py      → R_i = I^_i(T) / N_i              │
└──────────────────────────┬──────────────────────────────────┘
                           │ return results
┌──────────────────────────▼──────────────────────────────────┐
│              PYTHON BACKEND (FastAPI)                       │
│  Formats results as JSON                                    │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP Response
┌──────────────────────────▼──────────────────────────────────┐
│                    VUE FRONTEND                             │
│  Receives results, updates state, displays in UI            │
│  Saves to localStorage                                      │
└─────────────────────────────────────────────────────────────┘
```

---

## **4. STATE MANAGEMENT (Pinia Store)**

### **Store Structure:**
```javascript
useAppStore = {
  // STATE (ref)
  municipalities: [],          // Array of municipality objects
  simulationSettings: {},      // Simulation parameters
  simulationResults: {},       // Simulation output
  vaccinationRecommendations: [], // Vaccination suggestions
  isSimulationRunning: false,  // Simulation status
  currentSimulationDay: 0,     // Current day counter
  
  // COMPUTED (readonly derived state)
  totalMunicipalities,         // Count of municipalities
  totalDogPopulation,          // Sum of all dog populations
  totalCatPopulation,          // Sum of all cat populations
  totalHumanPopulation,        // Sum of all human populations
  currentInfectedDogs,         // Sum of infected dogs
  currentInfectedCats,         // Sum of infected cats
  currentInfectedHumans,       // Sum of infected humans
  
  // ACTIONS (functions to modify state)
  initializeApp(),             // Load data on startup
  saveAllData(),               // Persist to localStorage
  addMunicipality(m),          // Create new municipality
  updateMunicipality(id, m),   // Update existing municipality
  deleteMunicipality(id),      // Delete municipality
  updateSimulationSettings(s), // Update settings
  resetToDefaults()            // Reset all data
}
```

### **Municipality Data Structure:**
```javascript
{
  id: "1",                     // Unique ID (string)
  name: "Maco",                // Municipality name
  latitude: 7.3617,            // Coordinates (decimal)
  longitude: 125.8550,         // Coordinates (decimal)
  
  // NEW: Added Week 1 Day 1
  populationDensity: 295.2,    // ρ (persons/km²) for spatial heterogeneity
  
  // Populations
  humanPopulation: 87680,      // N_h (integer)
  dogPopulation: 1500,         // N_d (integer)
  catPopulation: 800,          // N_c (integer)
  
  // Initial Infected (I_0)
  infectedDogs: 12,            // I_d(0)
  infectedCats: 3,             // I_c(0)
  infectedHumans: 0,           // I_h(0)
  
  // Vaccination
  vaccinatedDogs: 450,         // u(0) - number vaccinated
  
  // Risk Assessment
  riskLevel: "moderate",       // safe, low, moderate, high, critical
  
  // Network
  connectedMunicipalities: ["2", "9"] // IDs of connected municipalities
}
```

### **Simulation Settings Structure:**
```javascript
{
  // Basic Settings
  simulationDays: 30,          // T (simulation period)
  simulationSpeed: 1,          // UI speed multiplier
  enableAdaptiveVaccination: false,
  
  // Current System Parameters
  transmissionRate: 0.15,      // β (basic transmission rate)
  vaccinationRate: 0.8,        // u (vaccination coverage target)
  fractionalAlpha: 0.3,        // NOT fractional order (legacy name)
  environmentalRandomness: 0.2, // Basic random factor
  
  // NEW: Paper Parameters (to be added Week 1 Day 3)
  fractionalOrder: 0.95,       // α ∈ (0,1] - memory effects
  recoveryRate: 0.1,           // γ - recovery/removal rate
  stochasticIntensity: 0.1,    // σ - stochastic fluctuations
  contactProbability: 0.3,     // p - transmission likelihood
}
```

---

## **5. KEY ALGORITHMS & FUNCTIONS**

### **A. Current Simulation (useSimulationEngine.js)**

**Process Flow:**
```
startSimulation()
  ↓
initializeSimulation()
  ↓
runSimulationDay() (called every interval)
  ↓
processTransmissionDay()
  ├→ processMunicipalityTransmission() (for each municipality)
  │   ├→ Dog-to-dog transmission
  │   ├→ Cat transmission
  │   ├→ Human transmission
  │   └→ Inter-municipality transmission
  ├→ calculateRiskLevel()
  └→ applyVaccinationRecommendations()
  ↓
updateSimulationTrends()
  ↓
Advance to next day
  ↓
Check if simulation complete → stopSimulation()
```

**Current Transmission Math:**
```javascript
// Simplified probabilistic model (NOT paper's model)
const randomFactor = 1 + (Math.random() - 0.5) * environmentalFactor
const effectiveRate = baseTransmissionRate * randomFactor

const dogTransmissionProbability = effectiveRate * (infectedDogs / dogPopulation)
const expectedNewDogInfections = susceptibleDogs * dogTransmissionProbability
const newInfectedDogs = Math.floor(Math.random() * expectedNewDogInfections * 2)
```

**Problem:** This is NOT the fractional-order stochastic model from the paper!

---

### **B. Risk Calculation (simulationUtils.js)**

**Current Risk Score:**
```javascript
// Multi-factor scoring (NOT paper's formula)
let score = 0
score += totalInfected * 3              // Infections weighted
score += infectionRate * 2              // Infection rate weighted
score += riskLevelScores[riskLevel]     // Risk level score
score += coverageGap * 0.5              // Vaccination gap
score += populationFactor               // Population size factor
score += infectedHumans * 10            // Human cases high priority
```

**Paper's Formula (NOT IMPLEMENTED YET):**
```
R_i = I^_i(T) / N_i

Where:
  R_i = Risk score for municipality i
  I^_i(T) = Predicted infected at end of simulation period T
  N_i = Total population of municipality i
```

**Gap:** Need to implement exact paper formula in backend.

---

### **C. Predictive Analysis (simulationUtils.js)**

**Current Prediction:**
```javascript
// Simple exponential growth model
const predictedInfected = currentInfected * Math.pow(1 + growthRate, days)

// Risk level determined by thresholds
if (predictedInfectionRate <= 2) return 'low'
else if (predictedInfectionRate <= 5) return 'moderate'
else return 'high'
```

**Problem:** Uses simple exponential model, not fractional-order differential equations.

---

### **D. Cost Estimation (simulationUtils.js)**

**DOH Standard Costs:**
```javascript
INTERVENTION_COSTS = {
  dogVaccine: ₱150,              // Per dose
  catVaccine: ₱120,              // Per dose
  humanPEP: ₱15,000,             // Post-exposure prophylaxis
  humanPreExposure: ₱8,000,      // Pre-exposure vaccination
  mobilizationPerMunicipality: ₱5,000,
  vaccinationTeamPerDay: ₱3,000,
  publicAwareness: ₱2,000,
  surveillancePerMunicipality: ₱1,500/month,
  laboratoryTestPerAnimal: ₱500,
  emergencyResponseTeam: ₱10,000,
  quarantineFacilityPerDay: ₱2,000,
  administrativeOverhead: 10%
}
```

**Cost Calculation:**
```javascript
totalCost = vaccinationCost + pepCost + emergencyCost

vaccinationCost = (dogs * ₱150) + (cats * ₱120) + operational costs
pepCost = exposedHumans * 0.2 * ₱15,000
emergencyCost = (for high/critical only) team + lab + quarantine costs
```

**Status:** ✅ FULLY IMPLEMENTED - This part is complete and working.

---

## **6. ROUTING STRUCTURE**

### **Routes:**
```javascript
/ (LandingPage)                    ← Welcome screen
  ↓ Click "Get Started"
/dashboard (AppLayout wrapper)     ← Main app with sidebar
  ├── /dashboard                   → DashboardPage (stats, charts)
  ├── /municipalities              → MunicipalityManagement (CRUD)
  ├── /simulation                  → SimulationPage (controls)
  ├── /results                     → ResultsPage (maps, results)
  ├── /predictive-analysis         → PredictiveAnalysisPage (forecasts)
  ├── /cost-estimation             → CostEstimationPage (budget)
  └── /about                       → AboutPage (info)
```

### **Navigation Flow:**
```
User lands on LandingPage
  ↓
Clicks "Get Started" → router.push('/dashboard')
  ↓
AppLayout loads (sidebar + top bar)
  ↓
Default child route: DashboardPage shows
  ↓
User navigates via sidebar:
  - Dashboard icon → /dashboard
  - Municipalities icon → /municipalities
  - Simulation icon → /simulation
  - Results icon → /results
  - Predictive Analysis icon → /predictive-analysis
  - Cost Estimation icon → /cost-estimation
  - About icon → /about
```

---

## **7. WHAT'S MISSING FOR ACADEMIC RESEARCH**

### **❌ NOT IMPLEMENTED (Must Add):**

1. **Fractional-Order Derivatives (α)**
   - Current: Simple Math.random() multiplication
   - Need: Grünwald-Letnikov method
   - Status: ✅ DONE in backend `fractional_calculus.py`

2. **Stochastic Processes (dW)**
   - Current: Basic Math.random()
   - Need: Wiener process, Brownian motion
   - Status: ⏳ TODO Week 1 Day 3

3. **Exact Paper Formula for Risk Score**
   - Current: Multi-factor weighted scoring
   - Need: R_i = I^_i(T) / N_i
   - Status: ⏳ TODO Week 1 Day 5

4. **SIR Model with All Parameters**
   - Current: Simplified probability calculations
   - Need: dI/dt^α = β*p*S*I/N - γ*I + u + σ*dW
   - Status: ⏳ TODO Week 1 Day 4-5

5. **Memory Effects**
   - Current: No memory of past states
   - Need: Fractional derivatives capture history
   - Status: ⏳ TODO (part of transmission model)

6. **Spatial Heterogeneity (ρ)**
   - Current: Simple cross-border reduction (30%)
   - Need: Proper ρ(x) integration in transmission
   - Status: ⏳ TODO (part of transmission model)

7. **Recovery Rate (γ)**
   - Current: Not implemented
   - Need: Animals/humans recover or removed
   - Status: ⏳ TODO (part of transmission model)

8. **Contact Probability (p)**
   - Current: Implicit in transmission rate
   - Need: Explicit p(t) parameter
   - Status: ⏳ TODO (part of transmission model)

---

## **8. DATA PERSISTENCE**

### **Current Storage (Browser localStorage):**
```
Keys stored:
- pawpatrol_municipalities       → municipalities array
- pawpatrol_simulation_settings  → settings object
- pawpatrol_simulation_results   → results object
- pawpatrol_vaccination_recommendations → recommendations array
```

**Flow:**
```
Page Load
  ↓
loadFromStorage() → check localStorage
  ├→ If empty: initializeDummyData() → 11 default municipalities
  └→ If exists: load saved data
  ↓
Store in Pinia state
  ↓
User makes changes
  ↓
saveAllData() → saveToStorage() → localStorage.setItem()
```

**Persistence:** All data survives page refresh (stored in browser).

---

## **9. UI/UX COMPONENTS**

### **Global Components (Registered in main.js):**
- Button, Card, Sidebar, InputText, InputNumber
- Dropdown, MultiSelect, DataTable, Column
- Dialog, Toast, ProgressBar, ConfirmDialog

### **Custom Components:**
- LoadingSpinner (with pulse animation)
- SkeletonCard (loading placeholder)

### **Directives:**
- v-tooltip (PrimeVue tooltip)

### **Styling:**
- Tailwind CSS (utility-first)
- PrimeVue theme (Lara Light Blue)
- Custom animations in main.css (pulse, rings)

---

## **10. COLOR SCHEME (From UI/COLOR PALLETE.txt)**

```
Primary: #5289AD (Blue)
Dark Blue: #243C4C
Muted Blue: #698696
Light Blue: #B0C4DE
Background: #F5F7FA

Risk Levels:
- Safe: #10B981 (Green)
- Low: #FBBF24 (Yellow)
- Moderate: #F97316 (Orange)
- High: #EF4444 (Red)
- Critical: #991B1B (Dark Red)
```

---

## **11. WHAT STAYS vs WHAT CHANGES**

### **✅ STAYS (95% of code):**
- All Vue pages and UI components
- Routing structure
- Pinia store structure
- Data persistence (localStorage)
- Municipality management (CRUD)
- Cost estimation (fully working)
- All styling and animations
- Navigation and layout

### **🔧 CHANGES (5% of code):**
- `useSimulationEngine.js` → Change to call backend API instead of local simulation
- Add `apiClient.js` → New file for HTTP requests
- `SimulationPage.vue` → Add new parameter controls (α, γ, σ, p)
- `ResultsPage.vue` → Display paper formulas and new results format

---

## **12. IMPLEMENTATION STRATEGY**

### **Phase 1: Backend Math (Week 1)**
Build Python backend with correct mathematical models

### **Phase 2: Frontend Integration (Week 2)**
Connect Vue app to Python backend

### **Phase 3: Testing & Validation (Week 3)**
Verify math correctness, test all features

### **Phase 4: Documentation & Deployment (Week 4)**
Document everything, deploy to free hosting

---

## **SUMMARY: SYSTEM UNDERSTANDING ✅ COMPLETE**

I now have complete knowledge of:
- ✅ Project structure and architecture
- ✅ Data flow and state management
- ✅ Current simulation algorithms
- ✅ What's implemented vs what's missing
- ✅ Routing and navigation
- ✅ UI components and styling
- ✅ Storage mechanisms
- ✅ Cost estimation (complete)
- ✅ All pages and their purposes
- ✅ Mathematical gaps that need filling
- ✅ Clear path forward for Week 1-4

**Ready to continue implementation with full context! 🚀**
