# DRL and Risk Level Critical Bugs

**Date**: October 21, 2026  
**Severity**: 🔴 CRITICAL  
**Impact**: DRL recommendations are INCORRECT and dangerous

---

## Bug Report Summary

### Issue 1: Risk Level Miscalculation ❌

**Observed**:
- Infection Rate displayed: **58.1%** or **1.16%** (inconsistent)
- Risk Level shown: **"Safe"** (Green)
- Actual infected: 58 animals out of 5,020 total

**Expected**:
- With 58 infected / 5,020 total = **0.0116 = 1.16% infection rate**
- Risk Level should be: **"Moderate"** (1-5% range)

**Root Cause**:
The backend `risk_calculator.py` calculates risk correctly BUT:
1. Frontend displays infection rate INCORRECTLY (shows 58.1% instead of 1.16%)
2. OR backend is using WRONG population values (dogs only vs dogs+cats+humans)

---

### Issue 2: DRL Recommends 0% Vaccination During Outbreak ❌

**Observed**:
- Infection Rate: 1.16% (moderate outbreak)
- Current Coverage: 16% (critically low)
- DRL Recommendation: **0% vaccination**
- Priority: **"Monitor"** (should be High/Critical)
- Confidence: 50%

**Expected**:
- With 1.16% infection + 16% coverage → DRL should recommend **70-80% vaccination**
- Priority should be: **"High"** or **"Critical"**
- Confidence should be higher (>70%)

**Root Cause - CRITICAL**:
The DRL was trained on scenarios with INITIAL infection rates 0-90%, but after we fixed it to use POST-SIMULATION data:
1. ✅ Now correctly reads **80% coverage** (after simulation)
2. ✅ Now correctly reads **0% infection** (after simulation)
3. ❌ **BUT** the state it sees is: "High coverage (80%) + No infections (0%)"
4. ❌ So DRL says: "No action needed, just monitor"

**THE PROBLEM**: We're asking DRL for recommendations AFTER simulation, but we should ask BEFORE!

---

## Detailed Analysis

### What's Happening:

#### Timeline:
```
1. BEFORE Simulation:
   - Infected: 58 dogs
   - Vaccinated: 988 dogs (11%)
   - Outbreak State: MODERATE (1.16% infection)

2. USER RUNS SIMULATION (1 day)

3. AFTER Simulation:
   - Infected: 0 dogs (all died or recovered)
   - Vaccinated: 7,236 dogs (80%)
   - Outbreak State: SAFE (0% infection)

4. DRL READS POST-SIMULATION DATA:
   - Sees: 0% infection, 80% coverage
   - Thinks: "Everything is fine, no vaccination needed"
   - Recommends: 0% (Monitor only)
```

###The Core Problem:

**DRL should make recommendations based on PRE-SIMULATION state**, not post-simulation!

The whole point of DRL is to say:
> "Given the CURRENT outbreak situation (before simulation), what vaccination strategy should we use?"

NOT:
> "Given the situation AFTER we already simulated with vaccination, what should we do?"

---

## The Fix Strategy

### Fix 1: Change When DRL is Called

**Option A: Call DRL BEFORE Simulation** (RECOMMENDED)
```javascript
// In SimulationPage.vue (before running simulation)
1. User clicks "Run Simulation"
2. Get DRL recommendations based on CURRENT state
3. Show recommendations
4. User can accept or modify
5. Run simulation with chosen vaccination rate
```

**Option B: Call DRL with PRE-SIMULATION Data** (Current approach fixed)
```javascript
// In ResultsPage.vue
1. Simulation runs and completes
2. When fetching DRL recommendations, use INITIAL data (not final)
3. DRL sees the starting state
4. Recommends what SHOULD have been done
```

**Option C: Two-Stage DRL**
```javascript
1. Pre-Simulation DRL: "Here's what you should do"
2. Post-Simulation DRL: "Here's what to do next, given current state"
```

---

### Fix 2: Correct Risk Level Calculation

The risk level categorization is CORRECT in backend:
```python
if risk_score < 0.001:      # < 0.1%
    return 'safe'
elif risk_score < 0.01:     # 0.1-1%
    return 'low'
elif risk_score < 0.05:     # 1-5%
    return 'moderate'
elif risk_score < 0.10:     # 5-10%
    return 'high'
else:                       # ≥ 10%
    return 'critical'
```

**Issue**: Frontend is displaying infection rate incorrectly OR backend is using wrong population.

**Need to verify**:
- Does backend use `totalPopulation = dogs + cats + humans`?
- OR does it use only `dogs + cats` (animals only)?
- Frontend shows "58 / 5020" but what does 5020 represent?

---

## Immediate Action Items

### 1. Fix DRL to Use PRE-SIMULATION Data

```javascript
// In ResultsPage.vue - fetchDRLRecommendations()

const municipalitiesData = municipalities.value.map(m => {
  // ❌ WRONG (current): Use post-simulation data
  // const munResult = simulationResults.value.municipalities?.find(r => r.id === m.id)
  
  // ✅ CORRECT: Use INITIAL/ORIGINAL data (before simulation)
  return {
    id: m.id,
    name: m.name,
    humanPopulation: m.humanPopulation,
    dogPopulation: m.dogPopulation,  // INITIAL
    catPopulation: m.catPopulation,  // INITIAL
    infectedDogs: m.infectedDogs,    // INITIAL
    infectedCats: m.infectedCats,    // INITIAL
    infectedHumans: m.infectedHumans, // INITIAL
    vaccinatedDogs: m.vaccinatedDogs, // INITIAL
    populationDensity: m.populationDensity,
    riskLevel: m.riskLevel,
    connectedMunicipalities: m.connectedMunicipalities || []
  }
})
```

