"""
PAWPATROL Rabies Simulation System - Backend API
Academic Research Implementation

This backend implements the Fractional-Order Stochastic Transmission Model
as described in the research paper for rabies prediction and risk assessment.

Mathematical Model:
    dI/dt^α = β * p(t) * S(t) * I(t) / N - γ * I(t) + u(t) + σ * dW(t)

Where:
    α = fractional order (memory effects)
    β = transmission rate
    p(t) = contact probability
    γ = recovery/removal rate
    u(t) = vaccination intervention
    σ = stochastic intensity
    dW(t) = Wiener process (Brownian motion)
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import numpy as np

from models.request_models import SimulationRequest, ParameterValidationRequest
from models.response_models import SimulationResponse, ValidationResponse
from simulation.transmission_model import run_fractional_stochastic_simulation
from simulation.risk_calculator import calculate_risk_scores, categorize_risk_levels, categorize_risk_level

# Import DRL module
try:
    from drl.inference import get_recommender
    DRL_AVAILABLE = True
    print("✅ DRL module loaded successfully")
except ImportError as e:
    DRL_AVAILABLE = False
    print(f"⚠️  DRL module not available: {e}")

# Initialize FastAPI app
app = FastAPI(
    title="PAWPATROL Rabies Simulation API",
    description="Fractional-Order Stochastic Transmission Model for Rabies Risk Prediction",
    version="1.0.0"
)

# CORS Configuration - Allow frontend to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "name": "PAWPATROL Rabies Simulation API",
        "version": "1.0.0",
        "status": "operational",
        "model": "Fractional-Order Stochastic Transmission Model",
        "documentation": "/docs"
    }

@app.get("/api/health")
async def health_check():
    """
    Health check endpoint
    
    Returns:
        dict: System health status
    """
    return {
        "status": "healthy",
        "service": "rabies-simulation",
        "timestamp": np.datetime64('now').item().isoformat()
    }

@app.post("/api/validate-parameters", response_model=ValidationResponse)
async def validate_parameters(request: ParameterValidationRequest):
    """
    Validate simulation parameters before running simulation
    
    Checks:
        - α (fractional order) ∈ (0, 1]
        - β (transmission rate) > 0
        - γ (recovery rate) > 0
        - σ (stochastic intensity) ≥ 0
        - p (contact probability) ∈ [0, 1]
    
    Args:
        request: Parameter validation request
        
    Returns:
        ValidationResponse: Validation result with errors if any
    """
    errors = []
    
    # Validate fractional order (α)
    alpha = request.fractionalOrder
    if alpha <= 0 or alpha > 1:
        errors.append("Fractional order (α) must be in range (0, 1]")
    
    # Validate transmission rate (β)
    beta = request.transmissionRate
    if beta <= 0:
        errors.append("Transmission rate (β) must be greater than 0")
    
    # Validate recovery rate (γ)
    gamma = request.recoveryRate
    if gamma <= 0:
        errors.append("Recovery rate (γ) must be greater than 0")
    
    # Validate stochastic intensity (σ)
    sigma = request.stochasticIntensity
    if sigma < 0:
        errors.append("Stochastic intensity (σ) must be non-negative")
    
    # Validate contact probability (p)
    p = request.contactProbability
    if p < 0 or p > 1:
        errors.append("Contact probability must be in range [0, 1]")
    
    is_valid = len(errors) == 0
    
    return ValidationResponse(
        isValid=is_valid,
        errors=errors if not is_valid else None,
        message="All parameters valid" if is_valid else "Parameter validation failed"
    )

@app.post("/api/simulate", response_model=SimulationResponse)
async def run_simulation(request: SimulationRequest):
    """
    Run fractional-order stochastic rabies transmission simulation
    
    This endpoint implements the core mathematical model from the research paper:
        dI/dt^α = β * p(t) * S(t) * I(t) / N - γ * I(t) + u(t) + σ * dW(t)
    
    Steps:
        1. Validate input parameters
        2. Run fractional-order stochastic simulation
        3. Calculate risk scores: R_i = I^_i(T) / N_i
        4. Categorize risk levels (low, moderate, high)
        5. Return results with predictions
    
    Args:
        request: Simulation request with municipalities and parameters
        
    Returns:
        SimulationResponse: Simulation results with predictions and risk scores
        
    Raises:
        HTTPException: If parameters invalid or simulation fails
    """
    try:
        # Validate parameters
        validation_request = ParameterValidationRequest(
            fractionalOrder=request.settings.fractionalOrder,
            transmissionRate=request.settings.transmissionRate,
            recoveryRate=request.settings.recoveryRate,
            stochasticIntensity=request.settings.stochasticIntensity,
            contactProbability=request.settings.contactProbability
        )
        
        validation_result = await validate_parameters(validation_request)
        
        if not validation_result.isValid:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Invalid simulation parameters",
                    "errors": validation_result.errors
                }
            )
        
        # Run simulation
        simulation_results = run_fractional_stochastic_simulation(
            municipalities=request.municipalities,
            settings=request.settings
        )
        
        # Calculate risk scores using paper's formula: R_i = I^_i(T) / N_i
        risk_scores = calculate_risk_scores(simulation_results)
        
        # Categorize risk levels
        risk_levels = categorize_risk_levels(risk_scores)
        
        # Merge risk scores back into municipality results
        risk_score_map = {score['municipalityId']: score for score in risk_scores}
        
        for result in simulation_results:
            mun_id = result['id']
            if mun_id in risk_score_map:
                score_data = risk_score_map[mun_id]
                result['riskScore'] = score_data['riskScore']
                result['riskLevel'] = categorize_risk_level(score_data['riskScore'])
            else:
                result['riskScore'] = 0.0
                result['riskLevel'] = 'unknown'
        
        # Prepare response
        response = SimulationResponse(
            success=True,
            municipalities=simulation_results,
            riskScores=risk_scores,
            riskLevels=risk_levels,
            metadata={
                "model": "Fractional-Order Stochastic Transmission Model",
                "fractional_order": request.settings.fractionalOrder,
                "simulation_days": request.settings.simulationDays,
                "formula": "R_i = I^_i(T) / N_i"
            }
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Simulation failed",
                "error": str(e)
            }
        )

@app.post("/api/drl-recommend")
async def get_drl_recommendations(request: dict):
    """
    Get DRL-based vaccination recommendations
    
    Uses trained Deep Q-Network to recommend optimal vaccination strategies
    based on current municipality conditions.
    
    Args:
        request: Dictionary with 'municipalities' list
        
    Returns:
        dict: DRL recommendations for each municipality
        
    Example Request:
        {
            "municipalities": [
                {
                    "id": "1",
                    "name": "Maco",
                    "dogPopulation": 3000,
                    "catPopulation": 1500,
                    "infectedDogs": 15,
                    "infectedCats": 3,
                    "vaccinatedDogs": 900,
                    "populationDensity": 295.2,
                    "riskLevel": "moderate",
                    "connectedMunicipalities": ["2", "3"]
                }
            ]
        }
    
    Example Response:
        {
            "success": true,
            "drl_available": true,
            "recommendations": [
                {
                    "municipality_id": "1",
                    "municipality_name": "Maco",
                    "recommended_vaccination": 0.8,
                    "confidence": 0.75,
                    "explanation": "DRL recommends high vaccination...",
                    "source": "drl"
                }
            ]
        }
    """
    try:
        if not DRL_AVAILABLE:
            raise HTTPException(
                status_code=503,
                detail={
                    "message": "DRL module not available",
                    "error": "Deep Reinforcement Learning model not loaded"
                }
            )
        
        # Get municipalities from request
        municipalities = request.get('municipalities', [])
        
        if not municipalities:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "No municipalities provided",
                    "error": "Request must include 'municipalities' array"
                }
            )
        
        # Get DRL recommender
        recommender = get_recommender()
        
        if not recommender.is_available():
            raise HTTPException(
                status_code=503,
                detail={
                    "message": "DRL model not loaded",
                    "error": "Trained DQN model file not found"
                }
            )
        
        # Get recommendations
        recommendations = recommender.get_batch_recommendations(municipalities)
        
        return {
            "success": True,
            "drl_available": True,
            "model_version": "1.0",
            "recommendations": recommendations,
            "metadata": {
                "model_type": "Deep Q-Network (DQN)",
                "training_steps": 100000,
                "municipalities_analyzed": len(municipalities)
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "message": "DRL recommendation failed",
                "error": str(e)
            }
        )

@app.get("/api/drl-status")
async def get_drl_status():
    """
    Check DRL model availability and status
    
    Returns:
        dict: DRL system status
    """
    if not DRL_AVAILABLE:
        return {
            "available": False,
            "loaded": False,
            "message": "DRL module not available (dependencies not installed)"
        }
    
    try:
        recommender = get_recommender()
        is_loaded = recommender.is_available()
        
        return {
            "available": True,
            "loaded": is_loaded,
            "model_path": "./drl/models/dqn_rabies_vaccination.zip",
            "model_version": "1.0",
            "message": "DRL model loaded and ready" if is_loaded else "DRL model file not found"
        }
    except Exception as e:
        return {
            "available": True,
            "loaded": False,
            "error": str(e),
            "message": "Error checking DRL status"
        }

# ============================================================================
# STARTUP / SHUTDOWN EVENTS
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    print("=" * 60)
    print("PAWPATROL Rabies Simulation API Starting...")
    print("Model: Fractional-Order Stochastic Transmission")
    if DRL_AVAILABLE:
        try:
            recommender = get_recommender()
            if recommender.is_available():
                print("DRL: ✅ Deep Q-Network Model Loaded")
            else:
                print("DRL: ⚠️  Model file not found")
        except Exception as e:
            print(f"DRL: ❌ Error: {e}")
    else:
        print("DRL: ⚠️  Module not available")
    print("=" * 60)

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("=" * 60)
    print("PAWPATROL API Shutting Down")
    print("=" * 60)

# ============================================================================
# RUN SERVER (Development)
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes (development only)
        log_level="info"
    )
