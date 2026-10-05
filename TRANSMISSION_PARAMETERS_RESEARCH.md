# Transmission Parameters - Research Documentation

**Date**: October 2026  
**Model**: Fractional-Order Stochastic Transmission Model  
**Location**: `rabies-backend/simulation/transmission_model.py`

---

## Executive Summary

Extensive literature review was conducted to validate cat-specific rabies transmission parameters used in the PAWPATROL model. **Key finding: No published studies directly quantify cat-to-cat or dog-to-cat transmission coefficients.** Parameters 0.7 and 0.4 are modeling assumptions based on qualitative understanding of cats as spillover hosts in dog-endemic areas.

---

## Research Questions Investigated

### 1. Cat-to-Cat Transmission Rate (β_cat vs β_dog)

**Model Parameter**: `beta_eff * 0.7` (Line 434)

**Research Findings**:
- ❌ **No published studies** directly comparing cat-to-cat versus dog-to-dog rabies transmission rates
- ✅ Dogs are the primary rabies reservoir globally (>95-99% of human cases)
- ✅ Cats are **spillover hosts**, not maintenance hosts
- ✅ No sustained cat-only epidemics documented without dog/wildlife reservoir
- ⚠️ Per-bite susceptibility may be similar (β_cat ≈ β_dog), but cats have fewer contacts

**Conclusion**: 
The factor **0.7 is a modeling assumption**, not empirically validated. It represents:
- Lower cat contact rates compared to dogs
- Spillover host dynamics (dependent on dog reservoir)
- Conservative estimate for dog-endemic areas (EDRA)

**Status**: ⚠️ **ASSUMPTION - Requires empirical validation**

---

### 2. Dog-to-Cat Cross-Species Transmission

**Model Parameter**: `cross_species_factor = 0.4` (Line 461)

**Research Findings**:
- ❌ **No empirical studies** providing transmission coefficients for dog→cat
- ❌ **No experimental data** on per-bite probability dog-to-cat
- ✅ Cats are susceptible to dog-mediated rabies variants
- ✅ Unvaccinated cats exposed to rabid dogs are euthanized per policy (high risk)
- ⚠️ Per-bite transmission mechanism likely similar to dog→dog
- ✅ Cross-species spillover contributes modestly to overall spread (Lagos/Nepal models)

**Conclusion**:
The factor **0.4 is arbitrary**, not data-driven. It represents:
- Reduced dog-cat contact frequency compared to dog-dog
- Qualitative understanding that spillover has lower transmission chains
- Modeling assumption in absence of published coefficients

**Status**: ⚠️ **ASSUMPTION - Requires empirical validation**

---

### 3. Cat Infectious Period (γ)

**Model Parameter**: `params.gamma = 0.1` (10-day period) (Line 436)

**Research Findings**:
- ✅ **10-day shedding period validated** for both dogs and cats (CDC, Merck Veterinary Manual)
- ✅ Both species may shed virus **up to 10 days before clinical signs**
- ✅ Death ensues quickly once symptomatic (~1 week)
- ✅ Public health guidelines use **10-day observation window** for both species
- ✅ No evidence cats die faster than dogs in terms of infectious period

**Key Sources**:
- CDC case reports: "10-day viral shedding period" for cats
- Merck Veterinary Manual: Dogs and cats have similar disease courses
- Public health quarantine standards: 10-day bite observation for both

**Conclusion**:
The **10-day infectious period is research-validated** and appropriate for both species.

**Status**: ✅ **VALIDATED - Research-supported**

---

## Parameter Summary Table

| Parameter | Current Value | Research Status | Source/Justification |
|-----------|---------------|-----------------|----------------------|
| β_dog (base) | 0.15 | Reasonable range (0.05-0.30) | Typical for rabies models |
| β_cat factor | 0.7 | ⚠️ NOT VALIDATED | Modeling assumption (spillover host) |
| Dog→Cat factor | 0.4 | ⚠️ NOT VALIDATED | Modeling assumption (reduced contacts) |
| γ (infectious period) | 0.1 (10 days) | ✅ VALIDATED | CDC, Merck Manual guidelines |
| Animal→Human | 0.01 | ASSUMPTION | Low transmission (PEP availability) |

---

## Epidemiological Context

### Dog-Mediated Rabies (EDRA - Enzootic Dog Rabies Areas)

**Davao de Oro, Philippines** is classified as an EDRA where:
- Dogs are the **primary reservoir** (~99% of human cases)
- Cats are **incidental hosts** (spillover from dog cycle)
- Cat rabies incidence ~10x lower than dogs
- Sustained transmission requires dog population

**Model Implications**:
- Cat parameters (0.7, 0.4) reflect secondary role in transmission
- Dog vaccination is primary intervention (not cat vaccination)
- Cat infections depend on dog reservoir maintenance

---

## Model Behavior Explained

