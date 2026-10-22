# Testing Guide: Regional Risk Map Fix

**Date:** January 15, 2027  
**Feature:** Centralized Regional Risk Map  
**Status:** Ready for Testing ✅

---

## 🧪 Test Plan

### Prerequisites
- System running (npm run dev)
- Clean browser cache or use incognito mode
- Multiple browser tabs/windows available

---

## Test Case 1: Basic Cross-Municipality Update

**Objective:** Verify that when Municipality A updates their risk level, Municipality B can see it.

### Steps:

1. **Open Browser Tab 1**
   ```
   - Go to http://localhost:5173
   - Click "Login"
   - Enter access code: MACO
   - You should see Dashboard
   ```

2. **Check Initial State**
   ```
   - Look at Regional Risk Map
   - Note MACO's current marker color (likely green/safe)
   - Note infection counts
   ```

3. **Run Simulation (MACO)**
   ```
   - Click "Simulation" in sidebar
   - Set parameters:
     • Simulation Days: 30
     • Environmental Uncertainty: 0.10 (Moderate)
   - Click "Run Simulation"
   - Wait for completion
   ```

4. **Check MACO's Results**
   ```
   - Click "Results" in sidebar
   - Note MACO's risk level (should change to moderate/high)
   - Go back to Dashboard
   - Regional Risk Map should show MACO with new color
   ```

5. **Open Browser Tab 2 (or different browser)**
   ```
   - Go to http://localhost:5173
   - Click "Login"
   - Enter access code: LAAK
   - You should see Dashboard
   ```

6. **Check LAAK's Regional Risk Map**
   ```
   ✅ EXPECTED: MACO should show the same risk level as in Tab 1
   ❌ BEFORE FIX: MACO would show as "safe" (outdated)
   ```

7. **Verify with Refresh Button**
   ```
   - Click the "Refresh" button on Regional Risk Map
   - Map should update with latest data
   - MACO's marker should match Tab 1
   ```

**Expected Result:** ✅ LAAK sees MACO's updated risk level without running their own simulation

---

## Test Case 2: Multiple Municipality Updates

**Objective:** Verify that multiple municipalities can update and all changes are visible to everyone.

### Steps:

1. **Tab 1: MACO**
   ```
   - Login as MACO
   - Run simulation → Risk becomes "moderate"
   - Note: MACO = Moderate (orange marker)
   ```

2. **Tab 2: PANTUKAN**
   ```
   - Login as PANTUKAN
   - Increase initial infected dogs to 50 in Municipality Management
   - Run simulation → Risk becomes "high"
   - Note: PANTUKAN = High (red marker)
   ```

3. **Tab 3: NABUNTURAN**
   ```
   - Login as NABUNTURAN
   - Open Dashboard
   - Check Regional Risk Map
   ```

**Expected Result:** 
```
✅ NABUNTURAN sees:
   - MACO: Moderate (orange)
   - PANTUKAN: High (red)
   - NABUNTURAN: Safe (green)
   - All other municipalities: Safe (green)
```

**Legend should show:**
```
Safe (8)
Low Risk (0)
Moderate (1)  ← MACO
High Risk (1)  ← PANTUKAN
Critical (0)
```

---

## Test Case 3: Data Persistence

**Objective:** Verify that regional risk data persists across browser sessions.

### Steps:

1. **Tab 1: MACO**
   ```
   - Login as MACO
   - Run simulation → Risk becomes "moderate"
   ```

2. **Close ALL browser tabs**
   ```
   - Close entire browser
   - Wait 10 seconds
   ```

3. **Reopen Browser**
   ```
   - Open NEW browser window
   - Go to http://localhost:5173
   - Login as LAAK
   - Open Dashboard
   - Check Regional Risk Map
   ```

**Expected Result:** 
```
✅ LAAK still sees MACO as "moderate"
✅ Data persisted in localStorage
```

---

## Test Case 4: Refresh Button

**Objective:** Verify the new Refresh button works correctly.

### Steps:

1. **Tab 1: MACO**
   ```
   - Login as MACO
   - Run simulation
   ```

