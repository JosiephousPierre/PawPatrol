"""
DRL Inference Module
Provides DRL-based vaccination recommendations using the trained DQN model

Author: PAWPATROL Research Team
Date: October 2026
"""

import numpy as np
from typing import Dict, List, Any, Optional
from stable_baselines3 import DQN
import os

from drl.environment import RabiesVaccinationEnv
from drl.config import DRLConfig, DEFAULT_CONFIG


class DRLRecommender:
    """
    DRL-based vaccination recommender
    Loads trained DQN model and provides vaccination recommendations
    """
    
    def __init__(
        self,
        model_path: str = "./drl/models/dqn_rabies_vaccination",
        config: DRLConfig = None
    ):
        """
        Initialize DRL Recommender
        
        Args:
            model_path: Path to trained DQN model (without .zip)
            config: DRL configuration
        """
        self.model_path = model_path
        self.config = config or DEFAULT_CONFIG
        self.model = None
        self.is_loaded = False
        
        # Vaccination levels mapping (discrete actions)
        self.vaccination_levels = [0.0, 0.5, 0.7, 0.8, 0.9, 0.95]
        
        # Load model
        self._load_model()
    
    def _load_model(self):
        """Load trained DQN model"""
        try:
            # Check if .zip file exists
            zip_path = f"{self.model_path}.zip"
            if os.path.exists(zip_path):
                self.model = DQN.load(self.model_path)
                self.is_loaded = True
                print(f"✅ DRL model loaded from: {zip_path}")
            else:
                print(f"⚠️  DRL model not found at: {zip_path}")
                print("    DRL recommendations will not be available.")
                self.is_loaded = False
        except Exception as e:
            print(f"❌ Error loading DRL model: {e}")
            print(f"    Attempted path: {self.model_path}")
            self.is_loaded = False
    
    def get_recommendation(
        self,
        municipality_data: Dict[str, Any],
        all_municipalities: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Get DRL vaccination recommendation for a municipality
        
        Args:
            municipality_data: Single municipality data
            all_municipalities: All municipalities (for neighbor risk calculation)
            
        Returns:
            Dictionary with recommendation and explanation
        """
        if not self.is_loaded:
            return self._fallback_recommendation(municipality_data)
        
        try:
            # Create observation from municipality data
            observation = self._create_observation(
                municipality_data,
                all_municipalities or [municipality_data]
            )
            
            # Get DQN prediction
            action, _ = self.model.predict(observation, deterministic=True)
            vaccination_pct = self.vaccination_levels[int(action)]
            
            # Get Q-values for explanation
            q_values = self._get_q_values(observation)
            
            # Calculate confidence
            confidence = self._calculate_confidence(q_values)
            
            # Generate explanation
            explanation = self._generate_explanation(
                municipality_data,
                observation,
                vaccination_pct,
                confidence
            )
            
            return {
                'recommended_vaccination': float(vaccination_pct),
                'confidence': float(confidence),
                'action': int(action),
                'q_values': {
                    f"{int(self.vaccination_levels[i]*100)}%": float(q_values[i])
                    for i in range(len(self.vaccination_levels))
                },
                'explanation': explanation,
                'source': 'drl',
                'model_version': '1.0'
            }
            
        except Exception as e:
            print(f"Error in DRL recommendation: {e}")
            return self._fallback_recommendation(municipality_data)
    
    def get_batch_recommendations(
        self,
        municipalities: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Get DRL recommendations for multiple municipalities
        
        Args:
            municipalities: List of municipality data
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        for municipality in municipalities:
            recommendation = self.get_recommendation(
                municipality,
                municipalities
            )
            recommendation['municipality_id'] = municipality['id']
            recommendation['municipality_name'] = municipality['name']
            recommendations.append(recommendation)
        
        return recommendations
    
    def _create_observation(
        self,
        municipality: Dict[str, Any],
        all_municipalities: List[Dict[str, Any]]
    ) -> np.ndarray:
        """
        Create observation vector from municipality data
        
        Observation: [infection_rate, vaccination_coverage, neighbor_risk,
                     population_density, risk_level_numeric, day_normalized]
        """
        # Feature 1: Infection rate
        total_animals = municipality['dogPopulation'] + municipality['catPopulation']
        total_infected = municipality['infectedDogs'] + municipality['infectedCats']
        infection_rate = total_infected / total_animals if total_animals > 0 else 0.0
        
        # Feature 2: Vaccination coverage
        vaccination_coverage = (
            municipality['vaccinatedDogs'] / municipality['dogPopulation']
            if municipality['dogPopulation'] > 0 else 0.0
        )
        
        # Feature 3: Neighbor risk
        neighbor_risk = self._calculate_neighbor_risk(municipality, all_municipalities)
        
        # Feature 4: Population density (normalized)
        population_density = min(municipality['populationDensity'] / 500.0, 1.0)
        
        # Feature 5: Risk level numeric
        risk_map = {'safe': 0, 'low': 1, 'moderate': 2, 'high': 3, 'critical': 4}
        risk_level_numeric = risk_map.get(municipality['riskLevel'], 2) / 4.0
        
        # Feature 6: Day normalized (assume day 0 for recommendations)
        day_normalized = 0.0
        
        # Construct observation
        observation = np.array([
            infection_rate,
            vaccination_coverage,
            neighbor_risk,
            population_density,
            risk_level_numeric,
            day_normalized
        ], dtype=np.float32)
        
        # Clip to [0, 1]
        observation = np.clip(observation, 0.0, 1.0)
        
        return observation
    
    def _calculate_neighbor_risk(
        self,
        municipality: Dict[str, Any],
        all_municipalities: List[Dict[str, Any]]
    ) -> float:
        """Calculate risk from neighboring municipalities"""
        if not municipality.get('connectedMunicipalities'):
            return 0.0
        
        total_risk = 0.0
        neighbor_count = 0
        
        for neighbor_id in municipality['connectedMunicipalities']:
            neighbor = next((m for m in all_municipalities if m['id'] == neighbor_id), None)
            if neighbor:
                total_animals = neighbor['dogPopulation'] + neighbor['catPopulation']
                total_infected = neighbor['infectedDogs'] + neighbor['infectedCats']
                neighbor_infection_rate = (
                    total_infected / total_animals if total_animals > 0 else 0.0
                )
                
                total_risk += neighbor_infection_rate * 10  # Scale to 0-10
                neighbor_count += 1
        
        avg_risk = total_risk / neighbor_count if neighbor_count > 0 else 0.0
        return min(avg_risk / 10.0, 1.0)  # Normalize to [0, 1]
    
    def _get_q_values(self, observation: np.ndarray) -> np.ndarray:
        """Get Q-values for all actions"""
        import torch
        
        obs_tensor = torch.as_tensor(observation).reshape(1, -1).to(self.model.device)
        with torch.no_grad():
            q_values = self.model.q_net(obs_tensor)
        
        return q_values.cpu().numpy().flatten()
    
    def _calculate_confidence(self, q_values: np.ndarray) -> float:
        """
        Calculate confidence based on Q-value spread
        Higher confidence when best action is clearly better than alternatives
        """
        if len(q_values) < 2:
            return 0.5
        
        sorted_q = np.sort(q_values)[::-1]
        q_spread = sorted_q[0] - sorted_q[1]
        
        # Normalize to [0, 1]
        # Larger spread = higher confidence
        confidence = min(abs(q_spread) / 100.0, 1.0)
        
        return max(confidence, 0.5)  # Minimum 50% confidence
    
    def _generate_explanation(
        self,
        municipality: Dict[str, Any],
        observation: np.ndarray,
        vaccination_pct: float,
        confidence: float
    ) -> str:
        """Generate human-readable explanation"""
        infection_rate = observation[0]
        vaccination_coverage = observation[1]
        neighbor_risk = observation[2]
        risk_level = municipality['riskLevel']
        
        # Determine recommendation reasoning
        if vaccination_pct >= 0.9:
            level = "very high"
            reason = "high infection risk"
        elif vaccination_pct >= 0.8:
            level = "high"
            reason = "elevated risk"
        elif vaccination_pct >= 0.7:
            level = "moderate"
            reason = "moderate risk"
        elif vaccination_pct >= 0.5:
            level = "standard"
            reason = "low to moderate risk"
        else:
            level = "minimal"
            reason = "very low risk"
        
        explanation = (
            f"DRL recommends {level} vaccination ({int(vaccination_pct*100)}%) "
            f"based on {reason}. "
        )
        
        # Add risk factors
        factors = []
        if infection_rate > 0.05:
            factors.append(f"current infection rate of {infection_rate*100:.1f}%")
        if vaccination_coverage < 0.7:
            factors.append(f"low vaccination coverage ({vaccination_coverage*100:.1f}%)")
        if neighbor_risk > 0.3:
            factors.append("risk from neighboring areas")
        if risk_level in ['high', 'critical']:
            factors.append(f"{risk_level} risk level")
        
        if factors:
            explanation += "Key factors: " + ", ".join(factors) + ". "
        
        explanation += f"Confidence: {confidence*100:.0f}%."
        
        return explanation
    
    def _fallback_recommendation(
        self,
        municipality: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Fallback to rule-based recommendation if DRL not available
        """
        # Simple rule-based logic
        risk_level = municipality['riskLevel']
        
        risk_to_vaccination = {
            'safe': 0.5,
            'low': 0.7,
            'moderate': 0.8,
            'high': 0.9,
            'critical': 0.95
        }
        
        vaccination_pct = risk_to_vaccination.get(risk_level, 0.7)
        
        return {
            'recommended_vaccination': vaccination_pct,
            'confidence': 0.6,
            'action': None,
            'q_values': {},
            'explanation': (
                f"Rule-based recommendation: {int(vaccination_pct*100)}% vaccination "
                f"for {risk_level} risk level. (DRL model not available)"
            ),
            'source': 'rule-based',
            'model_version': 'fallback'
        }
    
    def is_available(self) -> bool:
        """Check if DRL model is loaded and available"""
        return self.is_loaded


# =============================================================================
# GLOBAL INSTANCE
# =============================================================================

# Create global recommender instance
_global_recommender = None


def get_recommender() -> DRLRecommender:
    """Get global DRL recommender instance (singleton)"""
    global _global_recommender
    
    if _global_recommender is None:
        _global_recommender = DRLRecommender()
    
    return _global_recommender


# =============================================================================
# TESTING
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("DRL Inference - Test")
    print("=" * 70)
    
    # Test data
    test_municipality = {
        'id': '1',
        'name': 'Maco',
        'humanPopulation': 75033,
        'dogPopulation': 3000,
        'catPopulation': 1500,
        'infectedDogs': 15,
        'infectedCats': 3,
        'infectedHumans': 0,
        'vaccinatedDogs': 900,
        'populationDensity': 295.2,
        'latitude': 7.3667,
        'longitude': 126.0167,
        'riskLevel': 'moderate',
        'connectedMunicipalities': []
    }
    
    # Create recommender
    print("\n[1/3] Creating DRL recommender...")
    recommender = DRLRecommender()
    print(f"   Model loaded: {recommender.is_available()}")
    
    # Get recommendation
    print("\n[2/3] Getting recommendation...")
    recommendation = recommender.get_recommendation(test_municipality)
    
    print(f"\n   Municipality: {test_municipality['name']}")
    print(f"   Risk Level: {test_municipality['riskLevel']}")
    print(f"   Infected: {test_municipality['infectedDogs']} dogs, {test_municipality['infectedCats']} cats")
    print(f"   Vaccinated: {test_municipality['vaccinatedDogs']} / {test_municipality['dogPopulation']} dogs")
    print(f"\n   ✅ Recommended Vaccination: {recommendation['recommended_vaccination']*100:.0f}%")
    print(f"   ✅ Confidence: {recommendation['confidence']*100:.0f}%")
    print(f"   ✅ Source: {recommendation['source']}")
    print(f"\n   Explanation: {recommendation['explanation']}")
    
    # Test batch
    print("\n[3/3] Testing batch recommendations...")
    municipalities = [test_municipality] * 3
    batch_recommendations = recommender.get_batch_recommendations(municipalities)
    print(f"   ✅ Generated {len(batch_recommendations)} recommendations")
    
    print("\n" + "=" * 70)
    print("✅ DRL Inference test completed!")
    print("=" * 70)
