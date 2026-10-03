<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
      <div>
        <h2 class="text-2xl font-bold text-dark-blue">Predictive Risk Analysis</h2>
        <p class="text-muted-blue">AI-powered future risk forecasting for your municipality</p>
      </div>
      <div class="flex items-center gap-3">
        <div v-if="currentMunicipality" class="text-right mr-4">
          <p class="text-sm text-muted-blue">Forecasting for</p>
          <p class="text-lg font-semibold text-primary">{{ currentMunicipality.name }}</p>
        </div>
        <Dropdown 
          v-model="selectedForecastDays" 
          :options="forecastDaysOptions"
          optionLabel="label"
          optionValue="value"
          class="w-40"
          @change="updateForecast"
        />
        <Button 
          label="Export Predictions" 
          icon="pi pi-download" 
          severity="secondary"
          @click="exportPredictions"
        />
      </div>
    </div>

    <!-- No Login Warning -->
    <Card v-if="!currentMunicipality" class="bg-white">
      <template #content>
        <div class="p-6 text-center">
          <i class="pi pi-lock text-muted-blue text-6xl mb-4"></i>
          <h3 class="text-xl font-semibold text-dark-blue mb-2">Access Required</h3>
          <p class="text-muted-blue mb-4">Please log in with your municipality access code</p>
          <Button 
            label="Go to Login" 
            icon="pi pi-sign-in" 
            @click="navigateTo('/municipality-login')"
          />
        </div>
      </template>
    </Card>

    <!-- No Results Warning -->
    <Card v-else-if="!hasSimulationResults" class="bg-white">
      <template #content>
        <div class="p-6 text-center">
          <i class="pi pi-chart-line text-muted-blue text-6xl mb-4"></i>
          <h3 class="text-xl font-semibold text-dark-blue mb-2">No Simulation Data</h3>
          <p class="text-muted-blue mb-4">Run a simulation to generate predictive analysis.</p>
          <Button 
            label="Go to Simulation" 
            icon="pi pi-play" 
            @click="navigateTo('/simulation')"
          />
        </div>
      </template>
    </Card>

    <!-- Predictive Analysis Content (Municipality-Specific) -->
    <div v-else-if="myPrediction" class="space-y-6">
      <!-- Summary Statistics for My Municipality -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card class="bg-white border-l-4 border-l-primary">
          <template #content>
            <div class="p-4">
              <p class="text-xs text-muted-blue mb-1 font-medium">CURRENT INFECTED</p>
              <p class="text-4xl font-bold text-primary">{{ myPrediction.currentInfected }}</p>
              <p class="text-xs text-muted-blue mt-1">{{ myPrediction.currentInfectionRate.toFixed(2) }}% infection rate</p>
            </div>
          </template>
        </Card>

        <Card class="bg-white border-l-4 border-l-orange-500">
          <template #content>
            <div class="p-4">
              <p class="text-xs text-muted-blue mb-1 font-medium">PREDICTED INFECTED</p>
              <p class="text-4xl font-bold text-orange-600">{{ myPrediction.predictedInfected }}</p>
              <p class="text-xs text-muted-blue mt-1">In {{ selectedForecastDays }} days</p>
            </div>
          </template>
        </Card>

        <Card class="bg-white border-l-4" :class="getRiskTrendClass(myPrediction.riskChange)">
          <template #content>
            <div class="p-4">
              <p class="text-xs text-muted-blue mb-1 font-medium">RISK TREND</p>
              <p class="text-4xl font-bold" :class="getRiskTrendColor(myPrediction.riskChange)">
                <i :class="getRiskTrendIcon(myPrediction.riskChange)" class="text-3xl"></i>
              </p>
              <p class="text-xs text-muted-blue mt-1 capitalize">{{ myPrediction.riskChange }}</p>
            </div>
          </template>
        </Card>

        <Card class="bg-white border-l-4" :class="getPredictedRiskBorderClass(myPrediction.predictedRiskLevel)">
          <template #content>
            <div class="p-4">
              <p class="text-xs text-muted-blue mb-1 font-medium">PREDICTED RISK</p>
              <p class="text-2xl font-bold" :class="getPredictedRiskColorClass(myPrediction.predictedRiskLevel)">
                {{ myPrediction.predictedRiskLevel.toUpperCase() }}
              </p>
              <p class="text-xs text-muted-blue mt-1">{{ myPrediction.predictedInfectionRate.toFixed(2) }}% infection rate</p>
            </div>
          </template>
        </Card>
      </div>

      <!-- Risk Alert -->
      <Card v-if="myPrediction.riskChange === 'increasing'" class="bg-yellow-50 border-l-4 border-l-yellow-500">
        <template #content>
          <div class="p-6">
            <div class="flex items-start space-x-3">
              <i class="pi pi-exclamation-triangle text-yellow-600 text-3xl mt-1"></i>
              <div class="flex-1">
                <h4 class="text-xl font-semibold text-yellow-800 mb-2">⚠️ Risk Increasing Alert</h4>
                <p class="text-sm text-yellow-700 mb-2">
                  Your municipality is predicted to reach <strong>{{ myPrediction.predictedRiskLevel.toUpperCase() }}</strong> risk level within {{ selectedForecastDays }} days.
                </p>
                <p class="text-sm text-yellow-700">
                  Infections may increase from <strong>{{ myPrediction.currentInfected }}</strong> to <strong>{{ myPrediction.predictedInfected }}</strong> animals.
                </p>
              </div>
            </div>
          </div>
        </template>
      </Card>

      <!-- Success Alert -->
      <Card v-else-if="myPrediction.riskChange === 'decreasing'" class="bg-green-50 border-l-4 border-l-green-500">
        <template #content>
          <div class="p-6">
            <div class="flex items-start space-x-3">
              <i class="pi pi-check-circle text-green-600 text-3xl mt-1"></i>
              <div class="flex-1">
                <h4 class="text-xl font-semibold text-green-800 mb-2">✅ Risk Decreasing</h4>
                <p class="text-sm text-green-700 mb-2">
                  Good news! Your municipality's risk is predicted to improve to <strong>{{ myPrediction.predictedRiskLevel.toUpperCase() }}</strong> level.
                </p>
                <p class="text-sm text-green-700">
                  Expected reduction: <strong>{{ myPrediction.currentInfected }}</strong> → <strong>{{ myPrediction.predictedInfected }}</strong> infected animals.
                </p>
              </div>
            </div>
          </div>
        </template>
      </Card>

      <!-- My Municipality Prediction Details -->
      <Card class="bg-white">
        <template #header>
          <div class="px-6 py-4 border-b border-light-blue">
            <h3 class="text-lg font-semibold text-dark-blue">Detailed Prediction for {{ currentMunicipality.name }}</h3>
            <p class="text-muted-blue text-sm">{{ selectedForecastDays }}-day risk forecast and analysis</p>
          </div>
        </template>
        <template #content>
          <div class="p-6">
            <DataTable 
              :value="[myPrediction]" 
              dataKey="municipalityId"
              class="p-datatable-sm"
            >
              <Column field="municipalityName" header="Municipality" :sortable="true">
                <template #body="slotProps">
                  <div class="flex items-center space-x-2">
                    <i class="pi pi-map-marker text-primary text-sm"></i>
                    <span class="font-medium">{{ slotProps.data.municipalityName }}</span>
                  </div>
                </template>
              </Column>

              <Column field="currentRiskLevel" header="Current Risk" :sortable="true">
                <template #body="slotProps">
                  <span 
                    class="px-2 py-1 rounded text-xs font-medium"
                    :class="getRiskBadgeClass(slotProps.data.currentRiskLevel)"
                  >
                    {{ getRiskLabel(slotProps.data.currentRiskLevel) }}
                  </span>
                </template>
              </Column>

              <Column field="predictedRiskLevel" header="Predicted Risk" :sortable="true">
                <template #body="slotProps">
                  <span 
                    class="px-2 py-1 rounded text-xs font-medium"
                    :class="getRiskBadgeClass(slotProps.data.predictedRiskLevel)"
                  >
                    {{ getRiskLabel(slotProps.data.predictedRiskLevel) }}
                  </span>
                </template>
              </Column>

              <Column field="riskChange" header="Trend" :sortable="true">
                <template #body="slotProps">
                  <span 
                    class="flex items-center space-x-1 text-sm font-medium"
                    :class="{
                      'text-risk-high': slotProps.data.riskChange === 'increasing',
                      'text-muted-blue': slotProps.data.riskChange === 'stable',
                      'text-risk-safe': slotProps.data.riskChange === 'decreasing'
                    }"
                  >
                    <i 
                      :class="{
                        'pi pi-arrow-up': slotProps.data.riskChange === 'increasing',
                        'pi pi-minus': slotProps.data.riskChange === 'stable',
                        'pi pi-arrow-down': slotProps.data.riskChange === 'decreasing'
                      }"
                    ></i>
                    <span class="capitalize">{{ slotProps.data.riskChange }}</span>
                  </span>
                </template>
              </Column>

              <Column field="predictedInfected" header="Predicted Infections" :sortable="true">
                <template #body="slotProps">
                  <div class="text-sm">
                    <span class="font-semibold">{{ slotProps.data.predictedInfected }}</span>
                    <span class="text-muted-blue text-xs ml-1">
                      ({{ slotProps.data.predictedInfectionRate?.toFixed(1) || 0 }}%)
                    </span>
                  </div>
                </template>
              </Column>

              <Column field="growthRate" header="Growth Rate" :sortable="true">
                <template #body="slotProps">
                  <span 
                    class="text-sm font-medium"
                    :class="{
                      'text-risk-high': slotProps.data.growthRate > 0.05,
                      'text-risk-moderate': slotProps.data.growthRate > 0.02 && slotProps.data.growthRate <= 0.05,
                      'text-risk-safe': slotProps.data.growthRate <= 0.02
                    }"
                  >
                    {{ (slotProps.data.growthRate * 100).toFixed(2) }}% / day
                  </span>
                </template>
              </Column>

              <Column field="confidence" header="Confidence" :sortable="true">
                <template #body="slotProps">
                  <span 
                    class="px-2 py-1 rounded text-xs font-medium"
                    :class="{
                      'bg-green-100 text-green-700': slotProps.data.confidence === 'high',
                      'bg-yellow-100 text-yellow-700': slotProps.data.confidence === 'medium',
                      'bg-gray-100 text-gray-700': slotProps.data.confidence === 'low'
                    }"
                  >
                    {{ slotProps.data.confidence }}
                  </span>
                </template>
              </Column>

              <Column header="Actions" :exportable="false">
                <template #body="slotProps">
                  <Button 
                    icon="pi pi-eye" 
                    size="small"
                    text 
                    @click="viewPredictionDetails(slotProps.data)" 
                    v-tooltip.top="'View Forecast Details'"
                  />
                </template>
              </Column>
            </DataTable>
          </div>
        </template>
      </Card>

      <!-- Forecast Info -->
      <Card class="bg-white">
        <template #content>
          <div class="p-4 flex items-center justify-between text-sm">
            <div class="flex items-center space-x-2 text-muted-blue">
              <i class="pi pi-info-circle"></i>
              <span>Predictions based on current infection trends and vaccination rates</span>
            </div>
            <div class="text-muted-blue">
              <span class="font-medium">Average growth rate:</span>
              <span class="ml-2 font-bold text-primary">{{ ((predictiveAnalysis.averageGrowthRate || 0) * 100).toFixed(2) }}% per day</span>
            </div>
          </div>
        </template>
      </Card>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAppStore } from '@/stores'
