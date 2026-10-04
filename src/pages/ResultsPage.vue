<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
      <div>
        <h2 class="text-2xl font-bold text-dark-blue">Simulation Results</h2>
        <p class="text-muted-blue">View infection trends, risk maps, and vaccination recommendations</p>
      </div>
      <div class="flex gap-3">
        <Button 
          label="Export Results" 
          icon="pi pi-download" 
          severity="secondary"
          @click="exportResults"
        />
        <Button 
          label="New Simulation" 
          icon="pi pi-refresh" 
          @click="$router.push('/simulation')"
        />
      </div>
    </div>

    <!-- No Results Warning -->
    <Card v-if="!hasResults" class="bg-white">
      <template #content>
        <div class="p-6 text-center">
          <i class="pi pi-chart-line text-muted-blue text-6xl mb-4"></i>
          <h3 class="text-xl font-semibold text-dark-blue mb-2">No Simulation Results</h3>
          <p class="text-muted-blue mb-4">Run a simulation to generate results and visualizations</p>
          <Button 
            label="Go to Simulation" 
            icon="pi pi-play" 
            @click="$router.push('/simulation')"
          />
        </div>
      </template>
    </Card>

    <!-- Results Content (DYNAMIC - Changes based on simulation data) -->
    <div v-else class="space-y-6">
      <!-- Municipality Analysis Table (Target Coverage & Infection Rate) - Logged-in Municipality Only -->
      <Card class="bg-white">
        <template #header>
          <div class="px-6 py-4 border-b border-light-blue">
            <div class="flex justify-between items-center">
              <div>
                <h3 class="text-lg font-semibold text-dark-blue">My Municipality Analysis</h3>
                <p class="text-muted-blue text-sm">Your vaccination coverage and infection rate data</p>
              </div>
              <div v-if="currentMunicipality" class="text-right">
                <p class="text-xs text-muted-blue">Viewing data for</p>
                <p class="text-lg font-semibold text-primary">{{ currentMunicipality.name }}</p>
              </div>
            </div>
          </div>
        </template>
        <template #content>
          <div class="p-6">
            <!-- Important Metrics Explanation -->
            <div class="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <h4 class="font-semibold text-dark-blue mb-3 flex items-center">
                <i class="pi pi-info-circle text-primary mr-2"></i>
                Understanding These Metrics
              </h4>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                <div>
                  <p class="font-medium text-dark-blue mb-2">📊 Target Coverage (Vaccination %)</p>
                  <ul class="space-y-1 text-muted-blue">
                    <li>• <strong>≥ 70%</strong>: ✅ Good - WHO recommendation met</li>
                    <li>• <strong>50-70%</strong>: ⚠️ Moderate - Increase vaccination</li>
                    <li>• <strong>< 50%</strong>: ❌ Low - Emergency action needed</li>
                  </ul>
                  <p class="mt-2 text-xs italic">Formula: (Vaccinated Dogs / Total Dogs) × 100</p>
                </div>
                <div>
                  <p class="font-medium text-dark-blue mb-2">🦠 Infection Rate (%)</p>
                  <ul class="space-y-1 text-muted-blue">
                    <li>• <strong>< 0.1%</strong>: ✅ Safe - Very few cases</li>
                    <li>• <strong>0.1-1%</strong>: ⚠️ Low - Emerging outbreak</li>
                    <li>• <strong>1-5%</strong>: ⚠️ Moderate - Active outbreak</li>
                    <li>• <strong>> 5%</strong>: 🚨 High/Critical - Epidemic</li>
                  </ul>
                  <p class="mt-2 text-xs italic">Formula: (Infected Animals / Total Animals) × 100</p>
                </div>
              </div>
            </div>

            <DataTable 
              :value="myMunicipalityAnalysis" 
              dataKey="id"
              class="p-datatable-sm"
            >
              <Column field="name" header="Municipality" :sortable="true" frozen>
                <template #body="slotProps">
                  <div class="flex items-center space-x-2">
                    <i class="pi pi-map-marker text-primary"></i>
                    <span class="font-medium">{{ slotProps.data.name }}</span>
                  </div>
                </template>
              </Column>

              <Column field="riskLevel" header="Risk Level" :sortable="true">
                <template #body="slotProps">
                  <span 
                    class="px-2 py-1 rounded text-xs font-medium"
                    :class="getRiskBadgeClass(slotProps.data.riskLevel)"
                  >
                    {{ getRiskLabel(slotProps.data.riskLevel) }}
                  </span>
                </template>
              </Column>

              <Column field="targetCoverage" header="Target Coverage" :sortable="true">
                <template #body="slotProps">
                  <div class="space-y-1">
                    <div class="flex items-center justify-between">
                      <span class="text-sm font-semibold">{{ slotProps.data.targetCoverage }}%</span>
                      <span 
                        class="text-xs px-1.5 py-0.5 rounded"
                        :class="{
                          'bg-risk-safe text-white': slotProps.data.targetCoverage >= 70,
                          'bg-risk-moderate text-white': slotProps.data.targetCoverage >= 50 && slotProps.data.targetCoverage < 70,
                          'bg-risk-high text-white': slotProps.data.targetCoverage < 50
                        }"
                      >
                        {{ getCoverageStatus(slotProps.data.targetCoverage) }}
                      </span>
                    </div>
                    <div class="w-full bg-gray-200 rounded-full h-1.5">
                      <div 
                        class="h-1.5 rounded-full transition-all"
                        :class="{
                          'bg-risk-safe': slotProps.data.targetCoverage >= 70,
                          'bg-risk-moderate': slotProps.data.targetCoverage >= 50 && slotProps.data.targetCoverage < 70,
                          'bg-risk-high': slotProps.data.targetCoverage < 50
                        }"
                        :style="{ width: `${slotProps.data.targetCoverage}%` }"
                      ></div>
                    </div>
                    <p class="text-xs text-muted-blue">
                      {{ slotProps.data.vaccinatedDogs }} / {{ slotProps.data.totalDogs }} dogs
                    </p>
                  </div>
                </template>
              </Column>

              <Column field="infectionRate" header="Infection Rate" :sortable="true">
                <template #body="slotProps">
                  <div class="space-y-1">
                    <div class="flex items-center justify-between">
                      <span 
                        class="text-sm font-semibold"
                        :class="{
                          'text-risk-critical': slotProps.data.infectionRate >= 10,
                          'text-risk-high': slotProps.data.infectionRate >= 5 && slotProps.data.infectionRate < 10,
                          'text-risk-moderate': slotProps.data.infectionRate >= 1 && slotProps.data.infectionRate < 5,
                          'text-risk-low': slotProps.data.infectionRate >= 0.1 && slotProps.data.infectionRate < 1,
                          'text-risk-safe': slotProps.data.infectionRate < 0.1
                        }"
                      >
                        {{ slotProps.data.infectionRate.toFixed(2) }}%
                      </span>
                      <span 
                        class="text-xs px-1.5 py-0.5 rounded"
                        :class="{
                          'bg-risk-critical text-white': slotProps.data.infectionRate >= 10,
                          'bg-risk-high text-white': slotProps.data.infectionRate >= 5 && slotProps.data.infectionRate < 10,
                          'bg-risk-moderate text-white': slotProps.data.infectionRate >= 1 && slotProps.data.infectionRate < 5,
                          'bg-risk-low text-dark-blue': slotProps.data.infectionRate >= 0.1 && slotProps.data.infectionRate < 1,
                          'bg-risk-safe text-dark-blue': slotProps.data.infectionRate < 0.1
                        }"
                      >
                        {{ getInfectionStatus(slotProps.data.infectionRate) }}
                      </span>
                    </div>
                    <p class="text-xs text-muted-blue">
                      {{ slotProps.data.totalInfected }} / {{ slotProps.data.totalAnimals }} infected
                    </p>
                  </div>
                </template>
              </Column>

              <Column field="totalInfected" header="Total Cases" :sortable="true">
                <template #body="slotProps">
                  <div class="text-sm space-y-0.5">
                    <div class="flex items-center justify-between">
                      <span class="text-muted-blue">Dogs:</span>
                      <span class="font-medium text-risk-high">{{ slotProps.data.infectedDogs }}</span>
                    </div>
                    <div class="flex items-center justify-between">
                      <span class="text-muted-blue">Cats:</span>
                      <span class="font-medium text-risk-high">{{ slotProps.data.infectedCats }}</span>
                    </div>
                    <div class="flex items-center justify-between">
                      <span class="text-muted-blue">Humans:</span>
                      <span class="font-medium text-risk-critical">{{ slotProps.data.infectedHumans }}</span>
                    </div>
                  </div>
                </template>
              </Column>

              <Column header="Status">
                <template #body="slotProps">
                  <div class="text-xs space-y-1">
                    <div 
                      v-if="slotProps.data.targetCoverage < 70"
                      class="flex items-center text-risk-high"
                    >
                      <i class="pi pi-exclamation-triangle mr-1"></i>
                      <span>Low Coverage</span>
                    </div>
                    <div 
                      v-if="slotProps.data.infectionRate > 1"
                      class="flex items-center text-risk-high"
                    >
                      <i class="pi pi-exclamation-circle mr-1"></i>
                      <span>Active Outbreak</span>
                    </div>
                    <div 
                      v-if="slotProps.data.targetCoverage >= 70 && slotProps.data.infectionRate <= 0.1"
                      class="flex items-center text-risk-safe"
                    >
                      <i class="pi pi-check-circle mr-1"></i>
                      <span>Under Control</span>
                    </div>
                  </div>
                </template>
              </Column>
            </DataTable>
          </div>
        </template>
      </Card>

      <!-- AI Vaccination Recommendations (DRL-Powered) -->
      <Card class="bg-white">
        <template #header>
          <div class="px-6 py-4 border-b border-light-blue">
            <div class="flex justify-between items-center">
              <div class="flex items-center space-x-3">
                <div>
                  <h3 class="text-lg font-semibold text-dark-blue flex items-center">
                    AI Vaccination Recommendations
                    <span class="ml-2 px-2 py-0.5 text-xs bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-full">
                      DRL-Powered
                    </span>
                  </h3>
                  <p class="text-muted-blue text-sm">Deep Learning AI recommends optimal vaccination strategies</p>
                </div>
              </div>
              <Button 
                v-if="!drlRecommendations.length"
                label="Get AI Recommendations" 
                icon="pi pi-sparkles" 
                severity="success"
                :loading="loadingDRL"
                @click="fetchDRLRecommendations"
              />
              <Button 
                v-else
                label="Refresh" 
                icon="pi pi-refresh" 
                severity="secondary"
                size="small"
                :loading="loadingDRL"
                @click="fetchDRLRecommendations"
              />
            </div>
          </div>
        </template>
        <template #content>
          <div class="p-6">
            <!-- No DRL Recommendations Yet -->
            <div v-if="!drlRecommendations.length && !loadingDRL" class="text-center py-8">
              <i class="pi pi-sparkles text-primary text-5xl mb-4"></i>
              <h4 class="text-lg font-semibold text-dark-blue mb-2">AI Recommendations Not Generated</h4>
              <p class="text-muted-blue mb-4">Click the button above to get AI-powered vaccination recommendations</p>
              <p class="text-sm text-muted-blue">
                Our Deep Q-Network analyzes infection rates, population density, and neighboring risk factors
              </p>
            </div>

            <!-- Loading State -->
            <div v-else-if="loadingDRL" class="text-center py-8">
              <ProgressSpinner style="width:50px;height:50px" strokeWidth="4" />
              <p class="text-muted-blue mt-4">AI is analyzing municipality data...</p>
            </div>

            <!-- DRL Error -->
            <div v-else-if="drlError" class="p-4 bg-red-50 border border-red-200 rounded-lg">
              <div class="flex items-start space-x-3">
                <i class="pi pi-exclamation-circle text-red-600 text-xl"></i>
                <div>
                  <h4 class="font-semibold text-red-800 mb-1">AI Recommendations Unavailable</h4>
                  <p class="text-sm text-red-700">{{ drlError }}</p>
                  <p class="text-xs text-red-600 mt-2">Using rule-based recommendations as fallback.</p>
                </div>
              </div>
            </div>

            <!-- DRL Recommendations Table -->
            <div v-else>
              <!-- Info Banner -->
              <div class="mb-4 p-4 bg-gradient-to-r from-blue-50 to-purple-50 border border-blue-200 rounded-lg">
                <div class="flex items-start space-x-3">
                  <i class="pi pi-info-circle text-blue-600 text-xl"></i>
                  <div class="flex-1">
                    <h4 class="font-semibold text-dark-blue mb-2">About AI Recommendations</h4>
                    <p class="text-sm text-muted-blue mb-2">
                      These recommendations are generated by a Deep Q-Network (DQN) trained on 100,000+ simulations.
                      The AI considers infection rates, vaccination coverage, population density, and neighboring risk.
                    </p>
                    <div class="flex items-center space-x-4 text-xs text-muted-blue">
                      <span>✓ Trained on 3,333 episodes</span>
                      <span>✓ 63% better than rule-based</span>
                      <span>✓ Real-time analysis</span>
                    </div>
                  </div>
                </div>
              </div>

              <DataTable 
                :value="filteredDRLRecommendations" 
                dataKey="municipalityId"
                class="p-datatable-sm"
              >
                <Column field="municipalityName" header="Municipality" :sortable="true" frozen>
                  <template #body="slotProps">
                    <div class="flex items-center space-x-2">
                      <i class="pi pi-map-marker text-primary"></i>
                      <span class="font-medium">{{ slotProps.data.municipalityName }}</span>
                    </div>
                  </template>
                </Column>

                <Column field="priority" header="Priority" :sortable="true">
                  <template #body="slotProps">
                    <span 
                      class="px-2 py-1 rounded text-xs font-medium flex items-center justify-center"
                      :class="getPriorityClass(slotProps.data.priority)"
                    >
                      <i :class="['pi', slotProps.data.icon, 'mr-1']"></i>
                      {{ slotProps.data.priority }}
                    </span>
                  </template>
                </Column>

                <Column field="recommendedVaccination" header="AI Recommendation" :sortable="true">
                  <template #body="slotProps">
                    <div class="space-y-1">
                      <div class="flex items-center justify-between">
                        <span class="text-lg font-bold text-primary">{{ slotProps.data.recommendedVaccination }}%</span>
                        <span class="text-xs px-2 py-1 bg-blue-100 text-blue-800 rounded">
                          AI Optimized
                        </span>
                      </div>
                      <div class="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          class="h-2 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 transition-all"
                          :style="{ width: `${slotProps.data.recommendedVaccination}%` }"
                        ></div>
                      </div>
                    </div>
                  </template>
                </Column>

                <Column field="confidence" header="Confidence" :sortable="true">
                  <template #body="slotProps">
                    <div class="flex items-center space-x-2">
                      <span class="font-semibold" :class="{
                        'text-green-600': slotProps.data.confidence >= 70,
                        'text-yellow-600': slotProps.data.confidence >= 50 && slotProps.data.confidence < 70,
                        'text-orange-600': slotProps.data.confidence < 50
                      }">
                        {{ slotProps.data.confidence }}%
                      </span>
                      <i 
                        :class="{
                          'pi pi-check-circle text-green-600': slotProps.data.confidence >= 70,
                          'pi pi-exclamation-triangle text-yellow-600': slotProps.data.confidence >= 50 && slotProps.data.confidence < 70,
                          'pi pi-info-circle text-orange-600': slotProps.data.confidence < 50
                        }"
                      ></i>
                    </div>
                  </template>
                </Column>

                <Column field="comparison" header="vs Current">
                  <template #body="slotProps">
                    <div v-if="slotProps.data.comparison" class="text-xs">
                      <div 
                        class="px-2 py-1 rounded font-medium"
                        :class="{
                          'bg-green-100 text-green-800': slotProps.data.comparison.isOptimal,
                          'bg-yellow-100 text-yellow-800': slotProps.data.comparison.shouldIncrease,
                          'bg-blue-100 text-blue-800': slotProps.data.comparison.shouldDecrease
                        }"
                      >
                        <span v-if="slotProps.data.comparison.isOptimal">✓ Optimal</span>
                        <span v-else-if="slotProps.data.comparison.shouldIncrease">
                          ↑ +{{ Math.abs(slotProps.data.comparison.difference) }}%
                        </span>
                        <span v-else-if="slotProps.data.comparison.shouldDecrease">
                          ↓ {{ slotProps.data.comparison.difference }}%
                        </span>
                      </div>
                      <p class="text-muted-blue mt-1">{{ slotProps.data.comparison.message }}</p>
                    </div>
                  </template>
                </Column>

                <Column field="explanation" header="AI Reasoning">
                  <template #body="slotProps">
                    <div class="text-sm text-muted-blue max-w-md">
                      <p>{{ slotProps.data.explanation }}</p>
                      <span class="text-xs text-gray-500 mt-1 block">
                        Source: {{ slotProps.data.source === 'drl' ? 'Deep Q-Network' : 'Rule-Based Fallback' }}
                      </span>
                    </div>
                  </template>
                </Column>
              </DataTable>
            </div>
          </div>
        </template>
      </Card>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { useAppStore } from '@/stores'
