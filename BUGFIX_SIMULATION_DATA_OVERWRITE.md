# CRITICAL BUG FIX: Simulation Overwriting Actual Data

## Bug Report

**Severity:** CRITICAL  
**Status:** ✅ FIXED  
**Reported By:** User  
**Date:** Based on conversation

---

## Problem Description

When running a simulation, the system was **overwriting actual current infection data** with **predicted simulation results**. This caused users to **lose their real data** after running simulations.

### Example of the Bug:

```
USER ENTERS DATA:
- Current Infected Dogs: 1
- Current Infected Cats: 1  
- Current Infected Humans: 1

USER RUNS SIMULATION (365 days)

AFTER SIMULATION:
- Current Infected Dogs: 0 (LOST!)
- Current Infected Cats: 0 (LOST!)
- Current Infected Humans: 0 (LOST!)
```

The actual current infection counts disappeared completely!

---

## Root Cause

In `src/composables/useSimulationEngine.js`, the code was overwriting actual data:

```javascript
// 🐛 BUG: This overwrites actual data with predictions
municipality.infectedDogs = result.predictedInfectedDogs || 0
municipality.infectedCats = result.predictedInfectedCats || 0
municipality.infectedHumans = result.predictedInfectedHumans || 0
```

This meant:
1. User-entered actual infection data was replaced with simulation predictions
2. After simulation, there was no way to distinguish actual vs predicted data
3. Users lost their real current case data permanently

---

## The Fix

**Changed the simulation engine to:**
1. **Store predictions separately** in `predictedInfected*` fields
2. **Preserve actual current data** in `infected*` fields
3. **Never overwrite user-entered data** during simulation

### Code Changes:

**File:** `src/composables/useSimulationEngine.js`

**BEFORE (Buggy Code):**
```javascript
// Update predicted values (for results display)
municipality.predictedInfectedDogs = result.predictedInfectedDogs
municipality.predictedInfectedCats = result.predictedInfectedCats
municipality.predictedInfectedHumans = result.predictedInfectedHumans

// 🐛 BUG: Overwrites actual data!
municipality.infectedDogs = result.predictedInfectedDogs || 0
municipality.infectedCats = result.predictedInfectedCats || 0
municipality.infectedHumans = result.predictedInfectedHumans || 0
```

**AFTER (Fixed Code):**
```javascript
// ✅ FIXED: Store predictions separately, don't overwrite actual current data
municipality.predictedInfectedDogs = result.predictedInfectedDogs || 0
municipality.predictedInfectedCats = result.predictedInfectedCats || 0
municipality.predictedInfectedHumans = result.predictedInfectedHumans || 0

// Keep actual current data unchanged
// municipality.infectedDogs - NOT CHANGED (keeps user-entered value)
// municipality.infectedCats - NOT CHANGED (keeps user-entered value)
// municipality.infectedHumans - NOT CHANGED (keeps user-entered value)
```

---

## Data Structure After Fix

### Municipality Data Model:

```javascript
{
  id: 'maco',
  name: 'Maco',
  
  // ACTUAL CURRENT DATA (User-entered, never overwritten by simulation)
  infectedDogs: 1,           // Real current cases
  infectedCats: 1,           // Real current cases
  infectedHumans: 1,         // Real current cases
  
  // PREDICTED DATA (Simulation results, separate from actual)
  predictedInfectedDogs: 50,    // Predicted after X days
  predictedInfectedCats: 30,    // Predicted after X days
  predictedInfectedHumans: 5,   // Predicted after X days
  totalPredictedInfected: 85,   // Sum of all predictions
  
  // OTHER DATA
  riskScore: 0.05,
  riskLevel: 'moderate',
  // ... other fields
}
```

---

## How It Works Now

### Correct Flow:

```
1. USER ENTERS DATA:
   - Current Infected Dogs: 1
   - Current Infected Cats: 1
   - Current Infected Humans: 1

2. USER RUNS SIMULATION (365 days)

3. SIMULATION RUNS:
   - Backend calculates predictions
   - Frontend receives predicted values

4. AFTER SIMULATION:
   ✅ Current Infected Dogs: 1 (PRESERVED - actual data)
   ✅ Predicted Infected Dogs (365d): 50 (NEW - simulation result)
   ✅ Current Infected Cats: 1 (PRESERVED - actual data)
   ✅ Predicted Infected Cats (365d): 30 (NEW - simulation result)
   ✅ Current Infected Humans: 1 (PRESERVED - actual data)
   ✅ Predicted Infected Humans (365d): 5 (NEW - simulation result)
```

---

## Impact

### Before Fix (Buggy):
- ❌ Actual data lost after simulation
- ❌ No distinction between current and predicted
- ❌ Users had to re-enter data after every simulation
- ❌ Data integrity compromised

### After Fix:
- ✅ Actual data preserved forever
- ✅ Clear separation: actual vs predicted
- ✅ Users can run multiple simulations without losing data
- ✅ Data integrity maintained

---

## Testing

To verify the fix:

1. **Go to Municipality Management**
   - Enter infection data: 1 dog, 1 cat, 1 human
   - Save data

2. **Go to Simulation Page**
   - Run simulation for 365 days
   - Wait for completion

3. **Check Results Page**
   - Verify predicted infections are shown (separate from actual)

4. **Go Back to Municipality Management**
   - ✅ Verify actual data still shows: 1 dog, 1 cat, 1 human
   - ✅ Data should NOT be 0 or changed

5. **Go to Dashboard**
   - ✅ Verify cards show actual current cases (not predictions)

---

## Related Files

- `src/composables/useSimulationEngine.js` - Main fix location
- `src/pages/ResultsPage.vue` - Displays predictions
- `src/pages/DashboardPage.vue` - Displays actual current data
- `src/pages/MunicipalityManagement.vue` - Data entry form

---

## Recommendations

1. **Always use:**
   - `infectedDogs/Cats/Humans` for **actual current data**
   - `predictedInfectedDogs/Cats/Humans` for **simulation results**

2. **Never overwrite actual data** during simulation

3. **UI should clearly label:**
   - "Current Infected" (actual data)
   - "Predicted Infected" (simulation results)

4. **Add data backup:**
   - Consider backing up municipality data before simulation
   - Add "Restore Original Data" button in case of issues

---

## Status: ✅ FIXED

The bug has been completely resolved. Actual infection data is now preserved when running simulations, and predictions are stored separately.

**Date Fixed:** Based on conversation  
**Tested:** Pending user verification
