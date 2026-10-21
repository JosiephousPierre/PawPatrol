"""
Response Models for PAWPATROL API
Pydantic models for API responses
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class MunicipalityResult(BaseModel):
    """
    Simulation results for a single municipality
    SI+V+BD Model (Susceptible-Infected-Vaccinated with Births-Deaths)
    """
    id: str
    name: str
    
    # Infection counts
    predictedInfectedDogs: int = Field(description="I^_i(T) for dogs")
    predictedInfectedCats: int = Field(description="I^_i(T) for cats")
    predictedInfectedHumans: int = Field(description="I^_i(T) for humans")
    totalPredictedInfected: int = Field(description="Total I^_i(T)")
    
    # Initial infection counts (for risk calculation)
    initialInfectedDogs: Optional[int] = Field(default=None, description="Initial infected dogs (before simulation)")
    initialInfectedCats: Optional[int] = Field(default=None, description="Initial infected cats (before simulation)")
    initialInfectedHumans: Optional[int] = Field(default=None, description="Initial infected humans (before simulation)")
    totalInitialInfected: Optional[int] = Field(default=None, description="Total initial infected (before simulation)")
    
    # Population compartments
    susceptibleDogs: int = Field(description="Susceptible dogs remaining")
    recoveredDogs: int = Field(default=0, description="DEPRECATED - SI model has no recovery")
    vaccinatedDogs: int = Field(description="Vaccinated dogs")
    totalPopulation: int = Field(description="Total population N_i")
    
    # Risk assessment
    riskScore: float = Field(description="R_i = I^_i(T) / N_i")
    riskLevel: str = Field(description="Categorized risk level")
    
    # Time series
    dailyInfections: List = Field(default_factory=list, description="Day-by-day infection counts")
    
    # =========================================================================
    # NEW FIELDS - POPULATION DYNAMICS (Phase 1)
    # =========================================================================
    
    # Initial populations
    initialDogPopulation: Optional[int] = Field(default=None, description="Initial dog population")
    initialCatPopulation: Optional[int] = Field(default=None, description="Initial cat population")
    initialHumanPopulation: Optional[int] = Field(default=None, description="Initial human population")
    
    # Final populations
    finalDogPopulation: Optional[int] = Field(default=None, description="Final dog population")
    finalCatPopulation: Optional[int] = Field(default=None, description="Final cat population")
    finalHumanPopulation: Optional[int] = Field(default=None, description="Final human population")
    
    # Birth statistics
    totalDogBirths: Optional[int] = Field(default=None, description="Total dog births during simulation")
    totalCatBirths: Optional[int] = Field(default=None, description="Total cat births during simulation")
    totalHumanBirths: Optional[int] = Field(default=None, description="Total human births during simulation")
    
    # Natural death statistics
    totalDogNaturalDeaths: Optional[int] = Field(default=None, description="Total dog natural deaths (μ)")
    totalCatNaturalDeaths: Optional[int] = Field(default=None, description="Total cat natural deaths (μ)")
    totalHumanNaturalDeaths: Optional[int] = Field(default=None, description="Total human natural deaths (μ)")
    
    # Rabies death statistics
    totalDogRabiesDeaths: Optional[int] = Field(default=None, description="Total dog rabies deaths (δ)")
    totalCatRabiesDeaths: Optional[int] = Field(default=None, description="Total cat rabies deaths (δ)")
    totalHumanRabiesDeaths: Optional[int] = Field(default=None, description="Total human rabies deaths (δ)")
    
    # Vaccination statistics
    totalDogVaccinations: Optional[int] = Field(default=None, description="Total dogs vaccinated during simulation")
    totalCatVaccinations: Optional[int] = Field(default=None, description="Total cats vaccinated during simulation")
    totalHumanVaccinations: Optional[int] = Field(default=None, description="Total humans receiving PEP during simulation")
    
    # Initial and final infected counts (for change tracking)
    initialInfectedDogs: Optional[int] = Field(default=None, description="Initial infected dogs at simulation start")
    initialInfectedCats: Optional[int] = Field(default=None, description="Initial infected cats at simulation start")
    initialInfectedHumans: Optional[int] = Field(default=None, description="Initial infected humans at simulation start")
    finalInfectedDogs: Optional[int] = Field(default=None, description="Final infected dogs at simulation end")
    finalInfectedCats: Optional[int] = Field(default=None, description="Final infected cats at simulation end")
    finalInfectedHumans: Optional[int] = Field(default=None, description="Final infected humans at simulation end")

class RiskScore(BaseModel):
    """
    Risk score for a municipality
    Formula: R_i = I^_i(T) / N_i
    """
    municipalityId: str
    municipalityName: str
    predictedInfected: int = Field(description="I^_i(T)")
    totalPopulation: int = Field(description="N_i")
    riskScore: float = Field(description="R_i")
    formula: str = Field(default="R_i = I^_i(T) / N_i", description="Formula used")

class RiskLevelDistribution(BaseModel):
    """
    Distribution of municipalities by risk level
    """
    low: int = Field(description="Count of low-risk municipalities")
    moderate: int = Field(description="Count of moderate-risk municipalities")
    high: int = Field(description="Count of high-risk municipalities")

class ValidationResponse(BaseModel):
    """
    Parameter validation response
    """
    isValid: bool
    errors: Optional[List[str]] = None
    message: str

class SimulationResponse(BaseModel):
    """
    Complete simulation response
    """
    success: bool
    municipalities: List[MunicipalityResult]
    riskScores: List[RiskScore]
    riskLevels: RiskLevelDistribution
    metadata: Dict[str, Any] = Field(description="Simulation metadata")
