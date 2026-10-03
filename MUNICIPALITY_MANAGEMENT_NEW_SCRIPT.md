# New Municipality Management Script

This is what the new script section should be - focused on managing only OWN municipality data:

```javascript
<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useAppStore } from '@/stores'
import { useMunicipalityAuth } from '@/services/municipalityAuth'
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'

const appStore = useAppStore()
const { currentMunicipality, hasPermission } = useMunicipalityAuth()
const toast = useToast()
const confirm = useConfirm()

// Get own municipality data from store
const ownMunicipalityData = computed(() => appStore.ownMunicipalityData)

// Form data - populated from own municipality
const municipalityForm = ref({
  humanPopulation: 0,
  dogPopulation: 0,
  catPopulation: 0,
  populationDensity: 0,
  infectedDogs: 0,
  infectedCats: 0,
  infectedHumans: 0,
  vaccinatedDogs: 0
})

const errors = ref({})
const saving = ref(false)

// Load own municipality data into form
const loadOwnData = () => {
  if (ownMunicipalityData.value) {
    municipalityForm.value = {
      humanPopulation: ownMunicipalityData.value.humanPopulation || 0,
      dogPopulation: ownMunicipalityData.value.dogPopulation || 0,
      catPopulation: ownMunicipalityData.value.catPopulation || 0,
      populationDensity: ownMunicipalityData.value.populationDensity || 0,
      infectedDogs: ownMunicipalityData.value.infectedDogs || 0,
      infectedCats: ownMunicipalityData.value.infectedCats || 0,
      infectedHumans: ownMunicipalityData.value.infectedHumans || 0,
      vaccinatedDogs: ownMunicipalityData.value.vaccinatedDogs || 0
    }
  }
}

// Save municipality data
const saveMunicipalityData = async () => {
  errors.value = {}
  
  // Validate
  if (!municipalityForm.value.humanPopulation || municipalityForm.value.humanPopulation < 1) {
    errors.value.humanPopulation = 'Human population is required'
    return
  }
  
  if (!municipalityForm.value.dogPopulation || municipalityForm.value.dogPopulation < 1) {
    errors.value.dogPopulation = 'Dog population is required'
    return
  }
  
  try {
    saving.value = true
    
    // Update own municipality data
    await appStore.updateOwnMunicipalityData(municipalityForm.value)
    
    toast.add({
      severity: 'success',
      summary: 'Success',
      detail: 'Municipality data updated successfully',
      life: 3000
    })
    
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: error.message || 'Failed to update municipality data',
      life: 5000
    })
  } finally {
    saving.value = false
  }
}

// Helper functions
const getRiskBadgeClass = (riskLevel) => {
  const classes = {
    safe: 'bg-risk-safe/10 text-risk-safe',
    low: 'bg-risk-low/10 text-risk-low',
    moderate: 'bg-risk-moderate/10 text-risk-moderate',
    high: 'bg-risk-high/10 text-risk-high',
    critical: 'bg-risk-critical/10 text-risk-critical'
  }
  return classes[riskLevel] || classes.safe
}

const getRiskLevelLabel = (riskLevel) => {
  const labels = {
    safe: 'Safe',
    low: 'Low Risk',
    moderate: 'Moderate Risk',
    high: 'High Risk',
    critical: 'Critical'
  }
  return labels[riskLevel] || 'Unknown'
}

// Initialize
onMounted(() => {
  loadOwnData()
})

// Watch for changes in ownMunicipalityData
watch(ownMunicipalityData, () => {
  loadOwnData()
})
</script>
```

Key changes:
1. Removed all DataTable logic
2. Removed multi-municipality management
3. Only shows/edits OWN municipality data
4. Uses `appStore.ownMunicipalityData` 
5. Uses `appStore.updateOwnMunicipalityData()` to save
6. Much simpler and focused
