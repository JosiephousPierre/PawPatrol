"""
PHASE 2: SI+V+BD Transmission Model
Susceptible-Infected-Vaccinated with Births and Deaths

Implements the EXACT equations from Formulas.docx:

CANINE (Dogs):
    dS_d/dt^α = Λ_d - β_dd(S_d·I_d)/N_d - μ_d·S_d - u_d(t)
    dI_d/dt^α = β_dd(S_d·I_d)/N_d - (μ_d + δ_d)·I_d + σ₁·dW₁(t)
    dV_d/dt   = u_d(t) - μ_d·V_d

FELINE (Cats):
    dS_c/dt^α = Λ_c - β_dc(S_c·I_d)/N_d - β_cc(S_c·I_c)/N_c - μ_c·S_c - u_c(t)
    dI_c/dt^α = β_dc(S_c·I_d)/N_d + β_cc(S_c·I_c)/N_c - (μ_c + δ_c)·I_c + σ₂·dW₂(t)
    dV_c/dt   = u_c(t) - μ_c·V_c