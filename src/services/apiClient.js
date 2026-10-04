/**
 * API Client for PAWPATROL Backend
 * Connects Vue.js frontend to Python FastAPI backend
 */

const API_BASE_URL = 'http://localhost:8000'

class ApiClient {
  constructor() {
    this.baseURL = API_BASE_URL
  }

  /**
   * Generic GET request
   * @param {string} endpoint - API endpoint (e.g., '/drl-status')
   * @returns {Promise<Object>} Response data
   */
  async get(endpoint) {
    const url = endpoint.startsWith('http') ? endpoint : `${this.baseURL}/api${endpoint}`
    console.log('🔍 API Client GET:', url)
    
    try {
      const response = await fetch(url)
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }
      
      const data = await response.json()
      console.log('✅ API Client GET success:', endpoint)
      return { data, status: response.status }
    } catch (error) {
      console.error('❌ API Client GET failed:', endpoint, error.message)
      throw error
    }
  }

  /**
   * Generic POST request
   * @param {string} endpoint - API endpoint (e.g., '/drl-recommend')
   * @param {Object} body - Request body
   * @returns {Promise<Object>} Response data
   */
  async post(endpoint, body) {
    const url = endpoint.startsWith('http') ? endpoint : `${this.baseURL}/api${endpoint}`
    console.log('📤 API Client POST:', url, body)
    
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      })
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail?.message || `HTTP ${response.status}: ${response.statusText}`)
      }
      
      const data = await response.json()
      console.log('✅ API Client POST success:', endpoint)
      return { data, status: response.status }
    } catch (error) {
      console.error('❌ API Client POST failed:', endpoint, error.message)
      throw error
    }
  }

  async healthCheck() {
    console.log('🔍 API Client: Checking backend health at', `${this.baseURL}/api/health`)
    try {
      const response = await fetch(`${this.baseURL}/api/health`)
      console.log('✅ API Client: Health check response status:', response.status)
      const data = await response.json()
      console.log('✅ API Client: Health check data:', data)
      return data
    } catch (error) {
      console.error('❌ API Client: Health check failed:', error.message)
      throw error
    }
  }

  async validateParameters(params) {
    const response = await fetch(`${this.baseURL}/api/validate-parameters`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(params)
    })
    return await response.json()
  }

  async runSimulation(municipalities, settings) {
    const response = await fetch(`${this.baseURL}/api/simulate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ municipalities, settings })
    })
    return await response.json()
  }
}

export const apiClient = new ApiClient()
export default apiClient