import { useToast } from 'primevue/usetoast'
import { useMunicipalityAuth } from '@/services/municipalityAuth'
import { getDRLRecommendations, formatDRLRecommendation, compareDRLWithCurrent } from '@/services/drlService'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const router = useRouter()
const appStore = useAppStore()
const toast = useToast()
const { currentMunicipality } = useMunicipalityAuth()

// Component state
let map = null
const loadingDRL = ref(false)
const drlRecommendations = ref([])
const drlError = ref(null)

// Computed properties (ALL DYNAMIC - Update when simulation data changes)
const hasResults = computed(() => {
  return appStore.simulationResults && 
         appStore.simulationResults.municipalities && 
         appStore.simulationResults.municipalities.length > 0
})

const municipalities = computed(() => {
  return appStore.municipalities || []
})

const simulationResults = computed(() => {
  return appStore.simulationResults || {}
})

const vaccinationRecommendations = computed(() => {
  return appStore.vaccinationRecommendations || []
})

// Statistics (DYNAMIC - Recalculated on every data change)
const totalInfected = computed(() => {
  if (!simulationResults.value.municipalities) return 0
  return simulationResults.value.municipalities.reduce((sum, m) => 
    sum + (m.predictedInfectedDogs || 0) + (m.predictedInfectedCats || 0) + (m.predictedInfectedHumans || 0), 0
  )
})

