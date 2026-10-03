// Simulation Logger Service for PAWPATROL

export class SimulationLogger {
  constructor() {
    this.logs = []
    this.maxLogs = 10000 // Prevent memory overflow
    this.currentDay = 0
  }
  
  addLog(message, severity = 'info', municipalityId = null, data = null) {
    const logEntry = {
      id: this.generateId(),
      timestamp: new Date().toISOString(),
      day: this.getCurrentDay(),
      message,
      severity,
      municipalityId,
      data,
      category: this.categorizeLog(message, severity)
    }
    
    this.logs.push(logEntry)
    
    // Maintain log size limit
    if (this.logs.length > this.maxLogs) {
      this.logs = this.logs.slice(-this.maxLogs)
    }
    
    return logEntry
  }
  
  addTransmissionLog(fromMunicipality, toMunicipality, count, species) {
    const message = `Transmission: ${count} ${species} infected in ${toMunicipality} from ${fromMunicipality}`
    return this.addLog(message, 'warning', null, {
      type: 'transmission',
      from: fromMunicipality,
      to: toMunicipality,
      count,
      species
    })
  }
  
  addVaccinationLog(municipality, count, reason) {
    const message = `Vaccination: ${count} dogs vaccinated in ${municipality} - ${reason}`
    return this.addLog(message, 'success', null, {
      type: 'vaccination',
      municipality,
      count,
      reason
    })
  }
  
  addRiskChangeLog(municipality, oldRisk, newRisk) {
    const message = `Risk Level: ${municipality} changed from ${oldRisk} to ${newRisk}`
    return this.addLog(message, 'warning', null, {
      type: 'risk_change',
      municipality,
      oldRisk,
      newRisk
    })
  }
  
  addOutbreakLog(municipality, infectedCount, species) {
    const message = `Outbreak Alert: ${infectedCount} ${species} infected in ${municipality}`
    return this.addLog(message, 'error', null, {
      type: 'outbreak',
      municipality,
      infectedCount,
      species
    })
  }
  
  addSimulationStateLog(state, details) {
    const messages = {
      started: 'Simulation started successfully',
      paused: 'Simulation paused',
      resumed: 'Simulation resumed',
      stopped: 'Simulation stopped',
      completed: 'Simulation completed successfully',
      error: 'Simulation error occurred'
    }
    
    return this.addLog(messages[state] || `Simulation ${state}`, 'info', null, {
      type: 'simulation_state',
      state,
      details
    })
  }
  
  getDayLogs(day) {
    return this.logs.filter(log => log.day === day)
  }
  
  getLogsByCategory(category) {
    return this.logs.filter(log => log.category === category)
  }
  
  getLogsBySeverity(severity) {
    return this.logs.filter(log => log.severity === severity)
  }
  
  getRecentLogs(count = 50) {
    return this.logs.slice(-count)
  }
  
  getLogsByMunicipality(municipalityId) {
    return this.logs.filter(log => 
      log.municipalityId === municipalityId || 
      (log.data && (log.data.municipality === municipalityId || log.data.to === municipalityId || log.data.from === municipalityId))
    )
  }
  
  getLogsByDateRange(startDate, endDate) {
    const start = new Date(startDate).getTime()
    const end = new Date(endDate).getTime()
    
    return this.logs.filter(log => {
      const logTime = new Date(log.timestamp).getTime()
      return logTime >= start && logTime <= end
    })
  }
  
  exportLogs(format = 'json') {
    switch (format.toLowerCase()) {
      case 'json':
        return JSON.stringify(this.logs, null, 2)
      
      case 'csv':
        return this.exportToCSV()
      
      case 'txt':
        return this.exportToText()
      
      default:
        throw new Error(`Unsupported export format: ${format}`)
    }
  }
  
  exportToCSV() {
    const headers = ['Timestamp', 'Day', 'Severity', 'Category', 'Message', 'Municipality', 'Data']
    const rows = this.logs.map(log => [
      log.timestamp,
      log.day,
      log.severity,
      log.category,
      `"${log.message.replace(/"/g, '""')}"`, // Escape quotes
      log.municipalityId || '',
      log.data ? `"${JSON.stringify(log.data).replace(/"/g, '""')}"` : ''
    ])
    
    return [headers, ...rows].map(row => row.join(',')).join('\n')
  }
  
