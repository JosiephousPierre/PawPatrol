<template>
  <div id="app" class="min-h-screen bg-background">
    <router-view />
    <Toast />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAppStore } from '@/stores'

const appStore = useAppStore()

onMounted(() => {
  appStore.initializeApp()
})
</script>

<style>
#app {
  font-family: 'Inter', ui-sans-serif, system-ui, sans-serif;
}
</style>