import { useToast } from 'primevue/usetoast'
import { useFormatting } from '@/composables/useFormatting'
import { useMunicipalityAuth } from '@/services/municipalityAuth'
import { 
  generatePredictiveAnalysisSummary,
  identifyFutureHighRiskMunicipalities,
  predictFutureRiskLevel
} from '@/utils/simulationUtils'

const router = useRouter()
const appStore = useAppStore()
const toast = useToast()
const { getRiskBadgeClass, getRiskLabel } = useFormatting()
const { currentMunicipality } = useMunicipalityAuth()

// Component state
const selectedForecastDays = ref(30)
const showPredictionDialog = ref(false)
const selectedPrediction = ref(null)

// Options
const forecastDaysOptions = [
  { label: '7 Days', value: 7 },
  { label: '14 Days', value: 14 },
  { label: '30 Days', value: 30 },
  { label: '60 Days', value: 60 },
  { label: '90 Days', value: 90 }
]

// Computed properties
const hasSimulationResults = computed(() => {
  return appStore.simulationResults && 
         appStore.simulationResults.dailyData && 
         appStore.simulationResults.dailyData.length > 0
})

// Get prediction for ONLY the logged-in municipality
const myPrediction = computed(() => {
  if (!currentMunicipality.value || !hasSimulationResults.value) return null
  
  const municipality = appStore.municipalities.find(m => m.id === currentMunicipality.value.id)
  if (!municipality) return null
  
  return predictFutureRiskLevel(municipality, null, selectedForecastDays.value)
})

