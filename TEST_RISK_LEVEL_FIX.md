# Testing Instructions: Risk Level Fix

**Date**: October 21, 2026  
**Purpose**: Verify that risk level calculation now works correctly

---

## What Was Fixed

The risk level was showing "Safe" when it should show "Moderate" because it was looking at the infected count AFTER simulation (could be 0) instead of BEFORE simulation (actual outbreak severity).

**Fix**: Risk calculation now uses the initial infected count (before simulation runs).

---

## How to Test

### Step 1: Restart Backend Server

The backend needs to be restarted to load the new code:

```bash
# Navigate to backend directory
cd PawPatrol/rabies-backend

# Stop the backend if running (Ctrl+C)

# Start backend
python main.py
```

You should see:
```
✅ DRL module loaded successfully
PAWPATROL Rabies Simulation API Starting...
```

### Step 2: Run the 1-Day Simulation Test

1. **Open the frontend** (http://localhost:5173 or your dev URL)

2. **Login** to your municipality

3. **Set up the simulation**:
   - Duration: **1 day**
   - Municipality with:
     - Infected: **58 animals** (or similar moderate outbreak)
     - Total Population: **~5,000 animals**
     - Vaccination Coverage: **16%** (or similar low coverage)

4. **Click "Run Simulation"**

5. **Go to Results Page**

### Step 3: Verify Risk Level (Municipality Analysis Table)

Check the **Municipality Analysis** table:

| Expected Field | Expected Value | What to Check |
|---------------|----------------|---------------|
| **Risk Level** | **"Moderate"** (YELLOW) | Should NOT be "Safe" (green) |
| **Infection Rate** | **~1.16%** | Should be in 1-5% range |
| **Target Coverage** | **70-80%** | After simulation runs |

**PASS**: Risk Level shows "Moderate" or "High" (not "Safe") ✅  
**FAIL**: Risk Level shows "Safe" when there's an outbreak ❌

### Step 4: Verify DRL Recommendations

Check the **AI Vaccination Recommendations** section:

| Expected Field | Expected Value | What to Check |
|---------------|----------------|---------------|
| **Recommended Coverage** | **70-80%** | Should NOT be 0% |
| **Priority** | **"High"** or **"Critical"** | Should NOT be "Monitor" |
| **Confidence** | **>50%** | Should be reasonable |

**PASS**: DRL recommends 70-80% vaccination during outbreak ✅  
**FAIL**: DRL recommends 0% or very low vaccination ❌

### Step 5: Check Backend Logs

In the backend console, look for these log entries:

```python
🔍 Starting simulation with X municipalities
   First municipality: [Name]
   INPUT infectedDogs: 58
   
🔍 Simulation completed
   OUTPUT predictedInfectedDogs: 0  (or some low number)
   
🤖 DRL Input Data:
   infectedDogs: 58  (should match INPUT, not OUTPUT)
   riskLevel: moderate  (should be moderate/high, not safe)
```

**PASS**: DRL Input shows initial infected (58), not predicted (0) ✅  
**FAIL**: DRL Input shows 0 infected ❌

---

## Expected Test Results

### Scenario: 58 Infected, 16% Coverage, 1-Day Simulation

**Municipality Analysis Table**:
```
Risk Level: Moderate (YELLOW)
Infection Rate: 1.16%
Infected: 58 animals
Total: 5,020 animals
Target Coverage: 80% (after simulation)
```

**AI Vaccination Recommendations**:
```
Recommended Coverage: 75-80%
Priority: High
Confidence: 65%
Explanation: "Moderate outbreak detected..."
```

**Backend Console**:
```
INPUT infectedDogs: 58
totalInitialInfected: 58
Risk Score: 0.0116
Risk Level: moderate
```

---

## Additional Test Cases

### Test Case 2: High Outbreak (5% infection)
```
Setup:
- Infected: 250 animals
- Total: 5,000 animals
- Coverage: 10%

Expected:
- Risk Level: "High" (5-10% range)
- DRL: 80-90% recommended
- Priority: "Critical"
```

### Test Case 3: Critical Outbreak (>10% infection)
```
Setup:
- Infected: 600 animals
- Total: 5,000 animals
- Coverage: 5%

Expected:
- Risk Level: "Critical" (>10%)
- DRL: 90%+ recommended
- Priority: "Critical"
```

### Test Case 4: Safe Situation
```
Setup:
- Infected: 2 animals
- Total: 5,000 animals
- Coverage: 80%

Expected:
- Risk Level: "Safe" (<0.1%)
- DRL: 70-75% (maintain)
- Priority: "Monitor"
```

---

## Troubleshooting

### Issue: Still shows "Safe" with 1.16% infection

**Check**:
1. Did you restart the backend? (Old code cached)
2. Check backend logs for `totalInitialInfected` field
3. Try clearing browser cache and refreshing

**Solution**: Restart backend and hard refresh browser (Ctrl+Shift+R)

### Issue: Backend crashes on startup

**Check**: Python dependencies installed?

```bash
pip install -r requirements.txt
```

### Issue: DRL still recommends 0%

**Check**: 
1. Is DRL model loaded? (Check backend startup logs)
2. Is the model file present? (`drl/models/dqn_rabies_vaccination.zip`)

---

## Success Criteria

The fix is successful if:

1. ✅ Risk Level shows "Moderate" (not "Safe") for 1.16% infection
2. ✅ DRL recommends 70-80% vaccination (not 0%)
3. ✅ Priority is "High" or "Critical" (not "Monitor")
4. ✅ Backend logs show `totalInitialInfected: 58` (not 0)
5. ✅ Frontend displays consistent data across tables

---

## If Tests Fail

If any test fails, please provide:

1. **Screenshot** of Municipality Analysis table
2. **Screenshot** of AI Vaccination Recommendations
3. **Backend console logs** (copy all output)
4. **Simulation parameters** used (infected count, coverage, days)

This will help diagnose any remaining issues.

---

## Next Steps After Testing

Once confirmed working:

1. ✅ Mark issue as resolved in bug tracker
2. ✅ Update thesis documentation
3. ✅ Prepare for thesis defense demo
4. ✅ Document this as a learning case

---

**Prepared By**: Kiro AI  
**Date**: October 21, 2026  
**Status**: Ready for user testing
