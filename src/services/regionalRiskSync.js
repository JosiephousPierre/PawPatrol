/**
 * Regional Risk Data Synchronization Service
 * 
 * This service maintains a centralized, shared regional risk map
 * that is visible to all municipalities.
 * 
 * Purpose: Fix the issue where each municipality's risk level updates
 * are only visible in their own session. With this service, when MACO
 * runs a simulation and their risk level changes to "moderate", ALL
 * other municipalities will see MACO as "moderate" on their regional map.
 * 
 * Implementation: Uses a shared localStorage key that all users read/write
 */

const REGIONAL_RISK_KEY = 'pawpatrol_regional_risk_data'

// Custom event name for same-tab synchronization
const REGIONAL_RISK_UPDATE_EVENT = 'pawpatrol_regional_risk_updated'

/**
 * Update the centralized regional risk data
 * Called whenever a municipality's data changes (after simulation, etc.)
 * 
 * @param {Array} municipalities - Current municipality data
 */
export const updateRegionalRiskData = (municipalities) => {
  try {
    // Load existing regional data
    const existingData = loadRegionalRiskData()
    
    // Extract only the risk-related fields we want to share
    const riskUpdates = municipalities.map(mun => ({
      id: mun.id,
      name: mun.name,
      riskLevel: mun.riskLevel || 'safe',
      infectedDogs: mun.infectedDogs || 0,
      infectedCats: mun.infectedCats || 0,
      infectedHumans: mun.infectedHumans || 0,
      vaccinatedDogs: mun.vaccinatedDogs || 0,
      lastUpdated: new Date().toISOString(),
      // Include simulation results if available
      predictedInfectedDogs: mun.predictedInfectedDogs,
      predictedInfectedCats: mun.predictedInfectedCats,
      predictedInfectedHumans: mun.predictedInfectedHumans
    }))
    
    // Merge with existing data (keep latest update per municipality)
    const merged = { ...existingData }
    riskUpdates.forEach(update => {
      const existing = merged[update.id]
      // Only update if this is newer or doesn't exist
      if (!existing || new Date(update.lastUpdated) > new Date(existing.lastUpdated)) {
        merged[update.id] = update
      }
    })
    
    // Save to centralized storage
    localStorage.setItem(REGIONAL_RISK_KEY, JSON.stringify(merged))
    
    console.log('✅ Regional risk data updated:', Object.keys(merged).length, 'municipalities')
    
    // Dispatch custom event for same-tab updates (localStorage events don't fire in same tab)
    window.dispatchEvent(new CustomEvent(REGIONAL_RISK_UPDATE_EVENT, { 
      detail: merged 
    }))
    
  } catch (error) {
    console.error('❌ Error updating regional risk data:', error)
  }
}

/**
 * Load the centralized regional risk data
 * 
 * @returns {Object} Map of municipality ID to risk data
 */
export const loadRegionalRiskData = () => {
  try {
    const data = localStorage.getItem(REGIONAL_RISK_KEY)
    return data ? JSON.parse(data) : {}
  } catch (error) {
    console.error('❌ Error loading regional risk data:', error)
    return {}
  }
}

/**
 * Merge user's local municipality data with centralized regional risk data
 * 
 * This ensures:
 * 1. User can edit their own municipality's demographic data (population, etc.)
 * 2. User sees the latest risk levels from ALL municipalities (including others' simulations)
 * 
 * Priority:
 * - For own municipality: Keep all local data
 * - For other municipalities: Use regional risk data for risk-related fields
 * 
 * @param {Array} localMunicipalities - User's local municipality data
 * @returns {Array} Merged municipality data with latest regional risk levels
 */
