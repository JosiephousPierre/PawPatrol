# Regional Risk Map - Quick Reference Card

**🎯 Purpose:** See real-time rabies risk across ALL 11 municipalities

---

## 👤 For Municipality Users

### ✅ What You Can Do Now:

**1. See Other Municipalities' Risk Levels**
- Open Dashboard → Regional Risk Map
- All municipalities show their current risk status
- Updates automatically when anyone runs a simulation

**2. Refresh Latest Data**
- Click "Refresh" button (top-right of map)
- Gets latest risk levels from all municipalities
- Takes less than 1 second

**3. View Municipality Details**
- Click any marker on the map
- See: Risk level, infected counts, vaccinations
- Map auto-recenters when popup closes

### 🎨 Risk Level Colors:

| Color | Risk Level | Meaning |
|-------|------------|---------|
| 🟢 Green | Safe | <0.1% infection rate |
| 🟡 Yellow | Low Risk | 0.1-1% infection rate |
| 🟠 Orange | Moderate | 1-5% infection rate |
| 🔴 Red | High Risk | 5-10% infection rate |
| 🟤 Dark Red | Critical | >10% infection rate |

---

## 👨‍💼 For Admin Users

### ✅ What You Can See:

**Regional Overview:**
- All 11 municipalities on one map
- Real-time risk distribution
- Summary statistics in cards
- Legend with exact counts

**Example:**
```
Safe (7)
Low Risk (1)
Moderate (2)
High Risk (1)
Critical (0)
```

**How to Use:**
1. Login with admin code: `ADMIN`
2. Open Dashboard
3. Check Regional Risk Map
4. Identify municipalities needing intervention
5. Prioritize resources based on risk levels

---

## 🔄 How It Works

```
Simple Flow:

MACO runs simulation
    ↓
Risk level changes to "Moderate"
    ↓
Data saved to shared regional storage
    ↓
LAAK opens dashboard
    ↓
Sees MACO's "Moderate" status automatically ✅
```

---

## 🛠️ Troubleshooting

### Issue: Map shows outdated data

**Solution:**
1. Click "Refresh" button
2. Or refresh browser page (F5)

### Issue: Risk levels not matching

**Solution:**
1. Check that simulation completed successfully
2. Wait a moment, then refresh map
3. Verify in Results page that risk level changed

### Issue: Map not loading

**Solution:**
1. Check internet connection (map tiles need to load)
2. Clear browser cache
3. Refresh page

---

## 💡 Tips

**Best Practices:**
- ✅ Click Refresh before important meetings
- ✅ Check Regional Risk Map daily
- ✅ Run simulations regularly to keep data current
- ✅ Use popup details for quick status checks

**Things to Know:**
- ⚠️ Works on same computer (different browser tabs)
- ⚠️ Need to refresh page to see very latest updates
- ⚠️ Different computers: Use Refresh button to sync

---

## 📱 Quick Actions

| I Want To... | How To Do It |
|-------------|--------------|
| See all municipality risks | Open Dashboard → Check Regional Risk Map |
| Update my municipality's risk | Run Simulation → Data syncs automatically |
| Get latest regional data | Click "Refresh" button on map |
| See infection details | Click marker → View popup |
| Check risk categories | Look at legend below map |
| Find high-risk areas | Look for red/dark red markers |

---

## 📊 Understanding the Data

**Your Regional Risk Map Shows:**

✅ **Current** risk levels (real-time)  
✅ **All** 11 municipalities  
✅ **Latest** simulation results  
✅ **Shared** data (everyone sees same map)

**Legend Numbers:**
- Show how many municipalities in each category
- Update automatically when risks change
- Help identify trends (improving vs worsening)

---

## 🎓 Example Scenario

**Scenario:**
```
Monday 8 AM:
- MACO runs simulation
- Risk level: Moderate (orange)

Monday 9 AM:
- LAAK opens dashboard
- Sees MACO as moderate ✅
- Clicks Refresh to confirm
- Decides to increase own vaccinations

Monday 10 AM:
- Admin checks dashboard
- Sees regional picture:
  * MACO: Moderate
  * LAAK: Safe
  * Others: Safe
- Allocates resources to MACO
```

---

## ⚡ Keyboard Shortcuts

None currently, but you can:
- Press **F5** to refresh page
- Press **Ctrl+Shift+R** to hard reload
- Press **F12** to open DevTools (for debugging)

---

## 📞 Need Help?

**Common Questions:**

**Q: How often should I refresh?**  
A: Once per day is usually enough. Click Refresh before important checks.

**Q: Can I see yesterday's risk levels?**  
A: Not yet. System shows current status only. Historical tracking coming soon.

**Q: Why is my municipality not updating?**  
A: Make sure you completed the simulation. Check Results page first.

**Q: Can other provinces see our data?**  
A: No. System is for Davao de Oro only (11 municipalities).

---

**Need More Info?**
- Detailed Guide: `REGIONAL_RISK_MAP_FIX.md`
- Testing Guide: `TEST_REGIONAL_RISK_MAP_FIX.md`
- Full Summary: `REGIONAL_RISK_MAP_FIX_SUMMARY.md`

---

**Last Updated:** January 15, 2027  
**Version:** 1.0  
**Status:** ✅ Active
