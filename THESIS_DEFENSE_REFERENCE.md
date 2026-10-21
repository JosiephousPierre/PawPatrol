# Thesis Defense - Quick Reference Guide

## Cat Transmission Parameters Q&A

---

### Q: "Why did cats drop from initial numbers to very few infected?"

**Answer**:
> "This behavior reflects the epidemiological reality that cats are spillover hosts, not maintenance hosts for rabies. Over the 365-day simulation, with reduced cat-to-cat transmission (β_cc = 0.105, which is 0.7× the dog rate of 0.15) and reduced dog-to-cat spillover (β_dc = 0.06, which is 0.4× the dog rate), new cat infections couldn't keep pace with rabies deaths. The remaining infected cats represent recent spillover cases. This is mathematically consistent with the fact that sustained cat-only rabies epidemics have never been documented without a dog or wildlife reservoir."

---

### Q: "How did you validate the 0.7 cat transmission factor?"

**Answer**:
> "Extensive literature review found no published studies directly quantifying cat-to-cat versus dog-to-dog transmission rates. The actual coefficient β_cc = 0.105 represents 70% of the dog-to-dog coefficient (β_dd = 0.15), hence the 0.7 factor. This is a modeling assumption based on qualitative evidence that: (1) dogs cause >95-99% of human rabies cases globally, (2) cats are incidental spillover hosts not maintenance hosts, and (3) no sustained cat-only epidemics exist. This represents a conservative estimate reflecting cats' secondary role in transmission dynamics in dog-endemic areas like the Philippines."

**Follow-up if pressed**: 
> "Research shows cats may have similar per-bite susceptibility to dogs, but the 0.7 factor captures their lower contact rates and dependence on the dog reservoir. This is a known gap in the rabies literature - we documented this limitation and recommend empirical field studies as future work."

---

### Q: "Is the 0.4 dog-to-cat factor research-based?"

**Answer**:
> "No, this is also a modeling assumption. The actual coefficient β_dc = 0.06 represents 40% of the dog-to-dog rate (β_dd = 0.15). No published studies provide empirical transmission coefficients for dog-to-cat spillover. The 0.4 factor represents reduced cross-species contact frequency compared to dog-to-dog interactions. Research on other species (dog-jackal models in Lagos/Nepal) shows cross-species spillover contributes modestly to overall transmission chains, which supports using a reduction factor, though the exact value lacks empirical validation."

---

### Q: "What parameters ARE validated?"

**Answer**:
> "The 10-day infectious period is validated by CDC guidelines and the Merck Veterinary Manual, which document that both dogs and cats shed virus up to 10 days before clinical signs and die within approximately one week after symptoms appear. Public health quarantine standards use the same 10-day observation window for both species. The base transmission rate (β = 0.15) falls within typical ranges (0.05-0.30) used in rabies epidemiological models."

---

### Q: "Isn't your model unreliable if it uses assumptions?"

**Answer**:
> "All epidemiological models make assumptions - the key is transparency. The lack of cat-specific transmission data represents a gap in the scientific literature, not a flaw in our model. We explicitly documented which parameters are validated versus assumed, conducted literature review to justify our assumptions, and recommend sensitivity analysis as future work. This level of transparency actually strengthens the academic rigor of the research."

---

### Q: "Why did you use 365 days if it creates artifacts?"

**Answer**:
> "The 365-day simulation demonstrates long-term dynamics and allows observation of endemic equilibrium states. The cat population decline is not an artifact - it's epidemiologically accurate behavior for a spillover host dependent on a reservoir species. In real-world rabies control, cat infections would similarly decline if dog vaccination reaches critical coverage. For operational planning, shorter time horizons (30-90 days) may be more practical and we could add that as a recommended simulation setting."

---

### Q: "How would you improve the model with more resources?"

**Answer**:
> "Three priority improvements: (1) Field studies in Davao de Oro to quantify actual cat-cat and dog-cat contact rates; (2) Sensitivity analysis testing parameter ranges (e.g., cat factor from 0.5 to 1.0) to quantify uncertainty; (3) Validation against historical rabies surveillance data from the Philippines to calibrate parameters to regional conditions. These would transform modeling assumptions into empirically-validated coefficients."

---

### Q: "Did you consider that cats don't recover from rabies - they die?"

**Answer**:
> "Yes, absolutely correct. The PAWPATROL system uses an SI+V+BD model (Susceptible-Infected-Vaccinated with Births-Deaths), NOT an SIR model. There is NO recovery compartment in the model. Rabies is 100% fatal - infected animals die from the disease (rabies mortality rate δ) or natural causes (natural mortality rate μ). The model explicitly tracks rabies deaths separately from natural deaths. When infected cats 'disappear' from the infected compartment, they have died from rabies - they do not recover. This is documented in the code with the comment 'REMOVED in Phase 2 - SI model has no recovery'."

---

## Actual Parameter Values (CRITICAL - MEMORIZE THESE)

### Transmission Coefficients

| Parameter | Value | Calculation | Meaning |
|-----------|-------|-------------|---------|
| **β_dd** | 0.15 | Baseline | Dog-to-dog transmission (100%) |
| **β_cc** | 0.105 | 0.15 × 0.7 | Cat-to-cat transmission (70% of dog rate) |
| **β_dc** | 0.06 | 0.15 × 0.4 | Dog-to-cat spillover (40% of dog rate) |
| **β_dh** | 0.0015 | 0.15 × 0.01 | Dog-to-human (1% - rare) |
| **β_ch** | 0.00075 | 0.0015 × 0.5 | Cat-to-human (0.5% - very rare) |

