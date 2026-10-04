"""
Rabies Vaccination Environment for Deep Reinforcement Learning
Wraps the fractional-order stochastic transmission model as a Gymnasium environment

This environment allows the DQN agent to learn optimal vaccination strategies
by interacting with the transmission model simulation.

State Space: 6 features per municipality
    - infection_rate: % of animals infected (0-1)
    - vaccination_coverage: % of dogs vaccinated (0-1)
    - neighbor_risk: Risk from neighboring municipalities (0-1)
    - population_density: Normalized density (0-1)
    - risk_level_numeric: Categorical risk (0-1)
    - day_normalized: Current day / max days (0-1)

Action Space: Continuous
    - Vaccination percentage (0-1) representing 0% to 100%

Reward Function:
    reward = -(new_infections * 1.0 + vaccination_cost * 0.01 + human_infections * 1000.0)
           + outbreak_control_bonus (if controlled)

Author: PAWPATROL Research Team
Date: October 2026
"""

import numpy as np
import gymnasium as gym
from gymnasium import spaces
from typing import Dict, List, Any, Optional, Tuple
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from simulation.transmission_model import run_fractional_stochastic_simulation
    from simulation.risk_calculator import calculate_risk_scores, categorize_risk_level
except ImportError:
    print("Warning: Could not import transmission model. Using dummy simulation.")
    run_fractional_stochastic_simulation = None

from drl.config import DRLConfig, DEFAULT_CONFIG


