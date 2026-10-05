<template>
  <div class="min-h-screen bg-background">
    <!-- Navigation -->
    <nav class="bg-white shadow-soft border-b border-light-blue">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-4">
          <div class="flex items-center space-x-3">
            <div class="w-10 h-10 bg-primary rounded-lg flex items-center justify-center">
              <i class="pi pi-shield text-white text-xl"></i>
            </div>
            <h1 class="text-2xl font-bold text-dark-blue">PAWPATROL</h1>
          </div>
          <Button 
            label="Get Started" 
            icon="pi pi-arrow-right" 
            @click="navigateToDashboard"
            class="px-6 py-2 gap-2"
          />
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <section class="py-24 px-4 relative overflow-hidden">
      <!-- Background decoration -->
      <div class="absolute inset-0 overflow-hidden pointer-events-none">
        <div class="absolute top-20 right-10 w-72 h-72 bg-primary/5 rounded-full blur-3xl"></div>
        <div class="absolute bottom-20 left-10 w-96 h-96 bg-primary/5 rounded-full blur-3xl"></div>
      </div>
      
      <div class="max-w-6xl mx-auto text-center relative z-10">
        <!-- Animated badge -->
        <div class="inline-flex items-center space-x-2 bg-primary/10 text-primary px-4 py-2 rounded-full mb-6 animate-fade-in">
          <i class="pi pi-shield text-sm"></i>
          <span class="text-sm font-medium">Public Health Research Prototype</span>
        </div>
        
        <h1 class="text-5xl md:text-7xl font-bold text-dark-blue mb-6 animate-slide-up">
          <span class="text-primary">PAWPATROL</span>
          <br>
          <span class="text-3xl md:text-5xl font-semibold text-muted-blue">Research Framework</span>
        </h1>
        
        <p class="text-xl md:text-2xl text-muted-blue mb-4 max-w-4xl mx-auto leading-relaxed animate-slide-up-delay-1">
          Fractional-Order Stochastic Transmission Model with Deep Reinforcement Learning 
          for Rabies Outbreak Prediction and Vaccination Optimization
        </p>
        
        <p class="text-lg text-muted-blue mb-10 max-w-3xl mx-auto animate-slide-up-delay-2">
          <i class="pi pi-map-marker text-primary mr-2"></i>
          Davao de Oro Municipalities, Philippines
        </p>
        
        <div class="flex flex-col sm:flex-row gap-4 justify-center animate-slide-up-delay-3">
          <Button 
            label="Explore Dashboard" 
            icon="pi pi-chart-line" 
            iconPos="right"
            @click="navigateToDashboard"
            class="px-10 py-4 text-lg font-semibold shadow-lg hover:shadow-xl transition-all gap-2"
          />
          <Button 
            label="View Coverage Map" 
            icon="pi pi-map" 
            iconPos="right"
            severity="secondary"
            outlined
            @click="scrollToMap"
            class="px-10 py-4 text-lg font-semibold gap-2"
          />
        </div>
        
        <!-- Statistics cards -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mt-16 max-w-4xl mx-auto animate-slide-up-delay-4">
          <div class="bg-white rounded-xl p-6 shadow-card border border-light-blue">
            <div class="text-4xl font-bold text-primary mb-2">11</div>
            <div class="text-sm text-muted-blue">Municipalities Covered</div>
          </div>
          <div class="bg-white rounded-xl p-6 shadow-card border border-light-blue">
            <div class="text-4xl font-bold text-primary mb-2">100k+</div>
            <div class="text-sm text-muted-blue">DQN Training Episodes</div>
          </div>
          <div class="bg-white rounded-xl p-6 shadow-card border border-light-blue">
            <div class="text-4xl font-bold text-primary mb-2">Multi-Species</div>
            <div class="text-sm text-muted-blue">Transmission Model</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Map Section - Davao de Oro Coverage -->
    <section id="map-section" class="py-24 px-4 bg-gradient-to-b from-white to-background">
      <div class="max-w-6xl mx-auto">
        <div class="text-center mb-12">
          <h2 class="text-4xl md:text-5xl font-bold text-dark-blue mb-4">Coverage Area</h2>
          <p class="text-lg text-muted-blue max-w-3xl mx-auto">
            Serving all 11 municipalities across Davao de Oro Province, Philippines
          </p>
        </div>
        
        <Card class="bg-white">
          <template #content>
            <div class="p-6">
              <!-- Map Container -->
              <div id="landing-map" class="w-full h-96 rounded-lg border border-light-blue shadow-lg"></div>
              
              <!-- Map Legend (DYNAMIC - Shows risk distribution) -->
              <div class="mt-4 flex flex-wrap gap-4 justify-center">
                <div class="flex items-center space-x-2">
                  <div class="w-4 h-4 rounded-full bg-risk-safe"></div>
                  <span class="text-sm text-muted-blue">Safe ({{ safeCount }})</span>
                </div>
                <div class="flex items-center space-x-2">
                  <div class="w-4 h-4 rounded-full bg-risk-low"></div>
                  <span class="text-sm text-muted-blue">Low Risk ({{ lowRiskCount }})</span>
                </div>
                <div class="flex items-center space-x-2">
                  <div class="w-4 h-4 rounded-full bg-risk-moderate"></div>
                  <span class="text-sm text-muted-blue">Moderate ({{ moderateRiskCount }})</span>
                </div>
                <div class="flex items-center space-x-2">
                  <div class="w-4 h-4 rounded-full bg-risk-high"></div>
                  <span class="text-sm text-muted-blue">High Risk ({{ highRiskCount }})</span>
                </div>
                <div class="flex items-center space-x-2">
                  <div class="w-4 h-4 rounded-full bg-risk-critical"></div>
                  <span class="text-sm text-muted-blue">Critical ({{ criticalRiskCount }})</span>
                </div>
              </div>
              
              <!-- Municipality List -->
              <div class="mt-8">
                <h3 class="text-xl font-semibold text-dark-blue mb-4 text-center">11 Municipalities</h3>
                <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
                  <div 
                    v-for="municipality in municipalities" 
                    :key="municipality.name"
                    class="flex items-center space-x-2 p-3 bg-gradient-to-r from-primary/5 to-primary/10 rounded-lg hover:from-primary/10 hover:to-primary/15 transition-all cursor-pointer border border-primary/20"
                  >
                    <i class="pi pi-map-marker text-primary text-sm"></i>
                    <span class="text-sm font-medium text-dark-blue">{{ municipality.name }}</span>
                  </div>
                </div>
              </div>
            </div>
          </template>
        </Card>
      </div>
    </section>

    <!-- About Section -->
    <section id="about" class="py-24 px-4 bg-white">
      <div class="max-w-6xl mx-auto">
        <div class="text-center mb-16">
          <h2 class="text-4xl md:text-5xl font-bold text-dark-blue mb-4">About the Research</h2>
          <p class="text-lg text-muted-blue max-w-3xl mx-auto">
            Innovative computational framework for disease control and public health optimization
          </p>
        </div>
        
        <div class="grid md:grid-cols-2 gap-12 items-center mb-12">
          <div>
            <h3 class="text-3xl font-semibold text-dark-blue mb-6">Project Description</h3>
            <p class="text-muted-blue mb-6 leading-relaxed text-lg">
              PAWPATROL implements a fractional-order stochastic transmission model for rabies outbreak 
              prediction across the 11 municipalities of Davao de Oro, Philippines. The system combines 
              advanced mathematical modeling with Deep Reinforcement Learning (Deep Q-Network) to provide 
              AI-powered vaccination recommendations.
            </p>
            <p class="text-muted-blue leading-relaxed text-lg mb-8">
              The fractional-order approach captures long-term memory effects in disease transmission, 
              while stochastic components model environmental uncertainty. A trained Deep Q-Network provides 
              adaptive vaccination strategies by learning optimal resource allocation patterns from 100,000+ 
              simulated outbreak scenarios.
            </p>
            
            <!-- Key Statistics -->
            <div class="grid grid-cols-2 gap-4">
              <div class="bg-background p-4 rounded-lg border-l-4 border-l-primary">
                <div class="text-2xl font-bold text-primary mb-1">Multi-Species</div>
                <div class="text-sm text-muted-blue">Dogs, Cats, Humans</div>
              </div>
              <div class="bg-background p-4 rounded-lg border-l-4 border-l-primary">
                <div class="text-2xl font-bold text-primary mb-1">Cross-Municipal</div>
                <div class="text-sm text-muted-blue">Network Transmission</div>
              </div>
            </div>
          </div>
          
          <div class="bg-gradient-to-br from-primary/5 to-primary/10 p-10 rounded-2xl shadow-lg border border-primary/20">
            <h4 class="text-2xl font-semibold text-dark-blue mb-6">Key Features</h4>
            <ul class="space-y-4">
              <li class="flex items-start space-x-4">
                <div class="w-8 h-8 bg-primary rounded-lg flex items-center justify-center flex-shrink-0">
                  <i class="pi pi-check text-white"></i>
                </div>
                <div>
                  <div class="font-semibold text-dark-blue">Fractional-Order Stochastic Model</div>
                  <div class="text-sm text-muted-blue">Memory effects & environmental uncertainty</div>
                </div>
              </li>
              <li class="flex items-start space-x-4">
                <div class="w-8 h-8 bg-primary rounded-lg flex items-center justify-center flex-shrink-0">
                  <i class="pi pi-check text-white"></i>
                </div>
                <div>
                  <div class="font-semibold text-dark-blue">Deep Q-Network (DQN)</div>
                  <div class="text-sm text-muted-blue">AI-powered vaccination optimization</div>
                </div>
              </li>
              <li class="flex items-start space-x-4">
                <div class="w-8 h-8 bg-primary rounded-lg flex items-center justify-center flex-shrink-0">
                  <i class="pi pi-check text-white"></i>
                </div>
                <div>
                  <div class="font-semibold text-dark-blue">Multi-Species Transmission</div>
                  <div class="text-sm text-muted-blue">Dogs, cats, and humans modeling</div>
                </div>
              </li>
              <li class="flex items-start space-x-4">
                <div class="w-8 h-8 bg-primary rounded-lg flex items-center justify-center flex-shrink-0">
                  <i class="pi pi-check text-white"></i>
                </div>
                <div>
                  <div class="font-semibold text-dark-blue">Interactive Risk Maps</div>
                  <div class="text-sm text-muted-blue">Real-time geographic visualization</div>
                </div>
              </li>
              <li class="flex items-start space-x-4">
                <div class="w-8 h-8 bg-primary rounded-lg flex items-center justify-center flex-shrink-0">
                  <i class="pi pi-check text-white"></i>
                </div>
                <div>
                  <div class="font-semibold text-dark-blue">Spatial Network Modeling</div>
                  <div class="text-sm text-muted-blue">Inter-municipality transmission tracking</div>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <!-- Research Objectives -->
    <section class="py-20 px-4">
      <div class="max-w-6xl mx-auto">
        <div class="text-center mb-12">
          <h2 class="text-4xl md:text-5xl font-bold text-dark-blue mb-4">Research Objectives</h2>
          <p class="text-lg text-muted-blue max-w-3xl mx-auto">
            Advancing public health through intelligent disease modeling and intervention optimization
          </p>
        </div>
        
        <div class="grid md:grid-cols-3 gap-8">
          <Card class="text-center hover:shadow-xl transition-all duration-300 border-t-4 border-t-primary">
            <template #content>
              <div class="p-8">
                <div class="w-20 h-20 bg-gradient-to-br from-primary to-primary/70 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-lg">
                  <i class="pi pi-sitemap text-white text-3xl"></i>
                </div>
                <h3 class="text-2xl font-semibold text-dark-blue mb-4">Transmission Modeling</h3>
                <p class="text-muted-blue leading-relaxed">
                  Develop accurate multi-species transmission models for rabies spread across 
                  interconnected municipalities using fractional-order differential equations.
                </p>
              </div>
            </template>
          </Card>
          
          <Card class="text-center hover:shadow-xl transition-all duration-300 border-t-4 border-t-primary">
            <template #content>
              <div class="p-8">
                <div class="w-20 h-20 bg-gradient-to-br from-primary to-primary/70 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-lg">
                  <i class="pi pi-shield text-white text-3xl"></i>
                </div>
                <h3 class="text-2xl font-semibold text-dark-blue mb-4">Vaccination Optimization</h3>
                <p class="text-muted-blue leading-relaxed">
                  Create adaptive vaccination strategies that respond dynamically 
                  to changing outbreak conditions, resource constraints, and risk levels.
                </p>
              </div>
            </template>
          </Card>
          
          <Card class="text-center hover:shadow-xl transition-all duration-300 border-t-4 border-t-primary">
            <template #content>
              <div class="p-8">
                <div class="w-20 h-20 bg-gradient-to-br from-primary to-primary/70 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-lg">
                  <i class="pi pi-chart-line text-white text-3xl"></i>
                </div>
                <h3 class="text-2xl font-semibold text-dark-blue mb-4">Decision Support</h3>
                <p class="text-muted-blue leading-relaxed">
                  Provide real-time, data-driven recommendations to public health officials 
                  for optimal vaccination deployment and resource allocation.
                </p>
              </div>
            </template>
          </Card>
        </div>
      </div>
    </section>

    <!-- Technology Stack -->
    <section class="py-24 px-4 bg-gradient-to-b from-background to-white">
      <div class="max-w-6xl mx-auto">
        <div class="text-center mb-16">
          <h2 class="text-4xl md:text-5xl font-bold text-dark-blue mb-4">Technology Stack</h2>
          <p class="text-lg text-muted-blue max-w-3xl mx-auto">
            Built with modern web technologies for performance, reliability, and user experience
          </p>
        </div>
        
        <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
          <div 
            v-for="tech in technologies" 
            :key="tech.name" 
            class="bg-white text-center p-6 rounded-xl hover:shadow-xl transition-all duration-300 border border-light-blue hover:-translate-y-2 cursor-pointer"
          >
            <div class="w-16 h-16 bg-gradient-to-br from-primary/10 to-primary/5 rounded-xl flex items-center justify-center mx-auto mb-4">
              <i :class="tech.icon" class="text-primary text-2xl"></i>
            </div>
            <h4 class="font-bold text-dark-blue mb-2">{{ tech.name }}</h4>
            <p class="text-sm text-muted-blue">{{ tech.description }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Researchers -->
    <section class="py-20 px-4">
      <div class="max-w-4xl mx-auto text-center">
        <h2 class="text-4xl font-bold text-dark-blue mb-12">Research Team</h2>
        <Card>
          <template #content>
            <div class="p-8">
              <p class="text-lg text-muted-blue mb-6">
                This research prototype was developed as part of advanced studies in 
                epidemiological modeling and public health optimization.
              </p>
              <p class="text-muted-blue">
                For more information about this research, please contact the research team 
                through appropriate academic channels.
              </p>
            </div>
          </template>
        </Card>
      </div>
    </section>

    <!-- Footer -->
    <footer class="bg-dark-blue py-12 px-4">
      <div class="max-w-6xl mx-auto">
        <div class="grid md:grid-cols-3 gap-8">
          <div>
            <div class="flex items-center space-x-3 mb-4">
              <div class="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
                <i class="pi pi-shield text-white"></i>
              </div>
              <h3 class="text-xl font-bold text-white">PAWPATROL</h3>
            </div>
            <p class="text-light-blue">
              Research prototype for rabies transmission modeling and vaccination optimization.
            </p>
          </div>
          <div>
            <h4 class="font-semibold text-white mb-4">Disclaimer</h4>
            <p class="text-light-blue text-sm">
              This is a research prototype for academic purposes only. 
              Not intended for actual public health decision-making.
            </p>
          </div>
        </div>
        <div class="border-t border-muted-blue mt-8 pt-8 text-center">
          <p class="text-light-blue">&copy; 2026 PAWPATROL Research Prototype. All rights reserved.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAppStore } from '@/stores'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const router = useRouter()
