# 🚀 PHASE 1 INSTALLATION GUIDE

**Quick Start**: Run the automated installer!

---

## ⚡ FASTEST METHOD (RECOMMENDED)

### **Windows:**
```bash
cd "c:\rabies system\rabies-backend"
install_drl.bat
```

That's it! The script will:
1. ✅ Check Python
2. ✅ Upgrade pip
3. ✅ Install PyTorch
4. ✅ Install Stable-Baselines3
5. ✅ Install Gymnasium
6. ✅ Install all dependencies
7. ✅ Verify installation

**Time**: 5-10 minutes (mostly downloading)

---

## 📋 MANUAL METHOD (IF SCRIPT FAILS)

### **Step 1: Navigate**
```bash
cd "c:\rabies system\rabies-backend"
```

### **Step 2: Upgrade pip**
```bash
python -m pip install --upgrade pip
```

### **Step 3: Install PyTorch**
```bash
pip install torch==2.1.1 torchvision==0.16.1
```

### **Step 4: Install RL Libraries**
```bash
pip install stable-baselines3==2.2.1
pip install gymnasium==0.29.1
```

### **Step 5: Install Everything Else**
```bash
pip install -r requirements.txt
```

### **Step 6: Verify**
```bash
python -c "import torch; print('✅ PyTorch:', torch.__version__)"
python -c "import stable_baselines3; print('✅ SB3:', stable_baselines3.__version__)"
python -c "import gymnasium; print('✅ Gymnasium:', gymnasium.__version__)"
```

---

## ✅ VERIFICATION

### **Test Configuration**
```bash
python drl/config.py
```

**Expected Output**:
```
======================================================================
DRL Configuration
======================================================================

📊 Model Architecture:
  Policy: MlpPolicy
  Network: [64, 64]
  Activation: relu

⚙️ Training Settings:
  Total Timesteps: 100,000
  Learning Rate: 0.001
  ...

======================================================================
Configuration loaded successfully!
======================================================================
```

If you see this, **Phase 1 is complete!** ✅

---

## 🐛 TROUBLESHOOTING

### **Problem: "Python not found"**
**Solution**: Install Python 3.8+ from https://www.python.org/downloads/

### **Problem: pip install fails**
**Solution**: 
```bash
python -m pip install --upgrade pip
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
```

### **Problem: "torch not found" after install**
**Solution**: Wrong Python interpreter. Check:
```bash
python --version
which python  # or: where python (Windows)
```

### **Problem: Out of memory during install**
**Solution**: Install one package at a time:
```bash
pip install torch==2.1.1
pip install stable-baselines3==2.2.1
pip install gymnasium==0.29.1
pip install -r requirements.txt
```

---

## 📊 WHAT WAS INSTALLED?

| Package | Size | Purpose |
|---------|------|---------|
| PyTorch | ~1.5 GB | Neural network framework |
| Stable-Baselines3 | ~50 MB | DQN algorithm |
| Gymnasium | ~10 MB | RL environment framework |
| TensorBoard | ~100 MB | Training visualization |
| Others | ~100 MB | Supporting libraries |
| **Total** | **~2 GB** | |

---

## 🎯 NEXT STEPS

**After successful installation:**

1. ✅ Verify: `python drl/config.py`
2. ✅ Read: `DRL_PHASE1_SETUP_COMPLETE.md`
3. 🚀 Ready for: **Phase 2 - Environment Definition**

---

## 💡 TIPS

- **CPU vs GPU**: CPU is fine! Training takes ~15 mins on CPU
- **Internet**: You need internet for package downloads
- **Disk Space**: Make sure you have ~2 GB free
- **Time**: First install takes 5-10 minutes

---

**Status**: Phase 1 Setup  
**Next**: Phase 2 - Environment Definition  
**ETA**: Ready to proceed immediately after installation!
