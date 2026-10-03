// Formatting composable for PAWPATROL

import { computed } from 'vue'

export function useFormatting() {
  
  const formatNumber = (number) => {
    if (typeof number !== 'number') return '0'
    return number.toLocaleString()
  }
  
  const formatPercentage = (value, total) => {
    if (!total || total === 0) return '0%'
    return Math.round((value / total) * 100) + '%'
  }
  
  const formatCurrency = (amount, currency = 'PHP') => {
    return new Intl.NumberFormat('en-PH', {
      style: 'currency',
      currency: currency
    }).format(amount)
  }
  
  const formatDate = (date) => {
    if (!date) return ''
    return new Date(date).toLocaleDateString('en-PH', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  }
  
  const formatTime = (date) => {
    if (!date) return ''
    return new Date(date).toLocaleTimeString('en-PH', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    })
  }
  
  const formatDateTime = (date) => {
    if (!date) return ''
    return new Date(date).toLocaleString('en-PH')
  }
  
  const getRiskBadgeClass = (riskLevel) => {
    const classes = {
      safe: 'bg-risk-safe/10 text-risk-safe border-risk-safe/20',
      low: 'bg-risk-low/10 text-risk-low border-risk-low/20',
      moderate: 'bg-risk-moderate/10 text-risk-moderate border-risk-moderate/20',
      high: 'bg-risk-high/10 text-risk-high border-risk-high/20',
      critical: 'bg-risk-critical/10 text-risk-critical border-risk-critical/20'
    }
    return classes[riskLevel] || classes.safe
  }
  
  const getRiskColor = (riskLevel) => {
    const colors = {
      safe: '#22c55e',
      low: '#eab308',
      moderate: '#f97316',
      high: '#ef4444',
      critical: '#991b1b'
    }
    return colors[riskLevel] || colors.safe
  }
  
  const getRiskLabel = (riskLevel) => {
    const labels = {
      safe: 'Safe',
      low: 'Low Risk',
      moderate: 'Moderate Risk',
      high: 'High Risk',
      critical: 'Critical'
    }
    return labels[riskLevel] || 'Safe'
  }
  
  const getInfectionStatusClass = (count) => {
    if (count === 0) return 'text-risk-safe font-semibold'
    if (count < 5) return 'text-risk-low font-semibold'
    if (count < 10) return 'text-risk-moderate font-semibold'
    if (count < 20) return 'text-risk-high font-semibold'
    return 'text-risk-critical font-bold'
  }
  
  const getVaccinationStatusClass = (percentage) => {
    if (percentage >= 80) return 'text-risk-safe font-semibold'
    if (percentage >= 60) return 'text-risk-low font-semibold'
    if (percentage >= 40) return 'text-risk-moderate font-semibold'
    if (percentage >= 20) return 'text-risk-high font-semibold'
    return 'text-risk-critical font-bold'
  }
  
  const truncateText = (text, maxLength = 50) => {
    if (!text) return ''
    if (text.length <= maxLength) return text
    return text.substr(0, maxLength) + '...'
  }
  
  const capitalizeFirstLetter = (string) => {
    if (!string) return ''
    return string.charAt(0).toUpperCase() + string.slice(1)
  }
  
  const generateRandomId = () => {
    return Date.now().toString(36) + Math.random().toString(36).substr(2)
  }
  
  return {
    formatNumber,
    formatPercentage,
    formatCurrency,
    formatDate,
    formatTime,
    formatDateTime,
    getRiskBadgeClass,
    getRiskColor,
    getRiskLabel,
    getInfectionStatusClass,
    getVaccinationStatusClass,
    truncateText,
    capitalizeFirstLetter,
    generateRandomId
  }
}

// Export for use without composable
export const formatting = {
  formatNumber: (number) => {
    if (typeof number !== 'number') return '0'
    return number.toLocaleString()
  },
  
  formatPercentage: (value, total) => {
    if (!total || total === 0) return '0%'
    return Math.round((value / total) * 100) + '%'
  },
  
  getRiskBadgeClass: (riskLevel) => {
    const classes = {
      safe: 'bg-risk-safe/10 text-risk-safe border-risk-safe/20',
      low: 'bg-risk-low/10 text-risk-low border-risk-low/20',
      moderate: 'bg-risk-moderate/10 text-risk-moderate border-risk-moderate/20',
      high: 'bg-risk-high/10 text-risk-high border-risk-high/20',
      critical: 'bg-risk-critical/10 text-risk-critical border-risk-critical/20'
    }
    return classes[riskLevel] || classes.safe
  },
  
  getRiskLabel: (riskLevel) => {
    const labels = {
      safe: 'Safe',
      low: 'Low Risk',
      moderate: 'Moderate Risk',
      high: 'High Risk',
      critical: 'Critical'
    }
    return labels[riskLevel] || 'Safe'
  }
}