2. **Tab 2: LAAK (already open from before simulation)**
   ```
   - Dashboard is still showing old data
   - Click "Refresh" button on Regional Risk Map
   ```

**Expected Result:**
```
✅ Refresh icon spins
✅ Map updates within 1 second
✅ MACO's new risk level appears
✅ Legend counts update
```

---

## Test Case 5: Admin View

**Objective:** Verify admin can see all municipalities' risk levels.

### Steps:

1. **Multiple Municipalities Run Simulations**
   ```
   - MACO → Moderate
   - PANTUKAN → High
   - MONKAYO → Low
   ```

2. **Login as Admin**
   ```
   - Go to http://localhost:5173
   - Login with: ADMIN
   - Open Dashboard
   ```

**Expected Result:**
```
✅ Admin sees complete regional picture:
   - Summary cards show totals across ALL municipalities
   - Regional Risk Map shows all updated risk levels
   - Legend shows accurate counts
   - Can click any municipality marker for details
```

---

## Test Case 6: Same Device, Different Browsers

**Objective:** Verify data sync works across different browsers on same device.

### Steps:

1. **Chrome Browser**
   ```
   - Login as MACO
   - Run simulation → Moderate risk
   ```

2. **Firefox Browser** (same computer)
   ```
   - Go to http://localhost:5173
   - Login as LAAK
   - Check Regional Risk Map
   ```

**Expected Result:**
```
⚠️ LIMITATION: May NOT sync across different browsers
✅ Works within same browser (multiple tabs/windows)

Reason: Each browser has separate localStorage
Solution: This is expected behavior for localStorage-based approach
         For true cross-browser sync, need backend database
```

---

## Test Case 7: Risk Level Categories

**Objective:** Verify all risk levels display correctly with proper colors.

### Setup:
```javascript
// In browser DevTools console, manually set different risk levels:
const regionalData = JSON.parse(localStorage.getItem('pawpatrol_regional_risk_data')) || {}

regionalData['maco'] = { ...regionalData['maco'], riskLevel: 'safe', lastUpdated: new Date().toISOString() }
regionalData['laak'] = { ...regionalData['laak'], riskLevel: 'low', lastUpdated: new Date().toISOString() }
regionalData['mabini'] = { ...regionalData['mabini'], riskLevel: 'moderate', lastUpdated: new Date().toISOString() }
regionalData['pantukan'] = { ...regionalData['pantukan'], riskLevel: 'high', lastUpdated: new Date().toISOString() }
regionalData['monkayo'] = { ...regionalData['monkayo'], riskLevel: 'critical', lastUpdated: new Date().toISOString() }

localStorage.setItem('pawpatrol_regional_risk_data', JSON.stringify(regionalData))

// Refresh page
location.reload()
```

**Expected Result:**
```
✅ Map shows 5 different colors:
   🟢 MACO: Green (safe)
   🟡 LAAK: Yellow (low)
   🟠 MABINI: Orange (moderate)
   🔴 PANTUKAN: Red (high)
   🟤 MONKAYO: Dark Red (critical)

✅ Legend counts:
   Safe (6)
   Low Risk (1)
   Moderate (1)
   High Risk (1)
   Critical (1)
```

---

## Test Case 8: Popup Information

**Objective:** Verify municipality popups show correct data.

### Steps:

1. **Login as any municipality**
2. **Click on a marker on Regional Risk Map**

**Expected Popup Content:**
```
Municipality Name: [e.g., Maco]
Risk Level: [Current risk level]
Infected: [X] dogs
Vaccinated: [X] dogs
Last updated: [Date]
```

3. **Close popup** → Map should re-center automatically

**Expected Result:**
```
✅ Popup shows accurate data
✅ Risk level matches marker color
✅ Map re-centers after popup closes
```

---

## Debugging Tools

### View Regional Risk Data in Console

```javascript
// In browser DevTools console:

// View raw regional data
const regional = JSON.parse(localStorage.getItem('pawpatrol_regional_risk_data'))
console.table(regional)

// View municipalities data
const munis = JSON.parse(localStorage.getItem('pawpatrol_municipalities'))
console.table(munis.map(m => ({
  name: m.name,
  riskLevel: m.riskLevel,
  infectedDogs: m.infectedDogs
})))

// Clear all data (reset)
localStorage.clear()
location.reload()
```