export const mergeWithRegionalRiskData = (localMunicipalities) => {
  try {
    const regionalData = loadRegionalRiskData()
    
    console.log('🔀 Loading regional data for map...')
    console.log('🔀 Regional data available for:', Object.keys(regionalData).length, 'municipalities')
    
    // 🔥 SIMPLE FIX: For the map, ONLY use regional data, ignore local dummy data
    // If no regional data exists for a municipality, don't show it on the map
    const merged = localMunicipalities.map(mun => {
      const regionalInfo = regionalData[mun.id]
      
      if (regionalInfo) {
        console.log(`✅ ${mun.id}: Using REGIONAL data (infected: ${regionalInfo.infectedDogs})`)
        // Use regional data completely
        return {
          ...mun,  // Keep structure (lat, lng, connections)
          // Override with regional risk data
          riskLevel: regionalInfo.riskLevel,
          infectedDogs: regionalInfo.infectedDogs,
          infectedCats: regionalInfo.infectedCats,
          infectedHumans: regionalInfo.infectedHumans,
          vaccinatedDogs: regionalInfo.vaccinatedDogs,
          lastUpdated: regionalInfo.lastUpdated,
          predictedInfectedDogs: regionalInfo.predictedInfectedDogs,
          predictedInfectedCats: regionalInfo.predictedInfectedCats,
          predictedInfectedHumans: regionalInfo.predictedInfectedHumans,
          hasRegionalData: true  // Flag to indicate this has real data
        }
      } else {
        console.log(`⚠️ ${mun.id}: No regional data - will show as "No data"`)
        // Return municipality but mark as having no regional data
        return {
          ...mun,
          hasRegionalData: false,  // Flag so map can hide it or show "No data"
          riskLevel: 'safe',
          infectedDogs: 0,
          infectedCats: 0,
          infectedHumans: 0
        }
      }
    })
    
    return merged
    
  } catch (error) {
    console.error('❌ Error merging regional risk data:', error)
    return localMunicipalities
  }
}

/**
 * Get the latest regional risk summary
 * Useful for displaying regional statistics
 * 
 * @returns {Object} Summary of regional risk levels
 */
export const getRegionalRiskSummary = () => {
  try {
    const regionalData = loadRegionalRiskData()
    const municipalities = Object.values(regionalData)
    
    const summary = {
      total: municipalities.length,
      safe: 0,
      low: 0,
      moderate: 0,
      high: 0,
      critical: 0,
      totalInfectedDogs: 0,
      totalInfectedCats: 0,
      totalInfectedHumans: 0,
      lastUpdated: null
    }
    
    municipalities.forEach(mun => {
      const level = mun.riskLevel || 'safe'
      summary[level]++
      summary.totalInfectedDogs += mun.infectedDogs || 0
      summary.totalInfectedCats += mun.infectedCats || 0
      summary.totalInfectedHumans += mun.infectedHumans || 0
      
      // Track most recent update
      if (mun.lastUpdated) {
        const munDate = new Date(mun.lastUpdated)
        if (!summary.lastUpdated || munDate > summary.lastUpdated) {
          summary.lastUpdated = munDate
        }
      }
    })
    
    return summary
    
  } catch (error) {
    console.error('❌ Error getting regional risk summary:', error)
    return null
  }
}

/**
 * Clear all regional risk data (admin only)
 * Useful for testing or resetting the system
 */
export const clearRegionalRiskData = () => {
  try {
    localStorage.removeItem(REGIONAL_RISK_KEY)
    console.log('✅ Regional risk data cleared')
  } catch (error) {
    console.error('❌ Error clearing regional risk data:', error)
  }
}

/**
 * Set up listener for regional risk data changes
 * This allows real-time cross-tab synchronization
 * 
 * @param {Function} callback - Function to call when data changes
 * @returns {Function} Cleanup function to remove listener
 */
export const onRegionalRiskDataChange = (callback) => {
  // Handler for cross-tab changes (via localStorage event)
  const handleStorageChange = (event) => {
    // Only react to changes to the regional risk data key
    if (event.key === REGIONAL_RISK_KEY && event.newValue) {
      try {
        const newData = JSON.parse(event.newValue)
        console.log('🔄 Regional risk data changed (cross-tab sync)', Object.keys(newData).length, 'municipalities')
        callback(newData)
      } catch (error) {
        console.error('❌ Error parsing regional risk data change:', error)
      }
    }
  }
  
  // Handler for same-tab changes (via custom event)
  const handleCustomEvent = (event) => {
    console.log('🔄 Regional risk data changed (same-tab sync)', Object.keys(event.detail).length, 'municipalities')
    callback(event.detail)
  }
  
  window.addEventListener('storage', handleStorageChange)
  window.addEventListener(REGIONAL_RISK_UPDATE_EVENT, handleCustomEvent)
  
  // Return cleanup function
  return () => {
    window.removeEventListener('storage', handleStorageChange)
    window.removeEventListener(REGIONAL_RISK_UPDATE_EVENT, handleCustomEvent)
  }
}
