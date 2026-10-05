<template>
  <div class="space-y-6">
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
          <i class="pi pi-money-bill text-muted-blue text-6xl mb-4"></i>
          <h3 class="text-xl font-semibold text-dark-blue mb-2">No Simulation Data</h3>
          <p class="text-muted-blue mb-4">Run a simulation to calculate intervention costs.</p>
          <Button 
            label="Go to Simulation" 
            icon="pi pi-play" 
            @click="navigateTo('/simulation')"
          />
        </div>
      </template>
    </Card>

    <!-- Cost Estimation Content -->
    <div v-else-if="interventionBudget" class="space-y-6">
      <!-- Budget Summary Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card class="bg-white border-l-4 border-l-green-600 shadow-card">
          <template #content>
            <div class="p-4">
              <div class="flex items-center justify-between mb-2">
                <p class="text-xs text-muted-blue font-medium">TOTAL BUDGET</p>
                <i class="pi pi-wallet text-green-600 text-xl"></i>
              </div>
              <p class="text-3xl font-bold text-green-600">{{ formatPHP(interventionBudget.summary.grandTotal) }}</p>
              <p class="text-xs text-muted-blue mt-1">Total budget for {{ currentMunicipality?.name }}</p>
            </div>
          </template>
        </Card>

        <Card class="bg-white border-l-4 border-l-primary">
          <template #content>
            <div class="p-4">
              <div class="flex items-center justify-between mb-2">
                <p class="text-xs text-muted-blue font-medium">VACCINATION</p>
                <i class="pi pi-heart text-primary text-xl"></i>
              </div>
              <p class="text-3xl font-bold text-primary">{{ formatPHP(interventionBudget.summary.totalVaccinationCost) }}</p>
              <p class="text-xs text-muted-blue mt-1">{{ interventionBudget.vaccinations.total.toLocaleString() }} vaccines</p>
            </div>
          </template>
        </Card>

        <Card class="bg-white border-l-4 border-l-orange-500">
          <template #content>
            <div class="p-4">
              <div class="flex items-center justify-between mb-2">
                <p class="text-xs text-muted-blue font-medium">HUMAN PEP</p>
                <i class="pi pi-users text-orange-600 text-xl"></i>
              </div>
              <p class="text-3xl font-bold text-orange-600">{{ formatPHP(interventionBudget.summary.totalPEPCost) }}</p>
              <p class="text-xs text-muted-blue mt-1">Post-exposure treatments</p>
            </div>
          </template>
        </Card>

        <Card class="bg-white border-l-4 border-l-risk-high">
          <template #content>
            <div class="p-4">
              <div class="flex items-center justify-between mb-2">
                <p class="text-xs text-muted-blue font-medium">EMERGENCY</p>
                <i class="pi pi-exclamation-circle text-risk-high text-xl"></i>
              </div>
              <p class="text-3xl font-bold text-risk-high">{{ formatPHP(interventionBudget.summary.totalEmergencyCost) }}</p>
              <p class="text-xs text-muted-blue mt-1">High-risk responses</p>
            </div>
          </template>
        </Card>
      </div>

      <!-- My Municipality Risk & Cost Summary -->
      <Card v-if="myMunicipalityCost" class="bg-white border-l-4" :class="'border-l-' + getRiskColor(myMunicipalityCost.riskLevel)">
        <template #content>
          <div class="p-6">
            <div class="flex justify-between items-start mb-6">
              <div>
                <h3 class="text-2xl font-bold text-dark-blue mb-2">{{ myMunicipalityCost.municipalityName }}</h3>
                <span 
                  class="px-3 py-1 rounded text-sm font-medium"
                  :class="getRiskBadgeClass(myMunicipalityCost.riskLevel)"
                >
                  {{ getRiskLabel(myMunicipalityCost.riskLevel) }} Risk
                </span>
              </div>
              <div class="text-right">
                <p class="text-xs text-muted-blue mb-1">Total Budget Required</p>
                <p class="text-4xl font-bold text-green-600">{{ formatPHP(myMunicipalityCost.totalCost) }}</p>
                <p class="text-sm text-muted-blue mt-1">{{ formatPHP(myMunicipalityCost.costPerCapita) }} per capita</p>
              </div>
            </div>

            <!-- Cost Breakdown Grid -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div class="bg-blue-50 p-4 rounded-lg">
                <p class="text-xs text-muted-blue mb-2">VACCINATION COST</p>
                <p class="text-2xl font-bold text-primary mb-2">{{ formatPHP(myMunicipalityCost.breakdown.vaccination.costs.total) }}</p>
                <div class="text-xs space-y-1">
                  <p class="flex justify-between">
                    <span class="text-muted-blue">Dogs:</span>
                    <span class="font-medium">{{ myMunicipalityCost.breakdown.vaccination.vaccinations.dogs }} vaccines</span>
                  </p>
                  <p class="flex justify-between">
                    <span class="text-muted-blue">Cats:</span>
                    <span class="font-medium">{{ myMunicipalityCost.breakdown.vaccination.vaccinations.cats }} vaccines</span>
                  </p>
                  <p class="flex justify-between border-t pt-1 mt-1">
                    <span class="text-muted-blue">Total:</span>
                    <span class="font-semibold">{{ myMunicipalityCost.breakdown.vaccination.vaccinations.total }} vaccines</span>
                  </p>
                </div>
              </div>

              <div class="bg-orange-50 p-4 rounded-lg">
                <p class="text-xs text-muted-blue mb-2">HUMAN PEP COST</p>
                <p class="text-2xl font-bold text-orange-600 mb-2">{{ formatPHP(myMunicipalityCost.breakdown.humanPEP.cost) }}</p>
                <div class="text-xs space-y-1">
                  <p class="flex justify-between">
                    <span class="text-muted-blue">Estimated Cases:</span>
                    <span class="font-medium">{{ myMunicipalityCost.breakdown.humanPEP.estimatedCases }} people</span>
                  </p>
                  <p class="flex justify-between">
                    <span class="text-muted-blue">Cost per Treatment:</span>
                    <span class="font-medium">{{ formatPHP(myMunicipalityCost.breakdown.humanPEP.costPerPerson) }}</span>
                  </p>
                </div>
              </div>

              <div class="bg-red-50 p-4 rounded-lg">
                <p class="text-xs text-muted-blue mb-2">EMERGENCY RESPONSE</p>
                <p class="text-2xl font-bold text-risk-high mb-2">{{ formatPHP(myMunicipalityCost.breakdown.emergencyResponse.cost) }}</p>
                <div class="text-xs space-y-1">
                  <p class="text-muted-blue">Includes surveillance, testing, and emergency containment measures</p>
                </div>
              </div>
            </div>
          </div>
        </template>
      </Card>

      <!-- Detailed Cost Breakdown Table (My Municipality Only) -->
      <Card v-if="myMunicipalityCost" class="bg-white">
        <template #header>
          <div class="px-6 py-4 border-b border-light-blue">
            <h3 class="text-lg font-semibold text-dark-blue">Detailed Cost Breakdown</h3>
            <p class="text-muted-blue text-sm">Comprehensive cost analysis for {{ currentMunicipality?.name }}</p>
          </div>
        </template>
        <template #content>
          <div class="p-6">
            <DataTable 
              :value="[myMunicipalityCost]" 
              dataKey="municipalityId"
              class="p-datatable-sm"
            >
              <Column field="municipalityName" header="Municipality" frozen>
                <template #body="slotProps">
                  <div class="flex items-center space-x-2">
                    <i class="pi pi-map-marker text-primary text-sm"></i>
                    <span class="font-medium">{{ slotProps.data.municipalityName }}</span>
                  </div>
                </template>
              </Column>

              <Column field="riskLevel" header="Risk">
                <template #body="slotProps">
                  <span 
                    class="px-2 py-1 rounded text-xs font-medium"
                    :class="getRiskBadgeClass(slotProps.data.riskLevel)"
                  >
                    {{ getRiskLabel(slotProps.data.riskLevel) }}
                  </span>
                </template>
              </Column>

              <Column field="breakdown.vaccination.vaccinations.total" header="Vaccines Needed">
                <template #body="slotProps">
                  <div class="text-sm">
                    <span class="font-semibold">{{ slotProps.data.breakdown.vaccination.vaccinations.total.toLocaleString() }}</span>
                    <p class="text-xs text-muted-blue">
                      {{ slotProps.data.breakdown.vaccination.vaccinations.dogs }} dogs,
                      {{ slotProps.data.breakdown.vaccination.vaccinations.cats }} cats
                    </p>
                  </div>
                </template>
              </Column>

              <Column field="breakdown.vaccination.costs.total" header="Vaccination Cost">
                <template #body="slotProps">
                  <span class="text-sm font-semibold text-primary">
                    {{ formatPHP(slotProps.data.breakdown.vaccination.costs.total) }}
                  </span>
                </template>
              </Column>

              <Column field="breakdown.humanPEP.cost" header="Human PEP">
                <template #body="slotProps">
                  <span class="text-sm font-semibold text-orange-600">
                    {{ formatPHP(slotProps.data.breakdown.humanPEP.cost) }}
                  </span>
                </template>
              </Column>

              <Column field="breakdown.emergencyResponse.cost" header="Emergency">
                <template #body="slotProps">
                  <span class="text-sm font-semibold text-risk-high">
                    {{ formatPHP(slotProps.data.breakdown.emergencyResponse.cost) }}
                  </span>
                </template>
              </Column>

              <Column field="totalCost" header="Total Cost">
                <template #body="slotProps">
                  <span class="text-sm font-bold text-green-600">
                    {{ formatPHP(slotProps.data.totalCost) }}
                  </span>
                </template>
              </Column>
            </DataTable>
          </div>
        </template>
      </Card>

      <!-- Cost Information Footer -->
      <Card class="bg-white">
        <template #content>
          <div class="p-4">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm mb-4">
              <div>
                <p class="text-muted-blue mb-1">Target Vaccination Coverage</p>
                <p class="text-xl font-semibold text-primary">{{ selectedTargetCoverage }}%</p>
              </div>
              <div>
                <p class="text-muted-blue mb-1">Average Cost per Vaccine</p>
                <p class="text-xl font-semibold text-primary">{{ formatPHP(interventionBudget.costPerVaccine) }}</p>
              </div>
              <div>
                <p class="text-muted-blue mb-1">Total Vaccinations Needed</p>
                <p class="text-xl font-semibold text-primary">{{ interventionBudget.vaccinations.total.toLocaleString() }}</p>
              </div>
            </div>
            <div class="pt-4 border-t border-light-blue">
              <p class="text-xs text-muted-blue flex items-center">
                <i class="pi pi-info-circle mr-2"></i>
                Costs based on DOH standard rates: Dog vaccine ₱150, Cat vaccine ₱120, Human PEP ₱15,000. Includes operational, surveillance, and administrative costs (10% overhead).
              </p>
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
  calculateInterventionBudget,
  formatCurrency as formatPHP
} from '@/utils/simulationUtils'

