"""
Risk Score Calculator
Implements the exact risk formula from the research paper

Risk Formula:
    R_i = I^_i(T) / N_i

Where:
    R_i = Risk score for municipality i
    I^_i(T) = Predicted total infected at time T
    N_i = Total population of municipality i

Risk Categorization:
    - Safe: R_i < 0.001 (< 0.1%)
    - Low Risk: 0.001 ≤ R_i < 0.01 (0.1% - 1%)
    - Moderate Risk: 0.01 ≤ R_i < 0.05 (1% - 5%)
    - High Risk: 0.05 ≤ R_i < 0.10 (5% - 10%)
    - Critical: R_i ≥ 0.10 (≥ 10%)

Reference:
    Research paper: "Fractional-Order Stochastic Transmission Model"
"""

from typing import List, Dict

def calculate_risk_scores(simulation_results: List[Dict]) -> List[Dict]:
    """
    Calculate risk scores using the exact paper formula
    
    Formula:
        R_i = I^_i(T) / N_i
    
    Where:
        I^_i(T) = Total predicted infected (dogs + cats + humans)
        N_i = Total population (dogs + cats + humans)
    
    Args:
        simulation_results: List of municipality simulation results
        
    Returns:
        List[Dict]: Risk scores for each municipality
    """
    risk_scores = []
    
    for result in simulation_results:
        # Get predicted infected: I^_i(T)
        predicted_infected = result['totalPredictedInfected']
        
        # Get total population: N_i (should be in result now)
        total_population = result.get('totalPopulation', 0)
        
        # If population is zero, skip
        if total_population == 0:
            continue
        
        # Calculate risk score: R_i = I^_i(T) / N_i
        risk_score = predicted_infected / total_population
        
        risk_scores.append({
            'municipalityId': result['id'],
            'municipalityName': result['name'],
            'predictedInfected': predicted_infected,
            'totalPopulation': int(total_population),
            'riskScore': round(risk_score, 6),
            'formula': 'R_i = I^_i(T) / N_i'
        })
    
    return risk_scores

def categorize_risk_level(risk_score: float) -> str:
    """
    Categorize risk score into discrete levels
    
    Thresholds:
        - Safe: < 0.1% infected
        - Low Risk: 0.1% - 1% infected
        - Moderate Risk: 1% - 5% infected
        - High Risk: 5% - 10% infected
        - Critical: ≥ 10% infected
    
    Args:
        risk_score: R_i value (0 to 1)
        
    Returns:
        str: Risk level category
    """
    if risk_score < 0.001:
        return 'safe'
    elif risk_score < 0.01:
        return 'low'
    elif risk_score < 0.05:
        return 'moderate'
    elif risk_score < 0.10:
        return 'high'
    else:
        return 'critical'

def categorize_risk_levels(risk_scores: List[Dict]) -> Dict[str, int]:
    """
    Count municipalities in each risk category
    
    Args:
        risk_scores: List of risk scores
        
    Returns:
        Dict: Count of municipalities per risk level
    """
    distribution = {
        'safe': 0,
        'low': 0,
        'moderate': 0,
        'high': 0,
        'critical': 0
    }
    
    for score in risk_scores:
        risk_level = categorize_risk_level(score['riskScore'])
        distribution[risk_level] += 1
    
    return distribution

def get_high_risk_municipalities(risk_scores: List[Dict], threshold: float = 0.05) -> List[Dict]:
    """
    Get municipalities with risk score above threshold
    
    Args:
        risk_scores: List of risk scores
        threshold: Risk threshold (default 0.05 = 5%)
        
    Returns:
        List[Dict]: High-risk municipalities sorted by risk score (descending)
    """
    high_risk = [
        score for score in risk_scores
        if score['riskScore'] >= threshold
    ]
    
    # Sort by risk score (highest first)
    high_risk.sort(key=lambda x: x['riskScore'], reverse=True)
    
    return high_risk

def calculate_average_risk(risk_scores: List[Dict]) -> float:
    """
    Calculate average risk across all municipalities
    
    Args:
        risk_scores: List of risk scores
        
    Returns:
        float: Average risk score
    """
    if not risk_scores:
        return 0.0
    
    total_risk = sum(score['riskScore'] for score in risk_scores)
    return total_risk / len(risk_scores)

