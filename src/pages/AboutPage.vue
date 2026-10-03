<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="text-center">
      <div class="flex items-center justify-center space-x-3 mb-4">
        <div class="w-16 h-16 bg-primary rounded-xl flex items-center justify-center">
          <i class="pi pi-shield text-white text-3xl"></i>
        </div>
        <div>
          <h1 class="text-4xl font-bold text-dark-blue">PAWPATROL</h1>
          <p class="text-muted-blue">Research Prototype System</p>
        </div>
      </div>
      <p class="text-xl text-muted-blue max-w-3xl mx-auto">
        Hybrid Quantum-Classical Framework for Adaptive Rabies Transmission Modeling 
        and Vaccination Optimization in Davao de Oro Municipalities
      </p>
    </div>

    <!-- Abstract -->
    <Card class="bg-white">
      <template #header>
        <div class="px-6 py-4 border-b border-light-blue">
          <h2 class="text-2xl font-semibold text-dark-blue">Abstract</h2>
        </div>
      </template>
      <template #content>
        <div class="p-6">
          <p class="text-muted-blue leading-relaxed text-justify">
            This research prototype demonstrates an innovative approach to rabies transmission modeling 
            and vaccination optimization through a hybrid quantum-classical framework. The system 
            simulates rabies transmission dynamics across municipalities in Davao de Oro, Philippines, 
            utilizing a rule-based adaptive vaccination decision engine that mimics Deep Reinforcement 
            Learning behavior. The prototype serves as a proof-of-concept for integrating advanced 
            computational approaches with epidemiological modeling to support public health 
            decision-making in rabies control programs.
          </p>
          <br>
          <p class="text-muted-blue leading-relaxed text-justify">
            The framework incorporates multi-species transmission modeling (dogs, cats, and humans), 
            inter-municipality spread dynamics, environmental randomness factors, and adaptive 
            vaccination strategies based on real-time risk assessment. This web-based prototype 
            demonstrates the complete workflow from outbreak detection through vaccination 
            recommendation generation, providing an interactive platform for exploring 
            epidemiological scenarios and intervention strategies.
          </p>
        </div>
      </template>
    </Card>

    <!-- Research Objectives -->
    <Card class="bg-white">
      <template #header>
        <div class="px-6 py-4 border-b border-light-blue">
          <h2 class="text-2xl font-semibold text-dark-blue">Research Objectives</h2>
        </div>
      </template>
      <template #content>
        <div class="p-6">
          <div class="grid md:grid-cols-2 gap-8">
            <div>
              <h3 class="text-lg font-semibold text-dark-blue mb-4">Primary Objectives</h3>
              <ul class="space-y-3">
                <li class="flex items-start space-x-3">
                  <i class="pi pi-check-circle text-primary mt-1"></i>
                  <span class="text-muted-blue">Develop accurate rabies transmission models for interconnected municipalities</span>
                </li>
                <li class="flex items-start space-x-3">
                  <i class="pi pi-check-circle text-primary mt-1"></i>
                  <span class="text-muted-blue">Create adaptive vaccination strategies responsive to outbreak dynamics</span>
                </li>
                <li class="flex items-start space-x-3">
                  <i class="pi pi-check-circle text-primary mt-1"></i>
                  <span class="text-muted-blue">Integrate quantum-classical computational approaches for optimization</span>
                </li>
                <li class="flex items-start space-x-3">
                  <i class="pi pi-check-circle text-primary mt-1"></i>
                  <span class="text-muted-blue">Provide real-time decision support for public health officials</span>
                </li>
              </ul>
            </div>
            <div>
              <h3 class="text-lg font-semibold text-dark-blue mb-4">Secondary Objectives</h3>
              <ul class="space-y-3">
                <li class="flex items-start space-x-3">
                  <i class="pi pi-arrow-right text-muted-blue mt-1"></i>
                  <span class="text-muted-blue">Demonstrate workflow feasibility through interactive prototype</span>
                </li>
                <li class="flex items-start space-x-3">
                  <i class="pi pi-arrow-right text-muted-blue mt-1"></i>
                  <span class="text-muted-blue">Validate rule-based approximation of DRL behavior</span>
                </li>
                <li class="flex items-start space-x-3">
                  <i class="pi pi-arrow-right text-muted-blue mt-1"></i>
                  <span class="text-muted-blue">Assess computational efficiency and scalability</span>
                </li>
                <li class="flex items-start space-x-3">
                  <i class="pi pi-arrow-right text-muted-blue mt-1"></i>
                  <span class="text-muted-blue">Establish foundation for future implementation</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </template>
    </Card>

    <!-- Proposed Framework -->
    <Card class="bg-white">
      <template #header>
        <div class="px-6 py-4 border-b border-light-blue">
          <h2 class="text-2xl font-semibold text-dark-blue">Proposed Framework</h2>
        </div>
      </template>
      <template #content>
        <div class="p-6 space-y-8">
          <!-- Framework Overview -->
          <div class="text-center">
            <h3 class="text-xl font-semibold text-dark-blue mb-4">System Architecture</h3>
            <div class="bg-background p-6 rounded-xl">
              <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div class="text-center">
                  <div class="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-3">
                    <i class="pi pi-sitemap text-primary text-2xl"></i>
                  </div>
                  <h4 class="font-semibold text-dark-blue mb-2">Transmission Engine</h4>
                  <p class="text-sm text-muted-blue">Multi-species epidemiological modeling with network-based spread dynamics</p>
                </div>
                <div class="text-center">
                  <div class="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-3">
                    <i class="pi pi-brain text-primary text-2xl"></i>
                  </div>
                  <h4 class="font-semibold text-dark-blue mb-2">Adaptive Decision Module</h4>
                  <p class="text-sm text-muted-blue">Rule-based vaccination optimization mimicking DRL behavior</p>
                </div>
                <div class="text-center">
                  <div class="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-3">
                    <i class="pi pi-chart-line text-primary text-2xl"></i>
                  </div>
                  <h4 class="font-semibold text-dark-blue mb-2">Visualization Interface</h4>
                  <p class="text-sm text-muted-blue">Real-time monitoring and interactive result exploration</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Key Components -->
          <div class="grid md:grid-cols-2 gap-8">
            <div>
              <h3 class="text-lg font-semibold text-dark-blue mb-4">Core Components</h3>
              <div class="space-y-4">
                <div class="border border-light-blue rounded-lg p-4">
                  <h4 class="font-medium text-dark-blue mb-2">Transmission Modeling</h4>
                  <p class="text-sm text-muted-blue">Stochastic model incorporating environmental factors, population dynamics, and inter-municipal connections</p>
                </div>
                <div class="border border-light-blue rounded-lg p-4">
                  <h4 class="font-medium text-dark-blue mb-2">Risk Assessment</h4>
                  <p class="text-sm text-muted-blue">Real-time calculation of municipality risk levels based on infection rates and vaccination coverage</p>
                </div>
                <div class="border border-light-blue rounded-lg p-4">
                  <h4 class="font-medium text-dark-blue mb-2">Decision Engine</h4>
                  <p class="text-sm text-muted-blue">Rule-based vaccination recommendations with priority assignment and resource optimization</p>
                </div>
              </div>
            </div>
            
            <div>
              <h3 class="text-lg font-semibold text-dark-blue mb-4">Innovation Aspects</h3>
              <div class="space-y-4">
                <div class="border border-light-blue rounded-lg p-4">
                  <h4 class="font-medium text-dark-blue mb-2">Hybrid Approach</h4>
                  <p class="text-sm text-muted-blue">Integration of classical epidemiological models with quantum-inspired optimization concepts</p>
                </div>
                <div class="border border-light-blue rounded-lg p-4">
                  <h4 class="font-medium text-dark-blue mb-2">Adaptive Strategy</h4>
                  <p class="text-sm text-muted-blue">Dynamic vaccination recommendations that adapt to changing outbreak conditions</p>
                </div>
                <div class="border border-light-blue rounded-lg p-4">
                  <h4 class="font-medium text-dark-blue mb-2">Network Modeling</h4>
                  <p class="text-sm text-muted-blue">Explicit modeling of inter-municipal connections and cross-border transmission</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>
    </Card>

    <!-- Technology Stack -->
    <Card class="bg-white">
      <template #header>
        <div class="px-6 py-4 border-b border-light-blue">
          <h2 class="text-2xl font-semibold text-dark-blue">Technology Stack</h2>
        </div>
      </template>
      <template #content>
        <div class="p-6">
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div v-for="tech in technologies" :key="tech.category" class="text-center">
              <h3 class="font-semibold text-dark-blue mb-4">{{ tech.category }}</h3>
              <div class="space-y-3">
                <div v-for="item in tech.items" :key="item.name" class="flex items-center space-x-3">
                  <div class="w-8 h-8 bg-primary/10 rounded-lg flex items-center justify-center">
                    <i :class="item.icon" class="text-primary text-sm"></i>
                  </div>
                  <div class="text-left">
                    <p class="font-medium text-dark-blue text-sm">{{ item.name }}</p>
                    <p class="text-xs text-muted-blue">{{ item.purpose }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>
    </Card>

    <!-- Research Context -->
    <Card class="bg-white">
      <template #header>
        <div class="px-6 py-4 border-b border-light-blue">
          <h2 class="text-2xl font-semibold text-dark-blue">Research Context</h2>
        </div>
      </template>
      <template #content>
        <div class="p-6">
          <div class="grid md:grid-cols-2 gap-8">
            <div>
              <h3 class="text-lg font-semibold text-dark-blue mb-4">Geographic Focus</h3>
              <p class="text-muted-blue mb-4">
                This research focuses on Davao de Oro province in the Philippines, utilizing 
                real geographic and demographic data for the 11 municipalities:
              </p>
              <div class="grid grid-cols-2 gap-2 text-sm">
                <div v-for="municipality in municipalityNames" :key="municipality" class="flex items-center space-x-2">
                  <i class="pi pi-map-marker text-primary text-xs"></i>
                  <span class="text-muted-blue">{{ municipality }}</span>
                </div>
              </div>
            </div>
            
            <div>
              <h3 class="text-lg font-semibold text-dark-blue mb-4">Public Health Impact</h3>
              <p class="text-muted-blue mb-4">
                Rabies remains a significant public health challenge in the Philippines, 
                with over 200-300 human deaths annually. This research addresses:
              </p>
              <ul class="space-y-2 text-sm text-muted-blue">
                <li class="flex items-center space-x-2">
                  <i class="pi pi-arrow-right text-primary"></i>
                  <span>Optimal resource allocation for vaccination programs</span>
                </li>
                <li class="flex items-center space-x-2">
                  <i class="pi pi-arrow-right text-primary"></i>
                  <span>Early outbreak detection and containment</span>
                </li>
                <li class="flex items-center space-x-2">
                  <i class="pi pi-arrow-right text-primary"></i>
                  <span>Evidence-based vaccination strategy development</span>
                </li>
                <li class="flex items-center space-x-2">
                  <i class="pi pi-arrow-right text-primary"></i>
                  <span>Cross-border transmission prevention</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </template>
    </Card>

    <!-- Limitations and Future Work -->
    <Card class="bg-white">
      <template #header>
        <div class="px-6 py-4 border-b border-light-blue">
          <h2 class="text-2xl font-semibold text-dark-blue">Limitations & Future Work</h2>
        </div>
      </template>
      <template #content>
        <div class="p-6">
          <div class="grid md:grid-cols-2 gap-8">
            <div>
              <h3 class="text-lg font-semibold text-dark-blue mb-4">Current Limitations</h3>
              <ul class="space-y-3">
                <li class="flex items-start space-x-3">
                  <i class="pi pi-info-circle text-muted-blue mt-1"></i>
                  <span class="text-muted-blue">Prototype uses simulated data for demonstration purposes</span>
                </li>
                <li class="flex items-start space-x-3">
                  <i class="pi pi-info-circle text-muted-blue mt-1"></i>
                  <span class="text-muted-blue">Rule-based system approximates but doesn't implement actual DRL</span>
                </li>
                <li class="flex items-start space-x-3">
                  <i class="pi pi-info-circle text-muted-blue mt-1"></i>
                  <span class="text-muted-blue">Quantum computing aspects are conceptual framework only</span>
                </li>
                <li class="flex items-start space-x-3">
                  <i class="pi pi-info-circle text-muted-blue mt-1"></i>
                  <span class="text-muted-blue">Limited validation against real-world outbreak data</span>
                </li>
              </ul>
            </div>
            
            <div>
              <h3 class="text-lg font-semibold text-dark-blue mb-4">Future Enhancements</h3>
              <ul class="space-y-3">
                <li class="flex items-start space-x-3">
                  <i class="pi pi-arrow-circle-right text-primary mt-1"></i>
                  <span class="text-muted-blue">Integration with real surveillance data sources</span>
                </li>
                <li class="flex items-start space-x-3">
                  <i class="pi pi-arrow-circle-right text-primary mt-1"></i>
                  <span class="text-muted-blue">Implementation of actual DRL algorithms</span>
                </li>
                <li class="flex items-start space-x-3">
                  <i class="pi pi-arrow-circle-right text-primary mt-1"></i>
                  <span class="text-muted-blue">Quantum computing algorithm development</span>
                </li>
                <li class="flex items-start space-x-3">
                  <i class="pi pi-arrow-circle-right text-primary mt-1"></i>
                  <span class="text-muted-blue">Multi-scale modeling (regional to national level)</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </template>
    </Card>

    <!-- Disclaimer -->
    <Card class="bg-risk-moderate/5 border-risk-moderate/20">
      <template #header>
        <div class="px-6 py-4 border-b border-risk-moderate/20">
          <h2 class="text-2xl font-semibold text-dark-blue flex items-center space-x-2">
            <i class="pi pi-exclamation-triangle text-risk-moderate"></i>
            <span>Important Disclaimer</span>
          </h2>
        </div>
      </template>
      <template #content>
        <div class="p-6">
          <div class="space-y-4">
            <p class="text-dark-blue font-medium">
              This is a research prototype developed for academic demonstration purposes only.
            </p>
            <ul class="space-y-2 text-muted-blue">
              <li class="flex items-start space-x-2">
                <span class="font-bold text-risk-moderate">•</span>
                <span>Not intended for actual public health decision-making or operational use</span>
              </li>
              <li class="flex items-start space-x-2">
                <span class="font-bold text-risk-moderate">•</span>
                <span>All data used is simulated and does not represent real outbreak scenarios</span>
              </li>
              <li class="flex items-start space-x-2">
                <span class="font-bold text-risk-moderate">•</span>
                <span>Vaccination recommendations are generated by rule-based algorithms for demonstration</span>
              </li>
              <li class="flex items-start space-x-2">
                <span class="font-bold text-risk-moderate">•</span>
                <span>Results should not be used to guide actual vaccination or intervention strategies</span>
              </li>
              <li class="flex items-start space-x-2">
                <span class="font-bold text-risk-moderate">•</span>
                <span>For educational and research demonstration purposes only</span>
              </li>
            </ul>
            <p class="text-muted-blue text-sm mt-4">
              For actual rabies control and vaccination programs, consult with qualified public health 
              officials and veterinary authorities. This prototype serves to demonstrate computational 
              approaches and workflows that could be adapted for real-world implementation after 
              appropriate validation and testing.
            </p>
          </div>
        </div>
      </template>
    </Card>

    <!-- Footer -->
    <div class="text-center py-8">
      <div class="flex items-center justify-center space-x-3 mb-4">
        <div class="w-12 h-12 bg-primary rounded-lg flex items-center justify-center">
          <i class="pi pi-shield text-white text-xl"></i>
        </div>
        <div>
          <h3 class="text-xl font-bold text-dark-blue">PAWPATROL</h3>
          <p class="text-sm text-muted-blue">Research Prototype v1.0</p>
        </div>
      </div>
      <p class="text-muted-blue text-sm">
        Developed as part of advanced research in epidemiological modeling and computational optimization.
      </p>
      <p class="text-muted-blue text-xs mt-2">
        &copy; 2024 PAWPATROL Research Project. For academic use only.
      </p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAppStore } from '@/stores'

