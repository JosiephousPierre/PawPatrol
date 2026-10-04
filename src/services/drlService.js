/**
 * DRL (Deep Reinforcement Learning) Service
 * Handles communication with DRL API endpoints
 */

import apiClient from './apiClient'

/**
 * Check if DRL model is available and loaded
 * @returns {Promise<Object>} DRL status information
 */
export async function checkDRLStatus() {
  try {
    const response = await apiClient.get('/drl-status')
    return {
      success: true,
      ...response.data
    }
  } catch (error) {
    console.error('DRL Status Check Error:', error)
    return {
      success: false,
      available: false,
      loaded: false,
      error: error.message
    }
  }
}

/**
 * Get DRL-based vaccination recommendations for municipalities
 * @param {Array} municipalities - List of municipality data
 * @returns {Promise<Object>} Recommendations with confidence scores
 */
export async function getDRLRecommendations(municipalities) {
  try {
    const response = await apiClient.post('/drl-recommend', {
      municipalities: municipalities
    })
    
    return {
      success: true,
      ...response.data
    }
  } catch (error) {
    console.error('DRL Recommendation Error:', error)
    
    // Return error details
    return {
      success: false,
      drl_available: false,
      recommendations: [],
      error: error.response?.data?.detail?.message || error.message
    }
  }
}

/**
 * Format DRL recommendation for display
 * @param {Object} recommendation - Raw DRL recommendation
 * @returns {Object} Formatted recommendation
 */
export function formatDRLRecommendation(recommendation) {
  return {
    municipalityId: recommendation.municipality_id,
    municipalityName: recommendation.municipality_name,
    recommendedVaccination: Math.round(recommendation.recommended_vaccination * 100),
    confidence: Math.round(recommendation.confidence * 100),
    explanation: recommendation.explanation,
    qValues: recommendation.q_values || {},
    source: recommendation.source,
    action: recommendation.action,
    // Determine priority based on recommendation
    priority: determinePriority(recommendation.recommended_vaccination),
    // Icon based on vaccination level
    icon: getVaccinationIcon(recommendation.recommended_vaccination)
  }
}

/**
 * Determine priority level from vaccination recommendation
 * @param {number} vaccinationPct - Vaccination percentage (0-1)
 * @returns {string} Priority level
 */
function determinePriority(vaccinationPct) {
  if (vaccinationPct >= 0.9) return 'Critical'
  if (vaccinationPct >= 0.8) return 'High'
  if (vaccinationPct >= 0.7) return 'Medium'
  if (vaccinationPct >= 0.5) return 'Low'
  return 'Monitor'
}

/**
 * Get icon class based on vaccination level
 * @param {number} vaccinationPct - Vaccination percentage (0-1)
 * @returns {string} Icon class
 */
function getVaccinationIcon(vaccinationPct) {
  if (vaccinationPct >= 0.9) return 'pi-exclamation-triangle'
  if (vaccinationPct >= 0.7) return 'pi-exclamation-circle'
  if (vaccinationPct >= 0.5) return 'pi-info-circle'
  return 'pi-check-circle'
}

/**
 * Compare DRL recommendation with current coverage
 * @param {Object} recommendation - DRL recommendation
 * @param {number} currentCoverage - Current vaccination coverage (0-100)
 * @returns {Object} Comparison result
 */
export function compareDRLWithCurrent(recommendation, currentCoverage) {
  const recommendedPct = recommendation.recommendedVaccination
  const difference = recommendedPct - currentCoverage
  
  return {
    difference: Math.round(difference),
    shouldIncrease: difference > 5,
    shouldDecrease: difference < -5,
    isOptimal: Math.abs(difference) <= 5,
    message: getDifferenceMessage(difference)
  }
}

/**
 * Get message based on coverage difference
 * @param {number} difference - Difference in percentage
 * @returns {string} Message
 */
function getDifferenceMessage(difference) {
  if (difference > 20) return 'Urgent: Significantly increase vaccination'
  if (difference > 10) return 'Increase vaccination coverage'
  if (difference > 5) return 'Slightly increase vaccination'
  if (difference < -10) return 'Coverage exceeds recommendation'
  if (difference < -5) return 'Coverage slightly high'
  return 'Coverage is optimal'
}

export default {
  checkDRLStatus,
  getDRLRecommendations,
  formatDRLRecommendation,
  compareDRLWithCurrent
}