### Expected Console Logs

When system is working correctly, you should see:
```
✅ Regional risk data updated: 11 municipalities
✅ Merged with regional risk data: 11 municipalities
🔄 Refreshing regional risk data...
✅ Regional risk data refreshed
```

---

## Common Issues & Solutions

### Issue 1: Regional Risk Map Not Updating

**Symptoms:**
- LAAK doesn't see MACO's risk level change
- Map shows outdated colors

**Solutions:**
1. Click "Refresh" button on Regional Risk Map
2. Refresh browser page (F5)
3. Check DevTools console for errors
4. Verify regional data exists:
   ```javascript
   localStorage.getItem('pawpatrol_regional_risk_data')
   ```

### Issue 2: Refresh Button Not Working

**Symptoms:**
- Clicking Refresh does nothing
- No spinning animation

**Solutions:**
1. Check browser console for JavaScript errors
2. Verify `refreshRegionalRiskData()` is defined in store
3. Clear cache and hard reload (Ctrl+Shift+R)

### Issue 3: Wrong Municipality Count in Legend

**Symptoms:**
- Legend shows "Moderate (0)" but map has moderate markers
- Counts don't match visual

**Solutions:**
1. Refresh regional data
2. Check that risk levels are properly saved:
   ```javascript
   const regional = JSON.parse(localStorage.getItem('pawpatrol_regional_risk_data'))
   console.log(Object.values(regional).map(m => m.riskLevel))
   ```

### Issue 4: Data Not Persisting

**Symptoms:**
- Close browser → Data resets

**Solutions:**
1. Check localStorage quota (shouldn't exceed 5-10 MB)
2. Verify browser allows localStorage (not in private mode restrictions)
3. Check if localStorage is being cleared by browser settings

---

## Performance Benchmarks

**Expected Performance:**
- Regional data update: < 50ms
- Regional data load: < 20ms
- Merge operation: < 100ms
- Map refresh: < 500ms
- Total sync time: < 1 second

**Test Performance:**
```javascript
// In browser console:
console.time('Regional Update')
// Run simulation or click refresh
console.timeEnd('Regional Update')
// Should be < 1000ms
```

---

## Acceptance Criteria

All of these must pass for the fix to be considered successful:

- [ ] ✅ MACO updates risk → LAAK sees it
- [ ] ✅ Multiple municipalities can update simultaneously
- [ ] ✅ Data persists after browser close/reopen
- [ ] ✅ Refresh button works and shows loading state
- [ ] ✅ Admin sees all municipalities' current status
- [ ] ✅ All 5 risk levels display with correct colors
- [ ] ✅ Legend counts are accurate
- [ ] ✅ Map popups show correct information
- [ ] ✅ No console errors during operation
- [ ] ✅ Performance is acceptable (< 1 second)

---

## Rollback Procedure

If the fix causes issues, rollback:

1. **Delete new files:**
   ```bash
   rm src/services/regionalRiskSync.js
   rm TEST_REGIONAL_RISK_MAP_FIX.md
   rm REGIONAL_RISK_MAP_FIX.md
   ```

2. **Restore original localStorage.js:**
   ```bash
   git checkout src/services/localStorage.js
   git checkout src/stores/index.js
   git checkout src/pages/DashboardPage.vue
   ```

3. **Clear localStorage:**
   ```javascript
   localStorage.clear()
   location.reload()
   ```

---

## Next Steps After Testing

Once testing is complete:

1. **Document Results**
   - Record which test cases passed/failed
   - Note any unexpected behavior
   - Screenshot any visual issues

2. **User Training**
   - Explain Refresh button to users
   - Show how to verify regional data
   - Demonstrate cross-municipality visibility

3. **Consider Backend Migration**
   - If localStorage limitations are problematic
   - Plan PostgreSQL/MongoDB implementation
   - Design API endpoints for regional sync

---

**Tester Name:** _______________  
**Date Tested:** _______________  
**Test Results:** ✅ Pass / ❌ Fail  
**Notes:** _______________________________________________
