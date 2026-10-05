// Municipality Authentication Service
// Simple access control without complex user management

import { ref, computed } from 'vue'

const currentMunicipality = ref(null)
const isAuthenticated = ref(false)

// Predefined municipalities with access codes
const MUNICIPALITY_REGISTRY = {
  'MACO': {
    id: 'maco',
    name: 'Maco',
    code: 'MACO',
    region: 'Davao de Oro',
    permissions: ['manage_own_data', 'participate_simulation', 'view_regional_summary']
  },
  'MAWAB': {
    id: 'mawab', 
    name: 'Mawab',
    code: 'MAWAB',
    region: 'Davao de Oro',
    permissions: ['manage_own_data', 'participate_simulation', 'view_regional_summary']
  },
  'NABUNTURAN': {
    id: 'nabunturan',
    name: 'Nabunturan', 
    code: 'NABUNTURAN',
    region: 'Davao de Oro',
    permissions: ['manage_own_data', 'participate_simulation', 'view_regional_summary']
  },
  'PANTUKAN': {
    id: 'pantukan',
    name: 'Pantukan',
    code: 'PANTUKAN', 
    region: 'Davao de Oro',
    permissions: ['manage_own_data', 'participate_simulation', 'view_regional_summary']
  },
  'LAAK': {
    id: 'laak',
    name: 'Laak',
    code: 'LAAK',
    region: 'Davao de Oro',
    permissions: ['manage_own_data', 'participate_simulation', 'view_regional_summary']
  },
  'MONKAYO': {
    id: 'monkayo',
    name: 'Monkayo',
    code: 'MONKAYO',
    region: 'Davao de Oro',
    permissions: ['manage_own_data', 'participate_simulation', 'view_regional_summary']
  },
  'NEW BATAAN': {
    id: 'new_bataan',
    name: 'New Bataan',
    code: 'NEW BATAAN',
    region: 'Davao de Oro',
    permissions: ['manage_own_data', 'participate_simulation', 'view_regional_summary']
  },
  'COMPOSTELA': {
    id: 'compostela',
    name: 'Compostela',
    code: 'COMPOSTELA',
    region: 'Davao de Oro',
    permissions: ['manage_own_data', 'participate_simulation', 'view_regional_summary']
  },
  'MABINI': {
    id: 'mabini',
    name: 'Mabini',
    code: 'MABINI',
    region: 'Davao de Oro',
    permissions: ['manage_own_data', 'participate_simulation', 'view_regional_summary']
  },
  'MONTEVISTA': {
    id: 'montevista',
    name: 'Montevista',
    code: 'MONTEVISTA',
    region: 'Davao de Oro',
    permissions: ['manage_own_data', 'participate_simulation', 'view_regional_summary']
  },
  'MARAGUSAN': {
    id: 'maragusan',
    name: 'Maragusan',
    code: 'MARAGUSAN',
    region: 'Davao de Oro',
    permissions: ['manage_own_data', 'participate_simulation', 'view_regional_summary']
  },
  // Admin account
  'ADMIN': {
    id: 'admin',
    name: 'Regional Health Office',
    code: 'ADMIN',
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