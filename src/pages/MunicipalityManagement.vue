<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
      <div>
        <h2 class="text-2xl font-bold text-dark-blue">My Municipality Data</h2>
        <p class="text-muted-blue">Update your municipality's population and rabies case information</p>
      </div>
      <div v-if="currentMunicipality" class="flex items-center gap-3">
        <div class="text-right">
          <p class="text-sm text-muted-blue">Logged in as</p>
          <p class="text-lg font-semibold text-primary">{{ currentMunicipality.name }}</p>
        </div>
        <Button 
          label="Logout" 
          icon="pi pi-sign-out" 
          severity="secondary"
          outlined
          @click="handleLogout"
        />
      </div>
    </div>

    <!-- Redirect if not logged in -->
    <Card v-if="!currentMunicipality" class="bg-white">
      <template #content>
        <div class="p-6 text-center">
          <i class="pi pi-lock text-muted-blue text-6xl mb-4"></i>
          <h3 class="text-xl font-semibold text-dark-blue mb-2">Access Required</h3>
          <p class="text-muted-blue mb-4">Please log in with your municipality access code</p>
          <Button 
            label="Go to Login" 
            icon="pi pi-sign-in" 
            @click="goToLogin"
          />
        </div>
      </template>
    </Card>

    <!-- Municipality Data Form (Only for logged-in municipality) -->
    <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Main Data Entry Form -->
      <div class="lg:col-span-2">
        <Card class="bg-white">
          <template #header>
            <div class="px-6 py-4 border-b border-light-blue">
              <h3 class="text-lg font-semibold text-dark-blue">Population & Rabies Data</h3>
              <p class="text-muted-blue text-sm">Update your municipality's data regularly for accurate simulations</p>
            </div>
          </template>
          <template #content>
            <form @submit.prevent="saveData" class="p-6 space-y-6">
              <!-- Population Data Section -->
              <div>
                <h4 class="text-md font-semibold text-dark-blue mb-4 flex items-center">
                  <i class="pi pi-users text-primary mr-2"></i>
                  Population Data
                </h4>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <label class="block text-sm font-medium text-dark-blue mb-2">
                      Human Population *
                    </label>
                    <InputNumber 
                      v-model="formData.humanPopulation" 
                      :min="0"
                      :useGrouping="true"
                      placeholder="75,000"
                      class="w-full"
                      :class="{ 'p-invalid': errors.humanPopulation }"
                    />
                    <small v-if="errors.humanPopulation" class="p-error">{{ errors.humanPopulation }}</small>
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-dark-blue mb-2">
                      Dog Population *
                    </label>
                    <InputNumber 
                      v-model="formData.dogPopulation" 
                      :min="0"
                      :useGrouping="true"
                      placeholder="1,500"
                      class="w-full"
                      :class="{ 'p-invalid': errors.dogPopulation }"
                    />
                    <small v-if="errors.dogPopulation" class="p-error">{{ errors.dogPopulation }}</small>
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-dark-blue mb-2">
                      Cat Population *
                    </label>
                    <InputNumber 
                      v-model="formData.catPopulation" 
                      :min="0"
                      :useGrouping="true"
                      placeholder="800"
                      class="w-full"
                      :class="{ 'p-invalid': errors.catPopulation }"
                    />
                    <small v-if="errors.catPopulation" class="p-error">{{ errors.catPopulation }}</small>
                  </div>
                </div>
              </div>

              <!-- Current Rabies Cases Section -->
              <div class="border-t border-background pt-6">
                <h4 class="text-md font-semibold text-dark-blue mb-4 flex items-center">
                  <i class="pi pi-exclamation-triangle text-risk-high mr-2"></i>
                  Current Rabies Cases
                </h4>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <label class="block text-sm font-medium text-dark-blue mb-2">
                      Infected Dogs
                    </label>
                    <InputNumber 
                      v-model="formData.infectedDogs" 
                      :min="0"
                      placeholder="0"
                      class="w-full"
                    />
                    <small class="text-muted-blue">Currently infected animals</small>
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-dark-blue mb-2">
                      Infected Cats
                    </label>
                    <InputNumber 
                      v-model="formData.infectedCats" 
                      :min="0"
                      placeholder="0"
                      class="w-full"
                    />
                    <small class="text-muted-blue">Currently infected animals</small>
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-dark-blue mb-2">
                      Infected Humans
                    </label>
                    <InputNumber 
                      v-model="formData.infectedHumans" 
                      :min="0"
                      placeholder="0"
                      class="w-full"
                    />
                    <small class="text-muted-blue">Active human cases</small>
                  </div>
                </div>
              </div>

              <!-- Vaccination Data Section -->
              <div class="border-t border-background pt-6">
                <h4 class="text-md font-semibold text-dark-blue mb-4 flex items-center">
                  <i class="pi pi-shield text-risk-safe mr-2"></i>
                  Vaccination Data
                </h4>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label class="block text-sm font-medium text-dark-blue mb-2">
                      Vaccinated Dogs
                    </label>
                    <InputNumber 
                      v-model="formData.vaccinatedDogs" 
                      :min="0"
                      :max="formData.dogPopulation"
                      placeholder="0"
                      class="w-full"
                    />
                    <small class="text-muted-blue">
                      Coverage: {{ vaccinationCoverage }}%
                    </small>
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-dark-blue mb-2">
                      Population Density (per km²)
                    </label>
                    <InputNumber 
                      v-model="formData.populationDensity" 
                      :min="0"
                      :minFractionDigits="1"
                      :maxFractionDigits="2"
                      placeholder="100.0"
                      class="w-full"
                    />
                    <small class="text-muted-blue">Used for transmission modeling</small>
                  </div>
                </div>
              </div>

              <!-- Risk Level Section -->
              <div class="border-t border-background pt-6">
                <h4 class="text-md font-semibold text-dark-blue mb-4 flex items-center">
                  <i class="pi pi-chart-line text-primary mr-2"></i>
                  Risk Assessment
                </h4>
                <div>
                  <label class="block text-sm font-medium text-dark-blue mb-2">
                    Current Risk Level
                  </label>
                  <Dropdown 
                    v-model="formData.riskLevel" 
                    :options="riskLevelOptions"
                    optionLabel="label"
                    optionValue="value"
                    placeholder="Select risk level"
                    class="w-full"
                  >
                    <template #value="slotProps">
                      <span 
                        v-if="slotProps.value"
                        class="px-2 py-1 rounded text-xs font-medium"
                        :class="getRiskBadgeClass(slotProps.value)"
                      >
                        {{ getRiskLabel(slotProps.value) }}
                      </span>
                      <span v-else>Select risk level</span>
                    </template>
                    <template #option="slotProps">
                      <span 
                        class="px-2 py-1 rounded text-xs font-medium"
                        :class="getRiskBadgeClass(slotProps.option.value)"
                      >
                        {{ slotProps.option.label }}
                      </span>
                    </template>
                  </Dropdown>
                  <small class="text-muted-blue">
                    Based on current infection rates and vaccination coverage
                  </small>
                </div>
              </div>

              <!-- Save Button -->
              <div class="flex justify-between items-center pt-4 border-t border-background">
                <div class="text-sm text-muted-blue">
                  <i class="pi pi-info-circle mr-1"></i>
                  Last updated: {{ lastUpdated }}
                </div>
                <div class="flex gap-3">
                  <Button
                    type="button"
                    label="Reset Changes"
                    severity="secondary"
                    outlined
                    @click="resetForm"
                  />
                  <Button
                    type="submit"
                    label="Save Data"
                    icon="pi pi-save"
                    :loading="saving"
                  />
                </div>
              </div>
            </form>
          </template>
        </Card>
      </div>

      <!-- Summary & Statistics Sidebar -->
      <div class="space-y-6">
        <!-- Current Statistics -->
        <Card class="bg-white">
          <template #header>
            <div class="px-6 py-4 border-b border-light-blue">
              <h3 class="text-lg font-semibold text-dark-blue">Current Statistics</h3>
            </div>
          </template>
          <template #content>
            <div class="p-6 space-y-4">
              <div>
                <p class="text-xs text-muted-blue mb-1">Total Population</p>
                <p class="text-2xl font-bold text-dark-blue">
                  {{ formatNumber(formData.humanPopulation || 0) }}
                </p>
              </div>
              
              <div class="border-t border-background pt-3">
                <p class="text-xs text-muted-blue mb-1">Total Animals</p>
                <p class="text-xl font-bold text-primary">
                  {{ formatNumber((formData.dogPopulation || 0) + (formData.catPopulation || 0)) }}
                </p>
                <p class="text-xs text-muted-blue mt-1">
                  {{ formatNumber(formData.dogPopulation || 0) }} dogs, 
                  {{ formatNumber(formData.catPopulation || 0) }} cats
                </p>
              </div>
              
              <div class="border-t border-background pt-3">
                <p class="text-xs text-muted-blue mb-1">Total Infected</p>
                <p class="text-xl font-bold text-risk-high">
                  {{ (formData.infectedDogs || 0) + (formData.infectedCats || 0) + (formData.infectedHumans || 0) }}
                </p>
                <div class="text-xs text-muted-blue mt-1">
                  <div>🐕 {{ formData.infectedDogs || 0 }} dogs</div>
                  <div>🐈 {{ formData.infectedCats || 0 }} cats</div>
                  <div>👤 {{ formData.infectedHumans || 0 }} humans</div>
                </div>
              </div>
              
              <div class="border-t border-background pt-3">
                <p class="text-xs text-muted-blue mb-1">Vaccination Coverage</p>
                <p class="text-xl font-bold text-risk-safe">
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
              </div>
            </div>
          </template>
        </Card>

        <!-- Quick Tips -->
        <Card class="bg-primary/5 border border-primary/20">
          <template #content>
            <div class="p-6">
              <h4 class="font-semibold text-dark-blue mb-3 flex items-center">
                <i class="pi pi-lightbulb text-primary mr-2"></i>
                Data Entry Tips
              </h4>
              <ul class="space-y-2 text-sm text-muted-blue">
                <li class="flex items-start">
                  <i class="pi pi-check text-risk-safe mr-2 mt-0.5"></i>
                  <span>Update data weekly for accurate tracking</span>
                </li>
                <li class="flex items-start">
                  <i class="pi pi-check text-risk-safe mr-2 mt-0.5"></i>
                  <span>Report all suspected rabies cases immediately</span>
                </li>
                <li class="flex items-start">
                  <i class="pi pi-check text-risk-safe mr-2 mt-0.5"></i>
                  <span>Include all vaccination campaigns in the count</span>
                </li>
                <li class="flex items-start">
                  <i class="pi pi-check text-risk-safe mr-2 mt-0.5"></i>
                  <span>Contact RHO if you need help with data</span>
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
import { useFormatting } from '@/composables/useFormatting'
import { useMunicipalityAuth } from '@/services/municipalityAuth'

