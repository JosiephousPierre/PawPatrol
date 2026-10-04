// Simulation Engine composable for PAWPATROL

import { ref, computed } from 'vue'
import { useAppStore } from '@/stores'
import { simulationLogger, LogSeverity } from '@/services/simulationLogger'
import { apiClient } from '@/services/apiClient'

export function useSimulationEngine() {
  const appStore = useAppStore()
  
  let simulationInterval = null
  let simulationStartTime = null
  
  const isRunning = computed(() => appStore.isSimulationRunning)
  const currentDay = computed(() => appStore.currentSimulationDay)
  
  // Simulation state
  const dailyResults = ref([])
  
  const startSimulation = async () => {
    if (appStore.isSimulationRunning) {
      throw new Error('Simulation is already running')
    }
    
    try {
      // Initialize simulation
      initializeSimulation()
      
      // Prepare settings first
      const settings = {
        simulationDays: appStore.simulationSettings.simulationDays,
        fractionalOrder: appStore.simulationSettings.fractionalOrder || 0.95,  // Use configured value, default 0.95
        transmissionRate: appStore.simulationSettings.transmissionRate,
        recoveryRate: 0.1,
        contactProbability: 0.3,
        stochasticIntensity: appStore.simulationSettings.environmentalRandomness || 0.1,  // Use configured uncertainty level
        vaccinationRate: appStore.simulationSettings.vaccinationRate || 0.0,
        enableAdaptiveVaccination: appStore.simulationSettings.enableAdaptiveVaccination
      }

      // Prepare data for backend with municipality-specific parameters
      const municipalities = appStore.municipalities.map(m => ({
        id: m.id,
        name: m.name,
        latitude: m.latitude,
        longitude: m.longitude,
        humanPopulation: m.humanPopulation,
        dogPopulation: m.dogPopulation,
        catPopulation: m.catPopulation,
        populationDensity: m.populationDensity || 100.0,
        infectedDogs: m.infectedDogs,
        infectedCats: m.infectedCats,
        infectedHumans: m.infectedHumans,
        vaccinatedDogs: m.vaccinatedDogs,
        riskLevel: m.riskLevel,
        connectedMunicipalities: m.connectedMunicipalities || [],
        // Municipality-specific parameters (use custom if available, otherwise global)
        customTransmissionRate: m.customTransmissionRate || settings.transmissionRate,
        customVaccinationRate: m.customVaccinationRate || settings.vaccinationRate,
        customEnvironmentalFactor: m.customEnvironmentalFactor || settings.environmentalRandomness,
        customContactMultiplier: m.customContactMultiplier || 1.0,
        hasCustomParameters: m.hasCustomParameters || false
      }))

      // Call backend API
      appStore.isSimulationRunning = true
      simulationLogger.addSimulationStateLog('started', { settings, municipalities: municipalities.length })

      console.log('🚀 Simulation: Calling backend API with data:', { 
        municipalityCount: municipalities.length, 
        settings,
        municipalitiesWithCustomParams: municipalities.filter(m => m.hasCustomParameters).length,
        firstMunicipality: municipalities[0], // See exact structure
        customParameterSample: municipalities.find(m => m.hasCustomParameters) || 'None'
      })

      const response = await apiClient.runSimulation(municipalities, settings)
      console.log('📊 Simulation: Backend response received:', response)
      
      if (response.success) {
        // Update municipalities with results, but preserve actual current data
        response.municipalities.forEach(result => {
          const municipality = appStore.municipalities.find(m => m.id === result.id)
          if (municipality) {
            // ✅ FIXED: Store predictions separately, don't overwrite actual current data
            municipality.predictedInfectedDogs = result.predictedInfectedDogs || 0
            municipality.predictedInfectedCats = result.predictedInfectedCats || 0
            municipality.predictedInfectedHumans = result.predictedInfectedHumans || 0
            
            // Keep actual current data unchanged
            // municipality.infectedDogs - NOT CHANGED (keeps user-entered value)
            // municipality.infectedCats - NOT CHANGED (keeps user-entered value)
            // municipality.infectedHumans - NOT CHANGED (keeps user-entered value)
            
            // Only update risk level if user didn't manually set it
            if (!municipality.userSetRiskLevel) {
              municipality.riskLevel = result.riskLevel
            }
            municipality.riskScore = result.riskScore
            
            // Calculate total predicted infected for easier access
            municipality.totalPredictedInfected = (result.predictedInfectedDogs || 0) + 
                                                  (result.predictedInfectedCats || 0) + 
                                                  (result.predictedInfectedHumans || 0)
          }
        })
        
        // Save results
        appStore.simulationResults = {
          dailyData: [{ day: settings.simulationDays, totalInfected: { dogs: 0, cats: 0, humans: 0 } }], // Mock data
          municipalities: response.municipalities,
          riskScores: response.riskScores,
          riskLevels: response.riskLevels,
          metadata: response.metadata
        }
        
        // DRL vaccination recommendations are now handled via API
        // Users can click "Get AI Recommendations" button on Results page
        // This uses the trained Deep Q-Network model via /api/drl-recommend endpoint
        
        simulationLogger.addSimulationStateLog('completed', { 
          model: response.metadata.model,
          formula: response.metadata.formula
        })
      } else {
        throw new Error('Simulation failed')
      }

      appStore.isSimulationRunning = false
      appStore.saveAllData()
      
    } catch (error) {
      appStore.isSimulationRunning = false
      simulationLogger.addSimulationStateLog('error', { error: error.message })
      throw error
    }
  }
  
  const pauseSimulation = () => {
    if (simulationInterval) {
      clearInterval(simulationInterval)
      simulationInterval = null
    }
    simulationLogger.addSimulationStateLog('paused', { day: appStore.currentSimulationDay })
  }
  
  const resumeSimulation = () => {
    if (!appStore.isSimulationRunning) return
    
    simulationInterval = setInterval(() => {
      runSimulationDay()
    }, getSimulationDelay())
    
    simulationLogger.addSimulationStateLog('resumed', { day: appStore.currentSimulationDay })
  }
  
  const stopSimulation = () => {
    if (simulationInterval) {
      clearInterval(simulationInterval)
      simulationInterval = null
    }
    
    appStore.isSimulationRunning = false
    
    // Save final results
    saveFinalResults()
    simulationLogger.addSimulationStateLog('stopped', { 
      day: appStore.currentSimulationDay,
      totalInfected: appStore.currentInfectedDogs + appStore.currentInfectedCats + appStore.currentInfectedHumans
    })
  }
  
  const resetSimulation = () => {
    stopSimulation()
    
    // Reset all simulation data
    appStore.currentSimulationDay = 0
    dailyResults.value = []
    simulationLogger.clearLogs()
    simulationLogger.setCurrentDay(0)
    
    // Reset municipality infection data to initial state
    const municipalities = appStore.municipalities.map(municipality => ({
      ...municipality,
      infectedDogs: municipality.id === '1' ? 12 : 0, // Only Maco starts with infection
      infectedCats: municipality.id === '1' ? 3 : 0,
      infectedHumans: 0,
      riskLevel: municipality.id === '1' ? 'moderate' : 'safe'
    }))
    
    appStore.municipalities = municipalities
    appStore.saveAllData()
    
    // Clear results
    appStore.simulationResults = {
      dailyData: [],
      infectionTrends: { dogs: [], cats: [], humans: [] },
      vaccinationCoverage: [],
      riskLevels: []
    }
    
    simulationLogger.addSimulationStateLog('reset', { municipalities: municipalities.length })
  }
  
  const initializeSimulation = () => {
    dailyResults.value = []
    simulationLogger.clearLogs()
    
    // Log initial state
    const totalInfected = appStore.currentInfectedDogs + appStore.currentInfectedCats + appStore.currentInfectedHumans
    simulationLogger.addOutbreakLog('Maco', totalInfected, 'animals')
    
    // Reset results structure
    appStore.simulationResults = {
      dailyData: [],
      infectionTrends: {
        dogs: [],
        cats: [],
        humans: []
      },
      vaccinationCoverage: [],
      riskLevels: [],
      logs: []
    }
  }
  
  const runSimulationDay = () => {
    const settings = appStore.simulationSettings
    const currentDay = appStore.currentSimulationDay
    
    // Update logger's current day
    simulationLogger.setCurrentDay(currentDay)
    
    // Check if simulation should end
    if (currentDay >= settings.simulationDays) {
      stopSimulation()
      simulationLogger.addSimulationStateLog('completed', { 
        totalDays: settings.simulationDays,
        finalInfected: appStore.currentInfectedDogs + appStore.currentInfectedCats + appStore.currentInfectedHumans
      })
      return
    }
    
    // Run transmission for this day
    const dayResults = processTransmissionDay(currentDay)
    
    // DRL recommendations are now available via API endpoint
    // Not applied automatically during simulation to give users control
    
    // Save daily results
    dailyResults.value.push(dayResults)
    
    // Update trends
    updateSimulationTrends(dayResults)
    
    // Advance to next day
    appStore.currentSimulationDay += 1
    
    // Save progress
    appStore.saveAllData()
  }
  
  const processTransmissionDay = (day) => {
    const settings = appStore.simulationSettings
    const municipalities = [...appStore.municipalities]
    
    const dayResults = {
      day,
      timestamp: new Date().toISOString(),
      transmissions: [],
      newInfections: { dogs: 0, cats: 0, humans: 0 },
      totalInfected: { dogs: 0, cats: 0, humans: 0 },
      riskChanges: []
    }
    
    // Process each municipality
    municipalities.forEach(municipality => {
      const municipalityResults = processMunicipalityTransmission(municipality, settings)
      
      // Apply results to municipality
      municipality.infectedDogs += municipalityResults.newInfectedDogs
      municipality.infectedCats += municipalityResults.newInfectedCats
      municipality.infectedHumans += municipalityResults.newInfectedHumans
      
      // Update risk level only if it wasn't manually set by user
      // Preserve user-set risk levels for new municipalities
      const newRiskLevel = calculateRiskLevel(municipality)
      if (newRiskLevel !== municipality.riskLevel && !municipality.userSetRiskLevel) {
        dayResults.riskChanges.push({
          municipalityId: municipality.id,
          municipalityName: municipality.name,
          oldRisk: municipality.riskLevel,
          newRisk: newRiskLevel
        })
        
        simulationLogger.addRiskChangeLog(municipality.name, municipality.riskLevel, newRiskLevel)
        municipality.riskLevel = newRiskLevel
      }
      
      // Log transmissions
      if (municipalityResults.newInfectedDogs > 0 || municipalityResults.newInfectedCats > 0) {
        const totalNew = municipalityResults.newInfectedDogs + municipalityResults.newInfectedCats
        simulationLogger.addLog(`${totalNew} new infections in ${municipality.name}`, LogSeverity.WARNING, municipality.id)
        
        dayResults.transmissions.push({
          municipalityId: municipality.id,
          municipalityName: municipality.name,
          newInfectedDogs: municipalityResults.newInfectedDogs,
          newInfectedCats: municipalityResults.newInfectedCats,
          newInfectedHumans: municipalityResults.newInfectedHumans
        })
      }
      
      // Accumulate totals
      dayResults.newInfections.dogs += municipalityResults.newInfectedDogs
      dayResults.newInfections.cats += municipalityResults.newInfectedCats
      dayResults.newInfections.humans += municipalityResults.newInfectedHumans
      
      dayResults.totalInfected.dogs += municipality.infectedDogs
      dayResults.totalInfected.cats += municipality.infectedCats
      dayResults.totalInfected.humans += municipality.infectedHumans
    })
    
    // Update store
    appStore.municipalities = municipalities
    
    // Log daily summary
    const totalNewInfections = dayResults.newInfections.dogs + dayResults.newInfections.cats + dayResults.newInfections.humans
    if (totalNewInfections > 0) {
      simulationLogger.addLog(`Day ${day} summary: ${totalNewInfections} total new infections`, LogSeverity.INFO)
    } else {
      simulationLogger.addLog(`Day ${day}: No new infections detected`, LogSeverity.SUCCESS)
    }
    
    return dayResults
  }
  
  const processMunicipalityTransmission = (municipality, settings) => {
    const results = {
      newInfectedDogs: 0,
      newInfectedCats: 0,
      newInfectedHumans: 0
    }
    
    // Base transmission probability
    const baseTransmissionRate = settings.transmissionRate
    const environmentalFactor = settings.environmentalRandomness
    
    // Calculate effective transmission rate with environmental randomness
    const randomFactor = 1 + (Math.random() - 0.5) * environmentalFactor
    const effectiveRate = baseTransmissionRate * randomFactor
    
    // Dog-to-dog transmission within municipality
    const susceptibleDogs = municipality.dogPopulation - municipality.infectedDogs - municipality.vaccinatedDogs
    if (susceptibleDogs > 0 && municipality.infectedDogs > 0) {
      const dogTransmissionProbability = effectiveRate * (municipality.infectedDogs / municipality.dogPopulation)
      const expectedNewDogInfections = susceptibleDogs * dogTransmissionProbability
      results.newInfectedDogs = Math.floor(Math.random() * expectedNewDogInfections * 2) // Poisson-like distribution
    }
    
    // Cat transmission (lower rate)
    const susceptibleCats = municipality.catPopulation - municipality.infectedCats
    if (susceptibleCats > 0 && municipality.infectedDogs > 0) {
      const catTransmissionProbability = effectiveRate * 0.6 * (municipality.infectedDogs / municipality.dogPopulation)
      const expectedNewCatInfections = susceptibleCats * catTransmissionProbability
      results.newInfectedCats = Math.floor(Math.random() * expectedNewCatInfections * 2)
    }
    
    // Human transmission (very low rate, only if many infected animals)
    const totalInfectedAnimals = municipality.infectedDogs + municipality.infectedCats
    if (totalInfectedAnimals > 5) {
      const humanTransmissionProbability = effectiveRate * 0.01 * (totalInfectedAnimals / (municipality.dogPopulation + municipality.catPopulation))
      if (Math.random() < humanTransmissionProbability) {
        results.newInfectedHumans = 1
      }
    }
    
    // Inter-municipality transmission
    if (municipality.connectedMunicipalities && municipality.connectedMunicipalities.length > 0) {
      municipality.connectedMunicipalities.forEach(connectedId => {
        const connectedMunicipality = appStore.municipalities.find(m => m.id === connectedId)
        if (connectedMunicipality && connectedMunicipality.infectedDogs > 0) {
          // Cross-municipality transmission (reduced rate)
          const crossTransmissionRate = effectiveRate * 0.3
          const susceptibleLocal = municipality.dogPopulation - municipality.infectedDogs - municipality.vaccinatedDogs
          
          if (susceptibleLocal > 0) {
            const crossInfectionProbability = crossTransmissionRate * (connectedMunicipality.infectedDogs / connectedMunicipality.dogPopulation)
            const expectedCrossInfections = susceptibleLocal * crossInfectionProbability * 0.1 // Lower cross-border rate
            const crossInfections = Math.floor(Math.random() * expectedCrossInfections * 2)
            
            if (crossInfections > 0) {
              results.newInfectedDogs += crossInfections
              simulationLogger.addTransmissionLog(connectedMunicipality.name, municipality.name, crossInfections, 'dogs')
            }
          }
        }
      })
    }
    
    // Ensure we don't exceed population limits
    results.newInfectedDogs = Math.min(results.newInfectedDogs, municipality.dogPopulation - municipality.infectedDogs - municipality.vaccinatedDogs)
    results.newInfectedCats = Math.min(results.newInfectedCats, municipality.catPopulation - municipality.infectedCats)
    results.newInfectedHumans = Math.min(results.newInfectedHumans, municipality.humanPopulation - municipality.infectedHumans)
    
    return results
  }
  
  const calculateRiskLevel = (municipality) => {
    const totalAnimals = municipality.dogPopulation + municipality.catPopulation
    const totalInfected = municipality.infectedDogs + municipality.infectedCats
    const infectionRate = totalAnimals > 0 ? (totalInfected / totalAnimals) * 100 : 0
    const vaccinationCoverage = municipality.dogPopulation > 0 ? (municipality.vaccinatedDogs / municipality.dogPopulation) * 100 : 0
    
    if (infectionRate === 0 && vaccinationCoverage >= 80) return 'safe'
    if (infectionRate <= 2 && vaccinationCoverage >= 60) return 'low'
    if (infectionRate <= 5 && vaccinationCoverage >= 40) return 'moderate'
    if (infectionRate <= 10) return 'high'
    return 'critical'
  }
  
  // Removed: applyVaccinationRecommendations()
  // DRL recommendations are now provided via API, users manually decide whether to apply them
  
  const updateSimulationTrends = (dayResults) => {
    if (!appStore.simulationResults.infectionTrends) {
      appStore.simulationResults.infectionTrends = { dogs: [], cats: [], humans: [] }
    }
    
    appStore.simulationResults.infectionTrends.dogs.push({
      day: dayResults.day,
      count: dayResults.totalInfected.dogs
    })
    
    appStore.simulationResults.infectionTrends.cats.push({
      day: dayResults.day,
      count: dayResults.totalInfected.cats
    })
    
    appStore.simulationResults.infectionTrends.humans.push({
      day: dayResults.day,
      count: dayResults.totalInfected.humans
    })
    
    // Add to daily data
    if (!appStore.simulationResults.dailyData) {
      appStore.simulationResults.dailyData = []
    }
    
    appStore.simulationResults.dailyData.push(dayResults)
  }
  
  const saveFinalResults = () => {
    appStore.simulationResults.logs = simulationLogger.logs
    appStore.simulationResults.completedAt = new Date().toISOString()
    appStore.simulationResults.duration = simulationStartTime ? Date.now() - simulationStartTime : 0
    appStore.simulationResults.statistics = simulationLogger.getStatistics()
    appStore.saveAllData()
  }
  
  const getSimulationDelay = () => {
    const speed = appStore.simulationSettings.simulationSpeed || 1
    const baseDelay = 1000 // 1 second per day at 1x speed
    return baseDelay / speed
  }
  
  return {
    // State
    isRunning,
    currentDay,
    dailyResults,
    
    // Methods
    startSimulation,
    pauseSimulation,
    resumeSimulation,
    stopSimulation,
    resetSimulation,
    
    // Getters
    getSimulationProgress: () => {
      const settings = appStore.simulationSettings
      return settings.simulationDays > 0 ? (appStore.currentSimulationDay / settings.simulationDays) * 100 : 0
    },
    
    // Logger access
    getSimulationLogs: () => simulationLogger.logs,
    searchLogs: (query, field) => simulationLogger.searchLogs(query, field),
    getLogStatistics: () => simulationLogger.getStatistics()
  }
}