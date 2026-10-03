// Local Storage Service for PAWPATROL

const STORAGE_KEYS = {
  MUNICIPALITIES: 'pawpatrol_municipalities',
  SIMULATION_SETTINGS: 'pawpatrol_simulation_settings',
  SIMULATION_RESULTS: 'pawpatrol_simulation_results',
  VACCINATION_RECOMMENDATIONS: 'pawpatrol_vaccination_recommendations'
}

export const loadFromStorage = () => {
  try {
    return {
      municipalities: JSON.parse(localStorage.getItem(STORAGE_KEYS.MUNICIPALITIES)) || [],
      simulationSettings: JSON.parse(localStorage.getItem(STORAGE_KEYS.SIMULATION_SETTINGS)) || {},
      simulationResults: JSON.parse(localStorage.getItem(STORAGE_KEYS.SIMULATION_RESULTS)) || {},
      vaccinationRecommendations: JSON.parse(localStorage.getItem(STORAGE_KEYS.VACCINATION_RECOMMENDATIONS)) || []
    }
  } catch (error) {
    console.error('Error loading from localStorage:', error)
    return {
      municipalities: [],
      simulationSettings: {},
      simulationResults: {},
      vaccinationRecommendations: []
    }
  }
}

export const saveToStorage = (data) => {
  try {
    if (data.municipalities) {
      localStorage.setItem(STORAGE_KEYS.MUNICIPALITIES, JSON.stringify(data.municipalities))
    }
    if (data.simulationSettings) {
      localStorage.setItem(STORAGE_KEYS.SIMULATION_SETTINGS, JSON.stringify(data.simulationSettings))
    }
    if (data.simulationResults) {
      localStorage.setItem(STORAGE_KEYS.SIMULATION_RESULTS, JSON.stringify(data.simulationResults))
    }
    if (data.vaccinationRecommendations) {
      localStorage.setItem(STORAGE_KEYS.VACCINATION_RECOMMENDATIONS, JSON.stringify(data.vaccinationRecommendations))
    }
  } catch (error) {
    console.error('Error saving to localStorage:', error)
  }
}

