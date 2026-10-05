// Simulation Utilities for PAWPATROL

/**
 * Calculate transmission probability based on various factors
 */
export const calculateTransmissionProbability = (
  baseRate,
  infectedCount,
  populationSize,
  environmentalFactor = 0,
  crossBorder = false
) => {
  let rate = baseRate
  
  // Apply environmental randomness
  if (environmentalFactor > 0) {
    const randomFactor = 1 + (Math.random() - 0.5) * environmentalFactor
    rate *= randomFactor
  }
  
  // Apply cross-border reduction
  if (crossBorder) {
    rate *= 0.3
  }
  
  // Calculate based on infected proportion
  const infectedProportion = populationSize > 0 ? infectedCount / populationSize : 0
  return rate * infectedProportion
}

/**
 * Generate Poisson-distributed random number (approximation)
 */
export const poissonRandom = (lambda) => {
  if (lambda <= 0) return 0
  
  // For small lambda, use direct method
  if (lambda < 30) {
    let L = Math.exp(-lambda)
    let k = 0
    let p = 1
    
    do {
      k++
      p *= Math.random()
    } while (p > L)
    
    return k - 1
  }
  
  // For larger lambda, use normal approximation
  const mean = lambda
  const stdDev = Math.sqrt(lambda)
  const normal = normalRandom(mean, stdDev)
  return Math.max(0, Math.round(normal))
}

/**
 * Generate normally distributed random number (Box-Muller transform)
 */
export const normalRandom = (mean = 0, stdDev = 1) => {
  const u1 = Math.random()
  const u2 = Math.random()
  const z0 = Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2)
  return z0 * stdDev + mean
}

/**
 * Calculate basic reproduction number (R0)
 */
export const calculateR0 = (transmissionRate, contactRate, recoveryRate) => {
  return (transmissionRate * contactRate) / recoveryRate
}

/**
 * Estimate outbreak duration based on current parameters
 */
export const estimateOutbreakDuration = (
  currentInfected,
  susceptible,
  transmissionRate,
  vaccinationCoverage
) => {
  if (currentInfected === 0) return 0
  if (susceptible === 0) return 0
  
  // Simple SIR model estimation
  const effectiveTransmission = transmissionRate * (1 - vaccinationCoverage)
  const growthRate = effectiveTransmission * (susceptible / (susceptible + currentInfected))
  
  if (growthRate <= 0) return 7 // Already declining, estimate 1 week
  if (growthRate < 0.05) return 14 // Slow growth, 2 weeks
  if (growthRate < 0.1) return 30 // Moderate, 1 month
  if (growthRate < 0.2) return 60 // High growth, 2 months
  return 90 // Very high growth, 3+ months
}

/**
 * Calculate herd immunity threshold
 */
export const calculateHerdImmunityThreshold = (r0) => {
  if (r0 <= 1) return 0
  return 1 - (1 / r0)
}

/**
 * Estimate required vaccination coverage for control
 */
export const estimateRequiredVaccinationCoverage = (transmissionRate, population) => {
  // Simplified calculation
  const r0 = transmissionRate * population * 0.01 // Rough estimate
  const herdImmunity = calculateHerdImmunityThreshold(r0)
  
  // Add safety margin
  return Math.min(0.95, herdImmunity * 1.2)
}

/**
 * Calculate infection fatality rate (IFR)
 */
export const calculateIFR = (deaths, totalInfected) => {
  if (totalInfected === 0) return 0
  return (deaths / totalInfected) * 100
}

/**
 * Calculate case fatality rate (CFR)
 */
export const calculateCFR = (deaths, confirmedCases) => {
  if (confirmedCases === 0) return 0
  return (deaths / confirmedCases) * 100
}

/**
 * Estimate peak infection day
 */
export const estimatePeakDay = (dailyData) => {
  if (!dailyData || dailyData.length === 0) return null
  
  let maxInfections = 0
  let peakDay = 0
  
  dailyData.forEach(data => {
    const totalInfected = (data.totalInfected?.dogs || 0) + 
                         (data.totalInfected?.cats || 0) + 
                         (data.totalInfected?.humans || 0)
    
    if (totalInfected > maxInfections) {
      maxInfections = totalInfected
      peakDay = data.day
    }
  })
  
  return { day: peakDay, infections: maxInfections }
}

/**
 * Calculate doubling time
 */
export const calculateDoublingTime = (growthRate) => {
  if (growthRate <= 0) return Infinity
  return Math.log(2) / Math.log(1 + growthRate)
}

/**
 * Calculate transmission rate for a municipality
 * Based on daily infection changes
 */