const router = useRouter()
const appStore = useAppStore()
const toast = useToast()
const { getRiskBadgeClass, getRiskLabel } = useFormatting()
const { currentMunicipality } = useMunicipalityAuth()

// Component state
const selectedTargetCoverage = ref(80)
const showCostDialog = ref(false)
const selectedCostDetail = ref(null)

// Options
const targetCoverageOptions = [
  { label: '60% Coverage', value: 60 },
  { label: '70% Coverage', value: 70 },
  { label: '80% Coverage (Recommended)', value: 80 },
  { label: '90% Coverage', value: 90 },
  { label: '95% Coverage', value: 95 }
]

// Computed properties
const hasSimulationResults = computed(() => {
  return appStore.simulationResults && 
         appStore.simulationResults.dailyData && 
         appStore.simulationResults.dailyData.length > 0
})

// Get budget for ONLY the logged-in municipality
const interventionBudget = computed(() => {
  if (!hasSimulationResults.value || !currentMunicipality.value) return null
  
  const myMunicipality = appStore.municipalities.find(m => m.id === currentMunicipality.value.id)
  if (!myMunicipality) return null
  
  // Calculate budget for single municipality
  return calculateInterventionBudget([myMunicipality], selectedTargetCoverage.value)
})

// Single municipality cost data
const myMunicipalityCost = computed(() => {
  if (!interventionBudget.value || !interventionBudget.value.municipalityCosts) return null
  return interventionBudget.value.municipalityCosts[0] || null
})

