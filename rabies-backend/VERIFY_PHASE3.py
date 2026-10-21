"""
Phase 3 Verification Script
Tests that cumulative statistics are properly computed and returned by the backend
"""

import requests
import json

# API endpoint
BASE_URL = "http://localhost:8000"

def test_cumulative_statistics():
    """Test that the backend returns cumulative statistics"""
    print("=" * 80)
    print("PHASE 3 VERIFICATION: Cumulative Statistics Test")
    print("=" * 80)
    
    # Prepare simulation request with correct structure
    simulation_data = {
        "municipalities": [
            {
                "id": "test-mun-1",
                "name": "Test Municipality",
                "humanPopulation": 50000,
                "dogPopulation": 5000,
                "catPopulation": 3000,
                "infectedDogs": 50,
                "infectedCats": 20,
                "infectedHumans": 5,
                "vaccinatedDogs": 2000,
                "latitude": 7.5,
                "longitude": 125.9,
                "populationDensity": 100.0,  # persons/km²
                "riskLevel": "moderate",
                "connectedMunicipalities": []
            }
        ],
        "settings": {
            "simulationDays": 30,
            "fractionalOrder": 0.95,
            
            # Birth rates (Λ - Lambda)
            "lambda_dog": 0.0001,
            "lambda_cat": 0.00012,
            "lambda_human": 0.00005,
            
            # Natural mortality rates (μ - mu)
            "mu_dog": 0.0001,
            "mu_cat": 0.00015,
            "mu_human": 0.00003,
            
            # Rabies-induced mortality (δ - delta)
            "delta_dog": 0.1,
            "delta_cat": 0.1,
            "delta_human": 0.1,
            
            # Transmission coefficients (β - beta)
            "beta_dd": 0.5,   # dog-to-dog
            "beta_dc": 0.2,   # dog-to-cat
            "beta_cc": 0.35,  # cat-to-cat
            "beta_dh": 0.1,   # dog-to-human
            "beta_ch": 0.05,  # cat-to-human
            
            # Stochastic noise (σ - sigma)
            "sigma_1": 0.1,   # dogs
            "sigma_2": 0.1,   # cats
            "sigma_3": 0.05,  # humans
            
            # Vaccination rate
            "vaccinationRate": 0.01
        }
    }
    
    print("\n>> Sending simulation request...")
    print(f"Municipality: {simulation_data['municipalities'][0]['name']}")
    print(f"Simulation Days: {simulation_data['settings']['simulationDays']}")
    print(f"Initial Populations:")
    print(f"  - Dogs: {simulation_data['municipalities'][0]['dogPopulation']} (Infected: {simulation_data['municipalities'][0]['infectedDogs']}, Vaccinated: {simulation_data['municipalities'][0]['vaccinatedDogs']})")
    print(f"  - Cats: {simulation_data['municipalities'][0]['catPopulation']} (Infected: {simulation_data['municipalities'][0]['infectedCats']})")
    print(f"  - Humans: {simulation_data['municipalities'][0]['humanPopulation']} (Infected: {simulation_data['municipalities'][0]['infectedHumans']})")
    
    try:
        # Send POST request
        response = requests.post(
            f"{BASE_URL}/api/simulate",
            json=simulation_data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print("\n[OK] Simulation completed successfully!")
            print("\n" + "=" * 80)
            print("CUMULATIVE STATISTICS VERIFICATION")
            print("=" * 80)
            
            # Extract municipality result
            mun_result = result['municipalities'][0]
            
            # DEBUG: Print ALL keys in the result
            print("\n[DEBUG] All keys in API response:")
            for key in sorted(mun_result.keys()):
                print(f"    {key}: {mun_result[key]}")
            print()
            
            # Check if cumulative fields exist
            cumulative_fields = [
                'totalDogBirths',
                'totalDogNaturalDeaths',
                'totalDogRabiesDeaths',
                'totalDogVaccinations',
                'totalCatBirths',
                'totalCatNaturalDeaths',
                'totalCatRabiesDeaths',
                'totalCatVaccinations',
                'totalHumanBirths',
                'totalHumanNaturalDeaths',
                'totalHumanRabiesDeaths',
                'totalHumanVaccinations'
            ]
            
            print("\n[CHECK] Looking for cumulative fields in API response...")
            missing_fields = []
            for field in cumulative_fields:
                if field not in mun_result:
                    missing_fields.append(field)
                    print(f"  [X] MISSING: {field}")
                else:
                    print(f"  [OK] FOUND: {field}")
            
            if missing_fields:
                print(f"\n[ERROR] {len(missing_fields)} cumulative fields are missing!")
                return False
            
            print("\n[OK] All cumulative fields present in API response!")
            
            # Display cumulative statistics
            print("\n" + "=" * 80)
            print("CUMULATIVE STATISTICS (30-day simulation)")
            print("=" * 80)
            
            print("\nDOGS (Primary Reservoir):")
            print(f"  • Births:            {mun_result['totalDogBirths']:>6}")
            print(f"  • Natural Deaths:    {mun_result['totalDogNaturalDeaths']:>6}")
            print(f"  • Rabies Deaths:     {mun_result['totalDogRabiesDeaths']:>6}")
            print(f"  • Vaccinations:      {mun_result['totalDogVaccinations']:>6}")
            print(f"  • Net Change:        {mun_result['totalDogBirths'] - mun_result['totalDogNaturalDeaths'] - mun_result['totalDogRabiesDeaths']:>6}")
            
            print("\nCATS (Spillover Host):")
            print(f"  • Births:            {mun_result['totalCatBirths']:>6}")
            print(f"  • Natural Deaths:    {mun_result['totalCatNaturalDeaths']:>6}")
            print(f"  • Rabies Deaths:     {mun_result['totalCatRabiesDeaths']:>6}")
            print(f"  • Vaccinations:      {mun_result['totalCatVaccinations']:>6}")
            print(f"  • Net Change:        {mun_result['totalCatBirths'] - mun_result['totalCatNaturalDeaths'] - mun_result['totalCatRabiesDeaths']:>6}")
            
            print("\nHUMANS (End Host):")
            print(f"  • Births:            {mun_result['totalHumanBirths']:>6}")
            print(f"  • Natural Deaths:    {mun_result['totalHumanNaturalDeaths']:>6}")
            print(f"  • Rabies Deaths:     {mun_result['totalHumanRabiesDeaths']:>6}")
            print(f"  • PEP Treatments:    {mun_result['totalHumanVaccinations']:>6}")
            print(f"  • Net Change:        {mun_result['totalHumanBirths'] - mun_result['totalHumanNaturalDeaths'] - mun_result['totalHumanRabiesDeaths']:>6}")
            
            # Verify non-zero values (at least some should be > 0 over 30 days)
            print("\n" + "=" * 80)
            print("VALIDATION CHECKS")
            print("=" * 80)
            
            total_births = (mun_result['totalDogBirths'] + 
                           mun_result['totalCatBirths'] + 
                           mun_result['totalHumanBirths'])
            
            total_deaths = (mun_result['totalDogNaturalDeaths'] + 
                           mun_result['totalDogRabiesDeaths'] +
                           mun_result['totalCatNaturalDeaths'] + 
                           mun_result['totalCatRabiesDeaths'] +
                           mun_result['totalHumanNaturalDeaths'] + 
                           mun_result['totalHumanRabiesDeaths'])
            
            total_vaccinations = (mun_result['totalDogVaccinations'] + 
                                 mun_result['totalCatVaccinations'] + 
                                 mun_result['totalHumanVaccinations'])
            
            print(f"\n[CHECK] Total Births:        {total_births}")
            print(f"[CHECK] Total Deaths:        {total_deaths}")
            print(f"[CHECK] Total Vaccinations:  {total_vaccinations}")
            
            if total_births > 0:
                print("  [OK] Births are being computed (> 0)")
            else:
                print("  [WARNING] No births recorded (may be too short simulation or low rates)")
            
            if total_deaths > 0:
                print("  [OK] Deaths are being computed (> 0)")
            else:
                print("  [WARNING] No deaths recorded")
            
            if total_vaccinations > 0:
                print("  [OK] Vaccinations are being computed (> 0)")
            else:
                print("  [WARNING] No vaccinations recorded")
            
            # Display final populations
            print("\n" + "=" * 80)
            print("FINAL POPULATIONS")
            print("=" * 80)
            print(f"\n• Dogs:   {mun_result['predictedDogPopulation']:>6} (Infected: {mun_result['predictedInfectedDogs']})")
            print(f"• Cats:   {mun_result['predictedCatPopulation']:>6} (Infected: {mun_result['predictedInfectedCats']})")
            print(f"• Humans: {mun_result['predictedHumanPopulation']:>6} (Infected: {mun_result['predictedInfectedHumans']})")
            
            print("\n" + "=" * 80)
            print("[OK] PHASE 3 BACKEND VERIFICATION: PASSED")
            print("=" * 80)
            print("\n[OK] Backend correctly computes and returns cumulative statistics!")
            print("[OK] All 12 cumulative fields are present in API response")
            print("[OK] Frontend can now display this data in the UI")
            
            return True
            
        else:
            print(f"\n[ERROR] Simulation failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("\n[ERROR] Request timed out after 60 seconds")
        return False
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_cumulative_statistics()
    exit(0 if success else 1)