const appStore = useAppStore()

const technologies = [
  {
    category: 'Frontend',
    items: [
      { name: 'Vue 3', icon: 'pi pi-code', purpose: 'Framework' },
      { name: 'Vite', icon: 'pi pi-bolt', purpose: 'Build Tool' },
      { name: 'Pinia', icon: 'pi pi-database', purpose: 'State Management' },
      { name: 'Vue Router', icon: 'pi pi-sitemap', purpose: 'Navigation' }
    ]
  },
  {
    category: 'UI/UX',
    items: [
      { name: 'PrimeVue', icon: 'pi pi-palette', purpose: 'Components' },
      { name: 'Tailwind CSS', icon: 'pi pi-brush', purpose: 'Styling' },
      { name: 'PrimeIcons', icon: 'pi pi-star', purpose: 'Icons' }
    ]
  },
  {
    category: 'Visualization',
    items: [
      { name: 'Leaflet.js', icon: 'pi pi-map', purpose: 'Interactive Maps' },
      { name: 'Chart.js', icon: 'pi pi-chart-bar', purpose: 'Data Charts' },
      { name: 'Vue-ChartJS', icon: 'pi pi-chart-line', purpose: 'Chart Integration' }
    ]
  },
  {
    category: 'Storage',
    items: [
      { name: 'Local Storage', icon: 'pi pi-save', purpose: 'Data Persistence' },
      { name: 'JSON', icon: 'pi pi-file', purpose: 'Data Format' },
      { name: 'Browser APIs', icon: 'pi pi-globe', purpose: 'Web Standards' }
    ]
  }
]

const municipalityNames = computed(() => {
  return appStore.municipalities.map(m => m.name).sort()
})
</script>