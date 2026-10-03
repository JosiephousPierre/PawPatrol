// Municipality Authentication Service
// Simple access control without complex user management

import { ref, computed } from 'vue'

const currentMunicipality = ref(null)
const isAuthenticated = ref(false)

// Predefined municipalities with access codes
const MUNICIPALITY_REGISTRY = {
  'MACO-2024': {
    id: 'maco',
    name: 'Maco',
    code: 'MACO-2024',
    region: 'Davao de Oro',
    permissions: ['manage_own_data', 'participate_simulation', 'view_regional_summary']
  },
  'MAWAB-2024': {
    id: 'mawab', 
    name: 'Mawab',
    code: 'MAWAB-2024',
    region: 'Davao de Oro',
    permissions: ['manage_own_data', 'participate_simulation', 'view_regional_summary']
  },
  'NABUNTURAN-2024': {
    id: 'nabunturan',
    name: 'Nabunturan', 
    code: 'NABUNTURAN-2024',
    region: 'Davao de Oro',
    permissions: ['manage_own_data', 'participate_simulation', 'view_regional_summary']
  },
  'PANTUKAN-2024': {
    id: 'pantukan',
    name: 'Pantukan',
    code: 'PANTUKAN-2024', 
    region: 'Davao de Oro',
    permissions: ['manage_own_data', 'participate_simulation', 'view_regional_summary']
  },
  // Add all Davao de Oro municipalities
  'ADMIN-2024': {
    id: 'admin',
    name: 'Regional Health Office',
    code: 'ADMIN-2024',
    region: 'Davao de Oro',
    permissions: ['view_all_data', 'manage_simulations', 'regional_oversight']
  }
}

export function useMunicipalityAuth() {
  
  const login = (accessCode) => {
    const municipality = MUNICIPALITY_REGISTRY[accessCode.toUpperCase()]
    
    if (!municipality) {
      throw new Error('Invalid access code. Please check with your Regional Health Office.')
    }
    
    currentMunicipality.value = municipality
    isAuthenticated.value = true
    
    // Save session
    localStorage.setItem('currentMunicipality', JSON.stringify(municipality))
    
    return municipality
  }
  
  const logout = () => {
    currentMunicipality.value = null
    isAuthenticated.value = false
    localStorage.removeItem('currentMunicipality')
  }
  
  const restoreSession = () => {
    const saved = localStorage.getItem('currentMunicipality')
    if (saved) {
      try {
        currentMunicipality.value = JSON.parse(saved)
        isAuthenticated.value = true
        return true
      } catch (e) {
        localStorage.removeItem('currentMunicipality')
        return false
      }
    }
    return false
  }
  
  const hasPermission = (permission) => {
    return currentMunicipality.value?.permissions?.includes(permission) || false
  }
  
  const canAccessMunicipalityData = (municipalityId) => {
    if (!currentMunicipality.value) return false
    
    // Own municipality always accessible
    if (currentMunicipality.value.id === municipalityId) return true
    
    // Admin can access all
    if (hasPermission('view_all_data')) return true
    
    // Regional summary data accessible to all
    if (hasPermission('view_regional_summary')) return true
    
    return false
  }
  
  return {
    currentMunicipality: computed(() => currentMunicipality.value),
    isAuthenticated: computed(() => isAuthenticated.value),
    login,
    logout,
    restoreSession,
    hasPermission,
    canAccessMunicipalityData
  }
}