export const calculateTransmissionRate = (municipality, dailyData = null) => {
  // If no daily data provided, calculate from current state
  if (!dailyData || dailyData.length < 2) {
    const totalPopulation = municipality.dogPopulation + municipality.catPopulation
    const totalInfected = (municipality.infectedDogs || 0) + (municipality.infectedCats || 0)
    
    if (totalPopulation === 0) return 0
    return (totalInfected / totalPopulation) * 100
  }
  
  // Calculate from historical data (last 7 days or available data)
  const recentDays = dailyData.slice(-Math.min(7, dailyData.length))
  
  if (recentDays.length < 2) {
    return 0
  }
  
  // Calculate daily new infections
  const newCasesPerDay = []
  for (let i = 1; i < recentDays.length; i++) {
    const previousInfected = (recentDays[i - 1].infectedDogs || 0) + (recentDays[i - 1].infectedCats || 0)
    const currentInfected = (recentDays[i].infectedDogs || 0) + (recentDays[i].infectedCats || 0)
    newCasesPerDay.push(Math.max(0, currentInfected - previousInfected))
  }
  
  // Calculate average transmission rate
  const averageNewCases = newCasesPerDay.reduce((sum, cases) => sum + cases, 0) / newCasesPerDay.length
  const totalPopulation = municipality.dogPopulation + municipality.catPopulation
  
  if (totalPopulation === 0) return 0
  
  // Return as percentage per day
  return (averageNewCases / totalPopulation) * 100
}

/**
 * Identify the highest-risk municipality
 * Based on multiple factors: infections, transmission rate, risk score
 */
export const identifyHighestRiskMunicipality = (municipalities) => {
  if (!municipalities || municipalities.length === 0) return null
  
  let highestRisk = null
  let highestScore = -1
  
  municipalities.forEach(municipality => {
    const riskScore = calculateOverallRiskScore(municipality)
    
    if (riskScore > highestScore) {
      highestScore = riskScore
      highestRisk = {
        ...municipality,
        overallRiskScore: riskScore,
        transmissionRate: calculateTransmissionRate(municipality)
      }
    }
  })
  
  return highestRisk
}

/**
 * Calculate overall risk score for a municipality
 * Combines infections, transmission, vaccination, and risk level
 */
export const calculateOverallRiskScore = (municipality) => {
  let score = 0
  
  // Factor 1: Current infections (weighted heavily)
  const totalInfected = (municipality.infectedDogs || 0) + 
                       (municipality.infectedCats || 0) + 
                       (municipality.infectedHumans || 0)
  score += totalInfected * 3 // Weight: 3 points per infection
  
  // Factor 2: Infection rate as percentage
  const totalPopulation = municipality.dogPopulation + municipality.catPopulation
  if (totalPopulation > 0) {
    const infectionRate = (totalInfected / totalPopulation) * 100
    score += infectionRate * 2 // Weight: 2 points per percentage
  }
  
  // Factor 3: Risk level score
  const riskLevelScores = {
    safe: 0,
    low: 5,
    moderate: 15,
    high: 30,
    critical: 50
  }
  score += riskLevelScores[municipality.riskLevel] || 0
  
  // Factor 4: Vaccination coverage gap (penalty for low coverage)
  const vaccinationCoverage = municipality.dogPopulation > 0 
    ? (municipality.vaccinatedDogs / municipality.dogPopulation) * 100 
    : 0
  const coverageGap = Math.max(0, 80 - vaccinationCoverage)
  score += coverageGap * 0.5 // Weight: 0.5 points per percentage gap
  
  // Factor 5: Population size (larger populations = higher potential risk)
  const populationFactor = Math.min(10, (totalPopulation / 1000)) // Cap at 10 points
  score += populationFactor
  
  // Factor 6: Human infections (highest priority)
  score += (municipality.infectedHumans || 0) * 10 // Weight: 10 points per human case
  
  return Math.round(score)
}

/**
 * Find municipality with fastest transmission rate
 */
export const findFastestTransmissionMunicipality = (municipalities, dailyDataByMunicipality = null) => {
  if (!municipalities || municipalities.length === 0) return null
  
  let fastest = null
  let fastestRate = -1
  
  municipalities.forEach(municipality => {
    const municipalityData = dailyDataByMunicipality 
      ? dailyDataByMunicipality[municipality.id] 
      : null
    
    const transmissionRate = calculateTransmissionRate(municipality, municipalityData)
    
    if (transmissionRate > fastestRate) {
      fastestRate = transmissionRate
      fastest = {
        ...municipality,
        transmissionRate: transmissionRate,
        transmissionRateLabel: formatTransmissionRate(transmissionRate)
      }
    }
  })
  
  return fastest
}

/**
 * Format transmission rate for display
 */
export const formatTransmissionRate = (rate) => {
  if (rate === 0) return '0% per day'
  if (rate < 0.1) return `${rate.toFixed(3)}% per day (Very Low)`
  if (rate < 0.5) return `${rate.toFixed(2)}% per day (Low)`
  if (rate < 1) return `${rate.toFixed(2)}% per day (Moderate)`
  if (rate < 2) return `${rate.toFixed(2)}% per day (High)`
  return `${rate.toFixed(2)}% per day (Critical)`
}

/**
 * Get transmission rate severity level
 */
export const getTransmissionSeverity = (rate) => {
  if (rate === 0) return 'none'
  if (rate < 0.1) return 'very-low'
  if (rate < 0.5) return 'low'
  if (rate < 1) return 'moderate'
  if (rate < 2) return 'high'
  return 'critical'
}

