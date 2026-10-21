"""
Request Models for PAWPATROL API
Pydantic models for API request validation
"""

from pydantic import BaseModel, Field
from typing import List, Optional

class MunicipalityData(BaseModel):
    """
    Municipality data structure matching frontend format
    """
    id: str
    name: str
    latitude: float
    longitude: float
    humanPopulation: int = Field(gt=0, description="Human population")
    dogPopulation: int = Field(gt=0, description="Dog population")
    catPopulation: int = Field(gt=0, description="Cat population")
    populationDensity: float = Field(gt=0, description="Population density (ρ) in persons/km²")
    infectedDogs: int = Field(ge=0, description="Initial infected dogs")
    infectedCats: int = Field(ge=0, description="Initial infected cats")
    infectedHumans: int = Field(ge=0, description="Initial infected humans")
    vaccinatedDogs: int = Field(ge=0, description="Number of vaccinated dogs")
    riskLevel: str = Field(description="Current risk level")
    connectedMunicipalities: List[str] = Field(default_factory=list, description="Connected municipality IDs")
    connectedMunicipalities: List[str] = Field(default_factory=list, description="Connected municipality IDs")

class SimulationSettings(BaseModel):
    """
    Simulation parameters from the paper - SI+V+BD Model
    
    Mathematical Parameters:
        - fractionalOrder (α): Memory effects parameter ∈ (0, 1]
        - transmissionRate (β): Disease transmission rate
        - recoveryRate (γ): Recovery/removal rate  
        - stochasticIntensity (σ): Environmental randomness
        - contactProbability (p): Likelihood of transmission
        - vaccinationRate (u): Vaccination intervention rate
    
    NEW PARAMETERS (Phase 2 - SI+V+BD Model):
    
    CALIBRATION NOTES:
    ===================
    These default values are based on:
    - WHO rabies epidemiology guidelines
    - Published literature on dog/cat demographics in Southeast Asia
    - Philippine population statistics (PSA)
    - Modeling assumptions for transmission coefficients
    
    REALISTIC vs MODELING ASSUMPTIONS:
    ----------------------------------
    ✅ VALIDATED FROM REAL DATA:
       - lambda_dog, lambda_human, mu_dog, mu_human (from demographic data)
       - delta_* (from clinical rabies progression literature)
    
    ⚠️  MODELING ASSUMPTIONS (calibrate with local data if available):
       - beta_* transmission coefficients (based on contact rate models)
       - sigma_* stochastic intensities (environmental variation estimates)
    
    RECOMMENDED FOR DAVAO DE ORO:
    -------------------------------
    If you have local surveillance data:
    1. Calibrate beta_* using historical case data
    2. Adjust lambda/mu using municipal census data
    3. Tune sigma_* based on environmental variability
    
    For planning/scenario analysis: Current defaults are appropriate
    For precise forecasting: Calibration with local data recommended
    
    Birth Rates (Λ):
        - lambda_dog, lambda_cat, lambda_human: Daily births per individual
    
    Natural Mortality (μ):
        - mu_dog, mu_cat, mu_human: Natural death rates (excluding rabies)
    
    Rabies Mortality (δ):
        - delta_dog, delta_cat, delta_human: Rabies-specific death rates
    
    Stochastic Intensities (σ):
        - sigma_1, sigma_2, sigma_3: Species-specific noise intensities
    
    Transmission Coefficients (β):
        - beta_dd: Dog-to-dog transmission
        - beta_dc: Dog-to-cat transmission
        - beta_cc: Cat-to-cat transmission
        - beta_dh: Dog-to-human transmission
        - beta_ch: Cat-to-human transmission
    """
    # =========================================================================
    # BASIC SETTINGS (Existing)
    # =========================================================================
    simulationDays: int = Field(gt=0, le=365, description="Simulation period (T)")
    fractionalOrder: float = Field(gt=0, le=1.0, default=0.95, description="Fractional order (α)")
    
    # Legacy parameters (will be replaced by explicit beta coefficients)
    transmissionRate: float = Field(gt=0, default=0.15, description="Base transmission rate (β) - for backward compatibility")
    recoveryRate: float = Field(gt=0, default=0.1, description="Recovery rate (γ) - NOT USED in SI model")
    stochasticIntensity: float = Field(ge=0, default=0.1, description="Base stochastic intensity - for backward compatibility")
    contactProbability: float = Field(ge=0, le=1.0, default=0.3, description="Contact probability (p)")
    vaccinationRate: float = Field(ge=0, le=1.0, default=0.8, description="Target vaccination coverage")
    
    # UI settings
    enableAdaptiveVaccination: bool = Field(default=False, description="Enable adaptive vaccination")
    simulationSpeed: int = Field(default=1, description="UI speed multiplier (not used in backend)")
    
    # =========================================================================
    # NEW PARAMETERS - BIRTH RATES (Λ)
    # =========================================================================
    lambda_dog: float = Field(ge=0, default=0.0001, description="Dog birth rate (Λ_d) - births per dog per day")
    lambda_cat: float = Field(ge=0, default=0.0007, description="Cat birth rate (Λ_c) - births per cat per day (25% annually - realistic for breeding populations)")
    lambda_human: float = Field(ge=0, default=0.00005, description="Human birth rate (Λ_h) - births per person per day")
    
    # =========================================================================
    # NEW PARAMETERS - NATURAL MORTALITY (μ)
    # =========================================================================
    mu_dog: float = Field(ge=0, default=0.0001, description="Dog natural mortality (μ_d) - natural deaths per dog per day")
    mu_cat: float = Field(ge=0, default=0.0002, description="Cat natural mortality (μ_c) - natural deaths per cat per day")
    mu_human: float = Field(ge=0, default=0.00003, description="Human natural mortality (μ_h) - natural deaths per person per day")
    
    # =========================================================================
    # NEW PARAMETERS - RABIES MORTALITY (δ)
    # =========================================================================
    delta_dog: float = Field(ge=0, default=0.1, description="Dog rabies mortality (δ_d) - rabies deaths per infected dog per day")
    delta_cat: float = Field(ge=0, default=0.12, description="Cat rabies mortality (δ_c) - rabies deaths per infected cat per day")
    delta_human: float = Field(ge=0, default=0.15, description="Human rabies mortality (δ_h) - rabies deaths per infected human per day")
    
    # =========================================================================
    # NEW PARAMETERS - STOCHASTIC INTENSITIES (σ)
    # =========================================================================
    sigma_1: float = Field(ge=0, default=0.1, description="Dog stochastic intensity (σ₁) - noise for dog infections")
    sigma_2: float = Field(ge=0, default=0.08, description="Cat stochastic intensity (σ₂) - noise for cat infections")
    sigma_3: float = Field(ge=0, default=0.05, description="Human stochastic intensity (σ₃) - noise for human infections")
    
    # =========================================================================
    # NEW PARAMETERS - TRANSMISSION COEFFICIENTS (β)
    # =========================================================================
    beta_dd: float = Field(ge=0, default=0.15, description="Dog-to-dog transmission coefficient (β_dd)")
    beta_dc: float = Field(ge=0, default=0.06, description="Dog-to-cat transmission coefficient (β_dc)")
    beta_cc: float = Field(ge=0, default=0.105, description="Cat-to-cat transmission coefficient (β_cc)")
    beta_dh: float = Field(ge=0, default=0.0015, description="Dog-to-human transmission coefficient (β_dh)")
    beta_ch: float = Field(ge=0, default=0.00075, description="Cat-to-human transmission coefficient (β_ch)")

class SimulationRequest(BaseModel):
    """
    Complete simulation request
    """
    municipalities: List[MunicipalityData]
    settings: SimulationSettings

class ParameterValidationRequest(BaseModel):
    """
    Request to validate simulation parameters
    """
    fractionalOrder: float
    transmissionRate: float
    recoveryRate: float
    stochasticIntensity: float
    contactProbability: float
