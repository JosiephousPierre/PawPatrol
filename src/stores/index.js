import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { initializeDummyData, loadFromStorage, saveToStorage, updateRegionalRiskFromManagement } from '@/services/localStorage'
import { useMunicipalityAuth } from '@/services/municipalityAuth'
import { mergeWithRegionalRiskData, getRegionalRiskSummary, onRegionalRiskDataChange, clearRegionalRiskData } from '@/services/regionalRiskSync'

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

  // Set up cross-tab synchronization for regional risk data
  const setupCrossTabSync = () => {
    // Listen for changes to regional risk data from other tabs/municipalities
    const cleanup = onRegionalRiskDataChange(() => {
      console.log('🔄 [STORE] onRegionalRiskDataChange callback triggered')
      console.log('🔄 [STORE] Current municipalities before merge:', municipalities.value.length)
      
      if (municipalities.value.length === 0) {
        console.log('⚠️ [STORE] No municipalities yet, skipping merge')
        return
      }
      
      // Merge the updated regional data with our municipalities
      const oldData = municipalities.value[0] ? JSON.parse(JSON.stringify(municipalities.value[0])) : null
      const mergedData = mergeWithRegionalRiskData(municipalities.value)
      
      console.log('🔄 [STORE] First municipality BEFORE merge:', oldData)
      console.log('🔄 [STORE] First municipality AFTER merge:', mergedData[0])
      
      // 🔥 CRITICAL: Replace the entire array to trigger Vue reactivity
      municipalities.value = [...mergedData]
      
      console.log('✅ [STORE] Municipalities array replaced - Vue watch should trigger now')
    })
    
    // Note: Cleanup not called because Pinia stores are singletons
    // The listener will remain active for the app lifetime
    return cleanup
  }
  
  // Start listening for cross-tab changes when store is created
  setupCrossTabSync()

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
    // 🔥 CRITICAL: Clear regional storage on first run to remove dummy data
    // Regional storage should ONLY contain real user-saved data from Municipality Management
    const regionalStorageCleared = localStorage.getItem('pawpatrol_regional_cleared')
    if (!regionalStorageCleared) {
      console.log('🧹 Clearing regional storage (first run - removing dummy data)')
      clearRegionalRiskData()
      localStorage.setItem('pawpatrol_regional_cleared', 'true')
    }
    
    const data = loadFromStorage()
    
    if (!data.municipalities || data.municipalities.length === 0) {
      console.log('🆕 No local data found, initializing with dummy data...')
      const dummyData = initializeDummyData()
      municipalities.value = dummyData.municipalities
      simulationSettings.value = dummyData.simulationSettings
      simulationResults.value = dummyData.simulationResults
      vaccinationRecommendations.value = dummyData.vaccinationRecommendations
      saveAllData()
      
      // 🔥 Mark all dummy municipalities as NOT having regional data
      municipalities.value = municipalities.value.map(m => ({
        ...m,
        hasRegionalData: false  // Dummy data flag
      }))
      
      console.log('⚠️ Dummy data loaded locally but NOT synced to regional storage')
    } else {
      console.log('📂 Loading existing data from storage...')
      municipalities.value = data.municipalities
      simulationSettings.value = data.simulationSettings
      simulationResults.value = data.simulationResults
      vaccinationRecommendations.value = data.vaccinationRecommendations
      municipalityData.value = data.municipalityData || {}
    }
  }

  const saveAllData = () => {
    console.log('💾 Saving all data (without regional risk sync)...')
    
    saveToStorage({
      municipalities: municipalities.value,
      municipalityData: municipalityData.value,
      simulationSettings: simulationSettings.value,
      simulationResults: simulationResults.value,
      vaccinationRecommendations: vaccinationRecommendations.value
    })
    
    console.log('✅ Data saved')
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
      
      // ✅ SYNC TO REGIONAL RISK MAP
      // When Municipality Management saves baseline data, sync it to Regional Risk Map
      // so all municipalities see the updated baseline (not simulation predictions)
      syncRegionalRiskFromManagement()
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

  // NEW: Refresh regional risk data
  // This allows any municipality to see the latest risk levels from all municipalities
  const refreshRegionalRiskData = () => {
    console.log('🔄 Refreshing regional risk data...')
    
    // Merge current municipalities with latest regional risk data
    municipalities.value = mergeWithRegionalRiskData(municipalities.value)
    
    console.log('✅ Regional risk data refreshed')
  }

  // NEW: Get regional risk summary statistics
  const regionalRiskSummary = computed(() => {
    return getRegionalRiskSummary()
  })

  // NEW: Sync regional risk data from Municipality Management saves
  // This ensures Regional Risk Map shows baseline data, not simulation predictions
  const syncRegionalRiskFromManagement = () => {
    console.log('📍 syncRegionalRiskFromManagement() called')
    console.log('📍 Current municipalities count:', municipalities.value.length)
    console.log('📍 Sample municipality:', municipalities.value[0])
    updateRegionalRiskFromManagement(municipalities.value)
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
    clearSimulationData,
    refreshRegionalRiskData,
    regionalRiskSummary
  }
})