def calculate_weighted_risk(risk_scores: List[Dict]) -> float:
    """
    Calculate population-weighted average risk
    
    Weighted by municipality population size.
    Larger populations contribute more to overall risk.
    
    Args:
        risk_scores: List of risk scores
        
    Returns:
        float: Weighted average risk score
    """
    if not risk_scores:
        return 0.0
    
    total_weighted = 0.0
    total_population = 0
    
    for score in risk_scores:
        population = score['totalPopulation']
        risk = score['riskScore']
        total_weighted += risk * population
        total_population += population
    
    if total_population == 0:
        return 0.0
    
    return total_weighted / total_population

def get_risk_summary(risk_scores: List[Dict]) -> Dict:
    """
    Get comprehensive risk summary statistics
    
    Args:
        risk_scores: List of risk scores
        
    Returns:
        Dict: Summary statistics
    """
    if not risk_scores:
        return {
            'totalMunicipalities': 0,
            'averageRisk': 0.0,
            'weightedRisk': 0.0,
            'maxRisk': 0.0,
            'minRisk': 0.0,
            'highRiskCount': 0
        }
    
    risk_values = [score['riskScore'] for score in risk_scores]
    
    return {
        'totalMunicipalities': len(risk_scores),
        'averageRisk': round(calculate_average_risk(risk_scores), 6),
        'weightedRisk': round(calculate_weighted_risk(risk_scores), 6),
        'maxRisk': round(max(risk_values), 6),
        'minRisk': round(min(risk_values), 6),
        'highRiskCount': len(get_high_risk_municipalities(risk_scores))
    }

# ============================================================================
# TESTING / VALIDATION
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("Risk Calculator - Test")
    print("=" * 70)
    
    # Test data
    test_results = [
        {
            'id': '1',
            'name': 'Low Risk City',
            'predictedInfectedDogs': 5,
            'predictedInfectedCats': 2,
            'predictedInfectedHumans': 0,
            'totalPredictedInfected': 7,
            'susceptibleDogs': 980,
            'recoveredDogs': 5,
            'vaccinatedDogs': 10,
            'totalPopulation': 1500  # Dogs + Cats + Humans
        },
        {
            'id': '2',
            'name': 'Moderate Risk City',
            'predictedInfectedDogs': 30,
            'predictedInfectedCats': 10,
            'predictedInfectedHumans': 1,
            'totalPredictedInfected': 41,
            'susceptibleDogs': 950,
            'recoveredDogs': 10,
            'vaccinatedDogs': 0,
            'totalPopulation': 1200
        },
        {
            'id': '3',
            'name': 'High Risk City',
            'predictedInfectedDogs': 80,
            'predictedInfectedCats': 20,
            'predictedInfectedHumans': 3,
            'totalPredictedInfected': 103,
            'susceptibleDogs': 900,
            'recoveredDogs': 15,
            'vaccinatedDogs': 0,
            'totalPopulation': 1300
        }
    ]
    
    # Calculate risk scores
    print("\nCalculating risk scores using formula: R_i = I^_i(T) / N_i")
    risk_scores = calculate_risk_scores(test_results)
    
    print("\nRisk Scores:")
    for score in risk_scores:
        print(f"\n  {score['municipalityName']}:")
        print(f"    Predicted Infected (I^_i): {score['predictedInfected']}")
        print(f"    Total Population (N_i): {score['totalPopulation']}")
        print(f"    Risk Score (R_i): {score['riskScore']:.6f} ({score['riskScore']*100:.3f}%)")
        print(f"    Risk Level: {categorize_risk_level(score['riskScore']).upper()}")
    
    # Test categorization
    print("\n" + "-" * 70)
    print("Risk Level Distribution:")
    distribution = categorize_risk_levels(risk_scores)
    for level, count in distribution.items():
        print(f"  {level.capitalize()}: {count}")
    
    # Test summary
    print("\n" + "-" * 70)
    print("Risk Summary:")
    summary = get_risk_summary(risk_scores)
    for key, value in summary.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.6f} ({value*100:.3f}%)")
        else:
            print(f"  {key}: {value}")
    
    # Test high-risk municipalities
    print("\n" + "-" * 70)
    print("High-Risk Municipalities (≥ 5%):")
    high_risk = get_high_risk_municipalities(risk_scores)
    if high_risk:
        for mun in high_risk:
            print(f"  {mun['municipalityName']}: {mun['riskScore']*100:.3f}%")
    else:
        print("  None")
    
    print("\n" + "=" * 70)
    print("Test completed successfully!")
    print("=" * 70)