/**
 * Calculate growth rate from infection data
 */
export const calculateGrowthRate = (currentInfected, previousInfected) => {
  if (previousInfected === 0) return 0
  return (currentInfected - previousInfected) / previousInfected
}

/**
 * Predict future infections (with population constraints)
 * Uses logistic growth model to prevent unrealistic exponential explosion
 */
export const predictFutureInfections = (currentInfected, growthRate, days, totalPopulation = null) => {
  if (growthRate <= 0 || currentInfected <= 0) return currentInfected
  
  // If no population provided, use simple exponential with reasonable cap
  if (!totalPopulation || totalPopulation <= 0) {
    const predicted = Math.round(currentInfected * Math.pow(1 + growthRate, days))
    // Cap at 10x current infected as safety measure
    return Math.min(predicted, currentInfected * 10)
  }
  
  // Use logistic growth model for realistic population-constrained growth
  // Formula: P(t) = K / (1 + ((K - P0) / P0) * e^(-r*t))
  // Where: K = carrying capacity (total population)
  //        P0 = initial infected
  //        r = growth rate
  //        t = time (days)
  
  const K = totalPopulation // Carrying capacity
  const P0 = currentInfected
  const r = growthRate
  const t = days
  
  // Calculate logistic growth
  const exponent = -r * t
  const denominator = 1 + ((K - P0) / P0) * Math.exp(exponent)
  const predicted = K / denominator
  
  // Ensure we don't exceed total population
  const result = Math.min(Math.round(predicted), K)
  
  // Sanity check: if result is somehow less than current, return current
  return Math.max(result, currentInfected)
}

/**
 * Predict future risk level for a municipality
 * Uses historical infection data and trends to forecast future risk
 */
export const predictFutureRiskLevel = (municipality, dailyData = null, futureDays = 30) => {
  // Calculate current infection rate and trend
  const totalPopulation = municipality.dogPopulation + municipality.catPopulation
  const currentInfected = (municipality.infectedDogs || 0) + (municipality.infectedCats || 0)
  const currentInfectionRate = totalPopulation > 0 ? (currentInfected / totalPopulation) * 100 : 0
  
  // Calculate growth rate from recent data
  let growthRate = 0
  if (dailyData && dailyData.length >= 7) {
    const recentDays = dailyData.slice(-7)
    const oldInfected = (recentDays[0].infectedDogs || 0) + (recentDays[0].infectedCats || 0)
    const newInfected = (recentDays[recentDays.length - 1].infectedDogs || 0) + (recentDays[recentDays.length - 1].infectedCats || 0)
    
    if (oldInfected > 0) {
      growthRate = (newInfected - oldInfected) / oldInfected / 7 // Daily average growth rate
    }
  } else {
    // Estimate growth rate from current state
    const vaccinationCoverage = municipality.dogPopulation > 0 
      ? (municipality.vaccinatedDogs / municipality.dogPopulation) 
      : 0
    
    // Lower vaccination = higher potential growth
    growthRate = Math.max(0, (1 - vaccinationCoverage) * 0.05) // Up to 5% daily growth
    
    if (currentInfected > 0) {
      growthRate += 0.02 // Base growth if already infected
    }
  }
  
  // Predict future infected count WITH POPULATION CONSTRAINT
  const predictedInfected = predictFutureInfections(currentInfected, growthRate, futureDays, totalPopulation)
  const predictedInfectionRate = totalPopulation > 0 ? (predictedInfected / totalPopulation) * 100 : 0
  
  // Predict vaccination coverage (assuming some vaccination effort)
  const vaccinationCoverage = municipality.dogPopulation > 0 
    ? (municipality.vaccinatedDogs / municipality.dogPopulation) * 100 
    : 0
  const predictedVaccinationCoverage = Math.min(95, vaccinationCoverage + (futureDays * 0.5)) // 0.5% increase per day
  
  // Determine predicted risk level
  let predictedRiskLevel = 'safe'
  if (predictedInfectionRate === 0 && predictedVaccinationCoverage >= 80) {
    predictedRiskLevel = 'safe'
  } else if (predictedInfectionRate <= 2 && predictedVaccinationCoverage >= 60) {
    predictedRiskLevel = 'low'
  } else if (predictedInfectionRate <= 5 && predictedVaccinationCoverage >= 40) {
    predictedRiskLevel = 'moderate'
  } else if (predictedInfectionRate <= 10) {
    predictedRiskLevel = 'high'
  } else {
    predictedRiskLevel = 'critical'
  }
  
  return {
    municipalityId: municipality.id,
    municipalityName: municipality.name,
    currentRiskLevel: municipality.riskLevel,
    currentInfected: currentInfected,
    currentInfectionRate: currentInfectionRate,
    predictedRiskLevel: predictedRiskLevel,
    predictedInfected: predictedInfected,
    predictedInfectionRate: predictedInfectionRate,
    growthRate: growthRate,
    futureDays: futureDays,
    confidence: calculatePredictionConfidence(dailyData, currentInfected),
    riskChange: getRiskChange(municipality.riskLevel, predictedRiskLevel)
  }
}

