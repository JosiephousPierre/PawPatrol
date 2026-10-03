import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { initializeDummyData, loadFromStorage, saveToStorage } from '@/services/localStorage'
import { useMunicipalityAuth } from '@/services/municipalityAuth'

export const useAppStore = defineStore('app', () => {
  const { currentMunicipality, hasPermission, canAccessMunicipalityData } = useMunicipalityAuth()
  
  // State
  const municipalities = ref([])
  const municipalityData = ref({}) // Municipality-scoped data storage
  const simulationSettings = ref({})
  const simulationResults = ref({})
  const vaccinationRecommendations = ref([])
  const isSimulationRunning = ref(false)
  const currentSimulationDay = ref(0)

  // Computed - Municipality-aware
  const totalMunicipalities = computed(() => {
    if (hasPermission('view_all_data')) {
      return municipalities.value.length
    }
    return 1 // Current municipality only
  })
  
  const ownMunicipalityData = computed(() => {
    if (!currentMunicipality.value) return null
    return municipalities.value.find(m => m.id === currentMunicipality.value.id)
  })
  
  const totalDogPopulation = computed(() => {
    if (hasPermission('view_all_data')) {
      return municipalities.value.reduce((sum, m) => sum + (m.dogPopulation || 0), 0)
    }
    return ownMunicipalityData.value?.dogPopulation || 0
  })
  
  const totalCatPopulation = computed(() => {
    if (hasPermission('view_all_data')) {
      return municipalities.value.reduce((sum, m) => sum + (m.catPopulation || 0), 0)
    }
    return ownMunicipalityData.value?.catPopulation || 0
  })
  
  const totalHumanPopulation = computed(() => {
    if (hasPermission('view_all_data')) {
      return municipalities.value.reduce((sum, m) => sum + (m.humanPopulation || 0), 0)
    }
    return ownMunicipalityData.value?.humanPopulation || 0
  })
  
  const currentInfectedDogs = computed(() => {
    if (hasPermission('view_all_data')) {
      return municipalities.value.reduce((sum, m) => sum + (m.infectedDogs || 0), 0)
    }
    return ownMunicipalityData.value?.infectedDogs || 0
  })
  
  const currentInfectedCats = computed(() => {
    if (hasPermission('view_all_data')) {
      return municipalities.value.reduce((sum, m) => sum + (m.infectedCats || 0), 0)
    }
    return ownMunicipalityData.value?.infectedCats || 0
  })
  
  const currentInfectedHumans = computed(() => {
    if (hasPermission('view_all_data')) {
      return municipalities.value.reduce((sum, m) => sum + (m.infectedHumans || 0), 0)
    }
    return ownMunicipalityData.value?.infectedHumans || 0
  })

  // Actions - Municipality-aware
  const initializeApp = () => {
    const data = loadFromStorage()
    
    if (!data.municipalities || data.municipalities.length === 0) {
      const dummyData = initializeDummyData()
      municipalities.value = dummyData.municipalities
      simulationSettings.value = dummyData.simulationSettings
      simulationResults.value = dummyData.simulationResults
      vaccinationRecommendations.value = dummyData.vaccinationRecommendations
      saveAllData()
    } else {
      municipalities.value = data.municipalities
      simulationSettings.value = data.simulationSettings
      simulationResults.value = data.simulationResults
      vaccinationRecommendations.value = data.vaccinationRecommendations
      municipalityData.value = data.municipalityData || {}
    }
  }

  const saveAllData = () => {
    saveToStorage({
      municipalities: municipalities.value,
      municipalityData: municipalityData.value,
      simulationSettings: simulationSettings.value,
      simulationResults: simulationResults.value,
      vaccinationRecommendations: vaccinationRecommendations.value
    })
  }

  const addMunicipality = (municipality) => {
    // Only admin can add new municipalities
    if (!hasPermission('view_all_data')) {
      throw new Error('Insufficient permissions to add municipalities')
    }
    
    municipality.id = Date.now().toString()
    municipalities.value.push(municipality)
    console.log('🏙️ Added municipality:', municipality.name, 'Total municipalities:', municipalities.value.length)
    saveAllData()
  }

  const updateMunicipality = (id, updatedMunicipality) => {
    // Check if user can update this municipality
    if (!canAccessMunicipalityData(id)) {
      throw new Error('Insufficient permissions to update this municipality')
    }
    
    const index = municipalities.value.findIndex(m => m.id === id)
    if (index !== -1) {
      municipalities.value[index] = { ...municipalities.value[index], ...updatedMunicipality }
      saveAllData()
    }
  }

  const deleteMunicipality = (id) => {
    // Only admin can delete municipalities
    if (!hasPermission('view_all_data')) {
      throw new Error('Insufficient permissions to delete municipalities')
    }
    
    municipalities.value = municipalities.value.filter(m => m.id !== id)
    saveAllData()
  }

  const updateOwnMunicipalityData = (data) => {
    if (!currentMunicipality.value) {
      throw new Error('No municipality context available')
    }
    
    const municipalityId = currentMunicipality.value.id
    
    // Find and update own municipality
    const index = municipalities.value.findIndex(m => m.id === municipalityId)
    if (index !== -1) {
      municipalities.value[index] = { ...municipalities.value[index], ...data }
      saveAllData()
    }
  }

  const getMunicipalityData = (id) => {
    if (!canAccessMunicipalityData(id)) {
      return null // Return null for inaccessible data
    }
    
    return municipalities.value.find(m => m.id === id)
  }

  const getVisibleMunicipalities = () => {
    if (hasPermission('view_all_data')) {
      return municipalities.value
    }
    
    // Return only own municipality for regular users
    return ownMunicipalityData.value ? [ownMunicipalityData.value] : []
  }

  const updateSimulationSettings = (settings) => {
    simulationSettings.value = { ...simulationSettings.value, ...settings }
    saveAllData()
  }

  const resetToDefaults = () => {
    const dummyData = initializeDummyData()
    municipalities.value = dummyData.municipalities
    simulationSettings.value = dummyData.simulationSettings
    simulationResults.value = dummyData.simulationResults
    vaccinationRecommendations.value = dummyData.vaccinationRecommendations
    currentSimulationDay.value = 0
    isSimulationRunning.value = false
    saveAllData()
  }

  const setSimulationRunning = (running) => {
    isSimulationRunning.value = running
  }

  const setCurrentSimulationDay = (day) => {
    currentSimulationDay.value = day
  }

  const clearSimulationData = () => {
    simulationResults.value = {}
    vaccinationRecommendations.value = []
    currentSimulationDay.value = 0
    isSimulationRunning.value = false
    saveAllData()
  }

  return {
    // State
    municipalities,
    simulationSettings,
    simulationResults,
    vaccinationRecommendations,
    isSimulationRunning,
    currentSimulationDay,
    
    // Computed
    totalMunicipalities,
    totalDogPopulation,
    totalCatPopulation,
    totalHumanPopulation,
    currentInfectedDogs,
    currentInfectedCats,
    currentInfectedHumans,
    ownMunicipalityData,
    
    // Actions
    initializeApp,
    saveAllData,
    addMunicipality,
    updateMunicipality,
    deleteMunicipality,
    updateOwnMunicipalityData,
    getMunicipalityData,
    getVisibleMunicipalities,
    updateSimulationSettings,
    resetToDefaults,
    setSimulationRunning,
    setCurrentSimulationDay,
    clearSimulationData
  }
})