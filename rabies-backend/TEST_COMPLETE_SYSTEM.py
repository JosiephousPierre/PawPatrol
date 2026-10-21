"""
COMPREHENSIVE SYSTEM TEST - Phase 2 SI+V+BD Model
Run this to verify everything works correctly
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 80)
print("🧪 PAWPATROL PHASE 2 COMPLETE SYSTEM TEST")
print("=" * 80)
print()

# Test 1: Import all modules
print("📦 [Test 1/5] Importing modules...")
try:
    from models.request_models import SimulationSettings, MunicipalityData
    from simulation.transmission_model import run_fractional_stochastic_simulation
    from simulation.transmission_model import (
        calculate_births,
        calculate_natural_deaths,
        calculate_rabies_deaths,
        calculate_transmission,
        calculate_vaccination,
        generate_independent_wiener_processes
    )
    print("   ✅ All imports successful")
except Exception as e:
    print(f"   ❌ Import failed: {e}")
    sys.exit(1)

print()

# Test 2: Verify helper functions work
print("🔧 [Test 2/5] Testing helper functions...")
try:
    # Test births
    births = calculate_births(0.0001, 10000, 1.0)
    assert births == 1.0, f"Births incorrect: {births}"
    
    # Test deaths
    deaths = calculate_natural_deaths(0.0001, 5000, 1.0)
    assert deaths == 0.5, f"Deaths incorrect: {deaths}"
    
    # Test rabies deaths
    rabies_deaths = calculate_rabies_deaths(0.1, 100, 1.0)
    assert rabies_deaths == 10.0, f"Rabies deaths incorrect: {rabies_deaths}"
    
    # Test Wiener processes
    dW_list = generate_independent_wiener_processes(0.1, [0.1, 0.08, 0.05])
    assert len(dW_list) == 3, "Should return 3 Wiener increments"
    
    # Test transmission
    infections = calculate_transmission(900, 100, 1000, 0.15, 0.3, 1.0)
    assert infections > 0, "Should have some infections"
    
    # Test vaccination
    vax = calculate_vaccination(1000, 0, 1000, 0.8, 100, 1.0)
    assert vax > 0, "Should have vaccinations"
    
    print("   ✅ All helper functions working correctly")
except AssertionError as e:
    print(f"   ❌ Helper function test failed: {e}")
    sys.exit(1)

print()

# Test 3: Run simulation with new Phase 2 parameters
print("🚀 [Test 3/5] Running simulation with Phase 2 parameters...")
try:
    # Create settings with ALL Phase 2 parameters
    settings = SimulationSettings(
        fractionalOrder=0.95,
        transmissionRate=0.15,  # Legacy (for compatibility)
        recoveryRate=0.1,        # Legacy (not used in SI model)
        stochasticIntensity=0.1, # Legacy
        contactProbability=0.3,
        vaccinationRate=0.7,
        simulationDays=30,
        # NEW Phase 2 parameters
        lambda_dog=0.0001,
        lambda_cat=0.0002,
        lambda_human=0.00005,
        mu_dog=0.0001,
        mu_cat=0.0002,
        mu_human=0.00003,
        delta_dog=0.1,
        delta_cat=0.12,
        delta_human=0.15,
        sigma_1=0.1,
        sigma_2=0.08,
        sigma_3=0.05,
        beta_dd=0.15,
        beta_dc=0.06,
        beta_cc=0.105,
        beta_dh=0.0015,
        beta_ch=0.00075
    )
    
    # Create test municipality
    municipality = MunicipalityData(
        id="1",
        name="Test City",
        latitude=7.0,
        longitude=125.0,
        humanPopulation=100000,
        dogPopulation=10000,
        catPopulation=5000,
        populationDensity=1000.0,
        infectedDogs=100,
        infectedCats=50,
        infectedHumans=10,
        vaccinatedDogs=900,
        riskLevel="moderate",
        connectedMunicipalities=[]
    )
    
    # Run simulation
    results = run_fractional_stochastic_simulation([municipality], settings)
    
    assert len(results) == 1, "Should return 1 result"
    result = results[0]
    
    print(f"   ✅ Simulation completed successfully")
    print(f"      Municipality: {result['name']}")
    
except Exception as e:
    print(f"   ❌ Simulation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Test 4: Verify all predictions exist
print("📊 [Test 4/5] Verifying predictions for all species...")
try:
    # Check dog predictions
    assert 'predictedInfectedDogs' in result, "Missing dog infected prediction"
    assert 'predictedDogPopulation' in result, "Missing dog population"
    assert 'vaccinatedDogs' in result, "Missing dog vaccination"
    
    # Check cat predictions
    assert 'predictedInfectedCats' in result, "Missing cat infected prediction"
    assert 'predictedCatPopulation' in result, "Missing cat population"
    
    # Check human predictions
    assert 'predictedInfectedHumans' in result, "Missing human infected prediction"
    assert 'predictedHumanPopulation' in result, "Missing human population"
    
    print(f"   ✅ All species predictions present")
    print(f"      Dogs:   {result['predictedInfectedDogs']:.0f} infected, {result['predictedDogPopulation']:.0f} total")
    print(f"      Cats:   {result['predictedInfectedCats']:.0f} infected, {result['predictedCatPopulation']:.0f} total")
    print(f"      Humans: {result['predictedInfectedHumans']:.0f} infected, {result['predictedHumanPopulation']:.0f} total")
    
except AssertionError as e:
    print(f"   ❌ Prediction verification failed: {e}")
    sys.exit(1)

print()

# Test 5: Verify cumulative statistics (births, deaths, vaccinations)
print("📈 [Test 5/5] Verifying cumulative statistics...")
try:
    # Check dog statistics
    assert 'cumulativeDogBirths' in result, "Missing dog births"
    assert 'cumulativeDogDeaths' in result, "Missing dog natural deaths"
    assert 'cumulativeDogRabiesDeaths' in result, "Missing dog rabies deaths"
    assert 'cumulativeDogVaccinations' in result, "Missing dog vaccinations"
    
    # Check cat statistics
    assert 'cumulativeCatBirths' in result, "Missing cat births"
    assert 'cumulativeCatDeaths' in result, "Missing cat natural deaths"
    assert 'cumulativeCatRabiesDeaths' in result, "Missing cat rabies deaths"
    assert 'cumulativeCatVaccinations' in result, "Missing cat vaccinations"
    
    # Check human statistics
    assert 'cumulativeHumanBirths' in result, "Missing human births"
    assert 'cumulativeHumanDeaths' in result, "Missing human natural deaths"
    assert 'cumulativeHumanRabiesDeaths' in result, "Missing human rabies deaths"
    
    print(f"   ✅ All cumulative statistics present")
    print()
    print("   📊 DOGS:")
    print(f"      Births: {result['cumulativeDogBirths']:.0f}")
    print(f"      Natural Deaths: {result['cumulativeDogDeaths']:.0f}")
    print(f"      Rabies Deaths: {result['cumulativeDogRabiesDeaths']:.0f}")
    print(f"      Vaccinations: {result['cumulativeDogVaccinations']:.0f}")
    
    print()
    print("   📊 CATS:")
    print(f"      Births: {result['cumulativeCatBirths']:.0f}")
    print(f"      Natural Deaths: {result['cumulativeCatDeaths']:.0f}")
    print(f"      Rabies Deaths: {result['cumulativeCatRabiesDeaths']:.0f}")
    print(f"      Vaccinations: {result['cumulativeCatVaccinations']:.0f}")
    
    print()
    print("   📊 HUMANS:")
    print(f"      Births: {result['cumulativeHumanBirths']:.0f}")
    print(f"      Natural Deaths: {result['cumulativeHumanDeaths']:.0f}")
    print(f"      Rabies Deaths: {result['cumulativeHumanRabiesDeaths']:.0f}")
    
except AssertionError as e:
    print(f"   ❌ Statistics verification failed: {e}")
    sys.exit(1)

print()
print("=" * 80)
print("✅ ALL TESTS PASSED!")
print("=" * 80)
print()
print("🎉 PHASE 2 SI+V+BD MODEL IS WORKING CORRECTLY!")
print()
print("Summary:")
print("  ✅ All modules imported successfully")
print("  ✅ Helper functions working")
print("  ✅ Simulation runs with Phase 2 parameters")
print("  ✅ Predictions for dogs, cats, and humans")
print("  ✅ Cumulative statistics tracked (births, deaths, vaccinations)")
print()
print("The system is ready for use! 🚀")
print("=" * 80)
