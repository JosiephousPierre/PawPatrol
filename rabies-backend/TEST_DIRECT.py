"""
Direct test of transmission_model.py without FastAPI
"""

from simulation.transmission_model import run_fractional_stochastic_simulation
from models.request_models import MunicipalityData, SimulationSettings

# Create test municipality
mun = MunicipalityData(
    id="test-1",
    name="Test",
    latitude=7.5,
    longitude=125.9,
    humanPopulation=50000,
    dogPopulation=5000,
    catPopulation=3000,
    populationDensity=100.0,
    infectedDogs=50,
    infectedCats=20,
    infectedHumans=5,
    vaccinatedDogs=2000,
    riskLevel="moderate",
    connectedMunicipalities=[]
)

# Create settings
settings = SimulationSettings(
    simulationDays=30,
    fractionalOrder=0.95,
    lambda_dog=0.0001,
    lambda_cat=0.00012,
    lambda_human=0.00005,
    mu_dog=0.0001,
    mu_cat=0.00015,
    mu_human=0.00003,
    delta_dog=0.1,
    delta_cat=0.1,
    delta_human=0.1,
    beta_dd=0.5,
    beta_dc=0.2,
    beta_cc=0.35,
    beta_dh=0.1,
    beta_ch=0.05,
    sigma_1=0.1,
    sigma_2=0.1,
    sigma_3=0.05,
    vaccinationRate=0.01
)

print("Running simulation...")
results = run_fractional_stochastic_simulation([mun], settings)

print(f"\nResults: {len(results)} municipalities")
if results:
    r = results[0]
    print(f"\nMunicipality: {r['name']}")
    print(f"  totalDogBirths: {r.get('totalDogBirths', 'MISSING')}")
    print(f"  totalDogNaturalDeaths: {r.get('totalDogNaturalDeaths', 'MISSING')}")
    print(f"  totalDogRabiesDeaths: {r.get('totalDogRabiesDeaths', 'MISSING')}")
    print(f"  totalDogVaccinations: {r.get('totalDogVaccinations', 'MISSING')}")
    print(f"  totalHumanVaccinations: {r.get('totalHumanVaccinations', 'MISSING')}")