// Predictive analysis summary (for template reference)
const predictiveAnalysis = computed(() => {
  if (!myPrediction.value) return { averageGrowthRate: 0 }
  return {
    averageGrowthRate: myPrediction.value.growthRate || 0
  }
})

// Methods
const updateForecast = () => {
  toast.add({
    severity: 'info',
    summary: 'Forecast Updated',
    detail: `Showing ${selectedForecastDays.value}-day predictions`,
    life: 2000
  })
}

const viewPredictionDetails = (prediction) => {
  selectedPrediction.value = prediction
  showPredictionDialog.value = true
}

const getRiskTrendClass = (trend) => {
  return trend === 'increasing' ? 'border-l-orange-500' : trend === 'decreasing' ? 'border-l-green-500' : 'border-l-blue-500'
}

const getRiskTrendColor = (trend) => {
  return trend === 'increasing' ? 'text-orange-600' : trend === 'decreasing' ? 'text-green-600' : 'text-blue-600'
}

const getRiskTrendIcon = (trend) => {
  return trend === 'increasing' ? 'pi pi-arrow-up' : trend === 'decreasing' ? 'pi pi-arrow-down' : 'pi pi-minus'
}

const getPredictedRiskBorderClass = (risk) => {
  const classes = {
    safe: 'border-l-green-500',
    low: 'border-l-yellow-500',
    moderate: 'border-l-orange-500',
    high: 'border-l-red-500',
    critical: 'border-l-red-900'
  }
  return classes[risk] || 'border-l-gray-500'
}

const getPredictedRiskColorClass = (risk) => {
  const classes = {
    safe: 'text-green-600',
    low: 'text-yellow-600',
    moderate: 'text-orange-600',
    high: 'text-red-600',
    critical: 'text-red-900'
  }
  return classes[risk] || 'text-gray-600'
}

const exportPredictions = () => {
  const data = {
    municipality: currentMunicipality.value?.name,
    municipalityId: currentMunicipality.value?.id,
    forecastDays: selectedForecastDays.value,
    prediction: myPrediction.value,
    exportedAt: new Date().toISOString()
  }
  
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `predictive-analysis-${Date.now()}.json`
  a.click()
  URL.revokeObjectURL(url)

  toast.add({
    severity: 'success',
    summary: 'Predictions Exported',
    detail: 'Prediction data downloaded successfully',
    life: 3000
  })
}

const navigateTo = (path) => {
  router.push(path)
}
</script>
