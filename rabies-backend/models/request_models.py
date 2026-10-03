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
    Simulation parameters from the paper
    
    Mathematical Parameters:
        - fractionalOrder (α): Memory effects parameter ∈ (0, 1]
        - transmissionRate (β): Disease transmission rate
        - recoveryRate (γ): Recovery/removal rate  
        - stochasticIntensity (σ): Environmental randomness
        - contactProbability (p): Likelihood of transmission
        - vaccinationRate (u): Vaccination intervention rate
    """
    simulationDays: int = Field(gt=0, le=365, description="Simulation period (T)")
    fractionalOrder: float = Field(gt=0, le=1.0, default=0.95, description="Fractional order (α)")
    transmissionRate: float = Field(gt=0, description="Transmission rate (β)")
    recoveryRate: float = Field(gt=0, default=0.1, description="Recovery rate (γ)")
    stochasticIntensity: float = Field(ge=0, default=0.1, description="Stochastic intensity (σ)")
    contactProbability: float = Field(ge=0, le=1.0, default=0.3, description="Contact probability (p)")
    vaccinationRate: float = Field(ge=0, le=1.0, default=0.8, description="Vaccination rate (u)")
    enableAdaptiveVaccination: bool = Field(default=False, description="Enable adaptive vaccination")
    simulationSpeed: int = Field(default=1, description="UI speed multiplier (not used in backend)")

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
