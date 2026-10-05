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
          
          <!-- Profile Menu -->
          <div class="relative">
            <Button
              icon="pi pi-user"
              class="w-10 h-10"
              rounded
              text
              @click="toggleProfileMenu"
              aria-label="User profile"
            />
            
            <!-- Dropdown Menu -->
            <div
              v-if="showProfileMenu"
              class="absolute right-0 mt-2 w-64 bg-white rounded-lg shadow-xl border border-light-blue z-50"
            >
              <div class="p-4 border-b border-light-blue">
                <p class="text-xs text-muted-blue mb-1">Logged in as</p>
                <p class="font-semibold text-dark-blue">{{ currentMunicipalityName }}</p>
              </div>
              <div class="p-2">
                <button
                  @click="handleLogout"
                  class="w-full flex items-center space-x-3 px-4 py-3 text-left rounded-lg hover:bg-red-50 transition-colors"
                >
                  <i class="pi pi-sign-out text-red-600"></i>
                  <span class="text-red-600 font-medium">Logout</span>
                </button>
              </div>
            </div>
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
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAppStore } from '@/stores'
import { useMunicipalityAuth } from '@/services/municipalityAuth'
import MunicipalityHeader from '@/components/MunicipalityHeader.vue'

const route = useRoute()
const router = useRouter()
const appStore = useAppStore()
const { currentMunicipality, logout } = useMunicipalityAuth()

const sidebarOpen = ref(false)
const showProfileMenu = ref(false)

const currentMunicipalityName = computed(() => {
  return currentMunicipality.value?.name || 'Not logged in'
})

const toggleProfileMenu = () => {
  showProfileMenu.value = !showProfileMenu.value
}

const handleLogout = () => {
  showProfileMenu.value = false
  logout()
  router.push('/')  // Go to landing page instead of login
}

// Close profile menu when clicking outside
const handleClickOutside = (event) => {
  const profileMenu = event.target.closest('.relative')
  if (!profileMenu && showProfileMenu.value) {
    showProfileMenu.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

const navigationItems = [
  { name: 'Dashboard', path: '/dashboard', icon: 'pi pi-home' },
  { name: 'Municipality Management', path: '/municipalities', icon: 'pi pi-map-marker' },
  { name: 'Simulation', path: '/simulation', icon: 'pi pi-play' },
  { name: 'Results', path: '/results', icon: 'pi pi-chart-line' },
  { name: 'Cost Estimation', path: '/cost-estimation', icon: 'pi pi-money-bill' },
  { name: 'About', path: '/about', icon: 'pi pi-info-circle' }
]

const pageInfo = {
  '/dashboard': { title: 'Dashboard', description: 'Overview of simulation data and key metrics' },
  '/municipalities': { title: 'Municipality Management', description: 'Manage municipality data and connections' },
  '/simulation': { title: 'Simulation Configuration', description: 'Configure and run transmission simulations' },
  '/results': { title: 'Results & Analysis', description: 'View simulation results, predictions, and vaccination recommendations' },
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