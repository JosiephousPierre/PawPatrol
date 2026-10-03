<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
      <div>
        <h2 class="text-2xl font-bold text-dark-blue">Rabies Transmission Simulation</h2>
        <p class="text-muted-blue">Configure and run simulation for your municipality</p>
      </div>
      <div v-if="currentMunicipality" class="flex items-center gap-3">
        <div class="text-right">
          <p class="text-sm text-muted-blue">Simulating for</p>
          <p class="text-lg font-semibold text-primary">{{ currentMunicipality.name }}</p>
        </div>
      </div>
    </div>

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

    <!-- Simulation Status Banner -->
    <Card v-else-if="isRunning" class="bg-primary/5 border-primary/20">
      <template #content>
        <div class="p-4">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-3">
              <div class="w-3 h-3 bg-primary rounded-full animate-pulse"></div>
              <div>
                <h3 class="font-semibold text-primary">Simulation Running for {{ currentMunicipality.name }}</h3>
                <p class="text-muted-blue text-sm">Day {{ currentDay }} of {{ configForm.simulationDays }}</p>
              </div>
            </div>
            <div class="flex items-center space-x-2">
              <Button
                label="Stop"
                icon="pi pi-stop"
                size="small"
                severity="danger"
                @click="stopSimulation"
              />
            </div>
          </div>
          <div class="mt-3">
            <ProgressBar 
              :value="simulationProgress" 
              class="mb-2"
              :showValue="false"
            />
            <div class="flex justify-between text-sm text-muted-blue">
              <span>Progress: {{ simulationProgress.toFixed(1) }}%</span>
              <span>Analyzing transmission patterns...</span>
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

              <!-- Advanced Settings -->
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

    // Run simulation for ONLY the logged-in municipality
    await simulationEngine.startSimulation()

    toast.add({
      severity: 'success',
      summary: 'Simulation Complete',
      detail: `${currentMunicipality.value.name} simulation finished successfully`,
      life: 3000
    })

    // Auto-navigate to results
    setTimeout(() => {
      router.push('/results')
    }, 1500)

  } catch (error) {
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