class RabiesVaccinationEnv(gym.Env):
    """
    Gymnasium environment for rabies vaccination optimization
    
    Uses the fractional-order stochastic transmission model as the simulation backend.
    The agent learns to optimize vaccination strategies to minimize infections and costs.
    """
    
    metadata = {"render_modes": ["human"]}
    
    def __init__(
        self,
        municipalities_data: List[Dict] = None,
        config: DRLConfig = None,
        single_municipality_mode: bool = True
    ):
        """
        Initialize the environment
        
        Args:
            municipalities_data: List of municipality dictionaries
            config: DRL configuration
            single_municipality_mode: If True, agent controls one municipality at a time
        """
        super().__init__()
        
        self.config = config or DEFAULT_CONFIG
        self.single_municipality_mode = single_municipality_mode
        
        # Initialize municipalities
        if municipalities_data is None:
            self.municipalities = self._create_dummy_municipalities()
        else:
            self.municipalities = municipalities_data
        
        # Episode tracking
        self.current_day = 0
        self.max_days = self.config.simulation_days
        self.episode_count = 0
        
        # Current municipality index (for single municipality mode)
        self.current_municipality_idx = 0
        
        # History tracking
        self.infection_history = []
        self.action_history = []
        self.reward_history = []
        
        # Define spaces
        self._setup_spaces()
        
        # Initial state
        self.initial_state = None
        
    def _setup_spaces(self):
        """Define observation and action spaces"""
        
        # Observation space: 6 continuous features, all normalized to [0, 1]
        n_features = len(self.config.state_features)
        self.observation_space = spaces.Box(
            low=0.0,
            high=1.0,
            shape=(n_features,),
            dtype=np.float32
        )
        
        # Action space: DISCRETE actions for DQN
        # Actions: 0=0%, 1=50%, 2=70%, 3=80%, 4=90%, 5=95%
        self.discrete_vaccination_levels = [0.0, 0.5, 0.7, 0.8, 0.9, 0.95]
        self.action_space = spaces.Discrete(len(self.discrete_vaccination_levels))
    
    def _create_dummy_municipalities(self) -> List[Dict]:
        """Create dummy municipality data for testing"""
        return [
            {
                'id': '1',
                'name': 'Test Municipality',
                'humanPopulation': 10000,
                'dogPopulation': 1000,
                'catPopulation': 500,
                'infectedDogs': 10,
                'infectedCats': 2,
                'infectedHumans': 0,
                'vaccinatedDogs': 300,
                'populationDensity': 250.0,
                'latitude': 7.5,
                'longitude': 125.9,
                'riskLevel': 'moderate',
                'connectedMunicipalities': []
            }
        ]
    
    def reset(
        self,
        seed: Optional[int] = None,
        options: Optional[Dict[str, Any]] = None
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Reset the environment to initial state
        
        Returns:
            observation: Initial state
            info: Additional information
        """
        super().reset(seed=seed)
        
        # Reset episode tracking
        self.current_day = 0
        self.episode_count += 1
        
        # Reset municipality to random starting conditions
        if self.single_municipality_mode:
            self.current_municipality_idx = self.np_random.integers(0, len(self.municipalities))
        
        # Reset histories
        self.infection_history = []
        self.action_history = []
        self.reward_history = []
        
        # Store initial state
        self.initial_state = self._get_municipality_state()
        
        # Get initial observation
        observation = self._get_observation()
        info = self._get_info()
        
        return observation, info
    
    def step(self, action: int) -> Tuple[np.ndarray, float, bool, bool, Dict]:
        """
        Execute one step in the environment
        
        Args:
            action: Discrete action index (0-5)
            
        Returns:
            observation: New state
            reward: Reward for this action
            terminated: Whether episode is done (success/failure)
            truncated: Whether episode was cut short
            info: Additional information
        """
        # Convert discrete action to vaccination percentage
        vaccination_pct = self.discrete_vaccination_levels[action]
        
        # Store action
        self.action_history.append(vaccination_pct)
        
        # Get current state before action
        current_infections = self._get_total_infections()
        
        # Apply vaccination and simulate
        self._apply_vaccination(vaccination_pct)
        self._run_simulation_step()
        
        # Get new state after action
        new_infections = self._get_total_infections()
        
        # Calculate reward
        reward = self._calculate_reward(
            current_infections=current_infections,
            new_infections=new_infections,
            vaccination_pct=vaccination_pct
        )
        
        # Store reward
        self.reward_history.append(reward)
        self.infection_history.append(new_infections)
        
        # Increment day
        self.current_day += 1
        
        # Check if episode is done
        terminated = self._is_terminated()
        truncated = self.current_day >= self.max_days
        
        # Get new observation
        observation = self._get_observation()
        info = self._get_info()
        
        return observation, reward, terminated, truncated, info
    
    def _apply_vaccination(self, vaccination_pct: float):
        """Apply vaccination to current municipality"""
        if self.single_municipality_mode:
            municipality = self.municipalities[self.current_municipality_idx]
            
            # Calculate target vaccinated dogs
            target_vaccinated = int(municipality['dogPopulation'] * vaccination_pct)
            
            # Update vaccinated count (can't exceed susceptible)
            current_vaccinated = municipality.get('vaccinatedDogs', 0)
            current_infected = municipality.get('infectedDogs', 0)
            current_recovered = municipality.get('recoveredDogs', 0)
            susceptible = municipality['dogPopulation'] - current_infected - current_recovered - current_vaccinated
            
            additional_vaccinations = min(target_vaccinated - current_vaccinated, susceptible)
            additional_vaccinations = max(0, additional_vaccinations)
            
            municipality['vaccinatedDogs'] = current_vaccinated + additional_vaccinations
    
    def _run_simulation_step(self):
        """Run transmission model for one day"""
        if run_fractional_stochastic_simulation is None:
            # Dummy simulation for testing
            self._dummy_simulation_step()
            return
        
        # Prepare simulation settings
        settings = {
            'simulationDays': 1,  # Simulate 1 day
            'fractionalOrder': 0.95,
            'transmissionRate': 0.15,
            'recoveryRate': 0.1,
            'contactProbability': 0.3,
            'stochasticIntensity': 0.1,
            'vaccinationRate': 0.8
        }
        
        try:
            # Run simulation
            results = run_fractional_stochastic_simulation(self.municipalities, settings)
            
            # Update municipality data with results
            for result in results:
                mun = next((m for m in self.municipalities if m['id'] == result['id']), None)
                if mun:
                    mun['infectedDogs'] = result['predictedInfectedDogs']
                    mun['infectedCats'] = result['predictedInfectedCats']
                    mun['infectedHumans'] = result['predictedInfectedHumans']
                    if 'vaccinatedDogs' in result:
                        mun['vaccinatedDogs'] = result['vaccinatedDogs']
                    
                    # Update risk level
                    if 'totalPopulation' in result:
                        risk_scores = calculate_risk_scores([result])
                        if risk_scores:
                            risk_level = categorize_risk_level(risk_scores[0]['riskScore'])
                            mun['riskLevel'] = risk_level
        
        except Exception as e:
            print(f"Warning: Simulation failed, using dummy: {e}")
            self._dummy_simulation_step()
    
    def _dummy_simulation_step(self):
        """Dummy simulation for testing (when transmission model unavailable)"""
        if self.single_municipality_mode:
            municipality = self.municipalities[self.current_municipality_idx]
            
            # Simple infection spread model
            vaccination_coverage = municipality['vaccinatedDogs'] / municipality['dogPopulation']
            transmission_rate = 0.15 * (1 - vaccination_coverage * 0.8)
            
            # Update infections (simple exponential growth/decay)
            current_infected = municipality['infectedDogs']
            susceptible = municipality['dogPopulation'] - current_infected - municipality['vaccinatedDogs']
            
            new_infections = int(transmission_rate * current_infected * (susceptible / municipality['dogPopulation']))
            recoveries = int(0.1 * current_infected)
            
            municipality['infectedDogs'] = max(0, current_infected + new_infections - recoveries)
            municipality['infectedCats'] = max(0, int(municipality['infectedDogs'] * 0.2))
            municipality['infectedHumans'] = max(0, int(municipality['infectedDogs'] * 0.01))
    
    def _calculate_reward(
        self,
        current_infections: int,
        new_infections: int,
        vaccination_pct: float
    ) -> float:
        """
        Calculate reward for the action taken
        
        Reward components:
        - Infection penalty: More infections = worse reward
        - Cost penalty: More vaccination = higher cost
        - Human infection penalty: Heavy penalty for human cases
        - Control bonus: Bonus if outbreak is controlled
        
        Returns:
            reward: Scalar reward value
        """
        municipality = self.municipalities[self.current_municipality_idx]
        
        # Component 1: Infection penalty
        total_infected = (
            municipality['infectedDogs'] +
            municipality['infectedCats']
        )
        infection_penalty = total_infected * self.config.infection_penalty
        
        # Component 2: Vaccination cost penalty
        vaccination_cost = vaccination_pct * municipality['dogPopulation']
        cost_penalty = vaccination_cost * self.config.cost_penalty
        
        # Component 3: Human infection penalty (very high!)
        human_infections = municipality.get('infectedHumans', 0)
        human_penalty = human_infections * self.config.human_infection_penalty
        
        # Component 4: Outbreak control bonus
        outbreak_controlled = total_infected < (current_infections * 0.5)  # 50% reduction
        control_bonus = self.config.outbreak_control_bonus if outbreak_controlled else 0.0
        
        # Combined reward (negative penalties, positive bonus)
        reward = -(infection_penalty + cost_penalty + human_penalty) + control_bonus
        
        return float(reward)
    
    def _get_observation(self) -> np.ndarray:
        """
        Get current observation (state)
        
        Returns:
            observation: 6-feature state vector
        """
        municipality = self.municipalities[self.current_municipality_idx]
        
        # Calculate features
        total_animals = municipality['dogPopulation'] + municipality['catPopulation']
        total_infected = municipality['infectedDogs'] + municipality['infectedCats']
        
        # Feature 1: Infection rate (0-1)
        infection_rate = total_infected / total_animals if total_animals > 0 else 0.0
        
        # Feature 2: Vaccination coverage (0-1)
        vaccination_coverage = (
            municipality['vaccinatedDogs'] / municipality['dogPopulation']
            if municipality['dogPopulation'] > 0 else 0.0
        )
        
        # Feature 3: Neighbor risk (0-1, normalized)
        neighbor_risk = self._calculate_neighbor_risk() / 10.0  # Normalize to [0, 1]
        
        # Feature 4: Population density (0-1, normalized)
        population_density = min(municipality['populationDensity'] / 500.0, 1.0)
        
        # Feature 5: Risk level numeric (0-1)
        risk_map = {'safe': 0, 'low': 1, 'moderate': 2, 'high': 3, 'critical': 4}
        risk_level_numeric = risk_map.get(municipality['riskLevel'], 2) / 4.0
        
        # Feature 6: Day normalized (0-1)
        day_normalized = self.current_day / self.max_days
        
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
    
    def _calculate_neighbor_risk(self) -> float:
        """Calculate risk from neighboring municipalities"""
        municipality = self.municipalities[self.current_municipality_idx]
        
        if not municipality.get('connectedMunicipalities'):
            return 0.0
        
        total_risk = 0.0
        neighbor_count = 0
        
        for neighbor_id in municipality['connectedMunicipalities']:
            neighbor = next((m for m in self.municipalities if m['id'] == neighbor_id), None)
            if neighbor:
                total_animals = neighbor['dogPopulation'] + neighbor['catPopulation']
                total_infected = neighbor['infectedDogs'] + neighbor['infectedCats']
                neighbor_infection_rate = total_infected / total_animals if total_animals > 0 else 0.0
                
                total_risk += neighbor_infection_rate * 10  # Scale to 0-10
                neighbor_count += 1
        
        return total_risk / neighbor_count if neighbor_count > 0 else 0.0
    
    def _get_total_infections(self) -> int:
        """Get total infections in current municipality"""
        municipality = self.municipalities[self.current_municipality_idx]
        return (
            municipality['infectedDogs'] +
            municipality['infectedCats'] +
            municipality.get('infectedHumans', 0)
        )
    
    def _is_terminated(self) -> bool:
        """Check if episode should terminate early"""
        municipality = self.municipalities[self.current_municipality_idx]
        
        # Terminate if no more infections (success!)
        if self._get_total_infections() == 0:
            return True
        
        # Terminate if human infections exceed threshold (failure)
        if municipality.get('infectedHumans', 0) >= 10:
            return True
        
        # Terminate if outbreak explodes (failure)
        total_animals = municipality['dogPopulation'] + municipality['catPopulation']
        total_infected = municipality['infectedDogs'] + municipality['infectedCats']
        if total_infected > total_animals * 0.5:  # 50% infection rate
            return True
        
        return False
    
    def _get_info(self) -> Dict[str, Any]:
        """Get additional information"""
        municipality = self.municipalities[self.current_municipality_idx]
        
        return {
            'day': self.current_day,
            'episode': self.episode_count,
            'municipality_id': municipality['id'],
            'municipality_name': municipality['name'],
            'total_infections': self._get_total_infections(),
            'infected_dogs': municipality['infectedDogs'],
            'infected_cats': municipality['infectedCats'],
            'infected_humans': municipality.get('infectedHumans', 0),
            'vaccinated_dogs': municipality['vaccinatedDogs'],
            'vaccination_coverage': municipality['vaccinatedDogs'] / municipality['dogPopulation'],
            'cumulative_reward': sum(self.reward_history),
        }
    
    def _get_municipality_state(self) -> Dict:
        """Get copy of current municipality state"""
        return self.municipalities[self.current_municipality_idx].copy()
    
    def render(self):
        """Render the environment (for debugging)"""
        if self.single_municipality_mode:
            municipality = self.municipalities[self.current_municipality_idx]
            print(f"\n=== Day {self.current_day} ===")
            print(f"Municipality: {municipality['name']}")
            print(f"Infected Dogs: {municipality['infectedDogs']}")
            print(f"Infected Cats: {municipality['infectedCats']}")
            print(f"Infected Humans: {municipality.get('infectedHumans', 0)}")
            print(f"Vaccinated Dogs: {municipality['vaccinatedDogs']} / {municipality['dogPopulation']}")
            print(f"Coverage: {municipality['vaccinatedDogs'] / municipality['dogPopulation'] * 100:.1f}%")
            if self.reward_history:
                print(f"Last Reward: {self.reward_history[-1]:.2f}")
                print(f"Cumulative Reward: {sum(self.reward_history):.2f}")
    
    def close(self):
        """Clean up resources"""
        pass


# =============================================================================
# TESTING
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("Rabies Vaccination Environment - Test")
    print("=" * 70)
    
    # Create environment
    print("\n[1/5] Creating environment...")
    env = RabiesVaccinationEnv()
    print(f"   ✅ Observation space: {env.observation_space}")
    print(f"   ✅ Action space: {env.action_space}")
    
    # Reset environment
    print("\n[2/5] Resetting environment...")
    observation, info = env.reset()
    print(f"   ✅ Initial observation: {observation}")
    print(f"   ✅ Initial info: {info}")
    
    # Take random actions
    print("\n[3/5] Taking random actions...")
    for i in range(5):
        action = env.action_space.sample()
        observation, reward, terminated, truncated, info = env.step(action)
        vacc_pct = env.discrete_vaccination_levels[action]
        print(f"   Step {i+1}: action={action} ({vacc_pct*100:.0f}%), reward={reward:.2f}, infections={info['total_infections']}")
        
        if terminated or truncated:
            print(f"   Episode ended after {i+1} steps")
            break
    
    # Reset and test with fixed actions
    print("\n[4/5] Testing with fixed vaccination strategy (80% = action 3)...")
    observation, info = env.reset()
    cumulative_reward = 0
    
    for day in range(10):
        action = 3  # 80% vaccination
        observation, reward, terminated, truncated, info = env.step(action)
        cumulative_reward += reward
        
        if day % 3 == 0:  # Print every 3 days
            print(f"   Day {day+1}: infections={info['total_infections']}, reward={reward:.2f}")
        
        if terminated or truncated:
            break
    
    print(f"   Final cumulative reward: {cumulative_reward:.2f}")
    
    # Test observation space
    print("\n[5/5] Verifying observation space...")
    observation, info = env.reset()
    print(f"   ✅ Observation shape: {observation.shape}")
    print(f"   ✅ Observation range: [{observation.min():.3f}, {observation.max():.3f}]")
    print(f"   ✅ All values in [0, 1]: {np.all((observation >= 0) & (observation <= 1))}")
    
    # Close environment
    env.close()
    
    print("\n" + "=" * 70)
    print("✅ Environment test completed successfully!")
    print("=" * 70)
    print("\nEnvironment is ready for DQN training!")