### Why Cats Drop to Low Numbers (e.g., 2 infected from 11,145 initial)

**Mathematical Explanation**:
Over 365-day simulation with:
- Reduced cat transmission (0.7 factor)
- Reduced dog→cat input (0.4 factor)
- Standard removal rate (10 days)
- Result: **New infections < removals** → cat infections drain to near-zero

**Biological Interpretation**:
- Cats are not self-sustaining without dog reservoir
- Over long periods, cat infections exhaust susceptible population
- Remaining infected cats (e.g., 2) are recent spillover cases
- "Recovered" cats are actually **dead** (rabies is 100% fatal without PEP)

**Model Validity**:
- ✅ Behavior is **consistent with spillover host dynamics**
- ✅ Reflects reality: no sustained cat-only epidemics
- ⚠️ Long simulations (365 days) may amplify parameter uncertainty

---

## Recommendations for Thesis Defense

### When Asked: "How did you validate cat parameters?"

**Response Template**:
> "Extensive literature review (October 2026) found no published studies quantifying cat-to-cat or dog-to-cat rabies transmission coefficients. Global data emphasize that dogs cause >95-99% of human rabies cases, while cats are incidental spillover hosts. Given this, we used conservative reduction factors (0.7 and 0.4) to reflect cats' secondary role in transmission dynamics. The 10-day infectious period is validated by CDC and Merck Veterinary Manual guidelines. We acknowledge these transmission coefficients are modeling assumptions requiring empirical validation through future field studies or experimental work."

### Thesis Limitations Section

**Include**:
- Cat-specific transmission parameters lack empirical validation
- Model uses conservative assumptions based on spillover host biology
- Sensitivity analysis recommended for parameter uncertainty quantification
- Future work: empirical studies to measure cat transmission coefficients

### Future Work Suggestions

1. **Field Studies**: Quantify cat-cat and dog-cat contact rates in Philippines
2. **Experimental Studies**: Measure per-bite transmission probabilities
3. **Sensitivity Analysis**: Test model across parameter ranges (0.5-1.0 for cats)
4. **Comparative Analysis**: Validate against historical rabies data in Davao de Oro

---

## References

### Primary Sources Consulted

1. **World Health Organization (WHO)**  
   - Rabies Fact Sheets (2026)
   - Dogs cause >95-99% of human rabies deaths globally
   - Expert Consultation on Rabies Technical Reports

2. **Centers for Disease Control and Prevention (CDC)**  
   - Rabies case reports and investigation guidelines
   - 10-day observation period for exposed animals
   - Viral shedding period definitions

3. **Merck Veterinary Manual**  
   - Rabies clinical course in dogs and cats
   - 10-day pre-clinical shedding period
   - Similar disease progression both species

4. **MDPI Veterinary Sciences (2026)**  
   - Cat rabies incidence ~10x lower than dogs in EDRA
   - Cats as spillover vs maintenance hosts

5. **PubMed/PMC Database**  
   - Search terms: "rabies transmission coefficient", "cat rabies epidemiology"
   - Result: No quantitative cat-specific transmission rates found

### What Was NOT Found

- ❌ Cat-to-cat transmission rate vs dog-to-dog (quantitative)
- ❌ Dog-to-cat cross-species transmission coefficient
- ❌ Per-bite transmission probability for any species pair
- ❌ Field-measured contact rates between cats and dogs

---

## Model Defensibility

### Strengths

✅ **10-day infectious period is research-validated**  
✅ **Qualitative understanding of spillover dynamics is correct**  
✅ **Model behavior consistent with epidemiological theory**  
✅ **Conservative assumptions appropriate for dog-endemic areas**  
✅ **Transparent documentation of parameter limitations**

### Limitations

⚠️ **Cat transmission factors (0.7, 0.4) lack empirical validation**  
⚠️ **Parameter uncertainty not quantified through sensitivity analysis**  
⚠️ **Long simulation periods (365 days) may amplify assumptions**  
⚠️ **Regional differences (Philippines vs global data) not accounted for**

### Overall Assessment

**The model is defensible for research/thesis purposes** with proper acknowledgment of limitations. The lack of cat-specific data is a **gap in the scientific literature**, not a flaw in your model. Your transparent documentation and conservative assumptions demonstrate academic rigor.

---

## Conclusion

The PAWPATROL transmission model uses **best available knowledge** for cat parameters in the absence of published quantitative data. Parameters 0.7 and 0.4 are reasonable modeling assumptions based on qualitative understanding of cat spillover dynamics, and the 10-day infectious period is research-validated. 

**For thesis defense**: Acknowledge parameter uncertainty, document literature gaps, and propose empirical validation as future work.

---

**Document Version**: 1.0  
**Last Updated**: October 2026  
**Author**: PAWPATROL Research Team  
**Review Status**: Ready for thesis submission
