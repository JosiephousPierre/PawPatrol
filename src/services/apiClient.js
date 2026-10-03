/**
 * API Client for PAWPATROL Backend
 * Connects Vue.js frontend to Python FastAPI backend
 */

const API_BASE_URL = 'http://localhost:8000'

class ApiClient {
  constructor() {
    this.baseURL = API_BASE_URL
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