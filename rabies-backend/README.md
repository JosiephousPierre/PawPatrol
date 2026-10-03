# PAWPATROL Rabies Simulation Backend

## Academic Research Implementation - Fractional-Order Stochastic Transmission Model

This backend implements the mathematical model from the research paper for rabies risk prediction and adaptive vaccination recommendations.

---

## 📐 Mathematical Model

The system implements a **Fractional-Order Stochastic Transmission Model**:

```
dI/dt^α = β * p(t) * S(t) * I(t) / N - γ * I(t) + u(t) + σ * dW(t)
```

**Where:**
- `α` = Fractional order (memory effects) ∈ (0, 1]
- `β` = Transmission rate
- `p(t)` = Contact probability
- `γ` = Recovery/removal rate
- `u(t)` = Vaccination intervention
- `σ` = Stochastic intensity
- `dW(t)` = Wiener process (Brownian motion)

**Risk Score Formula:**
```
R_i = I^_i(T) / N_i
```
- `I^_i(T)` = Predicted infected at time T
- `N_i` = Total population of municipality i

---

## 🏗️ Project Structure

```
rabies-backend/
├── main.py                      # FastAPI application
├── requirements.txt             # Dependencies
├── README.md                    # This file
│
├── models/
│   ├── request_models.py        # API request schemas
│   └── response_models.py       # API response schemas
│
├── simulation/
│   ├── fractional_calculus.py   # Grünwald-Letnikov method ✅
│   ├── stochastic_processes.py  # Wiener process, Brownian motion ✅
│   ├── transmission_model.py    # SIR model (TODO)
│   └── risk_calculator.py       # Risk scoring (TODO)
│
├── utils/
│   └── validators.py            # Input validation (TODO)
│
└── tests/
    ├── test_fractional.py       # Fractional calculus tests
    ├── test_stochastic.py       # Stochastic processes tests ✅
    └── test_simulation.py       # Integration tests (TODO)
```

---

## 🚀 Installation

### Prerequisites
- Python 3.8+
- pip

### Install Dependencies

```bash
cd rabies-backend
pip install -r requirements.txt
```

**Dependencies:**
- FastAPI 0.104.1 - Web framework
- Uvicorn 0.24.0 - ASGI server
- Pydantic 2.5.0 - Data validation
- NumPy 1.26.2 - Numerical computing
- SciPy 1.11.4 - Scientific computing
- python-dotenv 1.0.0 - Configuration

---

## 🏃 Running the Server

### Development Mode (Auto-reload)

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

**Server will be available at:** `http://localhost:8000`

**API Documentation:** `http://localhost:8000/docs`

---

## 📡 API Endpoints

### Health Check
```http
GET /api/health
```
Returns server health status.

**Response:**
```json
{
  "status": "healthy",
  "service": "rabies-simulation",
  "timestamp": "2024-07-16T12:00:00"
}
```

---

### Validate Parameters
```http
POST /api/validate-parameters
```

Validates simulation parameters before running.

**Request Body:**
```json
{
  "fractionalOrder": 0.95,
  "transmissionRate": 0.15,
  "recoveryRate": 0.1,
  "stochasticIntensity": 0.1,
  "contactProbability": 0.3
}
```

**Response:**
```json
{
  "isValid": true,
  "errors": null,
  "message": "All parameters valid"
}
```

**Validation Rules:**
- `fractionalOrder` (α): 0 < α ≤ 1
- `transmissionRate` (β): β > 0
- `recoveryRate` (γ): γ > 0
- `stochasticIntensity` (σ): σ ≥ 0
- `contactProbability` (p): 0 ≤ p ≤ 1

---

### Run Simulation
```http
POST /api/simulate
```

Runs fractional-order stochastic simulation.

**Request Body:**
```json
{
  "municipalities": [
    {
      "id": "1",
      "name": "Maco",
      "humanPopulation": 87680,
      "dogPopulation": 1500,
      "catPopulation": 800,
      "populationDensity": 295.2,
      "infectedDogs": 12,
      "infectedCats": 3,
      "infectedHumans": 0,
      "vaccinatedDogs": 450,
      "latitude": 7.3617,
      "longitude": 125.8550,
      "riskLevel": "moderate",
      "connectedMunicipalities": ["2", "9"]
    }
  ],
  "settings": {
    "simulationDays": 30,
    "fractionalOrder": 0.95,
    "transmissionRate": 0.15,
    "recoveryRate": 0.1,
    "stochasticIntensity": 0.1,
    "contactProbability": 0.3,
    "vaccinationRate": 0.8
  }
}
```

**Response:**
```json
{
  "success": true,
  "municipalities": [...],
  "riskScores": [
    {
      "municipalityId": "1",
      "municipalityName": "Maco",
      "predictedInfected": 45,
      "totalPopulation": 90080,
      "riskScore": 0.0005,
      "formula": "R_i = I^_i(T) / N_i"
    }
  ],
  "riskLevels": {
    "low": 5,
    "moderate": 4,
    "high": 2
  },
  "metadata": {
    "model": "Fractional-Order Stochastic Transmission Model",
    "fractional_order": 0.95,
    "simulation_days": 30
  }
}
```