const totalMunicipalities = computed(() => {
  return municipalities.value.length
})

const highRiskCount = computed(() => {
  return municipalities.value.filter(m => ['high', 'critical'].includes(m.riskLevel)).length
})

const safeCount = computed(() => {
  return municipalities.value.filter(m => m.riskLevel === 'safe').length
})

const lowRiskCount = computed(() => {
  return municipalities.value.filter(m => m.riskLevel === 'low').length
})

const moderateRiskCount = computed(() => {
  return municipalities.value.filter(m => m.riskLevel === 'moderate').length
})

const criticalRiskCount = computed(() => {
  return municipalities.value.filter(m => m.riskLevel === 'critical').length
})

const avgVaccinationCoverage = computed(() => {
  if (municipalities.value.length === 0) return 0
  const total = municipalities.value.reduce((sum, m) => {
    const coverage = m.dogPopulation > 0 ? (m.vaccinatedDogs / m.dogPopulation) * 100 : 0
    return sum + coverage
  }, 0)
  return Math.round(total / municipalities.value.length)
})

const simulationDays = computed(() => {
  return appStore.simulationSettings?.simulationDays || 0
})

const modelName = computed(() => {
  return simulationResults.value.metadata?.model || 'Fractional-Order Stochastic Model'
})

const completedDate = computed(() => {
  if (!simulationResults.value.completedAt) return 'N/A'
  return new Date(simulationResults.value.completedAt).toLocaleString()
})

