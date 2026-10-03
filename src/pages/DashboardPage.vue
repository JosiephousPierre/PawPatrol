<template>
  <div class="space-y-6">
    <!-- Summary Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <template v-if="isLoadingData">
        <SkeletonCard v-for="i in 4" :key="i" />
      </template>
      
      <template v-else>
      <!-- Total Dog Population -->
      <Card class="bg-white hover:shadow-card transition-shadow">
        <template #content>
          <div class="p-6">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-muted-blue text-sm font-medium mb-1">Total Dog Population</p>
                <p class="text-4xl font-bold text-dark-blue">{{ formatNumber(appStore.totalDogPopulation) }}</p>
                <p class="text-xs text-muted-blue mt-1">Primary rabies hosts</p>
              </div>
              <div class="w-16 h-16 bg-primary/10 rounded-xl flex items-center justify-center">
                <i class="pi pi-heart text-primary text-2xl"></i>
              </div>
            </div>
          </div>
        </template>
      </Card>

      <!-- Total Cat Population -->
      <Card class="bg-white hover:shadow-card transition-shadow">
        <template #content>
          <div class="p-6">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-muted-blue text-sm font-medium mb-1">Total Cat Population</p>
                <p class="text-4xl font-bold text-dark-blue">{{ formatNumber(appStore.totalCatPopulation) }}</p>
                <p class="text-xs text-muted-blue mt-1">Secondary hosts</p>
              </div>
              <div class="w-16 h-16 bg-primary/10 rounded-xl flex items-center justify-center">
                <i class="pi pi-heart text-primary text-2xl"></i>
              </div>
            </div>
          </div>
        </template>
      </Card>

      <!-- Total Human Population -->
      <Card class="bg-white hover:shadow-card transition-shadow">
        <template #content>
          <div class="p-6">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-muted-blue text-sm font-medium mb-1">Total Human Population</p>
                <p class="text-4xl font-bold text-dark-blue">{{ formatNumber(appStore.totalHumanPopulation) }}</p>
                <p class="text-xs text-muted-blue mt-1">At-risk population</p>
              </div>
              <div class="w-16 h-16 bg-primary/10 rounded-xl flex items-center justify-center">
                <i class="pi pi-users text-primary text-2xl"></i>
              </div>
            </div>
          </div>
        </template>
      </Card>
      </template>
    </div>

    <!-- Infection Status Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <template v-if="isLoadingData">
        <SkeletonCard v-for="i in 4" :key="`infection-${i}`" />
      </template>
      
      <template v-else>
      <!-- Infected Dogs -->
      <Card class="bg-white hover:shadow-card transition-shadow border-l-4 border-l-risk-high">
        <template #content>
          <div class="p-6">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-muted-blue text-sm font-medium mb-1">Infected Dogs</p>
                <p class="text-4xl font-bold" :class="infectionColor(appStore.currentInfectedDogs)">
                  {{ appStore.currentInfectedDogs }}
                </p>
                <p class="text-xs text-muted-blue mt-1">Active cases</p>
              </div>
              <div class="w-16 h-16 bg-risk-high/10 rounded-xl flex items-center justify-center">
                <i class="pi pi-exclamation-triangle text-risk-high text-2xl"></i>
              </div>
            </div>
          </div>
        </template>
      </Card>

      <!-- Infected Cats -->
      <Card class="bg-white hover:shadow-card transition-shadow border-l-4 border-l-risk-moderate">
        <template #content>
          <div class="p-6">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-muted-blue text-sm font-medium mb-1">Infected Cats</p>
                <p class="text-4xl font-bold" :class="infectionColor(appStore.currentInfectedCats)">
                  {{ appStore.currentInfectedCats }}
                </p>
                <p class="text-xs text-muted-blue mt-1">Secondary cases</p>
              </div>
              <div class="w-16 h-16 bg-risk-moderate/10 rounded-xl flex items-center justify-center">
                <i class="pi pi-exclamation-triangle text-risk-moderate text-2xl"></i>
              </div>
            </div>
          </div>
        </template>
      </Card>

      <!-- Infected Humans -->
      <Card class="bg-white hover:shadow-card transition-shadow border-l-4 border-l-risk-critical">
        <template #content>
          <div class="p-6">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-muted-blue text-sm font-medium mb-1">Infected Humans</p>
                <p class="text-4xl font-bold" :class="infectionColor(appStore.currentInfectedHumans)">
                  {{ appStore.currentInfectedHumans }}
                </p>
                <p class="text-xs text-muted-blue mt-1">Critical cases</p>
              </div>
              <div class="w-16 h-16 bg-risk-critical/10 rounded-xl flex items-center justify-center">
                <i class="pi pi-exclamation-triangle text-risk-critical text-2xl"></i>
              </div>
            </div>
          </div>
        </template>
      </Card>
      </template>
    </div>

    <!-- Charts Section -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Regional Risk Map -->
      <Card class="bg-white">
        <template #header>
          <div class="px-6 py-4 border-b border-light-blue">
            <h3 class="text-lg font-semibold text-dark-blue">Regional Risk Map</h3>
            <p class="text-muted-blue text-sm">Interactive visualization of rabies risk across Davao de Oro</p>
          </div>
        </template>
        <template #content>
          <div class="p-6">
            <!-- Map Container (DYNAMIC - Updates with simulation data) -->
            <div id="dashboard-map" class="w-full h-96 rounded-lg border border-light-blue"></div>
            
            <!-- Map Legend (DYNAMIC) -->
            <div class="mt-4 flex flex-wrap gap-4 justify-center">
              <div class="flex items-center space-x-2">
                <div class="w-4 h-4 rounded-full bg-risk-safe"></div>
                <span class="text-sm text-muted-blue">Safe ({{ safeCount }})</span>
              </div>
              <div class="flex items-center space-x-2">
                <div class="w-4 h-4 rounded-full bg-risk-low"></div>
                <span class="text-sm text-muted-blue">Low Risk ({{ lowRiskCount }})</span>
              </div>
              <div class="flex items-center space-x-2">
                <div class="w-4 h-4 rounded-full bg-risk-moderate"></div>
                <span class="text-sm text-muted-blue">Moderate ({{ moderateRiskCount }})</span>
              </div>
              <div class="flex items-center space-x-2">
                <div class="w-4 h-4 rounded-full bg-risk-high"></div>
                <span class="text-sm text-muted-blue">High Risk ({{ highRiskCount }})</span>
              </div>
              <div class="flex items-center space-x-2">
                <div class="w-4 h-4 rounded-full bg-risk-critical"></div>
                <span class="text-sm text-muted-blue">Critical ({{ criticalRiskCount }})</span>
              </div>
            </div>
          </div>
        </template>
      </Card>

      <!-- Population Distribution Chart -->
      <Card class="bg-white">
        <template #header>
          <div class="px-6 py-4 border-b border-light-blue">
            <h3 class="text-lg font-semibold text-dark-blue">Population Distribution</h3>
          </div>
        </template>
        <template #content>
          <div class="p-6">
            <div v-if="isLoadingCharts" class="h-64 flex items-center justify-center">
              <LoadingSpinner size="lg" text="Loading population chart..." pulse />
            </div>
            <div v-else>
              <canvas ref="populationChartRef" width="400" height="200"></canvas>
            </div>
          </div>
        </template>
      </Card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAppStore } from '@/stores'
