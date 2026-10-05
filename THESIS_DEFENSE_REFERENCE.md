# Thesis Defense - Quick Reference Guide

## Cat Transmission Parameters Q&A

---

### Q: "Why did cats drop from 11,145 to only 2 infected?"

**Answer**:
> "This behavior reflects the epidemiological reality that cats are spillover hosts, not maintenance hosts for rabies. Over the 365-day simulation, with reduced cat-to-cat transmission (0.7 factor) and reduced dog-to-cat spillover (0.4 factor), new cat infections couldn't keep pace with removals. The remaining 2 infected cats represent recent spillover cases. This is mathematically consistent with the fact that sustained cat-only rabies epidemics have never been documented without a dog or wildlife reservoir."

---

### Q: "How did you validate the 0.7 cat transmission factor?"

**Answer**:
> "Extensive literature review found no published studies directly quantifying cat-to-cat versus dog-to-dog transmission rates. The 0.7 factor is a modeling assumption based on qualitative evidence that: (1) dogs cause >95-99% of human rabies cases globally, (2) cats are incidental spillover hosts not maintenance hosts, and (3) no sustained cat-only epidemics exist. This represents a conservative estimate reflecting cats' secondary role in transmission dynamics in dog-endemic areas like the Philippines."

**Follow-up if pressed**: 
> "Research shows cats may have similar per-bite susceptibility to dogs, but the 0.7 factor captures their lower contact rates and dependence on the dog reservoir. This is a known gap in the rabies literature - we documented this limitation and recommend empirical field studies as future work."

---

### Q: "Is the 0.4 dog-to-cat factor research-based?"

**Answer**:
> "No, this is also a modeling assumption. No published studies provide empirical transmission coefficients for dog-to-cat spillover. The 0.4 factor represents reduced cross-species contact frequency compared to dog-to-dog interactions. Research on other species (dog-jackal models in Lagos/Nepal) shows cross-species spillover contributes modestly to overall transmission chains, which supports using a reduction factor, though the exact value lacks empirical validation."

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

### Q: "Did you consider that 'recovered' cats should be 'dead'?"

**Answer**:
> "Yes, excellent observation. In the model, the 'recovered' compartment for cats represents removal from the infectious population - primarily through death, as rabies is nearly 100% fatal without treatment. The term 'recovered' is standard in SIR model notation but for cats specifically, this should be interpreted as 'removed/dead'. Dogs may have some true recoveries, but for cats, it's effectively a death count. We could clarify this in the model documentation by using 'removed' terminology for cats."

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

❌ "The parameters are literature-based" (they're not)  
❌ "We validated everything" (two key parameters are assumptions)  
❌ "The model is perfect" (acknowledge limitations)  
❌ "Cats recover from rabies" (they die)

### Do Say

✅ "We conducted extensive literature review"  
✅ "Assumptions are based on qualitative epidemiological understanding"  
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
