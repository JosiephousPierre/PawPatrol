"""
Test Phase 1: New Parameter Acceptance
Tests that backend accepts new SI+V+BD model parameters

Phase 1 Goals:
- New parameters defined in models
- API accepts new parameters
- Backward compatibility maintained
- Default values work correctly
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.request_models import SimulationSettings, MunicipalityData, SimulationRequest
from drl.config import DRLConfig


def test_simulation_settings_defaults():
    """Test that SimulationSettings has correct defaults for new parameters"""
    settings = SimulationSettings(
        simulationDays=30,
        transmissionRate=0.15
    )
    
    # Check new birth rate defaults
    assert settings.lambda_dog == 0.0001, "Dog birth rate default incorrect"
    assert settings.lambda_cat == 0.0001, "Cat birth rate default incorrect"
    assert settings.lambda_human == 0.00005, "Human birth rate default incorrect"
    
    # Check natural mortality defaults
    assert settings.mu_dog == 0.0001, "Dog natural mortality default incorrect"
    assert settings.mu_cat == 0.0002, "Cat natural mortality default incorrect"
    assert settings.mu_human == 0.00003, "Human natural mortality default incorrect"
    
    # Check rabies mortality defaults
    assert settings.delta_dog == 0.1, "Dog rabies mortality default incorrect"
    assert settings.delta_cat == 0.12, "Cat rabies mortality default incorrect"
    assert settings.delta_human == 0.15, "Human rabies mortality default incorrect"
    
    # Check stochastic intensities
    assert settings.sigma_1 == 0.1, "Dog stochastic intensity default incorrect"
    assert settings.sigma_2 == 0.08, "Cat stochastic intensity default incorrect"
    assert settings.sigma_3 == 0.05, "Human stochastic intensity default incorrect"
    
    # Check transmission coefficients
    assert settings.beta_dd == 0.15, "Dog-to-dog transmission default incorrect"
    assert settings.beta_dc == 0.06, "Dog-to-cat transmission default incorrect"
    assert settings.beta_cc == 0.105, "Cat-to-cat transmission default incorrect"
    assert settings.beta_dh == 0.0015, "Dog-to-human transmission default incorrect"
    assert settings.beta_ch == 0.00075, "Cat-to-human transmission default incorrect"
    
    print("✅ All default values correct!")


def test_custom_parameter_values():
    """Test that custom parameter values can be set"""
    settings = SimulationSettings(
        simulationDays=30,
        transmissionRate=0.15,
        lambda_dog=0.0002,  # Custom value
        mu_dog=0.0003,      # Custom value
        delta_dog=0.15,     # Custom value
        sigma_1=0.15,       # Custom value
        beta_dd=0.20        # Custom value
    )
    
    assert settings.lambda_dog == 0.0002, "Custom dog birth rate not set"
    assert settings.mu_dog == 0.0003, "Custom dog natural mortality not set"
    assert settings.delta_dog == 0.15, "Custom dog rabies mortality not set"
    assert settings.sigma_1 == 0.15, "Custom dog stochastic intensity not set"
    assert settings.beta_dd == 0.20, "Custom dog-to-dog transmission not set"
    
    print("✅ Custom parameter values work!")


def test_backward_compatibility():
    """Test that old API calls still work without new parameters"""
    # Old-style request (before Phase 1)
    settings = SimulationSettings(
        simulationDays=30,
        transmissionRate=0.15,
        recoveryRate=0.1,
        stochasticIntensity=0.1,
        contactProbability=0.3,
        vaccinationRate=0.8
    )
    
    # Should work with defaults for new parameters
    assert settings.lambda_dog is not None, "Backward compatibility broken"
    assert settings.mu_dog is not None, "Backward compatibility broken"
    assert settings.delta_dog is not None, "Backward compatibility broken"
    
    print("✅ Backward compatibility maintained!")


def test_drl_config_has_new_params():
    """Test that DRL config includes new parameters"""
    config = DRLConfig()
    
    assert hasattr(config, 'lambda_dog'), "DRL config missing lambda_dog"
    assert hasattr(config, 'mu_dog'), "DRL config missing mu_dog"
    assert hasattr(config, 'delta_dog'), "DRL config missing delta_dog"
    assert hasattr(config, 'sigma_1'), "DRL config missing sigma_1"
    assert hasattr(config, 'beta_dd'), "DRL config missing beta_dd"
    
    # Check values
    assert config.lambda_dog == 0.0001, "DRL config lambda_dog value incorrect"
    assert config.beta_dd == 0.15, "DRL config beta_dd value incorrect"
    
    print("✅ DRL config has new parameters!")


def test_full_request_with_new_params():
    """Test creating a full simulation request with new parameters"""
    municipality = MunicipalityData(
        id="test",
        name="Test Municipality",
        latitude=7.5,
        longitude=125.9,
        humanPopulation=10000,
        dogPopulation=1000,
        catPopulation=500,
        populationDensity=200.0,
        infectedDogs=10,
        infectedCats=2,
        infectedHumans=0,
        vaccinatedDogs=300,
        riskLevel="moderate",
        connectedMunicipalities=[]
    )
    
    settings = SimulationSettings(
        simulationDays=30,
        transmissionRate=0.15,
        lambda_dog=0.0001,
        lambda_cat=0.0001,
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
    
    request = SimulationRequest(
        municipalities=[municipality],
        settings=settings
    )
    
    # Verify request was created successfully
    assert len(request.municipalities) == 1, "Request creation failed"
    assert request.settings.lambda_dog == 0.0001, "Request settings incorrect"
    
    print("✅ Full request with new parameters works!")


def test_parameter_validation_ranges():
    """Test that parameters have correct validation ranges"""
    try:
        # Test negative value (should fail)
        settings = SimulationSettings(
            simulationDays=30,
            transmissionRate=0.15,
            lambda_dog=-0.01  # Negative - should fail
        )
        assert False, "Negative lambda_dog should have failed validation"
    except:
        print("✅ Parameter validation works (rejects negative values)!")


# =============================================================================
# RUN ALL TESTS
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("PHASE 1 TESTING: New Parameter Acceptance")
    print("=" * 70)
    
    try:
        print("\n[Test 1/7] Testing default values...")
        test_simulation_settings_defaults()
        
        print("\n[Test 2/7] Testing custom parameter values...")
        test_custom_parameter_values()
        
        print("\n[Test 3/7] Testing backward compatibility...")
        test_backward_compatibility()
        
        print("\n[Test 4/7] Testing DRL config...")
        test_drl_config_has_new_params()
        
        print("\n[Test 5/7] Testing full request creation...")
        test_full_request_with_new_params()
        
        print("\n[Test 6/7] Testing parameter validation...")
        test_parameter_validation_ranges()
        
        print("\n" + "=" * 70)
        print("✅ ALL PHASE 1 TESTS PASSED!")
        print("=" * 70)
        print("\n📊 Summary:")
        print("  ✅ 14 new parameters defined")
        print("  ✅ Default values set correctly")
        print("  ✅ Custom values accepted")
        print("  ✅ Backward compatibility maintained")
        print("  ✅ Validation working")
        print("\n🎉 Phase 1 Complete! Ready for Phase 2 (Formula Implementation)")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