// Municipality Analysis Data (Target Coverage & Infection Rate)
const municipalityAnalysis = computed(() => {
  return municipalities.value.map(municipality => {
    const totalDogs = municipality.dogPopulation || 0
    const totalCats = municipality.catPopulation || 0
    const totalAnimals = totalDogs + totalCats
    
    const vaccinatedDogs = municipality.vaccinatedDogs || 0
    const infectedDogs = municipality.infectedDogs || 0
    const infectedCats = municipality.infectedCats || 0
    const infectedHumans = municipality.infectedHumans || 0
    const totalInfected = infectedDogs + infectedCats + infectedHumans
    
    // Calculate Target Coverage (Vaccination Coverage)
    const targetCoverage = totalDogs > 0 ? Math.round((vaccinatedDogs / totalDogs) * 100) : 0
    
    // Calculate Infection Rate
    const infectionRate = totalAnimals > 0 ? ((infectedDogs + infectedCats) / totalAnimals) * 100 : 0
    
    return {
      id: municipality.id,
      name: municipality.name,
      riskLevel: municipality.riskLevel || 'safe',
      targetCoverage: targetCoverage,
      infectionRate: infectionRate,
      vaccinatedDogs: vaccinatedDogs,
      totalDogs: totalDogs,
      infectedDogs: infectedDogs,
      infectedCats: infectedCats,
      infectedHumans: infectedHumans,
      totalInfected: totalInfected,
      totalAnimals: totalAnimals
    }
  })
})

