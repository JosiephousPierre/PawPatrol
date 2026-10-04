"""
Test DRL API Endpoints
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_drl_status():
    """Test DRL status endpoint"""
    print("\n" + "=" * 70)
    print("TEST 1: DRL Status Check")
    print("=" * 70)
    
    response = requests.get(f"{BASE_URL}/api/drl-status")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response.status_code == 200

def test_drl_recommendation():
    """Test DRL recommendation endpoint"""
    print("\n" + "=" * 70)
    print("TEST 2: DRL Recommendation")
    print("=" * 70)
    
    # Test data
    test_data = {
        "municipalities": [
            {
                "id": "1",
                "name": "Maco",
                "humanPopulation": 75033,
                "dogPopulation": 3000,
                "catPopulation": 1500,
                "infectedDogs": 15,
                "infectedCats": 3,
                "infectedHumans": 0,
                "vaccinatedDogs": 900,
                "populationDensity": 295.2,
                "latitude": 7.3667,
                "longitude": 126.0167,
                "riskLevel": "moderate",
                "connectedMunicipalities": ["2", "3"]
            },
            {
                "id": "2",
                "name": "Mawab",
                "humanPopulation": 36418,
                "dogPopulation": 1500,
                "catPopulation": 750,
                "infectedDogs": 8,
                "infectedCats": 2,
                "infectedHumans": 0,
                "vaccinatedDogs": 450,
                "populationDensity": 212.5,
                "riskLevel": "low",
                "connectedMunicipalities": ["1"]
            }
        ]
    }
    
    print("Sending request...")
    response = requests.post(
        f"{BASE_URL}/api/drl-recommend",
        json=test_data
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ Success: {result['success']}")
        print(f"DRL Available: {result['drl_available']}")
        print(f"Model Version: {result['model_version']}")
        print(f"\nRecommendations:")
        
        for rec in result['recommendations']:
            print(f"\n  Municipality: {rec['municipality_name']}")
            print(f"  Recommended Vaccination: {rec['recommended_vaccination']*100:.0f}%")
            print(f"  Confidence: {rec['confidence']*100:.0f}%")
            print(f"  Explanation: {rec['explanation']}")
    else:
        print(f"Error: {response.json()}")
    
    return response.status_code == 200

def main():
    """Run all tests"""
    print("=" * 70)
    print("DRL API ENDPOINT TESTS")
    print("=" * 70)
    print("\nMake sure the FastAPI server is running:")
    print("  python main.py")
    print("\nOr in another terminal:")
    print("  uvicorn main:app --reload")
    
    try:
        # Test DRL status
        status_ok = test_drl_status()
        
        # Test DRL recommendation
        recommend_ok = test_drl_recommendation()
        
        # Summary
        print("\n" + "=" * 70)
        print("TEST SUMMARY")
        print("=" * 70)
        print(f"DRL Status: {'✅ PASS' if status_ok else '❌ FAIL'}")
        print(f"DRL Recommendation: {'✅ PASS' if recommend_ok else '❌ FAIL'}")
        print("=" * 70)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to API")
        print("Please start the FastAPI server first:")
        print("  cd rabies-backend")
        print("  python main.py")

if __name__ == "__main__":
    main()