const appStore = useAppStore()

// Map reference
let map = null

const technologies = [
  { name: 'FastAPI', icon: 'pi pi-server', description: 'Python Backend' },
  { name: 'Vue 3', icon: 'pi pi-code', description: 'Frontend Framework' },
  { name: 'Stable-Baselines3', icon: 'pi pi-brain', description: 'DRL (DQN)' },
  { name: 'NumPy/SciPy', icon: 'pi pi-calculator', description: 'Math Computing' },
  { name: 'Leaflet.js', icon: 'pi pi-map', description: 'Interactive Maps' },
  { name: 'Chart.js', icon: 'pi pi-chart-bar', description: 'Data Visualization' },
  { name: 'Fractional Calculus', icon: 'pi pi-sitemap', description: 'Memory Effects' },
  { name: 'Wiener Process', icon: 'pi pi-random', description: 'Stochastic Model' }
]

// Get municipalities from store (with dynamic risk data)
const municipalities = computed(() => appStore.municipalities)

// Risk level counts for legend
const safeCount = computed(() => municipalities.value.filter(m => (m.riskLevel || 'safe') === 'safe').length)
const lowRiskCount = computed(() => municipalities.value.filter(m => m.riskLevel === 'low').length)
const moderateRiskCount = computed(() => municipalities.value.filter(m => m.riskLevel === 'moderate').length)
const highRiskCount = computed(() => municipalities.value.filter(m => m.riskLevel === 'high').length)
const criticalRiskCount = computed(() => municipalities.value.filter(m => m.riskLevel === 'critical').length)