// Methods
const updateBudget = () => {
  toast.add({
    severity: 'info',
    summary: 'Budget Updated',
    detail: `Showing ${selectedTargetCoverage.value}% coverage budget`,
    life: 2000
  })
}

const viewCostDetails = (costData) => {
  selectedCostDetail.value = costData
  showCostDialog.value = true
}

const getRiskColor = (riskLevel) => {
  const colors = {
    safe: 'green-500',
    low: 'yellow-500',
    moderate: 'orange-500',
    high: 'red-500',
    critical: 'red-900'
  }
  return colors[riskLevel] || 'gray-500'
}

const exportBudget = () => {
  const data = {
    municipality: currentMunicipality.value?.name,
    municipalityId: currentMunicipality.value?.id,
    targetCoverage: selectedTargetCoverage.value,
    budget: interventionBudget.value,
    municipalityCost: myMunicipalityCost.value,
    exportedAt: new Date().toISOString()
  }
  
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `cost-estimation-${currentMunicipality.value?.id || 'unknown'}-${Date.now()}.json`
  a.click()
  URL.revokeObjectURL(url)

  toast.add({
    severity: 'success',
    summary: 'Budget Exported',
    detail: 'Cost estimation data downloaded successfully',
    life: 3000
  })
}

const navigateTo = (path) => {
  router.push(path)
}
</script>