/**
 * Calculate confidence level for prediction based on data availability
 */
const calculatePredictionConfidence = (dailyData, currentInfected) => {
  if (!dailyData || dailyData.length === 0) {
    return currentInfected > 0 ? 'medium' : 'low'
  }
  
  if (dailyData.length >= 14) return 'high'
  if (dailyData.length >= 7) return 'medium'
  return 'low'
}

/**
 * Determine risk change direction and severity
 */
const getRiskChange = (currentRisk, predictedRisk) => {
  const riskOrder = { safe: 0, low: 1, moderate: 2, high: 3, critical: 4 }
  const currentLevel = riskOrder[currentRisk] || 0
  const predictedLevel = riskOrder[predictedRisk] || 0
  const change = predictedLevel - currentLevel
  
  if (change > 0) return 'increasing'
  if (change < 0) return 'decreasing'
  return 'stable'
}

/**
 * Generate time-series forecast for all municipalities
 * Creates day-by-day predictions for the specified forecast period
 */
export const generateTimeSeriesForecast = (municipalities, dailyData = null, forecastDays = 30) => {
  const forecasts = []
  
  municipalities.forEach(municipality => {
    const municipalityForecast = {
      municipalityId: municipality.id,
      municipalityName: municipality.name,
      currentData: {
        infected: (municipality.infectedDogs || 0) + (municipality.infectedCats || 0),
        riskLevel: municipality.riskLevel,
        vaccinationCoverage: municipality.dogPopulation > 0 
          ? Math.round((municipality.vaccinatedDogs / municipality.dogPopulation) * 100) 
          : 0
      },
      dailyPredictions: []
    }
    
    // Calculate growth rate
    let dailyGrowthRate = 0
    const currentInfected = (municipality.infectedDogs || 0) + (municipality.infectedCats || 0)
    const totalPopulation = municipality.dogPopulation + municipality.catPopulation
    
    if (dailyData && dailyData.length >= 7) {
      const recentDays = dailyData.slice(-7)
      const oldInfected = (recentDays[0].infectedDogs || 0) + (recentDays[0].infectedCats || 0)
      const newInfected = (recentDays[recentDays.length - 1].infectedDogs || 0) + (recentDays[recentDays.length - 1].infectedCats || 0)
      
      if (oldInfected > 0) {
        dailyGrowthRate = (newInfected - oldInfected) / oldInfected / 7
      }
    } else {
      const vaccinationCoverage = municipality.dogPopulation > 0 
        ? (municipality.vaccinatedDogs / municipality.dogPopulation) 
        : 0
      dailyGrowthRate = currentInfected > 0 ? Math.max(0, (1 - vaccinationCoverage) * 0.03) : 0
    }
    
    // Generate day-by-day predictions
    let cumulativeInfected = currentInfected
    for (let day = 1; day <= forecastDays; day++) {
      // Predict infections for this day WITH POPULATION CONSTRAINT
      cumulativeInfected = predictFutureInfections(currentInfected, dailyGrowthRate, day, totalPopulation)
      const infectionRate = totalPopulation > 0 ? (cumulativeInfected / totalPopulation) * 100 : 0
      
      // Predict vaccination coverage growth
      const currentVaccinationCoverage = municipality.dogPopulation > 0 
        ? (municipality.vaccinatedDogs / municipality.dogPopulation) * 100 
        : 0
      const predictedVaccination = Math.min(95, currentVaccinationCoverage + (day * 0.5))
      
      // Determine risk level for this day
      let riskLevel = 'safe'
      if (infectionRate === 0 && predictedVaccination >= 80) {
        riskLevel = 'safe'
      } else if (infectionRate <= 2 && predictedVaccination >= 60) {
        riskLevel = 'low'
      } else if (infectionRate <= 5 && predictedVaccination >= 40) {
        riskLevel = 'moderate'
      } else if (infectionRate <= 10) {
        riskLevel = 'high'
      } else {
        riskLevel = 'critical'
      }
      
      municipalityForecast.dailyPredictions.push({
        day: day,
        predictedInfected: Math.round(cumulativeInfected),
        infectionRate: parseFloat(infectionRate.toFixed(2)),
        riskLevel: riskLevel,
        vaccinationCoverage: Math.round(predictedVaccination)
      })
    }
    
    forecasts.push(municipalityForecast)
  })
  
  return forecasts
}

/**
 * Identify municipalities that will become high-risk in the future
 */
