// Validation service for PAWPATROL

export const validateMunicipality = (municipality) => {
  const errors = {}
  
  // Name validation
  if (!municipality.name?.trim()) {
    errors.name = 'Municipality name is required'
  } else if (municipality.name.length < 2) {
    errors.name = 'Municipality name must be at least 2 characters'
  } else if (municipality.name.length > 50) {
    errors.name = 'Municipality name must be less than 50 characters'
  }
  
  // Coordinate validation for Davao de Oro region
  if (!municipality.latitude) {
    errors.latitude = 'Latitude is required'
  } else if (municipality.latitude < 6.5 || municipality.latitude > 8.5) {
    errors.latitude = 'Latitude must be between 6.5 and 8.5 for Davao de Oro region'
  }
  
  if (!municipality.longitude) {
    errors.longitude = 'Longitude is required'
  } else if (municipality.longitude < 124.5 || municipality.longitude > 127.5) {
    errors.longitude = 'Longitude must be between 124.5 and 127.5 for Davao de Oro region'
  }
  
  // Population validation
  if (!municipality.humanPopulation || municipality.humanPopulation < 1) {
    errors.humanPopulation = 'Human population must be at least 1'
  } else if (municipality.humanPopulation > 1000000) {
    errors.humanPopulation = 'Human population seems too large for a municipality'
  }
  
  if (!municipality.dogPopulation || municipality.dogPopulation < 1) {
    errors.dogPopulation = 'Dog population must be at least 1'
  } else if (municipality.dogPopulation > municipality.humanPopulation) {
    errors.dogPopulation = 'Dog population cannot exceed human population'
  }
  
  if (!municipality.catPopulation || municipality.catPopulation < 1) {
    errors.catPopulation = 'Cat population must be at least 1'
  } else if (municipality.catPopulation > municipality.humanPopulation) {
    errors.catPopulation = 'Cat population cannot exceed human population'
  }
  
  // Infection validation
  if (municipality.infectedDogs < 0) {
    errors.infectedDogs = 'Infected dogs cannot be negative'
  } else if (municipality.infectedDogs > municipality.dogPopulation) {
    errors.infectedDogs = 'Infected dogs cannot exceed total dog population'
  }
  
  if (municipality.infectedCats < 0) {
    errors.infectedCats = 'Infected cats cannot be negative'
  } else if (municipality.infectedCats > municipality.catPopulation) {
    errors.infectedCats = 'Infected cats cannot exceed total cat population'
  }
  
  if (municipality.infectedHumans < 0) {
    errors.infectedHumans = 'Infected humans cannot be negative'
  } else if (municipality.infectedHumans > municipality.humanPopulation) {
    errors.infectedHumans = 'Infected humans cannot exceed total human population'
  }
  
  // Vaccination validation
  if (municipality.vaccinatedDogs < 0) {
    errors.vaccinatedDogs = 'Vaccinated dogs cannot be negative'
  } else if (municipality.vaccinatedDogs > municipality.dogPopulation) {
    errors.vaccinatedDogs = 'Vaccinated dogs cannot exceed total dog population'
  }
  
  // Risk level validation
  const validRiskLevels = ['safe', 'low', 'moderate', 'high', 'critical']
  if (!validRiskLevels.includes(municipality.riskLevel)) {
    errors.riskLevel = 'Invalid risk level'
  }
  
  return {
    isValid: Object.keys(errors).length === 0,
    errors
  }
}

export const validateSimulationSettings = (settings) => {
  const errors = {}
  
  if (!settings.simulationDays || settings.simulationDays < 1) {
    errors.simulationDays = 'Simulation days must be at least 1'
  } else if (settings.simulationDays > 365) {
    errors.simulationDays = 'Simulation days cannot exceed 365'
  }
  
  if (settings.transmissionRate === null || settings.transmissionRate === undefined) {
    errors.transmissionRate = 'Transmission rate is required'
  } else if (settings.transmissionRate < 0 || settings.transmissionRate > 1) {
    errors.transmissionRate = 'Transmission rate must be between 0 and 1'
  }
  
  if (settings.vaccinationRate === null || settings.vaccinationRate === undefined) {
    errors.vaccinationRate = 'Vaccination efficiency is required'
  } else if (settings.vaccinationRate < 0 || settings.vaccinationRate > 1) {
    errors.vaccinationRate = 'Vaccination efficiency must be between 0 and 1'
  }
  
  if (settings.fractionalAlpha !== null && settings.fractionalAlpha !== undefined) {
    if (settings.fractionalAlpha < 0 || settings.fractionalAlpha > 1) {
      errors.fractionalAlpha = 'Fractional alpha must be between 0 and 1'
    }
  }
  
  if (settings.environmentalRandomness !== null && settings.environmentalRandomness !== undefined) {
    if (settings.environmentalRandomness < 0 || settings.environmentalRandomness > 1) {
      errors.environmentalRandomness = 'Environmental randomness must be between 0 and 1'
    }
  }
  
  const validSpeeds = [1, 2, 5, 10]
  if (settings.simulationSpeed && !validSpeeds.includes(settings.simulationSpeed)) {
    errors.simulationSpeed = 'Invalid simulation speed'
  }
  
  return {
    isValid: Object.keys(errors).length === 0,
    errors
  }
}

// Utility functions
export const generateMunicipalityId = () => {
  return Date.now().toString() + Math.random().toString(36).substr(2, 9)
}

export const calculateVaccinationCoverage = (municipality) => {
  if (!municipality.dogPopulation || municipality.dogPopulation === 0) return 0
  return Math.round((municipality.vaccinatedDogs / municipality.dogPopulation) * 100)
}

export const calculateInfectionRate = (municipality) => {
  const totalAnimals = municipality.dogPopulation + municipality.catPopulation
  const totalInfected = municipality.infectedDogs + municipality.infectedCats
  
  if (totalAnimals === 0) return 0
  return Math.round((totalInfected / totalAnimals) * 100)
}

export const assessRiskLevel = (municipality) => {
  const infectionRate = calculateInfectionRate(municipality)
  const vaccinationCoverage = calculateVaccinationCoverage(municipality)
  
  if (infectionRate === 0 && vaccinationCoverage >= 80) return 'safe'
  if (infectionRate <= 5 && vaccinationCoverage >= 60) return 'low'
  if (infectionRate <= 15 && vaccinationCoverage >= 40) return 'moderate'
  if (infectionRate <= 30) return 'high'
  return 'critical'
}