export const initializeDummyData = () => {
  const municipalities = [
    {
      id: 'maco',
      name: 'Maco',
      latitude: 7.3617,
      longitude: 125.8550,
      connectedMunicipalities: ['mawab', 'laak'],
      dogPopulation: 1500,
      catPopulation: 800,
      humanPopulation: 87680,
      infectedDogs: 12,
      infectedCats: 3,
      infectedHumans: 0,
      vaccinatedDogs: 450,
      riskLevel: 'moderate',
      populationDensity: 295.2,
      lastUpdated: null
    },
    {
      id: 'mawab',
      name: 'Mawab',
      latitude: 7.4833,
      longitude: 125.9167,
      connectedMunicipalities: ['maco', 'mabini'],
      dogPopulation: 1200,
      catPopulation: 650,
      humanPopulation: 41050,
      infectedDogs: 0,
      infectedCats: 0,
      infectedHumans: 0,
      vaccinatedDogs: 360,
      riskLevel: 'safe',
      populationDensity: 212.5,
      lastUpdated: null
    },
    {
      id: 'nabunturan',
      name: 'Nabunturan',
      latitude: 7.6078,
      longitude: 125.9664,
      connectedMunicipalities: ['maco', 'pantukan', 'monkayo'],
      dogPopulation: 2000,
      catPopulation: 1100,
      humanPopulation: 85949,
      infectedDogs: 0,
      infectedCats: 0,
      infectedHumans: 0,
      vaccinatedDogs: 600,
      riskLevel: 'safe',
      populationDensity: 283.8,
      lastUpdated: null
    },
    {
      id: 'pantukan',
      name: 'Pantukan',
      latitude: 7.127024,
      longitude: 125.897221,
      connectedMunicipalities: ['nabunturan', 'new-bataan', 'mabini'],
      dogPopulation: 1800,
      catPopulation: 950,
      humanPopulation: 91312,
      infectedDogs: 0,
      infectedCats: 0,
      infectedHumans: 0,
      vaccinatedDogs: 540,
      riskLevel: 'safe',
      populationDensity: 178.3,
      lastUpdated: null
    },
    {
      id: 'monkayo',
      name: 'Monkayo',
      latitude: 7.8150,
      longitude: 126.0556,
      connectedMunicipalities: ['nabunturan', 'compostela', 'montevista'],
      dogPopulation: 1400,
      catPopulation: 720,
      humanPopulation: 96405,
      infectedDogs: 0,
      infectedCats: 0,
      infectedHumans: 0,
      vaccinatedDogs: 420,
      riskLevel: 'safe',
      populationDensity: 124.7,
      lastUpdated: null
    },
    {
      id: 'new-bataan',
      name: 'New Bataan',
      latitude: 7.5467,
      longitude: 126.1167,
      connectedMunicipalities: ['pantukan', 'montevista'],
      dogPopulation: 1100,
      catPopulation: 580,
      humanPopulation: 50212,
      infectedDogs: 0,
      infectedCats: 0,
      infectedHumans: 0,
      vaccinatedDogs: 330,
      riskLevel: 'safe',
      populationDensity: 98.5,
      lastUpdated: null
    },
    {
      id: 'compostela',
      name: 'Compostela',
      latitude: 7.6740,
      longitude: 126.0880,
      connectedMunicipalities: ['monkayo', 'montevista'],
      dogPopulation: 1600,
      catPopulation: 850,
      humanPopulation: 89224,
      infectedDogs: 0,
      infectedCats: 0,
      infectedHumans: 0,
      vaccinatedDogs: 480,
      riskLevel: 'safe',
      populationDensity: 226.4,
      lastUpdated: null
    },
    {
      id: 'montevista',
      name: 'Montevista',
      latitude: 7.6956,
      longitude: 125.9889,
      connectedMunicipalities: ['monkayo', 'new-bataan', 'compostela'],
      dogPopulation: 900,
      catPopulation: 450,
      humanPopulation: 46581,
      infectedDogs: 0,
      infectedCats: 0,
      infectedHumans: 0,
      vaccinatedDogs: 270,
      riskLevel: 'safe',
      populationDensity: 187.9,
      lastUpdated: null
    },
    {
      id: 'laak',
      name: 'Laak',
      latitude: 7.818876,
      longitude: 125.792067,
      connectedMunicipalities: ['maco', 'maragusan'],
      dogPopulation: 1300,
      catPopulation: 700,
      humanPopulation: 83632,
      infectedDogs: 0,
      infectedCats: 0,
      infectedHumans: 0,
      vaccinatedDogs: 390,
      riskLevel: 'safe',
      populationDensity: 92.8,
      lastUpdated: null
    },
    {
      id: 'maragusan',
      name: 'Maragusan',
      latitude: 7.316616,
      longitude: 126.123625,
      connectedMunicipalities: ['laak', 'mabini'],
      dogPopulation: 1100,
      catPopulation: 600,
      humanPopulation: 67759,
      infectedDogs: 0,
      infectedCats: 0,
      infectedHumans: 0,
      vaccinatedDogs: 330,
      riskLevel: 'safe',
      populationDensity: 71.2,
      lastUpdated: null
    },
    {
      id: 'mabini',
      name: 'Mabini',
      latitude: 7.3097,
      longitude: 125.8539,
      connectedMunicipalities: ['mawab', 'pantukan', 'maragusan'],
      dogPopulation: 950,
      catPopulation: 500,
      humanPopulation: 43971,
      infectedDogs: 0,
      infectedCats: 0,
      infectedHumans: 0,
      vaccinatedDogs: 285,
      riskLevel: 'safe',
      populationDensity: 156.3,
      lastUpdated: null
    }
  ]

  const simulationSettings = {
    simulationDays: 30,
    transmissionRate: 0.15,
    vaccinationRate: 0.8,
    fractionalAlpha: 0.3,
    environmentalRandomness: 0.2,
    simulationSpeed: 1,
    enableAdaptiveVaccination: true
  }

  const simulationResults = {
    dailyData: [],
    infectionTrends: {
      dogs: [],
      cats: [],
      humans: []
    },
    vaccinationCoverage: [],
    riskLevels: []
  }

  const vaccinationRecommendations = [
    {
      municipalityId: '1',
      municipalityName: 'Maco',
      recommendedVaccinationPercentage: 90,
      priority: 'High',
      reason: 'Active outbreak detected with 12 infected dogs',
      timestamp: new Date().toISOString()
    }
  ]

  return {
    municipalities,
    simulationSettings,
    simulationResults,
    vaccinationRecommendations
  }
}