export const identifyFutureHighRiskMunicipalities = (municipalities, forecastDays = 30) => {
  const predictions = municipalities.map(municipality => 
    predictFutureRiskLevel(municipality, null, forecastDays)
  )
  
  // Filter for municipalities predicted to become high or critical
  const futureHighRisk = predictions.filter(prediction => 
    ['high', 'critical'].includes(prediction.predictedRiskLevel) &&
    prediction.riskChange === 'increasing'
  )
  
  // Sort by severity (critical first, then high)
  futureHighRisk.sort((a, b) => {
    const severityOrder = { critical: 2, high: 1 }
    const severityA = severityOrder[a.predictedRiskLevel] || 0
    const severityB = severityOrder[b.predictedRiskLevel] || 0
    
    if (severityB !== severityA) {
      return severityB - severityA
    }
    
    // If same severity, sort by predicted infection rate
    return b.predictedInfectionRate - a.predictedInfectionRate
  })
  
  return futureHighRisk
}

/**
 * Generate summary of predictive analysis for all municipalities
 */
export const generatePredictiveAnalysisSummary = (municipalities, forecastDays = 30) => {
  const predictions = municipalities.map(municipality => 
    predictFutureRiskLevel(municipality, null, forecastDays)
  )
  
  const summary = {
    forecastDays: forecastDays,
    totalMunicipalities: municipalities.length,
    predictions: predictions,
    riskDistribution: {
      currentSafe: predictions.filter(p => p.currentRiskLevel === 'safe').length,
      currentLow: predictions.filter(p => p.currentRiskLevel === 'low').length,
      currentModerate: predictions.filter(p => p.currentRiskLevel === 'moderate').length,
      currentHigh: predictions.filter(p => p.currentRiskLevel === 'high').length,
      currentCritical: predictions.filter(p => p.currentRiskLevel === 'critical').length,
      predictedSafe: predictions.filter(p => p.predictedRiskLevel === 'safe').length,
      predictedLow: predictions.filter(p => p.predictedRiskLevel === 'low').length,
      predictedModerate: predictions.filter(p => p.predictedRiskLevel === 'moderate').length,
      predictedHigh: predictions.filter(p => p.predictedRiskLevel === 'high').length,
      predictedCritical: predictions.filter(p => p.predictedRiskLevel === 'critical').length
    },
    riskChanges: {
      increasing: predictions.filter(p => p.riskChange === 'increasing').length,
      stable: predictions.filter(p => p.riskChange === 'stable').length,
      decreasing: predictions.filter(p => p.riskChange === 'decreasing').length
    },
    highRiskMunicipalities: predictions
      .filter(p => ['high', 'critical'].includes(p.predictedRiskLevel))
      .map(p => ({ name: p.municipalityName, predictedRisk: p.predictedRiskLevel })),
    averageGrowthRate: predictions.reduce((sum, p) => sum + p.growthRate, 0) / predictions.length
  }
  
  return summary
}

// ============================================================================
// INTERVENTION COST ESTIMATION FUNCTIONS
// ============================================================================

/**
 * Standard intervention costs (in Philippine Peso - PHP)
 * Based on DOH and LGU typical costs
 */
export const INTERVENTION_COSTS = {
  // Vaccination costs
  dogVaccine: 150,              // PHP per dose (includes vaccine + administration)
  catVaccine: 120,              // PHP per dose (cats slightly cheaper)
  humanPEP: 15000,              // PHP per person (Post-Exposure Prophylaxis - full course)
  humanPreExposure: 8000,       // PHP per person (Pre-exposure vaccination)
  
  // Operational costs
  mobilizationPerMunicipality: 5000,     // PHP (transport, setup per municipality)
  vaccinationTeamPerDay: 3000,           // PHP per day (vaccinators' wages)
  publicAwarenessPerMunicipality: 2000,  // PHP (IEC materials, announcements)
  
  // Surveillance and monitoring
  surveillancePerMunicipality: 1500,     // PHP per month
  laboratoryTestPerAnimal: 500,          // PHP per rabies test
  
  // Emergency response (for high-risk areas)
  emergencyResponseTeam: 10000,          // PHP per deployment
  quarantineFacilityPerDay: 2000,        // PHP per day
  
  // Administrative overhead
  administrativeOverhead: 0.10           // 10% of total direct costs
}

/**
 * Calculate vaccination cost for a municipality
 */