  exportToText() {
    return this.logs.map(log => {
      const timestamp = new Date(log.timestamp).toLocaleString()
      const severity = log.severity.toUpperCase()
      const day = log.day ? `Day ${log.day}` : 'Day 0'
      
      let text = `[${timestamp}] [${day}] [${severity}] ${log.message}`
      
      if (log.municipalityId) {
        text += ` (Municipality: ${log.municipalityId})`
      }
      
      if (log.data) {
        text += `\n  Data: ${JSON.stringify(log.data, null, 2)}`
      }
      
      return text
    }).join('\n\n')
  }
  
  getStatistics() {
    const stats = {
      totalLogs: this.logs.length,
      bySeverity: {},
      byCategory: {},
      byDay: {},
      timeRange: {
        first: null,
        last: null
      }
    }
    
    this.logs.forEach(log => {
      // Severity statistics
      stats.bySeverity[log.severity] = (stats.bySeverity[log.severity] || 0) + 1
      
      // Category statistics
      stats.byCategory[log.category] = (stats.byCategory[log.category] || 0) + 1
      
      // Day statistics
      if (log.day !== null && log.day !== undefined) {
        stats.byDay[log.day] = (stats.byDay[log.day] || 0) + 1
      }
      
      // Time range
      if (!stats.timeRange.first || log.timestamp < stats.timeRange.first) {
        stats.timeRange.first = log.timestamp
      }
      if (!stats.timeRange.last || log.timestamp > stats.timeRange.last) {
        stats.timeRange.last = log.timestamp
      }
    })
    
    return stats
  }
  
  clearLogs() {
    this.logs = []
  }
  
  searchLogs(query, field = 'message') {
    const searchTerm = query.toLowerCase()
    
    return this.logs.filter(log => {
      switch (field) {
        case 'message':
          return log.message.toLowerCase().includes(searchTerm)
        
        case 'severity':
          return log.severity.toLowerCase().includes(searchTerm)
        
        case 'category':
          return log.category.toLowerCase().includes(searchTerm)
        
        case 'all':
          return (
            log.message.toLowerCase().includes(searchTerm) ||
            log.severity.toLowerCase().includes(searchTerm) ||
            log.category.toLowerCase().includes(searchTerm) ||
            (log.municipalityId && log.municipalityId.toLowerCase().includes(searchTerm))
          )
        
        default:
          return log.message.toLowerCase().includes(searchTerm)
      }
    })
  }
  
  categorizeLog(message, severity) {
    const messageUpper = message.toUpperCase()
    
    if (messageUpper.includes('TRANSMISSION') || messageUpper.includes('INFECTED')) {
      return 'transmission'
    }
    
    if (messageUpper.includes('VACCINATION') || messageUpper.includes('VACCINATED')) {
      return 'vaccination'
    }
    
    if (messageUpper.includes('RISK') || messageUpper.includes('OUTBREAK')) {
      return 'risk_assessment'
    }
    
    if (messageUpper.includes('SIMULATION')) {
      return 'simulation_control'
    }
    
    if (messageUpper.includes('ERROR') || severity === 'error') {
      return 'error'
    }
    
    return 'general'
  }
  
  generateId() {
    return Date.now().toString(36) + Math.random().toString(36).substr(2, 9)
  }
  
  getCurrentDay() {
    return this.currentDay
  }
  
  // Set current day method (to be called by simulation engine)
  setCurrentDay(day) {
    this.currentDay = day
  }
}

// Export singleton instance
export const simulationLogger = new SimulationLogger()

// Export utilities
export const LogSeverity = {
  INFO: 'info',
  SUCCESS: 'success',
  WARNING: 'warning',
  ERROR: 'error'
}

export const LogCategory = {
  TRANSMISSION: 'transmission',
  VACCINATION: 'vaccination',
  RISK_ASSESSMENT: 'risk_assessment',
  SIMULATION_CONTROL: 'simulation_control',
  ERROR: 'error',
  GENERAL: 'general'
}