const router = useRouter()
const appStore = useAppStore()
const toast = useToast()
const { getRiskBadgeClass, getRiskLabel } = useFormatting()
const { currentMunicipality, logout } = useMunicipalityAuth()

// Component state
const saving = ref(false)
const errors = ref({})
const formData = ref({
  humanPopulation: 0,
  dogPopulation: 0,
  catPopulation: 0,
  infectedDogs: 0,
  infectedCats: 0,
  infectedHumans: 0,
  vaccinatedDogs: 0,
  populationDensity: 0,
  riskLevel: 'safe'
})

const riskLevelOptions = [
  { label: 'Safe', value: 'safe' },
  { label: 'Low Risk', value: 'low' },
  { label: 'Moderate Risk', value: 'moderate' },
  { label: 'High Risk', value: 'high' },
  { label: 'Critical Risk', value: 'critical' }
]

// Computed properties
const vaccinationCoverage = computed(() => {
  if (!formData.value.dogPopulation) return 0
  return Math.round((formData.value.vaccinatedDogs / formData.value.dogPopulation) * 100)
})

const lastUpdated = computed(() => {
  const municipality = appStore.municipalities.find(m => m.id === currentMunicipality.value?.id)
  if (municipality?.lastUpdated) {
    return new Date(municipality.lastUpdated).toLocaleString()
  }
  return 'Never'
})