export const calculateVaccinationCost = (municipality, targetCoveragePercent = 80, costConfig = INTERVENTION_COSTS) => {
  const currentVaccinated = municipality.vaccinatedDogs || 0
  const totalDogs = municipality.dogPopulation || 0
  const totalCats = municipality.catPopulation || 0
  
  // Calculate needed vaccinations to reach target coverage
  const targetDogVaccinations = Math.ceil(totalDogs * (targetCoveragePercent / 100))
  const additionalDogVaccines = Math.max(0, targetDogVaccinations - currentVaccinated)
  
  // Assume 50% cat coverage as standard (cats harder to reach)
  const targetCatVaccinations = Math.ceil(totalCats * 0.5)
  const currentCatVaccinated = 0 // Assume starting from zero for cats
  const additionalCatVaccines = Math.max(0, targetCatVaccinations - currentCatVaccinated)
  
  // Calculate costs
  const dogVaccineCost = additionalDogVaccines * costConfig.dogVaccine
  const catVaccineCost = additionalCatVaccines * costConfig.catVaccine
  const totalVaccineCost = dogVaccineCost + catVaccineCost
  
  // Operational costs
  const mobilizationCost = costConfig.mobilizationPerMunicipality
  const publicAwarenessCost = costConfig.publicAwarenessPerMunicipality
  
  // Estimate team days needed (assume 100 vaccinations per team per day)
  const totalVaccinations = additionalDogVaccines + additionalCatVaccines
  const teamDaysNeeded = Math.ceil(totalVaccinations / 100)
  const vaccinationTeamCost = teamDaysNeeded * costConfig.vaccinationTeamPerDay
  
  // Surveillance cost (1 month)
  const surveillanceCost = costConfig.surveillancePerMunicipality
  
  const subtotal = totalVaccineCost + mobilizationCost + publicAwarenessCost + vaccinationTeamCost + surveillanceCost
  const adminCost = subtotal * costConfig.administrativeOverhead
  const totalCost = subtotal + adminCost
  
  return {
    municipalityId: municipality.id,
    municipalityName: municipality.name,
    targetCoverage: targetCoveragePercent,
    vaccinations: {
      dogs: additionalDogVaccines,
      cats: additionalCatVaccines,
      total: totalVaccinations
    },
    costs: {
      dogVaccines: dogVaccineCost,
      catVaccines: catVaccineCost,
      mobilization: mobilizationCost,
      publicAwareness: publicAwarenessCost,
      vaccinationTeam: vaccinationTeamCost,
      surveillance: surveillanceCost,
      administrative: adminCost,
      subtotal: subtotal,
      total: totalCost
    },
    teamDaysNeeded: teamDaysNeeded,
    estimatedDuration: `${teamDaysNeeded} days`
  }
}

/**
 * Calculate human PEP (Post-Exposure Prophylaxis) cost
 */
export const calculateHumanPEPCost = (municipality, costConfig = INTERVENTION_COSTS) => {
  const infectedHumans = municipality.infectedHumans || 0
  
  // Assume 20% of exposed humans need full PEP (others may have pre-exposure)
  const fullPEPNeeded = Math.ceil(infectedHumans * 0.2)
  const pepCost = fullPEPNeeded * costConfig.humanPEP
  
  return {
    municipalityId: municipality.id,
    municipalityName: municipality.name,
    exposedHumans: infectedHumans,
    pepTreatments: fullPEPNeeded,
    cost: pepCost
  }
}

/**
 * Calculate emergency response cost for high-risk areas
 */
export const calculateEmergencyResponseCost = (municipality, costConfig = INTERVENTION_COSTS) => {
  const riskLevel = municipality.riskLevel
  const totalInfected = (municipality.infectedDogs || 0) + (municipality.infectedCats || 0)
  
  // Emergency response only for high and critical risk
  if (!['high', 'critical'].includes(riskLevel)) {
    return {
      municipalityId: municipality.id,
      municipalityName: municipality.name,
      riskLevel: riskLevel,
      emergencyResponseNeeded: false,
      cost: 0
    }
  }
  
  // Critical areas need more intensive response
  const isCritical = riskLevel === 'critical'
  
  // Emergency team deployments
  const teamDeployments = isCritical ? 2 : 1
  const emergencyTeamCost = teamDeployments * costConfig.emergencyResponseTeam
  
  // Laboratory testing for infected animals
  const testsNeeded = Math.min(totalInfected, 20) // Test up to 20 samples
  const labTestCost = testsNeeded * costConfig.laboratoryTestPerAnimal
  
  // Quarantine facility (if critical, assume 7 days; if high, 3 days)
  const quarantineDays = isCritical ? 7 : 3
  const quarantineCost = quarantineDays * costConfig.quarantineFacilityPerDay
  
  const totalCost = emergencyTeamCost + labTestCost + quarantineCost
  
  return {
    municipalityId: municipality.id,
    municipalityName: municipality.name,
    riskLevel: riskLevel,
    emergencyResponseNeeded: true,
    components: {
      emergencyTeams: emergencyTeamCost,
      laboratoryTests: labTestCost,
      quarantine: quarantineCost
    },
    teamDeployments: teamDeployments,
    labTests: testsNeeded,
    quarantineDays: quarantineDays,
    cost: totalCost
  }
}

/**
 * Calculate total intervention cost for a municipality
 */
export const calculateTotalInterventionCost = (municipality, targetCoveragePercent = 80, costConfig = INTERVENTION_COSTS) => {
  const vaccinationCost = calculateVaccinationCost(municipality, targetCoveragePercent, costConfig)
  const pepCost = calculateHumanPEPCost(municipality, costConfig)
  const emergencyCost = calculateEmergencyResponseCost(municipality, costConfig)
  
  const totalCost = vaccinationCost.costs.total + pepCost.cost + emergencyCost.cost
  
  return {
    municipalityId: municipality.id,
    municipalityName: municipality.name,
    riskLevel: municipality.riskLevel,
    breakdown: {
      vaccination: vaccinationCost,
      humanPEP: pepCost,
      emergencyResponse: emergencyCost
    },
    totalCost: totalCost,
    costPerCapita: municipality.humanPopulation > 0 
      ? totalCost / municipality.humanPopulation 
      : 0
  }
}

