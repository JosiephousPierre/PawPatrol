# 🧪 How to Test Phase 3 - Simulation Module

## 🚀 Getting Started

### 1. Start the Development Server
```bash
cd "C:\rabies system"
npm install
npm run dev
```

The application should open at `http://localhost:5173`

---

## 📝 Testing Checklist

### ✅ **Test 1: Simulation Configuration**

1. Navigate to **Dashboard** → Click **"Run Simulation"** button
   - Or go directly to `/simulation`

2. **Verify Configuration Form**:
   - [ ] Simulation Days field (default: 30)
   - [ ] Transmission Rate field (default: 0.15)
   - [ ] Vaccination Efficiency field (default: 0.80)
   - [ ] Fractional Alpha field (default: 0.30)
   - [ ] Environmental Randomness field (default: 0.20)
   - [ ] Simulation Speed dropdown (1x, 2x, 5x, 10x)
   - [ ] Adaptive Vaccination checkbox (default: enabled)
   - [ ] Detailed Logs checkbox (default: enabled)

3. **Test Validation**:
   - Try entering invalid values:
     - Simulation days: 0 or 400 (should show error)
     - Transmission rate: -0.5 or 2 (should show error)
   - Verify error messages appear
   - Fix values and verify errors clear

4. **Test Configuration Actions**:
   - [ ] Click "Save Configuration" → Should see success toast
   - [ ] Click "Reset to Defaults" → Should reset all values
   - [ ] Click "Export Configuration" → Should download JSON file

---

### ✅ **Test 2: Run Basic Simulation**

1. **Set Up Test Parameters**:
   - Simulation Days: **10** (short test)
   - Simulation Speed: **5x** (fast)
   - Keep other defaults

2. **Start Simulation**:
   - [ ] Click "Run Simulation" button
   - [ ] Verify simulation starts
   - [ ] Watch progress bar increase
   - [ ] See current day incrementing
   - [ ] Observe "Simulation Running" banner at top

3. **Monitor Progress**:
   - [ ] Check statistics panel updates
   - [ ] Watch current day counter
   - [ ] See progress percentage
   - [ ] Note any toast notifications

4. **Let Complete**:
   - [ ] Simulation should complete at Day 10
   - [ ] "Simulation Stopped" message should appear
   - [ ] Progress bar should reach 100%

---

### ✅ **Test 3: Simulation Controls**

1. **Test Pause/Resume**:
   - Start a simulation (30 days, 2x speed)
   - [ ] Click "Pause" when at day 5-10
   - [ ] Verify simulation pauses
   - [ ] Current day should stop incrementing
   - [ ] Click "Resume"
   - [ ] Simulation should continue from same day

2. **Test Stop**:
   - While simulation running
   - [ ] Click "Stop" button
   - [ ] Simulation should terminate immediately
   - [ ] Current day preserved
   - [ ] Results should be saved

3. **Test Reset**:
   - After simulation completes or stops
   - [ ] Click "Reset" button
   - [ ] Current day should reset to 0
   - [ ] Progress bar should reset
   - [ ] Municipality data should reset to initial state
   - [ ] Only Maco should have infections (12 dogs, 3 cats)

---

### ✅ **Test 4: Adaptive Vaccination**

1. **Enable Adaptive Vaccination**:
   - [ ] Ensure "Enable Adaptive Vaccination" is checked
   - Run simulation for 20 days, speed 5x

2. **Monitor Vaccination Actions**:
   - Go to **Dashboard** during/after simulation
   - [ ] Check "Vaccinated Dogs" counts increased
   - [ ] High-risk municipalities should have higher vaccination
   - [ ] Maco (outbreak area) should receive priority vaccination

3. **Check Recommendations**:
   - Navigate to **Results** page (Phase 4 will show these)
   - Or check Browser Console for vaccination logs
   - [ ] Recommendations generated for high-risk areas
   - [ ] Priority levels assigned correctly
   - [ ] Vaccination percentages make sense

---

### ✅ **Test 5: Cross-Municipality Transmission**

1. **Initial State Check**:
   - Go to **Municipality Management**
   - [ ] Verify only **Maco** has infections initially
   - [ ] Note Maco's connected municipalities (Mawab, Laak)

2. **Run Extended Simulation**:
   - Set Simulation Days: **30**
   - Set Speed: **5x**
   - Run simulation

3. **Check Transmission Spread**:
   - After simulation, go to **Municipality Management**
   - [ ] Check if infections spread to connected municipalities
   - [ ] Verify Mawab or Laak have infections
   - [ ] Risk levels should change from "Safe" to higher levels
   - [ ] Further connected municipalities may be affected

---

### ✅ **Test 6: Risk Level Changes**

1. **Monitor Risk Levels**:
   - Start simulation (30 days, 2x speed)
   - Watch Municipality Management table

2. **Expected Changes**:
   - [ ] Maco starts as "Moderate" risk
   - [ ] As infections spread, risk may increase to "High" or "Critical"
   - [ ] Municipalities receiving infections should change from "Safe"
   - [ ] Vaccinated areas should improve risk levels over time

---

### ✅ **Test 7: Data Persistence**