const navigateToDashboard = () => {
  router.push('/login')
}

const scrollToAbout = () => {
  document.getElementById('about')?.scrollIntoView({ behavior: 'smooth' })
}

const scrollToMap = () => {
  document.getElementById('map-section')?.scrollIntoView({ behavior: 'smooth' })
}

// Get risk color based on level
const getRiskColor = (riskLevel) => {
  const colors = {
    safe: '#10b981',      // Green
    low: '#fbbf24',       // Yellow
    moderate: '#f97316',  // Orange
    high: '#ef4444',      // Red
    critical: '#7f1d1d'   // Dark Red
  }
  return colors[riskLevel] || colors.safe
}

// Get risk label
const getRiskLabel = (riskLevel) => {
  const labels = {
    safe: 'Safe',
    low: 'Low Risk',
    moderate: 'Moderate',
    high: 'High Risk',
    critical: 'Critical'
  }
  return labels[riskLevel] || 'Safe'
}

// Initialize the Davao de Oro map with risk data
const initializeMap = () => {
  if (municipalities.value.length === 0) return

  // Create map centered on Davao de Oro (zoom disabled - fixed view)
  map = L.map('landing-map', {
    center: [7.5, 125.9],
    zoom: 9,
    zoomControl: false,      // Remove zoom buttons
    scrollWheelZoom: false,  // Disable scroll wheel zoom
    doubleClickZoom: false,  // Disable double-click zoom
    touchZoom: false,        // Disable touch zoom
    dragging: false,         // Disable map dragging
    boxZoom: false,          // Disable box zoom
    keyboard: false          // Disable keyboard navigation
  })
  
  // Add OpenStreetMap tiles
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
  }).addTo(map)

  // Store original center for recentering
  const originalCenter = [7.5, 125.9]
  const originalZoom = 9

  // Add municipality markers with DYNAMIC risk-based colors
  municipalities.value.forEach(municipality => {
    const riskColor = getRiskColor(municipality.riskLevel || 'safe')
    
    const marker = L.circleMarker([municipality.latitude, municipality.longitude], {
      radius: 10,
      fillColor: riskColor,
      color: '#fff',
      weight: 2,
      opacity: 1,
      fillOpacity: 0.8
    })

    // Add detailed popup with DYNAMIC data (same as dashboard)
    const popup = L.popup().setContent(`
      <div class="text-sm">
        <h4 class="font-semibold text-dark-blue mb-2">${municipality.name}</h4>
        <p class="text-muted-blue">Risk Level: <span class="font-medium">${getRiskLabel(municipality.riskLevel || 'safe')}</span></p>
        <p class="text-muted-blue">Infected: ${municipality.infectedDogs || 0} dogs</p>
        <p class="text-muted-blue">Vaccinated: ${municipality.vaccinatedDogs || 0} dogs</p>
        <p class="text-muted-blue mt-1 text-xs">Last updated: ${municipality.lastUpdated ? new Date(municipality.lastUpdated).toLocaleDateString() : 'N/A'}</p>
      </div>
    `)

    marker.bindPopup(popup)

    // Auto-recenter when popup closes
    popup.on('remove', () => {
      setTimeout(() => {
        map.setView(originalCenter, originalZoom, { animate: true })
      }, 100)
    })

    marker.addTo(map)
  })
}

onMounted(() => {
  // Initialize map after component is mounted
  setTimeout(() => {
    initializeMap()
  }, 300)
})
</script>

<style scoped>
#landing-map {
  z-index: 1;
}

@keyframes fade-in {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slide-up {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fade-in 0.6s ease-out;
}

.animate-slide-up {
  animation: slide-up 0.8s ease-out;
}

.animate-slide-up-delay-1 {
  animation: slide-up 0.8s ease-out 0.2s both;
}

.animate-slide-up-delay-2 {
  animation: slide-up 0.8s ease-out 0.4s both;
}

.animate-slide-up-delay-3 {
  animation: slide-up 0.8s ease-out 0.6s both;
}

.animate-slide-up-delay-4 {
  animation: slide-up 0.8s ease-out 0.8s both;
}
</style>