/**
 * Calculate intervention budget for all municipalities
 */
export const calculateInterventionBudget = (municipalities, targetCoveragePercent = 80, costConfig = INTERVENTION_COSTS) => {
  const municipalityCosts = municipalities.map(m => 
    calculateTotalInterventionCost(m, targetCoveragePercent, costConfig)
  )
  
  // Calculate totals
  const totalVaccinationCost = municipalityCosts.reduce((sum, m) => 
    sum + m.breakdown.vaccination.costs.total, 0
  )
  const totalPEPCost = municipalityCosts.reduce((sum, m) => 
    sum + m.breakdown.humanPEP.cost, 0
  )
  const totalEmergencyCost = municipalityCosts.reduce((sum, m) => 
    sum + m.breakdown.emergencyResponse.cost, 0
  )
  const grandTotal = totalVaccinationCost + totalPEPCost + totalEmergencyCost
  
  // Categorize by risk level
  const byRiskLevel = {
    safe: municipalityCosts.filter(m => m.riskLevel === 'safe').reduce((sum, m) => sum + m.totalCost, 0),
    low: municipalityCosts.filter(m => m.riskLevel === 'low').reduce((sum, m) => sum + m.totalCost, 0),
    moderate: municipalityCosts.filter(m => m.riskLevel === 'moderate').reduce((sum, m) => sum + m.totalCost, 0),
    high: municipalityCosts.filter(m => m.riskLevel === 'high').reduce((sum, m) => sum + m.totalCost, 0),
    critical: municipalityCosts.filter(m => m.riskLevel === 'critical').reduce((sum, m) => sum + m.totalCost, 0)
  }
  
  // Calculate total vaccinations needed
  const totalDogVaccinations = municipalityCosts.reduce((sum, m) => 
    sum + m.breakdown.vaccination.vaccinations.dogs, 0
  )
  const totalCatVaccinations = municipalityCosts.reduce((sum, m) => 
    sum + m.breakdown.vaccination.vaccinations.cats, 0
  )
  
  return {
    targetCoverage: targetCoveragePercent,
    totalMunicipalities: municipalities.length,
    municipalityCosts: municipalityCosts,
    summary: {
      totalVaccinationCost: totalVaccinationCost,
      totalPEPCost: totalPEPCost,
      totalEmergencyCost: totalEmergencyCost,
      grandTotal: grandTotal
    },
    byRiskLevel: byRiskLevel,
    vaccinations: {
      dogs: totalDogVaccinations,
      cats: totalCatVaccinations,
      total: totalDogVaccinations + totalCatVaccinations
    },
    costPerVaccine: (totalDogVaccinations + totalCatVaccinations) > 0 
      ? totalVaccinationCost / (totalDogVaccinations + totalCatVaccinations)
      : 0,
    priorityMunicipalities: municipalityCosts
      .filter(m => ['high', 'critical'].includes(m.riskLevel))
      .sort((a, b) => b.totalCost - a.totalCost)
      .slice(0, 5)
  }
}

/**
 * Calculate cost-benefit analysis (cost per infection prevented)
 */
export const calculateCostBenefit = (currentInfections, predictedInfections, interventionCost) => {
  const infectionsPrevented = Math.max(0, predictedInfections - currentInfections * 0.3) // Assume 70% reduction
  const costPerInfectionPrevented = infectionsPrevented > 0 
    ? interventionCost / infectionsPrevented 
    : Infinity
  
  // Estimate economic benefit (avoiding treatment costs, loss of animals, etc.)
  const treatmentCostSaved = infectionsPrevented * 5000 // PHP per infected animal treatment
  const economicBenefit = treatmentCostSaved - interventionCost
  const roi = interventionCost > 0 
    ? ((economicBenefit / interventionCost) * 100)
    : 0
  
  return {
    interventionCost: interventionCost,
    infectionsPrevented: Math.round(infectionsPrevented),
    costPerInfectionPrevented: costPerInfectionPrevented,
    treatmentCostSaved: treatmentCostSaved,
    economicBenefit: economicBenefit,
    roi: roi, // Return on Investment percentage
    recommendation: roi > 0 ? 'Cost-effective' : 'High cost, consider alternatives'
  }
}

/**
 * Format currency in Philippine Peso
 */
export const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-PH', {
    style: 'currency',
    currency: 'PHP',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(amount)
}

/**
 * Calculate attack rate
 */
export const calculateAttackRate = (infected, population) => {
  if (population === 0) return 0
  return (infected / population) * 100
}

/**
 * Calculate secondary attack rate
 */
export const calculateSecondaryAttackRate = (secondaryInfections, susceptibleContacts) => {
  if (susceptibleContacts === 0) return 0
  return (secondaryInfections / susceptibleContacts) * 100
}

/**
 * Estimate contact tracing effectiveness
 */