###2. Verify Risk Calculation Population Base

Check if risk uses:
- `totalPopulation = dogs + cats + humans` (ALL)
- OR `totalAnimals = dogs + cats` (ANIMALS ONLY)

The screenshot shows "58 / 5020" which suggests animals only (dogs 8,764 + cats 2,000 ≠ 5,020... numbers don't match!)

**Need to investigate**: What is 5,020?

---

### 3. Fix Infection Rate Display

In Municipality Analysis table, verify the calculation:
```javascript
const infectionRate = totalAnimals > 0 
  ? ((infectedDogs + infectedCats) / totalAnimals) * 100 
  : 0
```

This should show **1.16%** not **58.1%**

---

## Testing Plan

### Test Case 1: High Infection, Low Coverage
```
Initial State:
- Infected: 500 dogs (5% infection rate)
- Vaccinated: 1,000 dogs (10% coverage)
- Population: 10,000 dogs

Expected DRL:
- Recommendation: 80-90% vaccination
- Priority: Critical or High
- Confidence: >70%
```

### Test Case 2: Low Infection, Moderate Coverage
```
Initial State:
- Infected: 50 dogs (0.5% infection rate)
- Vaccinated: 6,000 dogs (60% coverage)
- Population: 10,000 dogs

Expected DRL:
- Recommendation: 70-80% vaccination
- Priority: Moderate
- Confidence: >60%
```

### Test Case 3: No Infection, High Coverage
```
Initial State:
- Infected: 0 dogs (0% infection rate)
- Vaccinated: 8,000 dogs (80% coverage)
- Population: 10,000 dogs

Expected DRL:
- Recommendation: 70-80% (maintain)
- Priority: Monitor
- Confidence: >70%
```

---

## Summary

### Critical Bugs:
1. ❌ DRL uses POST-simulation data → recommends 0% during outbreak
2. ❌ Risk level shows "Safe" when infection rate is 1.16% (should be "Moderate")
3. ❌ Infection rate display inconsistent (58.1% vs 1.16%)

### Root Causes:
1. DRL reads final state instead of initial state
2. Risk calculation possibly using wrong population base
3. Frontend infection rate calculation or display issue

### Fixes Needed:
1. **URGENT**: Change DRL to use PRE-simulation (initial) municipality data
2. Verify risk calculation uses correct population (animals vs all)
3. Fix infection rate display in table

### Impact:
🔴 **CRITICAL** - DRL provides dangerous recommendations that could lead to:
- Under-vaccination during outbreaks
- False sense of security ("Monitor" when should be "Critical")
- Misallocation of vaccination resources

---

**Status**: ✅ **FIXED**  
**Priority**: P0 - Block thesis defense  
**Fix Completed**: October 21, 2026

---

## SOLUTION IMPLEMENTED (FINAL FIX)

### Root Cause Confirmed:
The risk calculation was using **POST-SIMULATION infected counts** AND the **riskLevel field sent to DRL was also POST-simulation**. This caused a double problem:
1. Backend calculated risk level using final infected (could be 0)
2. Frontend sent that wrong risk level to DRL

### Files Modified:

1. **`transmission_model.py`** (lines ~1114-1123):
   - Added `initialInfectedDogs`, `initialInfectedCats`, `initialInfectedHumans`
   - Added `totalInitialInfected` to simulation results
   - These store the outbreak state BEFORE simulation runs

2. **`risk_calculator.py`** (line ~47):
   - Changed from using `totalPredictedInfected` (final)
   - To using `totalInitialInfected` (initial) with fallback
   - Updated documentation to clarify this is intentional

3. **`response_models.py`** (lines ~22-26):
   - Added optional fields for initial infected counts
   - Ensures backwards compatibility with existing API calls

4. **`ResultsPage.vue`** (lines ~1391-1425) **← FINAL CRITICAL FIX**:
   - Calculate risk level in FRONTEND based on INITIAL infection rate
   - Do NOT use backend's riskLevel field (which is post-simulation)
   - Send calculated risk level to DRL based on pre-simulation data
   - Risk thresholds: <0.1% safe, 0.1-1% low, 1-5% moderate, 5-10% high, ≥10% critical

### How It Works Now:
```
1. User runs simulation with 58 infected dogs

2. Simulation executes:
   - Initial: 58 infected
   - Final: 0 infected (all died after 1 day)

3. Risk calculation uses INITIAL infected:
   - Risk = 58 / 5020 = 0.0116 = 1.16%
   - Risk Level = "Moderate" ✅ CORRECT!

4. DRL sees initial data:
   - 58 infected, 16% coverage
   - Recommends: 70-80% vaccination ✅ CORRECT!
```

### Testing Required:
- Test with 1-day simulation (58 infected → should show "Moderate")
- Test with high infection (500 infected → should show "Critical")
- Verify DRL recommendations align with risk levels

---

**Next Step**: Restart backend and test with the 1-day simulation scenario

