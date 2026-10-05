<template>
  <div class="space-y-6">
    <!-- Redirect if not logged in -->
    <Card v-if="!currentMunicipality" class="bg-white">
      <template #content>
        <div class="p-6 text-center">
          <i class="pi pi-lock text-muted-blue text-6xl mb-4"></i>
          <h3 class="text-xl font-semibold text-dark-blue mb-2">Access Required</h3>
          <p class="text-muted-blue mb-4">Please log in with your municipality access code to run simulations</p>
          <Button 
            label="Go to Login" 
            icon="pi pi-sign-in" 
            @click="goToLogin"
          />
        </div>
      </template>
    </Card>

    <!-- Animated Simulation Status Banner -->
    <Card v-else-if="currentMunicipality && isRunning" class="bg-gradient-to-br from-primary/10 via-blue-50 to-primary/5 border-2 border-primary/30 shadow-xl simulation-running-card">
      <template #content>
        <div class="p-6">
          <!-- Header with Animated Icon -->
          <div class="flex items-center justify-between mb-6">
            <div class="flex items-center space-x-4">
              <!-- Pulsing Virus Animation -->
              <div class="relative">
                <div class="w-16 h-16 bg-gradient-to-br from-primary to-blue-600 rounded-full flex items-center justify-center animate-pulse-scale">
                  <i class="pi pi-spin pi-spinner text-white text-2xl"></i>
                </div>
                <div class="absolute inset-0 w-16 h-16 bg-primary rounded-full opacity-30 animate-ping"></div>
              </div>
              <div>
                <h3 class="text-xl font-bold text-primary mb-1 flex items-center">
                  Simulation in Progress
                  <span class="ml-2 inline-flex items-center px-2 py-1 text-xs bg-primary text-white rounded-full animate-pulse">
                    LIVE
                  </span>
                </h3>
                <p class="text-dark-blue font-medium">{{ currentMunicipality.name }}</p>
                <p class="text-muted-blue text-sm">Day {{ currentDay }} of {{ configForm.simulationDays }}</p>
              </div>
            </div>
            <Button
              label="Stop"
              icon="pi pi-stop"
              size="small"
              severity="danger"
              outlined
              @click="stopSimulation"
              class="hover:scale-105 transition-transform"
            />
          </div>

          <!-- Progress Bar with Gradient -->
          <div class="space-y-3">
            <div class="relative">
              <div class="w-full bg-gray-200 rounded-full h-4 overflow-hidden shadow-inner">
                <div 
                  class="h-4 rounded-full bg-gradient-to-r from-primary via-blue-500 to-primary bg-size-200 animate-gradient transition-all duration-500 ease-out relative"
                  :style="{ width: `${simulationProgress}%` }"
                >
                  <div class="absolute inset-0 bg-white/20 animate-shimmer"></div>
                </div>
              </div>
              <div class="absolute inset-0 flex items-center justify-center">
                <span class="text-xs font-bold text-dark-blue drop-shadow-sm">
                  {{ simulationProgress.toFixed(1) }}%
                </span>
              </div>
            </div>
            
            <!-- Animated Status Messages -->
            <div class="flex justify-between items-center text-sm">
              <span class="text-muted-blue font-medium">{{ currentSimulationStatus }}</span>
              <span class="text-primary font-semibold animate-pulse">{{ estimatedTimeRemaining }}</span>
            </div>
          </div>

          <!-- Live Activity Cards -->
          <div class="grid grid-cols-3 gap-3 mt-6">
            <div class="bg-white/70 backdrop-blur-sm rounded-lg p-3 border border-primary/20 animate-fade-in">
              <div class="flex items-center space-x-2 mb-1">
                <div class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span class="text-xs text-muted-blue">Transmission Model</span>
              </div>
              <p class="text-sm font-bold text-dark-blue">Active</p>
            </div>
            <div class="bg-white/70 backdrop-blur-sm rounded-lg p-3 border border-primary/20 animate-fade-in animation-delay-200">
              <div class="flex items-center space-x-2 mb-1">
                <div class="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
                <span class="text-xs text-muted-blue">Risk Calculation</span>
              </div>
              <p class="text-sm font-bold text-dark-blue">Processing</p>
            </div>
            <div class="bg-white/70 backdrop-blur-sm rounded-lg p-3 border border-primary/20 animate-fade-in animation-delay-400">
              <div class="flex items-center space-x-2 mb-1">
                <div class="w-2 h-2 bg-purple-500 rounded-full animate-pulse"></div>
                <span class="text-xs text-muted-blue">AI Analysis</span>
              </div>
              <p class="text-sm font-bold text-dark-blue">{{ configForm.enableAdaptiveVaccination ? 'Enabled' : 'Disabled' }}</p>
            </div>
          </div>
        </div>
      </template>
    </Card>

    <!-- Main Simulation Interface (Only for logged-in municipality) -->
    <div v-else-if="currentMunicipality" class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Simulation Configuration -->
      <div class="lg:col-span-2 space-y-6">
        <Card class="bg-white">
          <template #header>
            <div class="px-6 py-4 border-b border-light-blue">
              <div class="flex justify-between items-center mb-2">
                <h3 class="text-lg font-semibold text-dark-blue">Simulation Configuration</h3>
                <ApiStatus />
              </div>
              <p class="text-muted-blue text-sm">Set parameters for {{ currentMunicipality.name }} simulation</p>
            </div>
          </template>
          <template #content>
            <form @submit.prevent="startSimulation" class="p-6 space-y-6">
              <!-- Basic Settings -->
              <div>
                <h4 class="text-md font-semibold text-dark-blue mb-4 flex items-center">
                  <i class="pi pi-calendar text-primary mr-2"></i>
                  Simulation Duration
                </h4>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label class="block text-sm font-medium text-dark-blue mb-2">
                      Number of Days *
                    </label>
                    <InputNumber 
                      v-model="configForm.simulationDays" 
                      :min="1"
                      :max="365"
                      placeholder="30"
                      class="w-full"
                      :class="{ 'p-invalid': errors.simulationDays }"
                    />
                    <small class="text-muted-blue">Forecast period (1-365 days)</small>
                    <small v-if="errors.simulationDays" class="p-error block">{{ errors.simulationDays }}</small>
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-dark-blue mb-2">
                      Simulation Speed
                    </label>
                    <Dropdown 
                      v-model="configForm.simulationSpeed" 
                      :options="speedOptions"
                      optionLabel="label"
                      optionValue="value"
                      placeholder="Select speed"
                      class="w-full"
                    />
                    <small class="text-muted-blue">Processing speed</small>
                  </div>
                </div>
              </div>

              <!-- Transmission Parameters -->
              <div class="border-t border-background pt-6">
                <h4 class="text-md font-semibold text-dark-blue mb-4 flex items-center">
                  <i class="pi pi-bolt text-risk-high mr-2"></i>
                  Transmission Parameters
                </h4>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label class="block text-sm font-medium text-dark-blue mb-2">
                      Base Transmission Rate *
                    </label>
                    <InputNumber 
                      v-model="configForm.transmissionRate" 
                      :min="0"
                      :max="1"
                      :minFractionDigits="2"
                      :maxFractionDigits="3"
                      placeholder="0.15"
                      class="w-full"
                      :class="{ 'p-invalid': errors.transmissionRate }"
                    />
                    <small class="text-muted-blue">Disease spread probability (0-1)</small>
                    <small v-if="errors.transmissionRate" class="p-error block">{{ errors.transmissionRate }}</small>
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-dark-blue mb-2">
                      Environmental Uncertainty
                    </label>
                    <Dropdown 
                      v-model="configForm.environmentalRandomness" 
                      :options="uncertaintyOptions"
                      optionLabel="label"
                      optionValue="value"
                      placeholder="Select uncertainty level"
                      class="w-full"
                    />
                    <small class="text-muted-blue">{{ getUncertaintyDescription(configForm.environmentalRandomness) }}</small>
                  </div>
                </div>
              </div>

              <!-- Vaccination Parameters -->
              <div class="border-t border-background pt-6">
                <h4 class="text-md font-semibold text-dark-blue mb-4 flex items-center">
                  <i class="pi pi-shield text-risk-safe mr-2"></i>
                  Vaccination Parameters
                </h4>
                <div class="grid grid-cols-1 gap-4">
                  <div>
                    <label class="block text-sm font-medium text-dark-blue mb-2">
                      Vaccination Efficiency *
                    </label>
                    <InputNumber 
                      v-model="configForm.vaccinationRate" 
                      :min="0"
                      :max="1"
                      :minFractionDigits="2"
                      :maxFractionDigits="3"
                      placeholder="0.80"
                      class="w-full"
                      :class="{ 'p-invalid': errors.vaccinationRate }"
                    />
                    <small class="text-muted-blue">Vaccine effectiveness (0-1)</small>
                    <small v-if="errors.vaccinationRate" class="p-error block">{{ errors.vaccinationRate }}</small>
                  </div>
                </div>
              </div>

              <!-- Advanced Settings - HIDDEN (values enabled by default) -->
              <!-- Keeping checkboxes enabled in background -->
              <!--
              <div class="border-t border-background pt-6">
                <h4 class="text-md font-semibold text-dark-blue mb-4">Advanced Settings</h4>
                <div class="space-y-4">
                  <div class="flex items-center space-x-3">
                    <input
                      id="enableAdaptiveVaccination"
                      v-model="configForm.enableAdaptiveVaccination"
                      type="checkbox"
                      class="w-4 h-4 text-primary bg-gray-100 border-gray-300 rounded focus:ring-primary"
                    />
                    <label for="enableAdaptiveVaccination" class="text-sm font-medium text-dark-blue">
                      Enable AI-Based Vaccination Recommendations
                    </label>
                  </div>
                  
                  <div class="flex items-center space-x-3">
                    <input
                      id="enableDetailedLogs"
                      v-model="configForm.enableDetailedLogs"
                      type="checkbox"
                      class="w-4 h-4 text-primary bg-gray-100 border-gray-300 rounded focus:ring-primary"
                    />
                    <label for="enableDetailedLogs" class="text-sm font-medium text-dark-blue">
                      Enable Detailed Simulation Logs
                    </label>
                  </div>
                </div>
              </div>
              -->

              <!-- Action Buttons -->
              <div class="flex justify-between items-center pt-4 border-t border-background">
                <Button
                  type="button"
                  label="Reset to Defaults"
                  severity="secondary"
                  outlined
                  @click="resetConfiguration"
                />
                <Button
                  type="submit"
                  label="Run Simulation"
                  icon="pi pi-play"
                  :loading="starting"
                  :disabled="!isConfigurationValid"
                />
              </div>
            </form>
          </template>
        </Card>
      </div>

      <!-- Municipality Summary Sidebar -->
      <div class="space-y-6">
        <!-- Municipality Info -->
        <Card class="bg-white">
          <template #header>
            <div class="px-6 py-4 border-b border-light-blue">
              <h3 class="text-lg font-semibold text-dark-blue">Municipality Info</h3>
            </div>
          </template>
          <template #content>
            <div class="p-6 space-y-4">
              <div>
                <p class="text-xs text-muted-blue mb-1">Municipality</p>
                <p class="text-xl font-bold text-primary">{{ currentMunicipality.name }}</p>
              </div>
              
              <div class="border-t border-background pt-3">
                <p class="text-xs text-muted-blue mb-1">Current Status</p>
                <span 
                  class="inline-block px-3 py-1 rounded text-sm font-medium"
                  :class="getRiskBadgeClass(municipalityData.riskLevel)"
                >
                  {{ getRiskLabel(municipalityData.riskLevel) }}
                </span>
              </div>

              <div class="border-t border-background pt-3">
                <p class="text-xs text-muted-blue mb-2">Population Overview</p>
                <div class="space-y-2 text-sm">
                  <div class="flex justify-between">
                    <span class="text-muted-blue">Humans:</span>
                    <span class="font-medium">{{ formatNumber(municipalityData.humanPopulation) }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-muted-blue">Dogs:</span>
                    <span class="font-medium">{{ formatNumber(municipalityData.dogPopulation) }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-muted-blue">Cats:</span>
                    <span class="font-medium">{{ formatNumber(municipalityData.catPopulation) }}</span>
                  </div>
                </div>
              </div>

              <div class="border-t border-background pt-3">
                <p class="text-xs text-muted-blue mb-2">Current Cases</p>
                <div class="space-y-2 text-sm">
                  <div class="flex justify-between">
                    <span class="text-muted-blue">Infected Dogs:</span>
                    <span class="font-bold text-risk-high">{{ municipalityData.infectedDogs }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-muted-blue">Infected Cats:</span>
                    <span class="font-bold text-risk-high">{{ municipalityData.infectedCats }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-muted-blue">Infected Humans:</span>
                    <span class="font-bold text-risk-high">{{ municipalityData.infectedHumans }}</span>
                  </div>
                </div>
              </div>

              <div class="border-t border-background pt-3">
                <p class="text-xs text-muted-blue mb-1">Vaccination Coverage</p>
                <p class="text-2xl font-bold text-risk-safe">
                  {{ vaccinationCoverage }}%
                </p>
                <div class="mt-2">
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div 
                      class="bg-risk-safe h-2 rounded-full transition-all duration-300"
                      :style="{ width: `${vaccinationCoverage}%` }"
                    ></div>
                  </div>
                </div>
                <p class="text-xs text-muted-blue mt-1">
                  {{ municipalityData.vaccinatedDogs }} / {{ municipalityData.dogPopulation }} dogs vaccinated
                </p>
              </div>
            </div>
          </template>
        </Card>

        <!-- Current Configuration -->
        <Card class="bg-primary/5 border border-primary/20">
          <template #header>
            <div class="px-6 py-4 border-b border-primary/20">
              <h3 class="text-lg font-semibold text-dark-blue">Current Configuration</h3>
            </div>
          </template>
          <template #content>
            <div class="p-6 space-y-3 text-sm">
              <div class="flex justify-between">
                <span class="text-muted-blue">Duration:</span>
                <span class="font-medium">{{ configForm.simulationDays }} days</span>
              </div>
              <div class="flex justify-between">
                <span class="text-muted-blue">Transmission Rate:</span>
                <span class="font-medium">{{ (configForm.transmissionRate * 100).toFixed(1) }}%</span>
              </div>
              <div class="flex justify-between">
                <span class="text-muted-blue">Vaccination Efficiency:</span>
                <span class="font-medium">{{ (configForm.vaccinationRate * 100).toFixed(1) }}%</span>
              </div>
              <div class="flex justify-between">
                <span class="text-muted-blue">Environmental Uncertainty:</span>
                <span class="font-medium">{{ getUncertaintyLabel(configForm.environmentalRandomness) }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-muted-blue">AI Recommendations:</span>
                <span class="font-medium" :class="configForm.enableAdaptiveVaccination ? 'text-risk-safe' : 'text-muted-blue'">
                  {{ configForm.enableAdaptiveVaccination ? 'Enabled' : 'Disabled' }}
                </span>
              </div>
            </div>
          </template>
        </Card>

        <!-- Tips -->
        <Card class="bg-white">
          <template #content>
            <div class="p-6">
              <h4 class="font-semibold text-dark-blue mb-3 flex items-center">
                <i class="pi pi-info-circle text-primary mr-2"></i>
                Simulation Tips
              </h4>
              <ul class="space-y-2 text-sm text-muted-blue">
                <li class="flex items-start">
                  <i class="pi pi-check text-risk-safe mr-2 mt-0.5"></i>
                  <span>Update your data before running simulations</span>
                </li>
                <li class="flex items-start">
                  <i class="pi pi-check text-risk-safe mr-2 mt-0.5"></i>
                  <span>Higher transmission rates = faster spread</span>
                </li>
                <li class="flex items-start">
                  <i class="pi pi-check text-risk-safe mr-2 mt-0.5"></i>
                  <span>Enable AI for vaccination recommendations</span>
                </li>
                <li class="flex items-start">
                  <i class="pi pi-check text-risk-safe mr-2 mt-0.5"></i>
                  <span>View results to see infection trends</span>
                </li>
              </ul>
            </div>
          </template>
        </Card>
      </div>
    </div>

    <!-- Simulation Complete Dialog -->
    <Dialog 
      v-model:visible="showCompletionDialog" 
      modal 
      :closable="false"
      :draggable="false"
      class="simulation-complete-dialog"
      :style="{ width: '650px', maxWidth: '90vw' }"
    >
      <template #header>
        <div class="flex items-center space-x-4 p-2">
          <div class="w-14 h-14 bg-gradient-to-br from-green-400 to-green-600 rounded-full flex items-center justify-center animate-bounce-in shadow-lg">
            <i class="pi pi-check text-white text-3xl"></i>
          </div>
          <div>
            <h3 class="text-2xl font-bold text-dark-blue mb-1">Simulation Complete!</h3>
            <p class="text-sm text-muted-blue">Analysis ready for review</p>
          </div>
        </div>
      </template>
      
      <div class="space-y-8 py-6 px-4">
        <!-- Success Animation -->
        <div class="flex justify-center">
          <div class="relative">
            <div class="w-40 h-40 bg-gradient-to-br from-green-100 to-green-200 rounded-full flex items-center justify-center animate-scale-in shadow-xl">
              <i class="pi pi-chart-line text-green-600 text-6xl"></i>
            </div>
            <div class="absolute inset-0 w-40 h-40 bg-green-400 rounded-full opacity-20 animate-ping-slow"></div>
          </div>
        </div>

        <!-- Summary Stats -->
        <div class="bg-gradient-to-br from-blue-50 to-green-50 rounded-xl p-6 border-2 border-green-200 shadow-md">
          <h4 class="font-semibold text-dark-blue mb-4 flex items-center text-lg">
            <i class="pi pi-info-circle text-primary mr-2 text-xl"></i>
            Simulation Summary
          </h4>
          <div class="grid grid-cols-2 gap-6">
            <div>
              <p class="text-muted-blue mb-2 text-sm">Municipality</p>
              <p class="font-bold text-dark-blue text-lg">{{ currentMunicipality?.name }}</p>
            </div>
            <div>
              <p class="text-muted-blue mb-2 text-sm">Duration</p>
              <p class="font-bold text-dark-blue text-lg">{{ configForm.simulationDays }} days</p>
            </div>
            <div>
              <p class="text-muted-blue mb-2 text-sm">Model Type</p>
              <p class="font-bold text-dark-blue">Fractional-Order Stochastic</p>
            </div>
            <div>
              <p class="text-muted-blue mb-2 text-sm">AI Recommendations</p>
              <p class="font-bold text-lg" :class="configForm.enableAdaptiveVaccination ? 'text-green-600' : 'text-gray-500'">
                {{ configForm.enableAdaptiveVaccination ? 'Generated' : 'Disabled' }}
              </p>
            </div>
          </div>
        </div>

        <!-- Success Message -->
        <div class="text-center space-y-3 px-4">
          <p class="text-dark-blue font-semibold text-lg">
            Your simulation has been completed successfully!
          </p>
          <p class="text-muted-blue text-base leading-relaxed">
            View detailed results including infection predictions, risk maps, and vaccination recommendations.
          </p>
        </div>
      </div>

      <template #footer>
        <div class="flex justify-end gap-4 p-4">
          <Button 
            label="Stay Here" 
            severity="secondary" 
            outlined
            @click="closeCompletionDialog"
            class="hover:scale-105 transition-transform px-6 py-3 text-base"
          />
          <Button 
            label="View Results" 
            icon="pi pi-arrow-right"
            iconPos="right"
            @click="navigateToResults"
            class="bg-gradient-to-r from-primary to-blue-600 hover:from-primary/90 hover:to-blue-700 hover:scale-105 transition-all px-6 py-3 text-base text-white font-semibold shadow-lg"
          />
        </div>
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAppStore } from '@/stores'
import { useToast } from 'primevue/usetoast'
import { useSimulationEngine } from '@/composables/useSimulationEngine'
import { validateSimulationSettings } from '@/services/validation'
import { useFormatting } from '@/composables/useFormatting'
import { useMunicipalityAuth } from '@/services/municipalityAuth'
import ApiStatus from '@/components/ApiStatus.vue'

const router = useRouter()
const appStore = useAppStore()
const toast = useToast()
const simulationEngine = useSimulationEngine()
const { getRiskBadgeClass, getRiskLabel } = useFormatting()
const { currentMunicipality } = useMunicipalityAuth()

// Component state
const starting = ref(false)
const configForm = ref({
  simulationDays: 30,
  transmissionRate: 0.15,
  vaccinationRate: 0.8,
  fractionalOrder: 0.95,  // Hidden, fixed at 0.95 (standard for rabies)
  environmentalRandomness: 0.10,  // Default to Moderate
  simulationSpeed: 1,
  enableAdaptiveVaccination: true,
  enableDetailedLogs: true
})

const errors = ref({})
const showCompletionDialog = ref(false)
const currentSimulationStatus = ref('Initializing simulation...')
const estimatedTimeRemaining = ref('Calculating...')

// Store interval IDs for cleanup
let progressInterval = null
let statusInterval = null

// Speed options
const speedOptions = [
  { label: '1x (Normal)', value: 1 },
  { label: '2x (Fast)', value: 2 },
  { label: '5x (Very Fast)', value: 5 },
  { label: '10x (Ultra Fast)', value: 10 }
]

// Environmental uncertainty options
const uncertaintyOptions = [
  { 
    label: 'None (Deterministic)', 
    value: 0,
    description: 'No randomness - predictable results'
  },
  { 
    label: 'Low (Minimal Variation)', 
    value: 0.05,
    description: 'Slight environmental variation'
  },
  { 
    label: 'Moderate (Standard)', 
    value: 0.10,
    description: 'Realistic environmental uncertainty'
  }
]

// Get description for selected uncertainty level
const getUncertaintyDescription = (value) => {
  const option = uncertaintyOptions.find(opt => opt.value === value)
  return option ? option.description : 'Environmental variation factor'
}

// Get label for uncertainty level (for configuration summary)
const getUncertaintyLabel = (value) => {
  const option = uncertaintyOptions.find(opt => opt.value === value)
  return option ? option.label : `σ = ${value}`
}

// Computed properties
const isRunning = computed(() => appStore.isSimulationRunning)
const currentDay = computed(() => appStore.currentSimulationDay)

const municipalityData = computed(() => {
  if (!currentMunicipality.value) return {}
  
  const municipality = appStore.municipalities.find(m => m.id === currentMunicipality.value.id)
  return municipality || {}
})

const vaccinationCoverage = computed(() => {
  if (!municipalityData.value.dogPopulation) return 0
  return Math.round((municipalityData.value.vaccinatedDogs / municipalityData.value.dogPopulation) * 100)
})

const isConfigurationValid = computed(() => {
  const validation = validateSimulationSettings(configForm.value)
  return validation.isValid
})

const simulationProgress = computed(() => {
  if (!configForm.value.simulationDays || configForm.value.simulationDays === 0) return 0
  return (currentDay.value / configForm.value.simulationDays) * 100
})

const hasSimulationResults = computed(() => {
  return appStore.simulationResults && 
         appStore.simulationResults.municipalities && 
         appStore.simulationResults.municipalities.length > 0
})

// Methods
const formatNumber = (num) => {
  return new Intl.NumberFormat().format(num || 0)
}

const startSimulation = async () => {
  if (!currentMunicipality.value) {
    toast.add({
      severity: 'warn',
      summary: 'Not Logged In',
      detail: 'Please log in to run simulations',
      life: 3000
    })
    return
  }

  const validation = validateSimulationSettings(configForm.value)
  
  if (!validation.isValid) {
    errors.value = validation.errors
    toast.add({
      severity: 'error',
      summary: 'Validation Error',
      detail: 'Please fix the configuration errors',
      life: 3000
    })
    return
  }

  starting.value = true
  errors.value = {}

  try {
    // Save configuration
    appStore.updateSimulationSettings(configForm.value)
    
    toast.add({
      severity: 'info',
      summary: 'Simulation Starting',
      detail: `Running simulation for ${currentMunicipality.value.name}`,
      life: 3000
    })

    // Set initial day
    appStore.setCurrentSimulationDay(0)

    // Start the simulation engine (this will set isSimulationRunning = true internally)
    // We start it first, then begin visual progress animation
    const simulationPromise = simulationEngine.startSimulation()
    
    // Give the engine a moment to set isSimulationRunning state
    await new Promise(resolve => setTimeout(resolve, 50))
    
    // Update simulation status messages dynamically
    updateSimulationStatus()
    
    // Simulate progress (since backend doesn't provide real-time updates)
    const totalDays = configForm.value.simulationDays
    const updateInterval = 100 // Update every 100ms
    const totalDuration = 3000 // 3 seconds total animation
    const steps = totalDuration / updateInterval
    const daysPerStep = totalDays / steps
    
    let currentStep = 0
    progressInterval = setInterval(() => {
      currentStep++
      const newDay = Math.min(Math.floor(currentStep * daysPerStep), totalDays)
      appStore.setCurrentSimulationDay(newDay)
      
      if (currentStep >= steps) {
        clearInterval(progressInterval)
        progressInterval = null
      }
    }, updateInterval)

    // Wait for simulation to complete
    await simulationPromise
    
    // Wait for simulation to complete
    await simulationPromise
    
    // Clean up intervals
    if (progressInterval) {
      clearInterval(progressInterval)
      progressInterval = null
    }
    if (statusInterval) {
      clearInterval(statusInterval)
      statusInterval = null
    }
    
    // Ensure we reach 100%
    appStore.setCurrentSimulationDay(totalDays)
    // Note: isSimulationRunning is set to false by the engine, not here

    // Show completion dialog instead of toast
    showCompletionDialog.value = true

  } catch (error) {
    // Clean up intervals on error
    if (progressInterval) {
      clearInterval(progressInterval)
      progressInterval = null
    }
    if (statusInterval) {
      clearInterval(statusInterval)
      statusInterval = null
    }
    
    // Note: isSimulationRunning is set to false by the engine on error, not here
    appStore.setCurrentSimulationDay(0)
    
    toast.add({
      severity: 'error',
      summary: 'Simulation Error',
      detail: error.message || 'Failed to run simulation',
      life: 5000
    })
  } finally {
    starting.value = false
  }
}

const updateSimulationStatus = () => {
  const statusMessages = [
    'Initializing fractional-order model...',
    'Calculating transmission rates...',
    'Simulating dog-to-dog transmission...',
    'Analyzing cat spillover dynamics...',
    'Computing stochastic components...',
    'Applying vaccination interventions...',
    'Processing inter-municipality spread...',
    'Calculating risk scores...',
    'Generating AI recommendations...',
    'Finalizing predictions...'
  ]

  let currentIndex = 0
  
  // Clear any existing status interval
  if (statusInterval) {
    clearInterval(statusInterval)
  }
  
  statusInterval = setInterval(() => {
    if (!appStore.isSimulationRunning) {
      clearInterval(statusInterval)
      statusInterval = null
      currentSimulationStatus.value = 'Completed!'
      estimatedTimeRemaining.value = 'Done'
      return
    }

    currentSimulationStatus.value = statusMessages[currentIndex % statusMessages.length]
    currentIndex++

    // Update estimated time
    const progress = simulationProgress.value
    if (progress > 0 && progress < 100) {
      const remainingProgress = 100 - progress
      const estimatedSeconds = Math.ceil((remainingProgress / progress) * 2) // Rough estimate
      estimatedTimeRemaining.value = `~${estimatedSeconds}s remaining`
    }
  }, 800)
}

const closeCompletionDialog = () => {
  showCompletionDialog.value = false
}

const navigateToResults = () => {
  showCompletionDialog.value = false
  router.push('/results')
}

const stopSimulation = () => {
  simulationEngine.stopSimulation()
  toast.add({
    severity: 'info',
    summary: 'Simulation Stopped',
    detail: 'Simulation has been terminated',
    life: 2000
  })
}

const resetConfiguration = () => {
  configForm.value = {
    simulationDays: 30,
    transmissionRate: 0.15,
    vaccinationRate: 0.8,
    fractionalOrder: 0.95,  // Fixed value for rabies models
    environmentalRandomness: 0.10,  // Default to Moderate
    simulationSpeed: 1,
    enableAdaptiveVaccination: true,
    enableDetailedLogs: true
  }
  errors.value = {}
  
  toast.add({
    severity: 'info',
    summary: 'Configuration Reset',
    detail: 'Parameters reset to defaults',
    life: 2000
  })
}

const resetSimulation = () => {
  simulationEngine.resetSimulation()
  toast.add({
    severity: 'info',
    summary: 'Simulation Reset',
    detail: 'All simulation data has been cleared',
    life: 2000
  })
}

const viewResults = () => {
  router.push('/results')
}

const exportResults = () => {
  if (!hasSimulationResults.value) return
  
  const data = {
    municipality: currentMunicipality.value.name,
    municipalityId: currentMunicipality.value.id,
    configuration: configForm.value,
    results: appStore.simulationResults,
    exportedAt: new Date().toISOString()
  }
  
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `simulation-${currentMunicipality.value.id}-${Date.now()}.json`
  a.click()
  URL.revokeObjectURL(url)

  toast.add({
    severity: 'success',
    summary: 'Data Exported',
    detail: 'Simulation results downloaded successfully',
    life: 3000
  })
}

const goToLogin = () => {
  router.push('/municipality-login')
}

// Lifecycle
onMounted(() => {
  // Load saved configuration if exists
  if (appStore.simulationSettings) {
    configForm.value = { ...configForm.value, ...appStore.simulationSettings }
  }
})
</script>

<style scoped>
/* Simulation Running Card Animation */
.simulation-running-card {
  animation: slideInFromTop 0.5s ease-out;
}

@keyframes slideInFromTop {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Pulse Scale Animation for Icon */
@keyframes pulse-scale {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}

.animate-pulse-scale {
  animation: pulse-scale 2s ease-in-out infinite;
}

/* Gradient Background Animation */
@keyframes gradient {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

.animate-gradient {
  background-size: 200% 200%;
  animation: gradient 3s ease infinite;
}

.bg-size-200 {
  background-size: 200% 200%;
}

/* Shimmer Effect */
@keyframes shimmer {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

.animate-shimmer {
  animation: shimmer 2s infinite;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.4),
    transparent
  );
}

/* Fade In Animation */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fadeIn 0.5s ease-out forwards;
}

.animation-delay-200 {
  animation-delay: 0.2s;
}

.animation-delay-400 {
  animation-delay: 0.4s;
}

/* Bounce In Animation for Completion Dialog */
@keyframes bounceIn {
  0% {
    opacity: 0;
    transform: scale(0.3);
  }
  50% {
    opacity: 1;
    transform: scale(1.05);
  }
  70% {
    transform: scale(0.9);
  }
  100% {
    transform: scale(1);
  }
}

.animate-bounce-in {
  animation: bounceIn 0.6s ease-out;
}

/* Scale In Animation */
@keyframes scaleIn {
  from {
    opacity: 0;
    transform: scale(0.5);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.animate-scale-in {
  animation: scaleIn 0.5s ease-out;
}

/* Slow Ping Animation */
@keyframes pingSlow {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  75%, 100% {
    transform: scale(2);
    opacity: 0;
  }
}

.animate-ping-slow {
  animation: pingSlow 2s cubic-bezier(0, 0, 0.2, 1) infinite;
}

/* Dialog Backdrop */
:deep(.p-dialog-mask) {
  backdrop-filter: blur(5px);
  background-color: rgba(0, 0, 0, 0.5);
}

/* Dialog Animation */
:deep(.p-dialog) {
  animation: dialogSlideIn 0.3s ease-out;
  border-radius: 1rem;
}

/* Dialog Content Padding */
:deep(.p-dialog-content) {
  padding: 0 !important;
}

:deep(.p-dialog-header) {
  padding: 1.5rem 2rem !important;
  border-bottom: 1px solid #e5e7eb;
}

:deep(.p-dialog-footer) {
  padding: 0 !important;
  border-top: 1px solid #e5e7eb;
}

/* Force white text on View Results button */
:deep(.p-button.text-white),
:deep(.p-button.text-white .p-button-label),
:deep(.p-button.text-white .p-button-icon) {
  color: white !important;
}

@keyframes dialogSlideIn {
  from {
    opacity: 0;
    transform: scale(0.9) translateY(-20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

/* Custom Progress Bar Styling */
:deep(.p-progressbar) {
  border-radius: 1rem;
  height: 1rem;
}

:deep(.p-progressbar-value) {
  border-radius: 1rem;
}

/* Hover Effects */
.hover\:scale-105:hover {
  transform: scale(1.05);
}

.transition-transform {
  transition: transform 0.2s ease-in-out;
}

.transition-all {
  transition: all 0.3s ease-in-out;
}
</style>