---

## 🧪 Testing

### Run All Tests

```bash
# Test fractional calculus
python simulation/fractional_calculus.py

# Test stochastic processes
python simulation/stochastic_processes.py

# Or use pytest (if installed)
pytest tests/
```

### Test Individual Modules

```bash
# Fractional calculus
python -m simulation.fractional_calculus

# Stochastic processes
python -m simulation.stochastic_processes

# Unit tests
python tests/test_stochastic.py
```

---

## 📊 Module Documentation

### 1. Fractional Calculus (`fractional_calculus.py`)

**Implements:**
- Grünwald-Letnikov weights calculation
- Fractional derivative computation
- Fractional Euler method

**Key Functions:**
```python
grunwald_letnikov_weights(alpha, n) 
    → Calculate G-L weights for fractional derivative

fractional_derivative(f_values, alpha, h)
    → Compute D^α f(t)

fractional_euler_step(y, f_derivative, t, h, alpha, history)
    → One step of fractional Euler method
```

**Status:** ✅ Implemented and tested

---

### 2. Stochastic Processes (`stochastic_processes.py`)

**Implements:**
- Box-Muller transform (normal distribution)
- Wiener process (Brownian motion)
- Euler-Maruyama method (SDE solver)

**Key Functions:**
```python
box_muller_transform(u1, u2)
    → Generate N(0,1) random variables

wiener_increment(dt, sigma)
    → Generate dW(t) ~ N(0, dt)

wiener_process(T, dt, sigma, W0)
    → Generate complete Wiener path

euler_maruyama_simulate(x0, drift_fn, diffusion_fn, T, dt)
    → Solve SDE: dX = μ dt + σ dW
```

**Status:** ✅ Implemented and tested

---

### 3. Transmission Model (`transmission_model.py`) - TODO

**Will Implement:**
- Fractional-order SIR model
- Multi-species transmission (dogs, cats, humans)
- Spatial heterogeneity integration
- Vaccination intervention

**Expected Functions:**
```python
fractional_stochastic_sir(S0, I0, R0, alpha, beta, gamma, ...)
    → Run fractional SIR simulation

multi_species_transmission(populations, infected, parameters, ...)
    → Coupled species transmission

apply_spatial_heterogeneity(rate, density, connections)
    → Spatial modulation
```

**Status:** ⏳ Planned for Week 1 Day 4-5

---

### 4. Risk Calculator (`risk_calculator.py`) - TODO

**Will Implement:**
- Exact paper formula: R_i = I^_i(T) / N_i
- Risk categorization (low, moderate, high)
- Results aggregation

**Expected Functions:**
```python
calculate_risk_score(predicted_infected, total_population)
    → R_i = I^_i(T) / N_i

categorize_risk_level(risk_score)
    → Map score to category

calculate_risk_scores(simulation_results)
    → Process all municipalities
```

**Status:** ⏳ Planned for Week 1 Day 5

---

## 🔬 Mathematical Validation

### Fractional Calculus

**Test:** For α=1, fractional derivative should equal standard derivative

**Example:** D^1 (t²) = 2t

**Validation:** Error < 0.1 for test case

---

### Stochastic Processes

**Test 1:** Box-Muller produces N(0,1) distribution
- Mean ≈ 0 (within 0.05)
- Std ≈ 1 (within 0.05)

**Test 2:** Wiener process variance scales with time
- Var[W(T)] = σ² * T (within 15% error)

**Test 3:** Euler-Maruyama solves Geometric Brownian Motion
- All values remain positive
- Correct statistical properties

---

## 🐛 Troubleshooting

### Import Errors

```bash
# Add project root to Python path
export PYTHONPATH="${PYTHONPATH}:/path/to/rabies-backend"
```

### CORS Errors

Frontend cannot connect? Check `main.py` CORS settings:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Port Already in Use

```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process (Windows)
taskkill /PID <PID> /F
```

---

## 📝 Development Status

### ✅ Completed (Week 1 Day 1-3)
- [x] Project structure
- [x] FastAPI application setup
- [x] Request/response models
- [x] Parameter validation
- [x] Fractional calculus (Grünwald-Letnikov)
- [x] Stochastic processes (Wiener, Euler-Maruyama)
- [x] Unit tests for fractional calculus
- [x] Unit tests for stochastic processes

### ⏳ In Progress (Week 1 Day 4-5)
- [ ] Transmission model implementation
- [ ] Risk calculator with paper's formula
- [ ] Integration tests
- [ ] Full simulation pipeline

### 📅 Planned (Week 2)
- [ ] Frontend API client
- [ ] Frontend integration
- [ ] End-to-end testing

---

## 📚 References

- Research Paper: "Fractional-Order Stochastic Transmission Model for Rabies Risk Prediction"
- Grünwald-Letnikov Method: Fractional differential equations
- Wiener Process: Stochastic calculus
- Euler-Maruyama: Numerical methods for SDEs

---

## 👥 Contributors

- Academic Research Team
- PAWPATROL Development Team

---

## 📄 License

Academic Research Prototype - Educational Use Only

---

**Last Updated:** Week 1 Day 3 - July 16, 2026