import { Chart, registerables } from 'chart.js'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import SkeletonCard from '@/components/SkeletonCard.vue'

Chart.register(...registerables)

const router = useRouter()
const appStore = useAppStore()
const populationChartRef = ref(null)

// Map reference
let map = null

// Loading states
const isLoadingData = ref(true)
const isLoadingCharts = ref(true)

const riskDistribution = computed(() => {
  const municipalities = appStore.municipalities
  const total = municipalities.length
  
  const distribution = municipalities.reduce((acc, municipality) => {
    const level = municipality.riskLevel || 'safe'
    acc[level] = (acc[level] || 0) + 1
    return acc
  }, {})

  return [
    { level: 'safe', label: 'Safe', count: distribution.safe || 0, percentage: Math.round(((distribution.safe || 0) / total) * 100) },
    { level: 'low', label: 'Low Risk', count: distribution.low || 0, percentage: Math.round(((distribution.low || 0) / total) * 100) },
    { level: 'moderate', label: 'Moderate', count: distribution.moderate || 0, percentage: Math.round(((distribution.moderate || 0) / total) * 100) },
    { level: 'high', label: 'High Risk', count: distribution.high || 0, percentage: Math.round(((distribution.high || 0) / total) * 100) },
    { level: 'critical', label: 'Critical', count: distribution.critical || 0, percentage: Math.round(((distribution.critical || 0) / total) * 100) }
  ]
})

