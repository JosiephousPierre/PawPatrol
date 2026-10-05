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
        Fractional-Order Stochastic Transmission Model with Deep Reinforcement Learning 
        for Rabies Outbreak Prediction and Vaccination Optimization in Davao de Oro, Philippines
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
            PAWPATROL implements a fractional-order stochastic transmission model for rabies outbreak 
            prediction across the 11 municipalities of Davao de Oro, Philippines. The system combines 
            advanced mathematical modeling with Deep Reinforcement Learning (Deep Q-Network) to provide 
            AI-powered vaccination recommendations. The fractional-order approach captures long-term 
            memory effects in disease transmission, while stochastic components model environmental 
            uncertainty and randomness in contact patterns.
          </p>
          <br>
          <p class="text-muted-blue leading-relaxed text-justify">
            The model incorporates multi-species transmission dynamics (dogs, cats, and humans), 
            inter-municipality spread through explicit network connections, population-density-based 
            spatial heterogeneity, and time-series analysis of infection trends. A trained Deep Q-Network 
            provides adaptive vaccination strategies by learning optimal resource allocation patterns 
            from 100,000+ simulated outbreak scenarios. The system enables public health officials 
            to simulate outbreak scenarios, visualize transmission patterns on interactive maps, 
            and receive data-driven vaccination recommendations tailored to each municipality's 
            current outbreak status.
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
                  <span class="text-muted-blue">Develop fractional-order stochastic model for rabies transmission across interconnected municipalities</span>
                </li>
                <li class="flex items-start space-x-3">
                  <i class="pi pi-check-circle text-primary mt-1"></i>
                  <span class="text-muted-blue">Implement Deep Q-Network for adaptive vaccination optimization</span>
                </li>
                <li class="flex items-start space-x-3">
                  <i class="pi pi-check-circle text-primary mt-1"></i>
                  <span class="text-muted-blue">Model multi-species transmission (dogs, cats, humans) with spatial heterogeneity</span>
                </li>
                <li class="flex items-start space-x-3">
                  <i class="pi pi-check-circle text-primary mt-1"></i>
                  <span class="text-muted-blue">Provide data-driven decision support with interactive visualization</span>
                </li>
              </ul>
            </div>
            <div>
              <h3 class="text-lg font-semibold text-dark-blue mb-4">Secondary Objectives</h3>
              <ul class="space-y-3">
                <li class="flex items-start space-x-3">
                  <i class="pi pi-arrow-right text-muted-blue mt-1"></i>
                  <span class="text-muted-blue">Validate model predictions against historical outbreak data</span>
                </li>
                <li class="flex items-start space-x-3">
                  <i class="pi pi-arrow-right text-muted-blue mt-1"></i>
                  <span class="text-muted-blue">Assess environmental uncertainty effects on transmission dynamics</span>
                </li>
                <li class="flex items-start space-x-3">
                  <i class="pi pi-arrow-right text-muted-blue mt-1"></i>
                  <span class="text-muted-blue">Evaluate DRL vaccination strategy effectiveness through simulation</span>
                </li>
                <li class="flex items-start space-x-3">
                  <i class="pi pi-arrow-right text-muted-blue mt-1"></i>
                  <span class="text-muted-blue">Demonstrate system usability for public health decision-making</span>
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
                  <h4 class="font-semibold text-dark-blue mb-2">Fractional-Order Model</h4>
                  <p class="text-sm text-muted-blue">Stochastic transmission model with memory effects and environmental uncertainty</p>
                </div>
                <div class="text-center">
                  <div class="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-3">
                    <i class="pi pi-brain text-primary text-2xl"></i>
                  </div>
                  <h4 class="font-semibold text-dark-blue mb-2">Deep Q-Network (DQN)</h4>
                  <p class="text-sm text-muted-blue">Trained AI agent for optimal vaccination resource allocation</p>
                </div>
                <div class="text-center">
                  <div class="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-3">
                    <i class="pi pi-chart-line text-primary text-2xl"></i>
                  </div>
                  <h4 class="font-semibold text-dark-blue mb-2">Interactive Dashboard</h4>
                  <p class="text-sm text-muted-blue">Real-time visualization with maps, charts, and risk analysis</p>
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
                  <h4 class="font-medium text-dark-blue mb-2">Mathematical Model</h4>
                  <p class="text-sm text-muted-blue mb-2">Fractional-order stochastic SIR with Caputo derivative:</p>
                  <p class="text-xs font-mono text-dark-blue bg-gray-50 p-2 rounded">dI/dt<sup>α</sup> = β·p(t)·S·I/N - γ·I + σ·dW(t)</p>
                </div>
                <div class="border border-light-blue rounded-lg p-4">
                  <h4 class="font-medium text-dark-blue mb-2">Risk Assessment</h4>
                  <p class="text-sm text-muted-blue">Real-time risk scoring based on infection rates, vaccination coverage, and spatial factors</p>
                </div>
                <div class="border border-light-blue rounded-lg p-4">
                  <h4 class="font-medium text-dark-blue mb-2">DRL Recommendations</h4>
                  <p class="text-sm text-muted-blue">Deep Q-Network trained on 100,000+ simulation episodes for optimal vaccination strategies</p>
                </div>
              </div>
            </div>
            
            <div>
              <h3 class="text-lg font-semibold text-dark-blue mb-4">Innovation Aspects</h3>
              <div class="space-y-4">
                <div class="border border-light-blue rounded-lg p-4">
                  <h4 class="font-medium text-dark-blue mb-2">Memory Effects</h4>
                  <p class="text-sm text-muted-blue">Fractional calculus captures long-term disease history influence on current transmission</p>
                </div>
                <div class="border border-light-blue rounded-lg p-4">
                  <h4 class="font-medium text-dark-blue mb-2">Stochastic Components</h4>
                  <p class="text-sm text-muted-blue">Wiener process models environmental uncertainty (weather, behavior, contact randomness)</p>
                </div>
                <div class="border border-light-blue rounded-lg p-4">
                  <h4 class="font-medium text-dark-blue mb-2">AI-Powered Strategy</h4>
                  <p class="text-sm text-muted-blue">Reinforcement learning adapts vaccination allocation based on outbreak state</p>
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
                  <span class="text-muted-blue">Cat-specific transmission parameters based on modeling assumptions (limited empirical data)</span>
                </li>
                <li class="flex items-start space-x-3">
                  <i class="pi pi-info-circle text-muted-blue mt-1"></i>
                  <span class="text-muted-blue">Environmental uncertainty (σ) values derived from literature ranges, not Philippines-specific calibration</span>
                </li>
                <li class="flex items-start space-x-3">
                  <i class="pi pi-info-circle text-muted-blue mt-1"></i>
                  <span class="text-muted-blue">DRL model trained on simulated scenarios; requires validation with real outbreak data</span>
                </li>
                <li class="flex items-start space-x-3">
                  <i class="pi pi-info-circle text-muted-blue mt-1"></i>
                  <span class="text-muted-blue">Assumes homogeneous mixing within municipalities; sub-municipal heterogeneity not modeled</span>
                </li>
              </ul>
            </div>
            
            <div>
              <h3 class="text-lg font-semibold text-dark-blue mb-4">Future Enhancements</h3>
              <ul class="space-y-3">
                <li class="flex items-start space-x-3">
                  <i class="pi pi-arrow-circle-right text-primary mt-1"></i>
                  <span class="text-muted-blue">Empirical calibration of transmission parameters using Philippine rabies surveillance data</span>
                </li>
                <li class="flex items-start space-x-3">
                  <i class="pi pi-arrow-circle-right text-primary mt-1"></i>
                  <span class="text-muted-blue">Seasonal variation modeling (σ varies with monsoon/dry season)</span>
                </li>
                <li class="flex items-start space-x-3">
                  <i class="pi pi-arrow-circle-right text-primary mt-1"></i>
                  <span class="text-muted-blue">Real-time integration with DOH/LGU rabies case reporting systems</span>
                </li>
                <li class="flex items-start space-x-3">
                  <i class="pi pi-arrow-circle-right text-primary mt-1"></i>
                  <span class="text-muted-blue">Quantum computing acceleration for large-scale optimization and faster simulation convergence</span>
                </li>
                <li class="flex items-start space-x-3">
                  <i class="pi pi-arrow-circle-right text-primary mt-1"></i>
                  <span class="text-muted-blue">Expansion to regional/national scale with provincial-level networks</span>
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
              This system is a research implementation for academic and demonstration purposes.
            </p>
            <ul class="space-y-2 text-muted-blue">
              <li class="flex items-start space-x-2">
                <span class="font-bold text-risk-moderate">•</span>
                <span>Model parameters use best available estimates from literature; some lack Philippines-specific empirical validation</span>
              </li>
              <li class="flex items-start space-x-2">
                <span class="font-bold text-risk-moderate">•</span>
                <span>Deep Q-Network trained on simulated outbreak scenarios; requires real-world validation before operational deployment</span>
              </li>
              <li class="flex items-start space-x-2">
                <span class="font-bold text-risk-moderate">•</span>
                <span>Not certified for operational public health decision-making without further validation and regulatory approval</span>
              </li>
              <li class="flex items-start space-x-2">
                <span class="font-bold text-risk-moderate">•</span>
                <span>Results should be interpreted as model predictions subject to parameter uncertainty and modeling assumptions</span>
              </li>
              <li class="flex items-start space-x-2">
                <span class="font-bold text-risk-moderate">•</span>
                <span>For actual rabies control programs, consult qualified veterinary and public health authorities</span>
              </li>
            </ul>
            <p class="text-muted-blue text-sm mt-4">
              This research demonstrates the feasibility of fractional-order stochastic modeling and deep 
              reinforcement learning for rabies outbreak prediction. The system provides a computational framework 
              that can be adapted and validated for operational use after appropriate field testing, parameter 
              calibration with local outbreak data, and collaboration with public health authorities.
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
        Fractional-Order Stochastic Transmission Model with Deep Reinforcement Learning for Rabies Outbreak Prediction
      </p>
      <p class="text-muted-blue text-xs mt-2">
        Research System v1.0 | Davao de Oro, Philippines 
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
      { name: 'PrimeVue', icon: 'pi pi-palette', purpose: 'UI Components' }
    ]
  },
  {
    category: 'Backend',
    items: [
      { name: 'FastAPI', icon: 'pi pi-server', purpose: 'API Framework' },
      { name: 'Python 3.9+', icon: 'pi pi-code', purpose: 'Language' },
      { name: 'NumPy', icon: 'pi pi-calculator', purpose: 'Numerical Computing' },
      { name: 'Stable-Baselines3', icon: 'pi pi-brain', purpose: 'DRL (DQN)' }
    ]
  },
  {
    category: 'Visualization',
    items: [
      { name: 'Leaflet.js', icon: 'pi pi-map', purpose: 'Interactive Maps' },
      { name: 'Chart.js', icon: 'pi pi-chart-bar', purpose: 'Data Charts' },
      { name: 'Tailwind CSS', icon: 'pi pi-brush', purpose: 'Styling' },
      { name: 'PrimeIcons', icon: 'pi pi-star', purpose: 'Icons' }
    ]
  },
  {
    category: 'Mathematical',
    items: [
      { name: 'SciPy', icon: 'pi pi-chart-line', purpose: 'Scientific Computing' },
      { name: 'Fractional Calculus', icon: 'pi pi-sitemap', purpose: 'Memory Effects' },
      { name: 'Stochastic Processes', icon: 'pi pi-random', purpose: 'Uncertainty Modeling' },
      { name: 'Gym Environment', icon: 'pi pi-box', purpose: 'RL Training' }
    ]
  }
]

const municipalityNames = computed(() => {
  return appStore.municipalities.map(m => m.name).sort()
})
</script>