1. **Start Long Simulation**:
   - Set 60 days, 1x speed
   - Start simulation
   - Let it run for ~10-15 seconds (10-15 days)

2. **Test Persistence**:
   - [ ] **Refresh the browser page** (F5)
   - [ ] Go back to Dashboard
   - [ ] Check that current day is preserved
   - [ ] Infection counts should match pre-refresh
   - [ ] Go to Simulation page
   - [ ] Configuration should be saved

3. **Resume After Refresh**:
   - [ ] Configuration still loaded
   - [ ] Can start new simulation
   - [ ] Previous results preserved

---

### ✅ **Test 8: Simulation Speed**

Test each speed setting:

1. **1x Speed (Normal)**:
   - Set 10 days, 1x speed
   - Should take ~10 seconds
   - [ ] Verify timing

2. **2x Speed (Fast)**:
   - Set 10 days, 2x speed
   - Should take ~5 seconds
   - [ ] Verify faster execution

3. **5x Speed (Very Fast)**:
   - Set 10 days, 5x speed
   - Should take ~2 seconds
   - [ ] Verify very fast execution

4. **10x Speed (Ultra Fast)**:
   - Set 10 days, 10x speed
   - Should take ~1 second
   - [ ] Verify ultra-fast execution

---

### ✅ **Test 9: Parameter Effects**

**Test High Transmission Rate**:
1. Set Transmission Rate: **0.5** (high)
2. Run 20 days, 5x speed
3. [ ] Expect rapid infection spread
4. [ ] Multiple municipalities affected
5. [ ] High infection counts

**Test Low Transmission Rate**:
1. Reset simulation
2. Set Transmission Rate: **0.05** (low)
3. Run 20 days, 5x speed
4. [ ] Expect slow infection spread
5. [ ] Few municipalities affected
6. [ ] Lower infection counts

**Test High Vaccination Efficiency**:
1. Reset simulation
2. Set Vaccination Efficiency: **0.95** (very effective)
3. Enable Adaptive Vaccination
4. Run 30 days, 5x speed
5. [ ] Infections should be controlled faster
6. [ ] Risk levels should decrease
7. [ ] Spread limited

---

### ✅ **Test 10: UI Responsiveness**

1. **During Simulation**:
   - [ ] Progress bar updates smoothly
   - [ ] Day counter increments visibly
   - [ ] No UI freezing
   - [ ] Buttons remain responsive

2. **Dashboard Updates**:
   - [ ] Navigate to Dashboard during simulation
   - [ ] Infection counts should update
   - [ ] Statistics cards reflect current state
   - [ ] No lag or errors

3. **Navigation**:
   - [ ] Switch between pages during simulation
   - [ ] Simulation continues in background
   - [ ] No data loss
   - [ ] Consistent state across pages

---

## 🐛 Common Issues & Solutions

### Issue: Simulation doesn't start
**Solution**: 
- Check that all required fields have valid values
- Ensure Simulation Days is between 1-365
- Verify transmission rate is between 0-1

### Issue: Browser becomes slow
**Solution**:
- Use higher simulation speed (5x or 10x)
- Reduce simulation days
- Disable detailed logs if running very long simulations

### Issue: Data not persisting
**Solution**:
- Check browser Local Storage is enabled
- Check browser console for errors
- Verify you're not in incognito/private mode

### Issue: No cross-municipality spread
**Solution**:
- This is realistic! Transmission is probabilistic
- Try higher transmission rate (0.3-0.5)
- Run longer simulations (60+ days)
- Check municipality connections in Municipality Management

---

## ✅ Success Criteria

Phase 3 is working correctly if:

- [x] Simulation starts and completes without errors
- [x] Progress updates in real-time
- [x] Controls (pause, resume, stop, reset) work properly
- [x] Data persists after page refresh
- [x] Infections spread realistically
- [x] Adaptive vaccination activates automatically
- [x] Risk levels change based on infection rates
- [x] Configuration validates correctly
- [x] No browser console errors
- [x] UI remains responsive throughout

---

## 📊 Expected Results (Default Settings)

**After 30-day simulation with defaults**:
- Total infected dogs: 20-100 (varies due to randomness)
- Municipalities affected: 2-5
- Risk levels: 1-3 municipalities with elevated risk
- Vaccination coverage: Increased in high-risk areas
- Human infections: 0-2 (very rare, realistic)

---

## 🎯 Advanced Testing

### Stress Test:
- Run 365-day simulation
- Enable detailed logs
- Monitor browser memory usage
- Verify no crashes or slowdowns

### Network Test:
- Delete a connection between municipalities
- Verify transmission doesn't occur across deleted connection
- Add new connections
- Verify new transmission paths work

### Edge Cases:
- Set all populations to minimum (1)
- Set vaccination coverage to 100%
- Set transmission rate to 0
- Set transmission rate to 1
- Verify system handles edge cases gracefully

---

## 📞 Support

If you encounter issues:
1. Check browser console for errors
2. Verify all files are present
3. Clear Local Storage and restart
4. Check network tab for failed requests

---

**Phase 3 Testing Complete!** ✅

Once all tests pass, you're ready for **Phase 4: Results Visualization**.
