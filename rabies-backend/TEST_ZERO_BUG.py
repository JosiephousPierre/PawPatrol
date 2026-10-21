"""
Test to verify if infected counts inappropriately go to zero
"""
from simulation.transmission_model import run_fractional_stochastic_simulation
from models.request_models import MunicipalityData, SimulationSettings

# Create test municipality
mun = MunicipalityData(
    id='1',
    name='Test Municipality',
    latitude=7.5,
    longitude=125.9,
    humanPopulation=10000,
    dogPopulation=1000,
    catPopulation=500,
    populationDensity=250,
    infectedDogs=100,  # START: 100 infected dogs
    infectedCats=50,   # START: 50 infected cats
    infectedHumans=0,
    vaccinatedDogs=0,  # NO vaccination
    riskLevel='high',
    connectedMunicipalities=[]
)

# Settings for SHORT simulation (10 days)
settings = SimulationSettings(
    simulationDays=10,
    fractionalOrder=0.95,
    transmissionRate=0.15,
    recoveryRate=0.1,
    stochasticIntensity=0.0,  # NO randomness for predictable test
    contactProbability=0.3,
    vaccinationRate=0.0  # NO vaccination
)

print("=" * 70)
print("TESTING: Do infected counts inappropriately go to ZERO?")
print("=" * 70)
print("\nINITIAL STATE:")
print(f"  Infected Dogs: 100")
print(f"  Infected Cats: 50")
print(f"  Infected Humans: 0")
print(f"\nSIMULATION: 10 days, NO vaccination, NO randomness")
print(f"  Death rate (delta): Dogs=0.1/day, Cats=0.12/day")
print(f"  Transmission rate (beta): 0.15")
print()

result = run_fractional_stochastic_simulation([mun], settings)

r = result[0]
print("=" * 70)
print("RESULTS AFTER 10 DAYS:")
print("=" * 70)
print(f"  Infected Dogs: {r['predictedInfectedDogs']}")
print(f"  Infected Cats: {r['predictedInfectedCats']}")
print(f"  Infected Humans: {r['predictedInfectedHumans']}")
print()

# Analysis
print("=" * 70)
print("EXPECTED BEHAVIOR:")
print("=" * 70)
print("With death rate δ = 0.1/day (dogs):")
print("  After 10 days: 0.9^10 = 34.9% survival")
print("  Expected: ~35 dogs still infected (if no new infections)")
print("  PLUS: New infections from transmission β·S·I/N")
print()
print("With death rate δ = 0.12/day (cats):")
print("  After 10 days: 0.88^10 = 27.9% survival")
print("  Expected: ~14 cats still infected (if no new infections)")
print("  PLUS: Spillover from infected dogs")
print()

# Verdict
if r['predictedInfectedDogs'] == 0 and r['predictedInfectedCats'] == 0:
    print("🚨 BUG CONFIRMED: Infected counts went to ZERO!")
    print("   This is INCORRECT. Animals should remain infected for ~10 days.")
    print("   There is a bug in the simulation logic.")
elif r['predictedInfectedDogs'] > 0 or r['predictedInfectedCats'] > 0:
    print("✅ CORRECT: Some animals still infected!")
    print("   Infected animals remain alive and dangerous during infectious period.")
else:
    print("⚠️  UNUSUAL: Please investigate further.")

print("=" * 70)