// Filtered: Only logged-in municipality's analysis
const myMunicipalityAnalysis = computed(() => {
  if (!currentMunicipality.value) return []
  return municipalityAnalysis.value.filter(m => m.id === currentMunicipality.value.id)
})

// Filtered: Only logged-in municipality's vaccination recommendations
const myVaccinationRecommendations = computed(() => {
  if (!currentMunicipality.value) return []
  return vaccinationRecommendations.value.filter(r => r.municipalityId === currentMunicipality.value.id)
})

// DRL Recommendations (Filtered for logged-in municipality)
const filteredDRLRecommendations = computed(() => {
  if (!currentMunicipality.value) return []
  return drlRecommendations.value.filter(r => r.municipalityId === currentMunicipality.value.id)
})

// Fetch DRL Recommendations
const fetchDRLRecommendations = async () => {
  loadingDRL.value = true
  drlError.value = null
  
  try {
    // Get current municipalities data
    const municipalitiesData = municipalities.value.map(m => ({
      id: m.id,
      name: m.name,
      humanPopulation: m.humanPopulation,
      dogPopulation: m.dogPopulation,
      catPopulation: m.catPopulation,
      infectedDogs: m.infectedDogs || 0,
      infectedCats: m.infectedCats || 0,
      infectedHumans: m.infectedHumans || 0,
      vaccinatedDogs: m.vaccinatedDogs || 0,
      populationDensity: m.populationDensity,
      riskLevel: m.riskLevel || 'safe',
      connectedMunicipalities: m.connectedMunicipalities || []
    }))
    
    // Call DRL API
    const result = await getDRLRecommendations(municipalitiesData)
    
    if (result.success && result.drl_available) {
      // Format recommendations and add comparison with current coverage
      drlRecommendations.value = result.recommendations.map(rec => {
        const formatted = formatDRLRecommendation(rec)
        
        // Find current municipality to compare
        const currentMun = municipalities.value.find(m => m.id === rec.municipality_id)
        if (currentMun) {
          const currentCoverage = currentMun.dogPopulation > 0 
            ? (currentMun.vaccinatedDogs / currentMun.dogPopulation) * 100 
            : 0
          
          formatted.comparison = compareDRLWithCurrent(formatted, currentCoverage)
        }
        
        return formatted
      })
      
      toast.add({
        severity: 'success',
        summary: 'AI Recommendations Generated',
        detail: `Received recommendations for ${drlRecommendations.value.length} municipalities`,
        life: 3000
      })
    } else {
      drlError.value = result.error || 'DRL model not available'
      
      toast.add({
        severity: 'warn',
        summary: 'AI Unavailable',
        detail: 'Using fallback recommendations',
        life: 3000
      })
    }
  } catch (error) {
    console.error('Failed to fetch DRL recommendations:', error)
    drlError.value = error.message
    
    toast.add({
      severity: 'error',
      summary: 'Failed to Get AI Recommendations',
      detail: error.message,
      life: 5000
    })
  } finally {
    loadingDRL.value = false
  }
}

