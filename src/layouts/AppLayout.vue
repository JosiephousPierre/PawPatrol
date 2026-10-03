<template>
  <div class="min-h-screen bg-background flex">
    <!-- Sidebar -->
    <aside class="w-64 bg-dark-blue text-white flex flex-col fixed h-full z-40 lg:relative lg:translate-x-0 transition-transform duration-300" :class="{ '-translate-x-full': !sidebarOpen }">
      <!-- Logo -->
      <div class="p-6 border-b border-muted-blue">
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 bg-primary rounded-lg flex items-center justify-center">
            <i class="pi pi-shield text-white text-xl"></i>
          </div>
          <div>
            <h2 class="text-xl font-bold">PAWPATROL</h2>
            <p class="text-xs text-light-blue">Research Prototype</p>
          </div>
        </div>
      </div>

      <!-- Navigation -->
      <nav class="flex-1 py-6">
        <ul class="space-y-2 px-4">
          <li v-for="item in navigationItems" :key="item.name">
            <router-link
              :to="item.path"
              class="flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors duration-200 hover:bg-muted-blue"
              :class="{ 'bg-primary text-white': isActiveRoute(item.path) }"
            >
              <i :class="item.icon" class="text-lg"></i>
              <span class="font-medium">{{ item.name }}</span>
            </router-link>
          </li>
        </ul>
      </nav>

      <!-- Footer -->
      <div class="p-4 border-t border-muted-blue">
        <p class="text-xs text-light-blue text-center">
          Academic Research Tool
        </p>
      </div>
    </aside>

    <!-- Mobile overlay -->
    <div 
      v-if="sidebarOpen" 
      class="fixed inset-0 bg-black bg-opacity-50 z-30 lg:hidden"
      @click="sidebarOpen = false"
    ></div>

    <!-- Main Content -->
    <div class="flex-1 lg:ml-0" :class="{ 'ml-0': !sidebarOpen }">
      <!-- Municipality Header -->
      <MunicipalityHeader />
      
      <!-- Top Bar -->
      <header class="bg-white shadow-soft border-b border-light-blue px-6 py-4 flex items-center justify-between">
        <div class="flex items-center space-x-4">
          <Button
            icon="pi pi-bars"
            class="lg:hidden"
            text
            @click="sidebarOpen = !sidebarOpen"
          />
          <div>
            <h1 class="text-2xl font-bold text-dark-blue">{{ currentPageTitle }}</h1>
            <p class="text-muted-blue text-sm">{{ currentPageDescription }}</p>
          </div>
        </div>
        
        <div class="flex items-center space-x-4">
          <!-- Simulation Status -->
          <div v-if="appStore.isSimulationRunning" class="flex items-center space-x-2 bg-primary/10 px-3 py-2 rounded-lg">
            <div class="w-2 h-2 bg-primary rounded-full animate-pulse"></div>
            <span class="text-primary text-sm font-medium">Simulation Running</span>
          </div>
          
          <!-- Current Day -->
          <div class="bg-background px-3 py-2 rounded-lg">
            <span class="text-muted-blue text-sm">Day</span>
            <span class="text-dark-blue font-semibold ml-1">{{ appStore.currentSimulationDay }}</span>
          </div>
        </div>
      </header>

      <!-- Page Content -->
      <main class="p-6">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAppStore } from '@/stores'
import MunicipalityHeader from '@/components/MunicipalityHeader.vue'

const route = useRoute()
const appStore = useAppStore()
const sidebarOpen = ref(false)

const navigationItems = [
  { name: 'Dashboard', path: '/dashboard', icon: 'pi pi-home' },
  { name: 'Municipality Management', path: '/municipalities', icon: 'pi pi-map-marker' },
  { name: 'Simulation', path: '/simulation', icon: 'pi pi-play' },
  { name: 'Results', path: '/results', icon: 'pi pi-chart-line' },
  { name: 'Predictive Analysis', path: '/predictive-analysis', icon: 'pi pi-chart-bar' },
  { name: 'Cost Estimation', path: '/cost-estimation', icon: 'pi pi-money-bill' },
  { name: 'About', path: '/about', icon: 'pi pi-info-circle' }
]

const pageInfo = {
  '/dashboard': { title: 'Dashboard', description: 'Overview of simulation data and key metrics' },
  '/municipalities': { title: 'Municipality Management', description: 'Manage municipality data and connections' },
  '/simulation': { title: 'Simulation Configuration', description: 'Configure and run transmission simulations' },
  '/results': { title: 'Results & Analysis', description: 'View simulation results and vaccination recommendations' },
  '/predictive-analysis': { title: 'Predictive Risk Analysis', description: 'AI-powered future risk forecasting' },
  '/cost-estimation': { title: 'Intervention Cost Estimation', description: 'Budget planning and financial analysis' },
  '/about': { title: 'About', description: 'Research information and framework details' }
}

const currentPageTitle = computed(() => {
  return pageInfo[route.path]?.title || 'PAWPATROL'
})

const currentPageDescription = computed(() => {
  return pageInfo[route.path]?.description || 'Research Prototype'
})

const isActiveRoute = (path) => {
  return route.path === path
}
</script>