### Birth Rates (per day)
- **Dogs (λ_dog)**: 0.00050335 → 3.88% annual growth
- **Cats (λ_cat)**: 0.0004356 → 5.90% annual growth
- **Humans (λ_human)**: 0.00003288 → 0.58% annual growth

### Natural Death Rates (per day)
- **Dogs (μ_dog)**: 0.000397
- **Cats (μ_cat)**: 0.000274
- **Humans (μ_human)**: 0.00001699

### Rabies Death Rates (per day)
- **Dogs (δ_dog)**: 0.1 → ~10 day survival (VALIDATED by CDC)
- **Cats (δ_cat)**: 0.12 → ~8.3 day survival
- **Humans (δ_human)**: 0.15 → ~6.7 day survival

**Model Type**: SI+V+BD (NOT SIR - NO recovery from rabies)

---

## Model Clarification: SI+V+BD (NOT SIR)

### CRITICAL: Your Model Has NO Recovery

**What this means:**
- ✅ **S** (Susceptible): Can get infected
- ✅ **I** (Infected): Currently infected with rabies
- ❌ **R** (Recovered): **DOES NOT EXIST** in your model
- ✅ **V** (Vaccinated): Protected from infection
- ✅ **B** (Births): New individuals born into population
- ✅ **D** (Deaths): Natural deaths (μ) + Rabies deaths (δ)

**What happens to infected animals?**
1. They die from rabies (rate δ: 0.1 for dogs, 0.12 for cats, 0.15 for humans)
2. They die from natural causes (rate μ)
3. **They DO NOT recover** (rabies is 100% fatal without PEP for humans)

**Population equation:**
```
N(t) = S(t) + I(t) + V(t)

NOT: N(t) = S(t) + I(t) + R(t) + V(t)
```

**If someone asks about SIR:**
> "We use an SI+V+BD model, not SIR. The 'R' compartment doesn't exist because rabies is 100% fatal in animals. Infected animals die from the disease - they don't recover. The model explicitly tracks rabies deaths separately from natural deaths, which is critical for public health impact assessment."

---

## Key Talking Points

### Strengths to Emphasize

✅ **Research-validated infectious period** (10 days - CDC/Merck)  
✅ **Qualitatively correct spillover dynamics** (cats depend on dog reservoir)  
✅ **Transparent parameter documentation** (assumptions clearly stated)  
✅ **Conservative approach** (reduction factors reflect secondary role)  
✅ **Identifies literature gap** (cat-specific data missing globally)

### Limitations to Acknowledge

⚠️ **Cat transmission factors lack empirical validation** (known literature gap)  
⚠️ **Parameter uncertainty not quantified** (recommend sensitivity analysis)  
⚠️ **Regional variation not captured** (Philippines vs global data)  
⚠️ **Long-term dynamics may amplify assumptions** (shorter periods more robust)

### Don't Say

❌ "The parameters are literature-based" (cat transmission factors are modeling assumptions)  
❌ "We validated everything" (two key parameters are assumptions)  
❌ "The model is perfect" (acknowledge limitations)  
❌ "Animals recover from rabies" (they die - this is an SI+V+BD model, not SIR)  
❌ "We use an SIR model" (it's SI+V+BD - no recovery compartment)


### Do Say

✅ "We conducted extensive literature review"  
✅ "Cat transmission assumptions are based on qualitative epidemiological understanding"  
✅ "We use an SI+V+BD model - Susceptible-Infected-Vaccinated with Births-Deaths"  
✅ "There is no recovery from rabies - infected animals die (100% fatal without PEP)"  
✅ "β_cc = 0.105 is 70% of β_dd = 0.15, reflecting cats' secondary role"  
✅ "β_dc = 0.06 is 40% of β_dd = 0.15, representing dog-to-cat spillover reduction"  
✅ "We documented limitations transparently"  
✅ "This represents a gap in global rabies research"  
✅ "The model is defensible for research purposes with acknowledged limitations"


---

## If Challenged on Scientific Validity

### Response Framework

1. **Acknowledge the limitation**
   > "You're correct that these parameters lack direct empirical validation."

2. **Contextualize the gap**
   > "This reflects a gap in the rabies literature - no published studies quantify cat-specific transmission rates."

3. **Justify the approach**
   > "We used conservative assumptions based on qualitative evidence that cats are spillover hosts causing <1-5% of cases."

4. **Demonstrate rigor**
   > "We documented this limitation, conducted extensive literature search, and recommend empirical validation as future work."

5. **Pivot to strengths**
   > "The model successfully demonstrates the computational framework, validated DRL training, and produces epidemiologically plausible dynamics."

---

## One-Sentence Summary

> "The PAWPATROL model uses best available knowledge for cat parameters (validated 10-day infectious period, assumption-based transmission factors) with transparent documentation of limitations and recommendations for empirical validation as future work."

---

## Emergency Response to "This Undermines Everything"

**If someone says the lack of data invalidates your entire model:**

> "All models are wrong, but some are useful - that's Box's famous quote. Every epidemiological model makes simplifying assumptions. What matters is: (1) Are the assumptions reasonable? Yes - cats being spillover hosts with reduced transmission is well-established qualitatively. (2) Are they documented? Yes - we explicitly state which parameters are validated versus assumed. (3) Does the model achieve its research objectives? Yes - it demonstrates fractional-order stochastic modeling, DRL integration, and produces epidemiologically plausible dynamics. The lack of cat-specific data is a research opportunity, not a fatal flaw. In fact, our work highlights this gap and provides a framework for future validation studies."

---

**Good luck with your defense! You've got this! 🎓**