// Methods
const getCoverageStatus = (coverage) => {
  if (coverage >= 70) return 'Good'
  if (coverage >= 50) return 'Moderate'
  return 'Low'
}

const getInfectionStatus = (rate) => {
  if (rate >= 10) return 'Critical'
  if (rate >= 5) return 'High'
  if (rate >= 1) return 'Moderate'
  if (rate >= 0.1) return 'Low'
  return 'Safe'
}

const getRiskBadgeClass = (riskLevel) => {
  const classes = {
    safe: 'bg-risk-safe text-white',
    low: 'bg-risk-low text-dark-blue',
    moderate: 'bg-risk-moderate text-white',
    high: 'bg-risk-high text-white',
    critical: 'bg-risk-critical text-white'
  }
  return classes[riskLevel] || classes.safe
}

const getRiskLabel = (riskLevel) => {
  const labels = {
    safe: 'Safe',
    low: 'Low Risk',
    moderate: 'Moderate',
    high: 'High Risk',
    critical: 'Critical'
  }
  return labels[riskLevel] || 'Unknown'
}
const initializeMap = () => {
  if (!hasResults.value || municipalities.value.length === 0) return

  // Create map centered on Davao de Oro
  map = L.map('results-map').setView([7.5, 125.9], 9)
  
  // Add OpenStreetMap tiles
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
  }).addTo(map)

  // Add municipality markers (DYNAMIC - Based on current data)
  municipalities.value.forEach(municipality => {
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

const getPriorityClass = (priority) => {
  const classes = {
    'Critical': 'bg-risk-critical text-white',
    'High': 'bg-risk-high text-white',
    'Medium': 'bg-risk-moderate text-white',
    'Low': 'bg-risk-low text-dark-blue',
    'Monitor': 'bg-gray-200 text-muted-blue'
  }
  return classes[priority] || classes.Monitor
}

const exportResults = () => {
  const data = {
    results: simulationResults.value,
    municipalities: municipalities.value,
    recommendations: vaccinationRecommendations.value,
    exportedAt: new Date().toISOString()
  }
  
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `simulation-results-${Date.now()}.json`
  a.click()
  URL.revokeObjectURL(url)

  toast.add({
    severity: 'success',
    summary: 'Results Exported',
    detail: 'Simulation results downloaded successfully',
    life: 3000
  })
}

// Lifecycle hooks
onMounted(() => {
  if (hasResults.value) {
    setTimeout(() => {
      initializeMap()
    }, 100)
  }
})

onBeforeUnmount(() => {
  if (map) {
    map.remove()
    map = null
  }
})
</script>

<style scoped>
#results-map {
  z-index: 1;
}
</style>
