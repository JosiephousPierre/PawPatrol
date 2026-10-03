// Adaptive Vaccination Decision Module for PAWPATROL
// Rule-based system that mimics Deep Reinforcement Learning behavior

import { computed } from 'vue'
import { useAppStore } from '@/stores'

export function useAdaptiveVaccination() {
  const appStore = useAppStore()
  
  const generateRecommendations = () => {
    const municipalities = appStore.municipalities
    const recommendations = []
    
    municipalities.forEach(municipality => {
      const recommendation = evaluateMunicipality(municipality, municipalities)
      recommendations.push(recommendation)
    })
    
    // Sort by priority and infection severity
    recommendations.sort((a, b) => {
      const priorityOrder = { 'Critical': 5, 'High': 4, 'Medium': 3, 'Low': 2, 'Monitor': 1 }
      return priorityOrder[b.priority] - priorityOrder[a.priority]
    })
    
    // Save recommendations to store
    appStore.vaccinationRecommendations = recommendations
    appStore.saveAllData()
    
    return recommendations
  }
  
  const evaluateMunicipality = (municipality, allMunicipalities) => {
    // Calculate key metrics
    const infectionRate = calculateInfectionRate(municipality)
    const vaccinationCoverage = calculateVaccinationCoverage(municipality)
    const riskScore = calculateRiskScore(municipality, allMunicipalities)
    const neighborRisk = assessNeighborRisk(municipality, allMunicipalities)
    
    // Apply rule-based decision logic
    const decision = applyVaccinationRules(municipality, {
      infectionRate,
      vaccinationCoverage,
      riskScore,
      neighborRisk
    })
    
    return {
      municipalityId: municipality.id,
      municipalityName: municipality.name,
      recommendedVaccinationPercentage: decision.vaccinationPercentage,
      priority: decision.priority,
      reason: decision.reason,
      currentInfectionRate: infectionRate,
      currentVaccinationCoverage: vaccinationCoverage,
      riskScore: riskScore,
      neighborRiskLevel: neighborRisk,
      timestamp: new Date().toISOString(),
      day: appStore.currentSimulationDay
    }
  }
  
  const applyVaccinationRules = (municipality, metrics) => {
    const { infectionRate, vaccinationCoverage, riskScore, neighborRisk } = metrics
    
    // Rule 1: Critical outbreak (>10% infection rate)
    if (infectionRate > 10) {
      return {
        vaccinationPercentage: 95,
        priority: 'Critical',
        reason: `Critical outbreak detected: ${infectionRate.toFixed(1)}% infection rate. Emergency vaccination required.`
      }
    }
    
    // Rule 2: High infection rate (5-10%)
    if (infectionRate > 5) {
      return {
        vaccinationPercentage: 85,
        priority: 'High',
        reason: `High infection rate (${infectionRate.toFixed(1)}%) requires intensive vaccination campaign.`
      }
    }
    
    // Rule 3: Moderate infection with low vaccination coverage
    if (infectionRate > 2 && vaccinationCoverage < 40) {
      return {
        vaccinationPercentage: 75,
        priority: 'High',
        reason: `Active transmission (${infectionRate.toFixed(1)}%) with insufficient vaccination coverage (${vaccinationCoverage.toFixed(1)}%).`
      }
    }
    
    // Rule 4: Neighbor municipality outbreak risk
    if (neighborRisk >= 4 && vaccinationCoverage < 70) {
      return {
        vaccinationPercentage: 80,
        priority: 'High',
        reason: `High-risk neighboring areas detected. Preventive vaccination recommended.`
      }
    }
    
    // Rule 5: Early outbreak detection (1-5% infection rate)
    if (infectionRate > 1 && infectionRate <= 5) {
      const targetCoverage = Math.min(90, 60 + (infectionRate * 5)) // Scale with infection rate
      return {
        vaccinationPercentage: targetCoverage,
        priority: 'Medium',
        reason: `Early outbreak phase detected. Targeted vaccination to prevent spread.`
      }
    }
    
    // Rule 6: Preventive vaccination for high-risk areas
    if (riskScore > 7 && vaccinationCoverage < 60) {
      return {
        vaccinationPercentage: 70,
        priority: 'Medium',
        reason: `High-risk area with inadequate vaccination coverage. Preventive measures recommended.`
      }
    }
    
    // Rule 7: Neighbor outbreak containment
    if (neighborRisk >= 3 && vaccinationCoverage < 50) {
      return {
        vaccinationPercentage: 65,
        priority: 'Medium',
        reason: `Neighboring outbreak containment strategy. Ring vaccination approach.`
      }
    }
    
    // Rule 8: Maintain minimum coverage
    if (vaccinationCoverage < 40) {
      return {
        vaccinationPercentage: 50,
        priority: 'Low',
        reason: `Below minimum vaccination threshold. Routine vaccination recommended.`
      }
    }
    
    // Rule 9: Safe area maintenance
    if (infectionRate === 0 && vaccinationCoverage >= 70) {
      return {
        vaccinationPercentage: vaccinationCoverage, // Maintain current level
        priority: 'Monitor',
        reason: `Area secure. Continue monitoring and maintain current vaccination levels.`
      }
    }
    
    // Rule 10: Low-risk maintenance
    if (infectionRate <= 1 && vaccinationCoverage >= 60) {
      return {
        vaccinationPercentage: Math.max(vaccinationCoverage, 60),
        priority: 'Low',
        reason: `Low infection risk. Maintain protective vaccination coverage.`
      }
    }
    
    // Default rule: Standard prevention
    return {
      vaccinationPercentage: 60,
      priority: 'Low',
      reason: `Standard preventive vaccination protocol.`
    }
  }
  
  const calculateInfectionRate = (municipality) => {
    const totalAnimals = municipality.dogPopulation + municipality.catPopulation
    
    // Use simulation results if available, otherwise use current data
    let totalInfected = municipality.infectedDogs + municipality.infectedCats
    
    // Check if we have fresh simulation results
    if (appStore.simulationResults?.municipalities) {
      const simResult = appStore.simulationResults.municipalities.find(m => m.id === municipality.id)
      if (simResult) {
        totalInfected = (simResult.predictedInfectedDogs || 0) + (simResult.predictedInfectedCats || 0)
      }
    }
    
    if (totalAnimals === 0) return 0
    return (totalInfected / totalAnimals) * 100
  }
  
  const calculateVaccinationCoverage = (municipality) => {
    if (municipality.dogPopulation === 0) return 0
    return (municipality.vaccinatedDogs / municipality.dogPopulation) * 100
  }
  
  const calculateRiskScore = (municipality, allMunicipalities) => {
    let riskScore = 0
    
    // Base risk from current infection
    const infectionRate = calculateInfectionRate(municipality)
    riskScore += infectionRate * 2 // Weight infection rate heavily
    
    // Population density factor (higher population = higher risk)
    const populationDensity = (municipality.dogPopulation + municipality.catPopulation) / 1000
    riskScore += Math.min(populationDensity, 5) // Cap at 5 points
    
    // Vaccination coverage factor (lower coverage = higher risk)
    const vaccinationCoverage = calculateVaccinationCoverage(municipality)
    riskScore += Math.max(0, (80 - vaccinationCoverage) / 10) // Penalty for low coverage
    
    // Connection factor (more connections = higher risk)
    const connectionCount = municipality.connectedMunicipalities?.length || 0
    riskScore += connectionCount * 0.5
    
    // Historical risk factor (based on riskLevel)
    const riskLevelScore = {
      safe: 0,
      low: 1,
      moderate: 3,
      high: 6,
      critical: 10
    }
    riskScore += riskLevelScore[municipality.riskLevel] || 0
    
    return Math.min(riskScore, 20) // Cap at 20 points
  }
  
  const assessNeighborRisk = (municipality, allMunicipalities) => {
    if (!municipality.connectedMunicipalities || municipality.connectedMunicipalities.length === 0) {
      return 0
    }
    
    let totalNeighborRisk = 0
    let neighborCount = 0
    
    municipality.connectedMunicipalities.forEach(neighborId => {
      const neighbor = allMunicipalities.find(m => m.id === neighborId)
      if (neighbor) {
        const neighborInfectionRate = calculateInfectionRate(neighbor)
        const neighborVaccinationCoverage = calculateVaccinationCoverage(neighbor)
        
        // Calculate neighbor risk score
        let neighborRisk = neighborInfectionRate / 2 // Infection rate contribution
        neighborRisk += Math.max(0, (60 - neighborVaccinationCoverage) / 15) // Vaccination gap penalty
        
        // Risk level multiplier
        const riskMultiplier = {
          safe: 0.5,
          low: 1,
          moderate: 2,
          high: 4,
          critical: 6
        }
        neighborRisk *= (riskMultiplier[neighbor.riskLevel] || 1)
        
        totalNeighborRisk += neighborRisk
        neighborCount++
      }
    })
    
    return neighborCount > 0 ? totalNeighborRisk / neighborCount : 0
  }
  
  const getOptimalVaccinationStrategy = (recommendations) => {
    // Resource allocation strategy
    const totalRecommendations = recommendations.length
    const criticalCases = recommendations.filter(r => r.priority === 'Critical').length
    const highCases = recommendations.filter(r => r.priority === 'High').length
    
    return {
      totalMunicipalities: totalRecommendations,
      criticalCases,
      highCases,
      resourceAllocation: {
        immediate: criticalCases + highCases,
        scheduled: recommendations.filter(r => r.priority === 'Medium').length,
        monitoring: recommendations.filter(r => r.priority === 'Monitor').length
      },
      estimatedVaccinesNeeded: recommendations.reduce((total, rec) => {
        const municipality = appStore.municipalities.find(m => m.id === rec.municipalityId)
        if (municipality) {
          const targetVaccinated = municipality.dogPopulation * rec.recommendedVaccinationPercentage / 100
          const additionalNeeded = Math.max(0, targetVaccinated - municipality.vaccinatedDogs)
          return total + additionalNeeded
        }
        return total
      }, 0)
    }
  }
  
  const simulateVaccinationImpact = (municipalityId, vaccinationPercentage) => {
    const municipality = appStore.municipalities.find(m => m.id === municipalityId)
    if (!municipality) return null
    
    // Simulate vaccination impact on transmission
    const currentInfectionRate = calculateInfectionRate(municipality)
    const currentVaccinationCoverage = calculateVaccinationCoverage(municipality)
    
    // Calculate expected reduction in transmission
    const vaccinationIncrease = Math.max(0, vaccinationPercentage - currentVaccinationCoverage)
    const transmissionReduction = vaccinationIncrease * 0.8 // 80% vaccine efficiency
    const expectedInfectionRate = Math.max(0, currentInfectionRate - (transmissionReduction / 10))
    
    return {
      municipalityId,
      currentInfectionRate,
      expectedInfectionRate,
      transmissionReduction: currentInfectionRate - expectedInfectionRate,
      vaccinationIncrease,
      timeToControl: estimateControlTime(expectedInfectionRate)
    }
  }
  
  const estimateControlTime = (infectionRate) => {
    if (infectionRate <= 1) return 7 // 1 week for low infection
    if (infectionRate <= 5) return 14 // 2 weeks for moderate
    if (infectionRate <= 10) return 30 // 1 month for high
    return 60 // 2+ months for critical
  }
  
  return {
    generateRecommendations,
    evaluateMunicipality,
    getOptimalVaccinationStrategy,
    simulateVaccinationImpact,
    calculateInfectionRate,
    calculateVaccinationCoverage,
    calculateRiskScore,
    assessNeighborRisk
  }
}