// Computed properties for municipalities by risk level
const safeMunicipalities = computed(() => {
  return appStore.municipalities.filter(m => (m.riskLevel || 'safe') === 'safe').map(m => m.name)
})

const lowRiskMunicipalities = computed(() => {
  return appStore.municipalities.filter(m => m.riskLevel === 'low').map(m => m.name)
})

const moderateRiskMunicipalities = computed(() => {
  return appStore.municipalities.filter(m => m.riskLevel === 'moderate').map(m => m.name)
})

const highRiskMunicipalities = computed(() => {
  return appStore.municipalities.filter(m => m.riskLevel === 'high').map(m => m.name)
})

const criticalMunicipalities = computed(() => {
  return appStore.municipalities.filter(m => m.riskLevel === 'critical').map(m => m.name)
})

// Risk counts for map legend
const safeCount = computed(() => safeMunicipalities.value.length)
const lowRiskCount = computed(() => lowRiskMunicipalities.value.length)
const moderateRiskCount = computed(() => moderateRiskMunicipalities.value.length)
const highRiskCount = computed(() => highRiskMunicipalities.value.length)
const criticalRiskCount = computed(() => criticalMunicipalities.value.length)

// Helper function to get municipalities for a specific risk level
const getMunicipalitiesByRisk = (level) => {
  switch(level) {
    case 'safe': return safeMunicipalities.value
    case 'low': return lowRiskMunicipalities.value
    case 'moderate': return moderateRiskMunicipalities.value
    case 'high': return highRiskMunicipalities.value
    case 'critical': return criticalMunicipalities.value
    default: return []
  }
}

// Format municipality list for tooltip
const formatMunicipalityTooltip = (municipalities) => {
  if (municipalities.length === 0) {
    return 'No municipalities in this category'
  }
  return municipalities.map(name => `• ${name}`).join('\n')
}

const formatNumber = (num) => {
  return num.toLocaleString()
}

const formatTime = (date) => {
  return date.toLocaleTimeString()
}

const infectionColor = (count) => {
  if (count === 0) return 'text-risk-safe'
  if (count < 5) return 'text-risk-low'
  if (count < 10) return 'text-risk-moderate'
  return 'text-risk-high'
}

const getRiskColorClass = (level) => {
  const colors = {
    safe: 'bg-risk-safe',
    low: 'bg-risk-low',
    moderate: 'bg-risk-moderate',
    high: 'bg-risk-high',
    critical: 'bg-risk-critical'
  }
  return colors[level] || 'bg-muted-blue'
}

const navigateTo = (path) => {
  router.push(path)
}

