"""
Response Models for PAWPATROL API
Pydantic models for API responses
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class MunicipalityResult(BaseModel):
    """
    Simulation results for a single municipality
    """
    id: str
    name: str
    predictedInfectedDogs: int = Field(description="I^_i(T) for dogs")
    predictedInfectedCats: int = Field(description="I^_i(T) for cats")
    predictedInfectedHumans: int = Field(description="I^_i(T) for humans")
    totalPredictedInfected: int = Field(description="Total I^_i(T)")
    susceptibleDogs: int = Field(description="Susceptible dogs remaining")
    recoveredDogs: int = Field(description="Recovered dogs")
    vaccinatedDogs: int = Field(description="Vaccinated dogs")
    totalPopulation: int = Field(description="Total population N_i")
    riskScore: float = Field(description="R_i = I^_i(T) / N_i")
    riskLevel: str = Field(description="Categorized risk level")
    dailyInfections: List = Field(default_factory=list, description="Day-by-day infection counts")

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
