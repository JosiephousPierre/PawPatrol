"""
Test DRL Inference Module
"""

import sys
sys.path.insert(0, '.')

from drl.inference import get_recommender

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

print("=" * 70)
print("DRL Inference - Test")
print("=" * 70)

# Get recommender
print("\n[1/2] Getting DRL recommender...")
recommender = get_recommender()
print(f"   Model available: {recommender.is_available()}")

# Get recommendation
print("\n[2/2] Getting recommendation...")
recommendation = recommender.get_recommendation(test_municipality)

print(f"\n   Municipality: {test_municipality['name']}")
print(f"   Risk Level: {test_municipality['riskLevel']}")
print(f"   Infected: {test_municipality['infectedDogs']} dogs, {test_municipality['infectedCats']} cats")
print(f"   Vaccinated: {test_municipality['vaccinatedDogs']} / {test_municipality['dogPopulation']} dogs")
print(f"\n   ✅ Recommended Vaccination: {recommendation['recommended_vaccination']*100:.0f}%")
print(f"   ✅ Confidence: {recommendation['confidence']*100:.0f}%")
print(f"   ✅ Source: {recommendation['source']}")
print(f"\n   Explanation: {recommendation['explanation']}")

print("\n" + "=" * 70)
print("✅ DRL Inference test completed!")
print("=" * 70)