// Map initialization
const initializeMap = () => {
  if (appStore.municipalities.length === 0) return

  // Create map centered on Davao de Oro
  map = L.map('dashboard-map').setView([7.5, 125.9], 9)
  
  // Add OpenStreetMap tiles
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
  }).addTo(map)

  // Add municipality markers (DYNAMIC - Based on current data)
  appStore.municipalities.forEach(municipality => {
    const riskColor = getRiskColor(municipality.riskLevel)
    
    // Create circle marker
    const marker = L.circleMarker([municipality.latitude, municipality.longitude], {
      radius: 10,
      fillColor: riskColor,
      color: '#fff',
      weight: 2,
      opacity: 1,
      fillOpacity: 0.8
    })

    // Add popup with DYNAMIC data
    marker.bindPopup(`
      <div class="text-sm">
        <h4 class="font-semibold text-dark-blue mb-2">${municipality.name}</h4>
        <p class="text-muted-blue">Risk Level: <span class="font-medium">${municipality.riskLevel}</span></p>
        <p class="text-muted-blue">Infected: ${municipality.infectedDogs || 0} dogs</p>
        <p class="text-muted-blue">Vaccinated: ${municipality.vaccinatedDogs || 0} dogs</p>
        <p class="text-muted-blue mt-1 text-xs">Last updated: ${municipality.lastUpdated ? new Date(municipality.lastUpdated).toLocaleDateString() : 'N/A'}</p>
      </div>
    `)

    marker.addTo(map)
  })
}

const getRiskColor = (riskLevel) => {
  const colors = {
    safe: '#10b981',      // Green
    low: '#fbbf24',       // Yellow
    moderate: '#f97316',  // Orange
    high: '#ef4444',      // Red
    critical: '#7f1d1d'   // Dark Red
  }
  return colors[riskLevel] || colors.safe
}

onMounted(() => {
  // Simulate loading delay for better UX
  setTimeout(() => {
    isLoadingData.value = false
    
    // Set loading to false first so canvas renders
    isLoadingCharts.value = false
    
    // Initialize charts and map after canvas is rendered
    setTimeout(() => {
      // Initialize population chart
      if (populationChartRef.value) {
        const ctx = populationChartRef.value.getContext('2d')
        new Chart(ctx, {
          type: 'doughnut',
          data: {
            labels: ['Dogs', 'Cats', 'Humans'],
            datasets: [{
              data: [
                appStore.totalDogPopulation,
                appStore.totalCatPopulation,
                appStore.totalHumanPopulation
              ],
              backgroundColor: ['#5289AD', '#698696', '#243C4C'],
              borderWidth: 0,
              hoverBorderWidth: 2,
              hoverBorderColor: '#fff'
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                position: 'bottom',
                labels: {
                  padding: 20,
                  usePointStyle: true,
                  font: {
                    family: 'Inter'
                  }
                }
              },
              tooltip: {
                callbacks: {
                  label: function(context) {
                    const label = context.label || ''
                    const value = context.parsed.toLocaleString()
                    const percentage = ((context.parsed / (appStore.totalDogPopulation + appStore.totalCatPopulation + appStore.totalHumanPopulation)) * 100).toFixed(1)
                    return `${label}: ${value} (${percentage}%)`
                  }
                }
              }
            },
            animation: {
              animateScale: true,
              animateRotate: true
            }
          }
        })
      }
      
      // Initialize map
      initializeMap()
    }, 100) // Small delay to let Vue render the canvas and map div
  }, 500) // Reduced from 800ms
})
</script>

<style scoped>
#dashboard-map {
  z-index: 1;
}

:deep(.p-tooltip) {
  min-width: 280px !important;
  max-width: 450px !important;
}

:deep(.p-tooltip .p-tooltip-text) {
  white-space: pre-line !important;
  padding: 16px 24px !important;
  font-size: 15px !important;
  line-height: 1.8 !important;
  background-color: #243C4C !important;
  color: white !important;
  border-radius: 12px !important;
  box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1) !important;
  min-width: 280px !important;
  display: block !important;
  width: max-content !important;
}

:deep(.p-tooltip .p-tooltip-arrow) {
  border-left-color: #243C4C !important;
}

:deep(.p-tooltip-left .p-tooltip-arrow) {
  border-left-color: #243C4C !important;
}
</style>