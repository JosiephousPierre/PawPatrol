<template>
  <div class="min-h-screen bg-gradient-to-br from-primary to-primary-dark flex items-center justify-center p-4">
    <div class="w-full max-w-md">
      <!-- Logo and Title -->
      <div class="text-center mb-8">
        <div class="inline-flex items-center justify-center w-16 h-16 bg-white rounded-2xl mb-4">
          <i class="pi pi-shield text-primary text-2xl"></i>
        </div>
        <h1 class="text-3xl font-bold text-white mb-2">PAWPATROL</h1>
        <p class="text-primary-100">Municipality Access Portal</p>
      </div>

      <!-- Login Card -->
      <Card class="bg-white shadow-2xl">
        <template #content>
          <div class="p-6">
            <div class="text-center mb-6">
              <h2 class="text-xl font-semibold text-dark-blue mb-2">
                Municipality Access
              </h2>
              <p class="text-muted-blue text-sm">
                Enter your municipality access code to manage your population data
              </p>
            </div>

            <form @submit.prevent="handleLogin" class="space-y-4">
              <!-- Access Code Input -->
              <div>
                <label class="block text-sm font-medium text-dark-blue mb-2">
                  Municipality Access Code *
                </label>
                <InputText
                  v-model="accessCode"
                  placeholder="e.g., MACO-2024"
                  class="w-full uppercase"
                  :class="{ 'p-invalid': error }"
                  @input="error = null"
                />
                <small class="text-muted-blue">
                  Contact your Regional Health Office for your access code
                </small>
              </div>

              <!-- Error Message -->
              <div v-if="error" class="bg-red-50 border border-red-200 rounded-lg p-3">
                <div class="flex items-center">
                  <i class="pi pi-exclamation-triangle text-red-500 mr-2"></i>
                  <span class="text-red-700 text-sm">{{ error }}</span>
                </div>
              </div>

              <!-- Success Message -->
              <div v-if="success" class="bg-green-50 border border-green-200 rounded-lg p-3">
                <div class="flex items-center">
                  <i class="pi pi-check-circle text-green-500 mr-2"></i>
                  <span class="text-green-700 text-sm">{{ success }}</span>
                </div>
              </div>

              <!-- Login Button -->
              <Button
                type="submit"
                label="Access System"
                icon="pi pi-sign-in"
                class="w-full"
                :loading="loading"
                :disabled="!accessCode?.trim()"
              />
            </form>

            <!-- Help Section -->
            <div class="mt-6 pt-6 border-t border-background">
              <h3 class="text-sm font-medium text-dark-blue mb-2">Need Help?</h3>
              <div class="space-y-2 text-sm text-muted-blue">
                <div class="flex items-center">
                  <i class="pi pi-phone w-4 h-4 mr-2"></i>
                  <span>Regional Health Office: (082) XXX-XXXX</span>
                </div>
                <div class="flex items-center">
                  <i class="pi pi-envelope w-4 h-4 mr-2"></i>
                  <span>Email: health@davaodeoro.gov.ph</span>
                </div>
              </div>
            </div>

            <!-- Municipality List -->
            <div class="mt-6 pt-6 border-t border-background">
              <h3 class="text-sm font-medium text-dark-blue mb-3">Participating Municipalities</h3>
              <div class="grid grid-cols-2 gap-2 text-xs text-muted-blue">
                <div>• Maco</div>
                <div>• Mawab</div>
                <div>• Nabunturan</div>
                <div>• Pantukan</div>
                <div>• Laak</div>
                <div>• Mabini</div>
                <div>• Monkayo</div>
                <div>• Montevista</div>
                <div>• New Bataan</div>
                <div>• Maragusan</div>
                <div>• Compostela</div>
              </div>
            </div>
          </div>
        </template>
      </Card>

      <!-- Footer -->
      <div class="text-center mt-6">
        <p class="text-primary-100 text-sm">
          Rabies Prevention and Control System for Davao de Oro
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import { useMunicipalityAuth } from '@/services/municipalityAuth'

const router = useRouter()
const toast = useToast()
const { login } = useMunicipalityAuth()

const accessCode = ref('')
const error = ref(null)
const success = ref(null)
const loading = ref(false)

const handleLogin = async () => {
  if (!accessCode.value?.trim()) {
    error.value = 'Please enter your access code'
    return
  }

  loading.value = true
  error.value = null
  success.value = null

  try {
    const municipality = login(accessCode.value.trim())
    
    success.value = `Welcome, ${municipality.name}!`
    
    toast.add({
      severity: 'success',
      summary: 'Access Granted',
      detail: `Logged in as ${municipality.name}`,
      life: 3000
    })

    // Navigate to municipality dashboard
    setTimeout(() => {
      router.push('/dashboard')
    }, 1000)

  } catch (err) {
    error.value = err.message
    toast.add({
      severity: 'error',
      summary: 'Access Denied',
      detail: err.message,
      life: 5000
    })
  } finally {
    loading.value = false
  }
}
</script>