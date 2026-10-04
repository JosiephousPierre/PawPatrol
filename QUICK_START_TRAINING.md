# 🚀 QUICK START: Train Your DQN Model

**Goal**: Train an AI to optimize rabies vaccination strategies

---

## ⚡ FASTEST WAY (2 Commands)

```bash
# 1. Navigate
cd "c:\rabies system\rabies-backend"

# 2. Train (choose one)
python drl/train_dqn.py --preset fast      # 2-5 min (testing)
python drl/train_dqn.py --preset standard  # 10-15 min (recommended)
```

**That's it!** ✅

---

## 📊 WHAT TO EXPECT

### **Training will show**:
```
🚀 STARTING TRAINING
⏱️  Estimated time: ~10-15 minutes

Episode 10: Avg Reward: -125.3
Episode 50: Avg Reward: -85.2
Episode 100: Avg Reward: -45.7
Episode 500: Avg Reward: 15.3   ← Getting positive!

✅ Training completed!
📊 Evaluation: 70% success rate
🏆 DQN outperforms baseline by +173%!

Model saved to: ./drl/models/dqn_rabies_vaccination.zip
```

---

## ✅ SUCCESS = REWARD INCREASES

Watch the "Avg Reward" number:
- **Starting**: Negative (-100 to -200)
- **Learning**: Becoming less negative (-50 to -10)
- **Good**: Positive (0 to +50)
- **Excellent**: High positive (+50 to +100)

---

## 🛑 TO STOP EARLY

Press **Ctrl+C** - Model will be saved automatically!

---

## 🎯 AFTER TRAINING

You'll have:
- ✅ Trained AI model (`.zip` file)
- ✅ Training metadata (`.json` file)
- ✅ Ready for Phase 4 (Integration)!

---

## ❓ TROUBLESHOOTING

**"Training too slow?"**
→ Normal! CPU takes 10-15 min for 100K steps

**"Reward not improving?"**
→ Wait for 500+ episodes, it takes time

**"Error importing?"**
→ Run: `python drl/environment.py` to test

---

## 🚀 READY? RUN THIS:

```bash
cd "c:\rabies system\rabies-backend"
python drl/train_dqn.py --preset standard
```

**Then grab coffee and watch your AI learn!** ☕🤖