// Methods
const formatNumber = (num) => {
  return new Intl.NumberFormat().format(num)
}

const loadMunicipalityData = () => {
  if (!currentMunicipality.value) return
  
  const municipality = appStore.municipalities.find(m => m.id === currentMunicipality.value.id)
  
  if (municipality) {
    formData.value = {
      humanPopulation: municipality.humanPopulation || 0,
      dogPopulation: municipality.dogPopulation || 0,
      catPopulation: municipality.catPopulation || 0,
      infectedDogs: municipality.infectedDogs || 0,
      infectedCats: municipality.infectedCats || 0,
      infectedHumans: municipality.infectedHumans || 0,
      vaccinatedDogs: municipality.vaccinatedDogs || 0,
      populationDensity: municipality.populationDensity || 0,
      riskLevel: municipality.riskLevel || 'safe'
    }
  }
}

const saveData = async () => {
  errors.value = {}
  
  // Validation
  if (!formData.value.humanPopulation || formData.value.humanPopulation <= 0) {
    errors.value.humanPopulation = 'Human population is required'
  }
  if (!formData.value.dogPopulation || formData.value.dogPopulation <= 0) {
    errors.value.dogPopulation = 'Dog population is required'
  }
  if (!formData.value.catPopulation || formData.value.catPopulation <= 0) {
    errors.value.catPopulation = 'Cat population is required'
  }
  
  if (Object.keys(errors.value).length > 0) {
    toast.add({
      severity: 'error',
      summary: 'Validation Error',
      detail: 'Please fix the errors before saving',
      life: 3000
    })
    return
  }
  
  saving.value = true
  
  try {
    // Update municipality using store method
    const updateData = {
      ...formData.value,
      lastUpdated: new Date().toISOString()
    }
    
    appStore.updateMunicipality(currentMunicipality.value.id, updateData)
    
    toast.add({
      severity: 'success',
      summary: 'Data Saved',
      detail: `${currentMunicipality.value.name} data has been updated successfully`,
      life: 3000
    })
    
    // Reload data to show updated lastUpdated time
    loadMunicipalityData()
    
  } catch (error) {
    console.error('Save error:', error)
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: error.message || 'Failed to save data. Please try again.',
      life: 3000
    })
  } finally {
    saving.value = false
  }
}

const resetForm = () => {
  loadMunicipalityData()
  toast.add({
    severity: 'info',
    summary: 'Changes Reset',
    detail: 'Form data has been reset to last saved values',
    life: 2000
  })
}

const handleLogout = () => {
  logout()
  toast.add({
    severity: 'info',
    summary: 'Logged Out',
    detail: 'You have been logged out successfully',
    life: 2000
  })
  router.push('/municipality-login')
}

const goToLogin = () => {
  router.push('/municipality-login')
}

// Lifecycle
onMounted(() => {
  loadMunicipalityData()
})
</script>
