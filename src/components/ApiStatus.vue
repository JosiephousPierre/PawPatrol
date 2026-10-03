<template>
  <div class="flex items-center space-x-2 text-sm">
    <div 
      :class="[
        'w-2 h-2 rounded-full',
        connected ? 'bg-green-500' : 'bg-red-500'
      ]"
    ></div>
    <span :class="connected ? 'text-green-600' : 'text-red-600'">
      {{ connected ? 'Backend Connected' : 'Backend Offline' }}
    </span>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { apiClient } from '@/services/apiClient'

const connected = ref(false)

const checkConnection = async () => {
  console.log('🔌 ApiStatus: Checking backend connection...')
  try {
    await apiClient.healthCheck()
    connected.value = true
    console.log('✅ ApiStatus: Backend connected successfully')
  } catch (error) {
    connected.value = false
    console.error('❌ ApiStatus: Backend connection failed:', error.message)
  }
}

onMounted(checkConnection)

// Check every 30 seconds
setInterval(checkConnection, 30000)
</script>