export const estimateContactTracingEffectiveness = (
  infectionReduction,
  baselineInfections
) => {
  if (baselineInfections === 0) return 100
  return (infectionReduction / baselineInfections) * 100
}

/**
 * Calculate vaccination impact
 */
export const calculateVaccinationImpact = (
  populationSize,
  vaccinationCoverage,
  vaccineEffectiveness,
  transmissionRate
) => {
  const protectedPopulation = populationSize * vaccinationCoverage * vaccineEffectiveness
  const transmissionReduction = (protectedPopulation / populationSize) * transmissionRate
  
  return {
    protectedPopulation: Math.round(protectedPopulation),
    transmissionReduction: transmissionReduction * 100,
    effectiveR0Reduction: transmissionReduction
  }
}

/**
 * Format simulation duration
 */
export const formatDuration = (milliseconds) => {
  const seconds = Math.floor(milliseconds / 1000)
  const minutes = Math.floor(seconds / 60)
  const hours = Math.floor(minutes / 60)
  
  if (hours > 0) {
    return `${hours}h ${minutes % 60}m ${seconds % 60}s`
  } else if (minutes > 0) {
    return `${minutes}m ${seconds % 60}s`
  } else {
    return `${seconds}s`
  }
}

/**
 * Generate color for risk level
 */
export const getRiskColor = (riskLevel) => {
  const colors = {
    safe: '#22c55e',
    low: '#eab308',
    moderate: '#f97316',
    high: '#ef4444',
    critical: '#991b1b'
  }
  return colors[riskLevel] || colors.safe
}

/**
 * Calculate intervention effectiveness
 */
export const calculateInterventionEffectiveness = (
  baselineInfections,
  postInterventionInfections
) => {
  if (baselineInfections === 0) return 0
  const reduction = baselineInfections - postInterventionInfections
  return (reduction / baselineInfections) * 100
}

/**
 * Estimate resource requirements
 */
export const estimateResourceRequirements = (
  targetPopulation,
  vaccinationPercentage,
  currentVaccinated
) => {
  const targetVaccinations = Math.ceil(targetPopulation * (vaccinationPercentage / 100))
  const additionalNeeded = Math.max(0, targetVaccinations - currentVaccinated)
  
  return {
    targetVaccinations,
    currentVaccinated,
    additionalNeeded,
    percentageComplete: currentVaccinated > 0 
      ? Math.min(100, (currentVaccinated / targetVaccinations) * 100)
      : 0
  }
}

/**
 * Calculate cost-effectiveness ratio
 */
export const calculateCostEffectiveness = (
  interventionCost,
  casesAverted
) => {
  if (casesAverted === 0) return Infinity
  return interventionCost / casesAverted
}

/**
 * Generate simulation summary statistics
 */
export const generateSimulationSummary = (dailyData) => {
  if (!dailyData || dailyData.length === 0) {
    return {
      totalDays: 0,
      totalInfections: 0,
      peakDay: null,
      peakInfections: 0,
      averageDailyInfections: 0
    }
  }
  
  let totalInfections = 0
  let peakInfections = 0
  let peakDay = 0
  
  dailyData.forEach(data => {
    const dayTotal = (data.totalInfected?.dogs || 0) + 
                    (data.totalInfected?.cats || 0) + 
                    (data.totalInfected?.humans || 0)
    
    totalInfections = dayTotal
    
    if (dayTotal > peakInfections) {
      peakInfections = dayTotal
      peakDay = data.day
    }
  })
  
  return {
    totalDays: dailyData.length,
    totalInfections,
    peakDay,
    peakInfections,
    averageDailyInfections: Math.round(totalInfections / dailyData.length)
  }
}

export default {
  calculateTransmissionProbability,
  poissonRandom,
  normalRandom,
  calculateR0,
  estimateOutbreakDuration,
  calculateHerdImmunityThreshold,
  estimateRequiredVaccinationCoverage,
  calculateIFR,
  calculateCFR,
  estimatePeakDay,
  calculateDoublingTime,
  calculateGrowthRate,
  predictFutureInfections,
  calculateAttackRate,
  calculateSecondaryAttackRate,
  estimateContactTracingEffectiveness,
  calculateVaccinationImpact,
  formatDuration,
  getRiskColor,
  calculateInterventionEffectiveness,
  estimateResourceRequirements,
  calculateCostEffectiveness,
  generateSimulationSummary,
  calculateTransmissionRate,
  identifyHighestRiskMunicipality,
  calculateOverallRiskScore,
  findFastestTransmissionMunicipality,
  formatTransmissionRate,
  getTransmissionSeverity,
  predictFutureRiskLevel,
  generateTimeSeriesForecast,
  identifyFutureHighRiskMunicipalities,
  generatePredictiveAnalysisSummary,
  // Cost estimation functions
  INTERVENTION_COSTS,
  calculateVaccinationCost,
  calculateHumanPEPCost,
  calculateEmergencyResponseCost,
  calculateTotalInterventionCost,
  calculateInterventionBudget,
  calculateCostBenefit,
  formatCurrency
}