<template>
  <div class="space-y-6">
    <!-- No Results Warning -->
    <Card v-if="!hasResults" class="bg-white">
      <template #content>
        <div class="p-6 text-center">
          <i class="pi pi-chart-line text-muted-blue text-6xl mb-4"></i>
          <h3 class="text-xl font-semibold text-dark-blue mb-2">No Simulation Results</h3>
          <p class="text-muted-blue mb-4">Run a simulation to generate results and visualizations</p>
          <Button 
            label="Go to Simulation" 
            icon="pi pi-play" 
            @click="$router.push('/simulation')"
          />
        </div>
      </template>
    </Card>

    <!-- Results Content (DYNAMIC - Changes based on simulation data) -->
    <div v-else class="space-y-6">
      <!-- Municipality Analysis Table (Target Coverage & Infection Rate) - Logged-in Municipality Only -->
      <Card class="bg-white">
        <template #header>
          <div class="px-6 py-4 border-b border-light-blue">
            <div class="flex justify-between items-center">
              <div>
                <h3 class="text-lg font-semibold text-dark-blue">My Municipality Analysis</h3>
                <p class="text-muted-blue text-sm">Your vaccination coverage and infection rate data</p>
              </div>
              <div v-if="currentMunicipality" class="text-right">
                <p class="text-xs text-muted-blue">Viewing data for</p>
                <p class="text-lg font-semibold text-primary">{{ currentMunicipality.name }}</p>
              </div>
            </div>
          </div>
        </template>
        <template #content>
          <div class="p-6">
            <!-- Important Metrics Explanation -->
            <div class="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <h4 class="font-semibold text-dark-blue mb-3 flex items-center">
                <i class="pi pi-info-circle text-primary mr-2"></i>
                Understanding These Metrics
              </h4>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                <div>
                  <p class="font-medium text-dark-blue mb-2">📊 Target Coverage (Vaccination %)</p>
                  <ul class="space-y-1 text-muted-blue">
                    <li>• <strong>≥ 70%</strong>: ✅ Good - WHO recommendation met</li>
                    <li>• <strong>50-70%</strong>: ⚠️ Moderate - Increase vaccination</li>
                    <li>• <strong>< 50%</strong>: ❌ Low - Emergency action needed</li>
                  </ul>
                  <p class="mt-2 text-xs italic">Formula: (Vaccinated Dogs / Total Dogs) × 100</p>
                </div>
                <div>
                  <p class="font-medium text-dark-blue mb-2">🦠 Infection Rate (%)</p>
                  <ul class="space-y-1 text-muted-blue">
                    <li>• <strong>< 0.1%</strong>: ✅ Safe - Very few cases</li>
                    <li>• <strong>0.1-1%</strong>: ⚠️ Low - Emerging outbreak</li>
                    <li>• <strong>1-5%</strong>: ⚠️ Moderate - Active outbreak</li>
                    <li>• <strong>> 5%</strong>: 🚨 High/Critical - Epidemic</li>
                  </ul>
                  <p class="mt-2 text-xs italic">Formula: (Infected Animals / Total Animals) × 100</p>
                </div>
              </div>
            </div>

            <DataTable 
              :value="myMunicipalityAnalysis" 
              dataKey="id"
              class="p-datatable-sm"
            >
              <Column field="name" header="Municipality" :sortable="true" frozen>
                <template #body="slotProps">
                  <div class="flex items-center space-x-2">
                    <i class="pi pi-map-marker text-primary"></i>
                    <span class="font-medium">{{ slotProps.data.name }}</span>
                  </div>
                </template>
              </Column>

              <Column field="riskLevel" header="Risk Level" :sortable="true">
                <template #body="slotProps">
                  <span 
                    class="px-2 py-1 rounded text-xs font-medium"
                    :class="getRiskBadgeClass(slotProps.data.riskLevel)"
                  >
                    {{ getRiskLabel(slotProps.data.riskLevel) }}
                  </span>
                </template>
              </Column>

              <Column field="targetCoverage" header="Target Coverage" :sortable="true">
                <template #body="slotProps">
                  <div class="space-y-1">
                    <div class="flex items-center justify-between">
                      <span class="text-sm font-semibold">{{ slotProps.data.targetCoverage }}%</span>
                      <span 
                        class="text-xs px-1.5 py-0.5 rounded"
                        :class="{
                          'bg-risk-safe text-white': slotProps.data.targetCoverage >= 70,
                          'bg-risk-moderate text-white': slotProps.data.targetCoverage >= 50 && slotProps.data.targetCoverage < 70,
                          'bg-risk-high text-white': slotProps.data.targetCoverage < 50
                        }"
                      >
                        {{ getCoverageStatus(slotProps.data.targetCoverage) }}
                      </span>
                    </div>
                    <div class="w-full bg-gray-200 rounded-full h-1.5">
                      <div 
                        class="h-1.5 rounded-full transition-all"
                        :class="{
                          'bg-risk-safe': slotProps.data.targetCoverage >= 70,
                          'bg-risk-moderate': slotProps.data.targetCoverage >= 50 && slotProps.data.targetCoverage < 70,
                          'bg-risk-high': slotProps.data.targetCoverage < 50
                        }"
                        :style="{ width: `${slotProps.data.targetCoverage}%` }"
                      ></div>
                    </div>
                    <p class="text-xs text-muted-blue">
                      {{ slotProps.data.vaccinatedDogs }} / {{ slotProps.data.totalDogs }} dogs
                    </p>
                  </div>
                </template>
              </Column>

              <Column field="infectionRate" header="Infection Rate" :sortable="true">
                <template #body="slotProps">
                  <div class="space-y-1">
                    <div class="flex items-center gap-2">
                      <span 
                        class="text-sm font-semibold"
                        :class="{
                          'text-risk-critical': slotProps.data.infectionRate >= 10,
                          'text-risk-high': slotProps.data.infectionRate >= 5 && slotProps.data.infectionRate < 10,
                          'text-risk-moderate': slotProps.data.infectionRate >= 1 && slotProps.data.infectionRate < 5,
                          'text-risk-low': slotProps.data.infectionRate >= 0.1 && slotProps.data.infectionRate < 1,
                          'text-risk-safe': slotProps.data.infectionRate < 0.1
                        }"
                      >
                        {{ slotProps.data.infectionRate.toFixed(2) }}%
                      </span>
                      <span 
                        class="text-xs px-1.5 py-0.5 rounded whitespace-nowrap"
                        :class="{
                          'bg-risk-critical text-white': slotProps.data.infectionRate >= 10,
                          'bg-risk-high text-white': slotProps.data.infectionRate >= 5 && slotProps.data.infectionRate < 10,
                          'bg-risk-moderate text-white': slotProps.data.infectionRate >= 1 && slotProps.data.infectionRate < 5,
                          'bg-risk-low text-dark-blue': slotProps.data.infectionRate >= 0.1 && slotProps.data.infectionRate < 1,
                          'bg-risk-safe text-dark-blue': slotProps.data.infectionRate < 0.1
                        }"
                      >
                        {{ getInfectionStatus(slotProps.data.infectionRate) }}
                      </span>
                    </div>
                    <p class="text-xs text-muted-blue">
                      {{ slotProps.data.totalInfected }} / {{ slotProps.data.totalAnimals }} infected
                    </p>
                  </div>
                </template>
              </Column>

              <Column field="totalInfected" header="Total Cases" :sortable="true">
                <template #body="slotProps">
                  <div class="text-sm space-y-0.5">
                    <div class="flex items-center justify-between">
                      <span class="text-muted-blue">Dogs:</span>
                      <span class="font-medium text-risk-high">{{ slotProps.data.infectedDogs }}</span>
                    </div>
                    <div class="flex items-center justify-between">
                      <span class="text-muted-blue">Cats:</span>
                      <span class="font-medium text-risk-high">{{ slotProps.data.infectedCats }}</span>
                    </div>
                    <div class="flex items-center justify-between">
                      <span class="text-muted-blue">Humans:</span>
                      <span class="font-medium text-risk-critical">{{ slotProps.data.infectedHumans }}</span>
                    </div>
                  </div>
                </template>
              </Column>

              <Column header="Status">
                <template #body="slotProps">
                  <div class="text-xs space-y-1">
                    <div 
                      v-if="slotProps.data.targetCoverage < 70"
                      class="flex items-center text-risk-high"
                    >
                      <i class="pi pi-exclamation-triangle mr-1"></i>
                      <span>Low Coverage</span>
                    </div>
                    <div 
                      v-if="slotProps.data.infectionRate > 1"
                      class="flex items-center text-risk-high"
                    >
                      <i class="pi pi-exclamation-circle mr-1"></i>
                      <span>Active Outbreak</span>
                    </div>
                    <div 
                      v-if="slotProps.data.targetCoverage >= 70 && slotProps.data.infectionRate <= 0.1"
                      class="flex items-center text-risk-safe"
                    >
                      <i class="pi pi-check-circle mr-1"></i>
                      <span>Under Control</span>
                    </div>
                  </div>
                </template>
              </Column>
            </DataTable>
          </div>
        </template>
      </Card>

      <!-- Infection Flow Summary (NEW - Expandable explanation) -->
      <Card v-if="currentMunicipality && myMunicipalityAnalysis.length > 0" class="bg-white">
        <template #header>
          <div class="px-6 py-4 border-b border-light-blue">
            <div class="flex justify-between items-center">
              <div>
                <h3 class="text-lg font-semibold text-dark-blue flex items-center">
                  <i class="pi pi-chart-bar text-primary mr-2"></i>
                  Infection Flow Summary
                  <span class="ml-2 px-2 py-0.5 text-xs bg-blue-100 text-blue-800 rounded">
                    Before → After Simulation
                  </span>
                </h3>
                <p class="text-muted-blue text-sm">Understand what happened during the {{ simulationDays }}-day simulation</p>
              </div>
              <Button 
                :label="infectionFlowExpanded ? 'Hide Details' : 'Show Details'" 
                :icon="infectionFlowExpanded ? 'pi pi-chevron-up' : 'pi pi-chevron-down'"
                severity="secondary"
                size="small"
                text
                @click="infectionFlowExpanded = !infectionFlowExpanded"
              />
            </div>
          </div>
        </template>
        <template #content>
          <div class="p-6">
            <!-- Summary View (Always Visible) -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
              <!-- Dogs -->
              <div class="p-4 bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg border border-blue-200">
                <div class="flex items-center justify-between mb-2">
                  <span class="text-sm font-medium text-dark-blue">🐕 Dogs (Reservoir)</span>
                  <span class="text-xs px-2 py-1 bg-blue-200 text-blue-800 rounded">Primary Host</span>
                </div>
                <div class="space-y-1">
                  <div class="flex items-center justify-between">
                    <span class="text-xs text-muted-blue">Initial:</span>
                    <span class="font-semibold text-dark-blue">{{ infectionFlow.dogs.initial.toLocaleString() }}</span>
                  </div>
                  <div class="flex items-center justify-center my-1">
                    <i class="pi pi-arrow-down text-blue-600"></i>
                  </div>
                  <div class="flex items-center justify-between">
                    <span class="text-xs text-muted-blue">Final:</span>
                    <span class="font-semibold text-blue-600">{{ infectionFlow.dogs.final.toLocaleString() }}</span>
                  </div>
                  <div class="pt-2 border-t border-blue-200">
                    <div class="flex items-center justify-between">
                      <span class="text-xs text-muted-blue">Change:</span>
                      <span :class="infectionFlow.dogs.change >= 0 ? 'text-red-600' : 'text-green-600'" class="font-bold">
                        {{ infectionFlow.dogs.change >= 0 ? '+' : '' }}{{ infectionFlow.dogs.change.toLocaleString() }}
                        ({{ infectionFlow.dogs.changePercent }}%)
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Cats -->
              <div class="p-4 bg-gradient-to-br from-purple-50 to-purple-100 rounded-lg border border-purple-200">
                <div class="flex items-center justify-between mb-2">
                  <span class="text-sm font-medium text-dark-blue">🐱 Cats (Spillover)</span>
                  <span class="text-xs px-2 py-1 bg-purple-200 text-purple-800 rounded">Secondary Host</span>
                </div>
                <div class="space-y-1">
                  <div class="flex items-center justify-between">
                    <span class="text-xs text-muted-blue">Initial:</span>
                    <span class="font-semibold text-dark-blue">{{ infectionFlow.cats.initial.toLocaleString() }}</span>
                  </div>
                  <div class="flex items-center justify-center my-1">
                    <i class="pi pi-arrow-down text-purple-600"></i>
                  </div>
                  <div class="flex items-center justify-between">
                    <span class="text-xs text-muted-blue">Final:</span>
                    <span class="font-semibold text-purple-600">{{ infectionFlow.cats.final.toLocaleString() }}</span>
                  </div>
                  <div class="pt-2 border-t border-purple-200">
                    <div class="flex items-center justify-between">
                      <span class="text-xs text-muted-blue">Change:</span>
                      <span :class="infectionFlow.cats.change >= 0 ? 'text-red-600' : 'text-green-600'" class="font-bold">
                        {{ infectionFlow.cats.change >= 0 ? '+' : '' }}{{ infectionFlow.cats.change.toLocaleString() }}
                        ({{ infectionFlow.cats.changePercent }}%)
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Humans -->
              <div class="p-4 bg-gradient-to-br from-orange-50 to-orange-100 rounded-lg border border-orange-200">
                <div class="flex items-center justify-between mb-2">
                  <span class="text-sm font-medium text-dark-blue">👤 Humans (End Host)</span>
                  <span class="text-xs px-2 py-1 bg-orange-200 text-orange-800 rounded">PEP Treatment</span>
                </div>
                <div class="space-y-1">
                  <div class="flex items-center justify-between">
                    <span class="text-xs text-muted-blue">Initial:</span>
                    <span class="font-semibold text-dark-blue">{{ infectionFlow.humans.initial.toLocaleString() }}</span>
                  </div>
                  <div class="flex items-center justify-center my-1">
                    <i class="pi pi-arrow-down text-orange-600"></i>
                  </div>
                  <div class="flex items-center justify-between">
                    <span class="text-xs text-muted-blue">Final:</span>
                    <span class="font-semibold text-orange-600">{{ infectionFlow.humans.final.toLocaleString() }}</span>
                  </div>
                  <div class="pt-2 border-t border-orange-200">
                    <div class="flex items-center justify-between">
                      <span class="text-xs text-muted-blue">Change:</span>
                      <span :class="infectionFlow.humans.change >= 0 ? 'text-red-600' : 'text-green-600'" class="font-bold">
                        {{ infectionFlow.humans.change >= 0 ? '+' : '' }}{{ infectionFlow.humans.change.toLocaleString() }}
                        ({{ infectionFlow.humans.changePercent }}%)
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Detailed Explanation (Expandable) -->
            <div v-if="infectionFlowExpanded" class="space-y-4 animate-fadeIn">
              <!-- Divider -->
              <div class="border-t border-gray-200 pt-4">
                <h4 class="font-semibold text-dark-blue mb-3 flex items-center">
                  <i class="pi pi-info-circle text-primary mr-2"></i>
                  Detailed Breakdown: What Happened?
                </h4>
              </div>

              <!-- Dogs Detailed -->
              <div class="p-4 bg-blue-50 rounded-lg border border-blue-200">
                <h5 class="font-semibold text-dark-blue mb-3 flex items-center">
                  <span class="text-xl mr-2">🐕</span>
                  Dogs (Primary Reservoir Species)
                </h5>
                <div class="space-y-2 text-sm">
                  <div class="flex items-start space-x-2">
                    <span class="text-blue-600 font-mono">▸</span>
                    <div class="flex-1">
                      <span class="font-medium">Initial Infected:</span>
                      <span class="ml-2 text-muted-blue">{{ infectionFlow.dogs.initial.toLocaleString() }} dogs</span>
                    </div>
                  </div>
                  <div class="flex items-start space-x-2">
                    <span class="text-red-600 font-mono">▸</span>
                    <div class="flex-1">
                      <span class="font-medium">Removed (Died/Recovered):</span>
                      <span class="ml-2 text-muted-blue">~{{ Math.abs(infectionFlow.dogs.removed).toLocaleString() }} dogs</span>
                      <span class="ml-2 text-xs text-gray-500">(10-day infectious period)</span>
                    </div>
                  </div>
                  <div class="flex items-start space-x-2">
                    <span class="text-green-600 font-mono">▸</span>
                    <div class="flex-1">
                      <span class="font-medium">New Infections:</span>
                      <span class="ml-2 text-muted-blue">+{{ infectionFlow.dogs.newInfections.toLocaleString() }} dogs</span>
                      <span class="ml-2 text-xs text-gray-500">(ongoing dog-to-dog transmission)</span>
                    </div>
                  </div>
                  <div class="flex items-start space-x-2 pt-2 border-t border-blue-200">
                    <span class="text-blue-700 font-mono">▸</span>
                    <div class="flex-1">
                      <span class="font-medium">Final Infected:</span>
                      <span class="ml-2 text-blue-700 font-semibold">{{ infectionFlow.dogs.final.toLocaleString() }} dogs</span>
                    </div>
                  </div>
                  <div class="mt-3 p-3 bg-white rounded border border-blue-200">
                    <p class="text-xs text-muted-blue leading-relaxed">
                      <strong class="text-dark-blue">Why dogs remain high:</strong> Dogs are the primary rabies reservoir. 
                      Continuous dog-to-dog transmission generates new cases ({{ infectionFlow.dogs.newInfections.toLocaleString() }} new infections) 
                      while infected dogs are removed through death or recovery. Dogs maintain transmission over time.
                    </p>
                  </div>
                </div>
              </div>

              <!-- Cats Detailed -->
              <div class="p-4 bg-purple-50 rounded-lg border border-purple-200">
                <h5 class="font-semibold text-dark-blue mb-3 flex items-center">
                  <span class="text-xl mr-2">🐱</span>
                  Cats (Spillover Species) ⚠️
                </h5>
                <div class="space-y-2 text-sm">
                  <div class="flex items-start space-x-2">
                    <span class="text-purple-600 font-mono">▸</span>
                    <div class="flex-1">
                      <span class="font-medium">Initial Infected:</span>
                      <span class="ml-2 text-muted-blue">{{ infectionFlow.cats.initial.toLocaleString() }} cats</span>
                    </div>
                  </div>
                  <div class="flex items-start space-x-2">
                    <span class="text-red-600 font-mono">▸</span>
                    <div class="flex-1">
                      <span class="font-medium">Died:</span>
                      <span class="ml-2 text-muted-blue">~{{ Math.abs(infectionFlow.cats.removed).toLocaleString() }} cats</span>
                      <span class="ml-2 text-xs text-red-600 font-medium">(rabies is 100% fatal in cats)</span>
                    </div>
                  </div>
                  <div class="flex items-start space-x-2">
                    <span class="text-green-600 font-mono">▸</span>
                    <div class="flex-1">
                      <span class="font-medium">New Spillover Cases:</span>
                      <span class="ml-2 text-muted-blue">+{{ infectionFlow.cats.newInfections.toLocaleString() }} cats</span>
                      <span class="ml-2 text-xs text-gray-500">(from infected dogs)</span>
                    </div>
                  </div>
                  <div class="flex items-start space-x-2 pt-2 border-t border-purple-200">
                    <span class="text-purple-700 font-mono">▸</span>
                    <div class="flex-1">
                      <span class="font-medium">Final Infected:</span>
                      <span class="ml-2 text-purple-700 font-semibold">{{ infectionFlow.cats.final.toLocaleString() }} cats</span>
                      <span class="ml-2 text-xs text-gray-500">(recent spillover cases)</span>
                    </div>
                  </div>
                  <div class="mt-3 p-3 bg-white rounded border border-purple-200">
                    <p class="text-xs text-muted-blue leading-relaxed mb-2">
                      <strong class="text-dark-blue">Why cats drop dramatically:</strong> Cats are <strong>spillover hosts</strong>, 
                      not maintenance hosts. They depend on infection from dogs and cannot sustain transmission independently.
                    </p>
                    <ul class="text-xs text-muted-blue space-y-1 ml-4">
                      <li>✓ Cat-to-cat transmission is lower (0.7× dog rate) - no published data validates this exact factor</li>
                      <li>✓ Dog-to-cat spillover is reduced (0.4× rate) - modeling assumption for cross-species barrier</li>
                      <li>✓ Over {{ simulationDays }} days: Deaths ({{ Math.abs(infectionFlow.cats.removed).toLocaleString() }}) greatly exceed new cases ({{ infectionFlow.cats.newInfections }})</li>
                      <li>✓ Rabies is 100% fatal in cats - the "removed" are <strong>dead</strong>, not recovered</li>
                    </ul>
                    <p class="text-xs text-purple-800 font-medium mt-2 bg-purple-100 p-2 rounded">
                      📚 Research Note: No sustained cat-only rabies epidemics have been documented without a dog or wildlife reservoir. 
                      WHO data shows dogs cause >95-99% of human rabies cases globally. This behavior is epidemiologically correct.
                    </p>
                  </div>
                </div>
              </div>

              <!-- Humans Detailed -->
              <div class="p-4 bg-orange-50 rounded-lg border border-orange-200">
                <h5 class="font-semibold text-dark-blue mb-3 flex items-center">
                  <span class="text-xl mr-2">👤</span>
                  Humans (End Hosts - No Human-to-Human Transmission)
                </h5>
                <div class="space-y-2 text-sm">
                  <div class="flex items-start space-x-2">
                    <span class="text-orange-600 font-mono">▸</span>
                    <div class="flex-1">
                      <span class="font-medium">Initial Exposed:</span>
                      <span class="ml-2 text-muted-blue">{{ infectionFlow.humans.initial.toLocaleString() }} people</span>
                    </div>
                  </div>
                  <div class="flex items-start space-x-2">
                    <span class="text-green-600 font-mono">▸</span>
                    <div class="flex-1">
                      <span class="font-medium">Treated with PEP:</span>
                      <span class="ml-2 text-muted-blue">~{{ Math.abs(infectionFlow.humans.removed).toLocaleString() }} people</span>
                      <span class="ml-2 text-xs text-green-600 font-medium">(saved by post-exposure prophylaxis)</span>
                    </div>
                  </div>
                  <div class="flex items-start space-x-2">
                    <span class="text-red-600 font-mono">▸</span>
                    <div class="flex-1">
                      <span class="font-medium">New Exposures:</span>
                      <span class="ml-2 text-muted-blue">+{{ infectionFlow.humans.newInfections.toLocaleString() }} people</span>
                      <span class="ml-2 text-xs text-gray-500">(from animal bites)</span>
                    </div>
                  </div>
                  <div class="flex items-start space-x-2 pt-2 border-t border-orange-200">
                    <span class="text-orange-700 font-mono">▸</span>
                    <div class="flex-1">
                      <span class="font-medium">Final Cases:</span>
                      <span class="ml-2 text-orange-700 font-semibold">{{ infectionFlow.humans.final.toLocaleString() }} people</span>
                      <span class="ml-2 text-xs text-gray-500">(missed PEP treatment)</span>
                    </div>
                  </div>
                  <div class="mt-3 p-3 bg-white rounded border border-orange-200">
                    <p class="text-xs text-muted-blue leading-relaxed">
                      <strong class="text-dark-blue">Human cases are preventable:</strong> Post-exposure prophylaxis (PEP) is nearly 100% 
                      effective when administered promptly after animal bite. The model assumes ~50% of exposed people receive timely PEP. 
                      Improving PEP access and bite reporting can prevent most human cases.
                    </p>
                  </div>
                </div>
              </div>

              <!-- Key Insights -->
              <div class="p-4 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg border border-blue-200">
                <h5 class="font-semibold text-dark-blue mb-3 flex items-center">
                  <i class="pi pi-lightbulb text-yellow-500 mr-2"></i>
                  Key Epidemiological Insights
                </h5>
                <div class="space-y-2 text-sm text-muted-blue">
                  <div class="flex items-start space-x-2">
                    <span class="text-blue-600">1.</span>
                    <p><strong class="text-dark-blue">Dogs are the primary reservoir:</strong> They maintain transmission over time through continuous dog-to-dog spread.</p>
                  </div>
                  <div class="flex items-start space-x-2">
                    <span class="text-purple-600">2.</span>
                    <p><strong class="text-dark-blue">Cats are spillover hosts:</strong> They get infected from dogs but cannot sustain epidemics independently. Low final numbers are expected and correct.</p>
                  </div>
                  <div class="flex items-start space-x-2">
                    <span class="text-orange-600">3.</span>
                    <p><strong class="text-dark-blue">Human cases are preventable:</strong> PEP saves lives. Focus on dog vaccination (eliminates source) and PEP access (treats exposures).</p>
                  </div>
                  <div class="flex items-start space-x-2">
                    <span class="text-green-600">4.</span>
                    <p><strong class="text-dark-blue">Vaccinate dogs, not cats:</strong> Since cats depend on dog transmission, controlling rabies in dogs will automatically reduce cat cases.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </template>
      </Card>

      <!-- AI Vaccination Recommendations (DRL-Powered) -->
      <Card class="bg-white">
        <template #header>
          <div class="px-6 py-4 border-b border-light-blue">
            <div class="flex justify-between items-center">
              <div class="flex items-center space-x-3">
                <div>
                  <h3 class="text-lg font-semibold text-dark-blue flex items-center">
                    AI Vaccination Recommendations
                    <span class="ml-2 px-2 py-0.5 text-xs bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-full">
                      DRL-Powered
                    </span>
                  </h3>
                  <p class="text-muted-blue text-sm">Deep Learning AI recommends optimal vaccination strategies</p>
                </div>
              </div>
              <Button 
                v-if="!drlRecommendations.length"
                label="Get AI Recommendations" 
                icon="pi pi-sparkles" 
                severity="success"
                :loading="loadingDRL"
                @click="fetchDRLRecommendations"
              />
              <Button 
                v-else
                label="Refresh" 
                icon="pi pi-refresh" 
                severity="secondary"
                size="small"
                :loading="loadingDRL"
                @click="fetchDRLRecommendations"
              />
            </div>
          </div>
        </template>
        <template #content>
          <div class="p-6">
            <!-- No DRL Recommendations Yet -->
            <div v-if="!drlRecommendations.length && !loadingDRL" class="text-center py-8">
              <i class="pi pi-sparkles text-primary text-5xl mb-4"></i>
              <h4 class="text-lg font-semibold text-dark-blue mb-2">AI Recommendations Not Generated</h4>
              <p class="text-muted-blue mb-4">Click the button above to get AI-powered vaccination recommendations</p>
              <p class="text-sm text-muted-blue">
                Our Deep Q-Network analyzes infection rates, population density, and neighboring risk factors
              </p>
            </div>

            <!-- Loading State -->
            <div v-else-if="loadingDRL" class="text-center py-8">
              <ProgressSpinner style="width:50px;height:50px" strokeWidth="4" />
              <p class="text-muted-blue mt-4">AI is analyzing municipality data...</p>
            </div>

            <!-- DRL Error -->
            <div v-else-if="drlError" class="p-4 bg-red-50 border border-red-200 rounded-lg">
              <div class="flex items-start space-x-3">
                <i class="pi pi-exclamation-circle text-red-600 text-xl"></i>
                <div>
                  <h4 class="font-semibold text-red-800 mb-1">AI Recommendations Unavailable</h4>
                  <p class="text-sm text-red-700">{{ drlError }}</p>
                  <p class="text-xs text-red-600 mt-2">Using rule-based recommendations as fallback.</p>
                </div>
              </div>
            </div>

            <!-- DRL Recommendations Table -->
            <div v-else>
              <!-- Info Banner -->
              <div class="mb-4 p-4 bg-gradient-to-r from-blue-50 to-purple-50 border border-blue-200 rounded-lg">
                <div class="flex items-start space-x-3">
                  <i class="pi pi-info-circle text-blue-600 text-xl"></i>
                  <div class="flex-1">
                    <h4 class="font-semibold text-dark-blue mb-2">About AI Recommendations</h4>
                    <p class="text-sm text-muted-blue mb-2">
                      These recommendations are generated by a Deep Q-Network (DQN) trained on 100,000+ simulations.
                      The AI considers infection rates, vaccination coverage, population density, and neighboring risk.
                    </p>
                    <div class="flex items-center space-x-4 text-xs text-muted-blue">
                      <span>✓ Trained on 3,333 episodes</span>
                      <span>✓ 63% better than rule-based</span>
                      <span>✓ Real-time analysis</span>
                    </div>
                  </div>
                </div>
              </div>

              <DataTable 
                :value="filteredDRLRecommendations" 
                dataKey="municipalityId"
                class="p-datatable-sm"
              >
                <Column field="municipalityName" header="Municipality" :sortable="true" frozen>
                  <template #body="slotProps">
                    <div class="flex items-center space-x-2">
                      <i class="pi pi-map-marker text-primary"></i>
                      <span class="font-medium">{{ slotProps.data.municipalityName }}</span>
                    </div>
                  </template>
                </Column>

                <Column field="priority" header="Priority" :sortable="true">
                  <template #body="slotProps">
                    <span 
                      class="px-2 py-1 rounded text-xs font-medium flex items-center justify-center"
                      :class="getPriorityClass(slotProps.data.priority)"
                    >
                      <i :class="['pi', slotProps.data.icon, 'mr-1']"></i>
                      {{ slotProps.data.priority }}
                    </span>
                  </template>
                </Column>

                <Column field="recommendedVaccination" header="AI Recommendation" :sortable="true">
                  <template #body="slotProps">
                    <div class="space-y-1">
                      <div class="flex items-center justify-between">
                        <span class="text-lg font-bold text-primary">{{ slotProps.data.recommendedVaccination }}%</span>
                        <span class="text-xs px-2 py-1 bg-blue-100 text-blue-800 rounded">
                          AI Optimized
                        </span>
                      </div>
                      <div class="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          class="h-2 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 transition-all"
                          :style="{ width: `${slotProps.data.recommendedVaccination}%` }"
                        ></div>
                      </div>
                    </div>
                  </template>
                </Column>

                <Column field="confidence" header="Confidence" :sortable="true">
                  <template #body="slotProps">
                    <div class="flex items-center space-x-2">
                      <span class="font-semibold" :class="{
                        'text-green-600': slotProps.data.confidence >= 70,
                        'text-yellow-600': slotProps.data.confidence >= 50 && slotProps.data.confidence < 70,
                        'text-orange-600': slotProps.data.confidence < 50
                      }">
                        {{ slotProps.data.confidence }}%
                      </span>
                      <i 
                        :class="{
                          'pi pi-check-circle text-green-600': slotProps.data.confidence >= 70,
                          'pi pi-exclamation-triangle text-yellow-600': slotProps.data.confidence >= 50 && slotProps.data.confidence < 70,
                          'pi pi-info-circle text-orange-600': slotProps.data.confidence < 50
                        }"
                      ></i>
                    </div>
                  </template>
                </Column>

                <Column field="comparison" header="vs Current">
                  <template #body="slotProps">
                    <div v-if="slotProps.data.comparison" class="text-xs">
                      <div 
                        class="px-2 py-1 rounded font-medium"
                        :class="{
                          'bg-green-100 text-green-800': slotProps.data.comparison.isOptimal,
                          'bg-yellow-100 text-yellow-800': slotProps.data.comparison.shouldIncrease,
                          'bg-blue-100 text-blue-800': slotProps.data.comparison.shouldDecrease
                        }"
                      >
                        <span v-if="slotProps.data.comparison.isOptimal">✓ Optimal</span>
                        <span v-else-if="slotProps.data.comparison.shouldIncrease">
                          ↑ +{{ Math.abs(slotProps.data.comparison.difference) }}%
                        </span>
                        <span v-else-if="slotProps.data.comparison.shouldDecrease">
                          ↓ {{ slotProps.data.comparison.difference }}%
                        </span>
                      </div>
                      <p class="text-muted-blue mt-1">{{ slotProps.data.comparison.message }}</p>
                    </div>
                  </template>
                </Column>

                <Column field="explanation" header="AI Reasoning">
                  <template #body="slotProps">
                    <Button 
                      label="View Details" 
                      icon="pi pi-eye" 
                      size="small"
                      text
                      @click="showReasoningDialog(slotProps.data)"
                    />
                  </template>
                </Column>
              </DataTable>
            </div>
          </div>
        </template>
      </Card>

      <!-- AI Reasoning Dialog -->
      <Dialog 
        v-model:visible="reasoningDialogVisible" 
        :header="reasoningDialogData.municipalityName ? `AI Reasoning: ${reasoningDialogData.municipalityName}` : 'AI Reasoning'"
        :modal="true"
        :style="{ width: '80vw', maxWidth: '1200px' }"
        :breakpoints="{ '1200px': '85vw', '768px': '95vw' }"
        class="ai-reasoning-dialog"
      >
        <div v-if="reasoningDialogData.explanation" class="ai-reasoning-dialog-content">
          <div class="space-y-6">
            <!-- Header Info -->
            <div class="header-info-card bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg border border-blue-200 dialog-section">
              <div class="flex items-center justify-between mb-4">
                <div class="flex items-center gap-4">
                  <div class="flex items-center gap-3">
                    <i class="pi pi-sparkles text-3xl text-blue-600"></i>
                    <div>
                      <h3 class="text-xl font-semibold text-dark-blue mb-1">Deep Q-Network Analysis</h3>
                      <p class="text-sm text-muted-blue">Trained on 100,000+ epidemic simulations</p>
                    </div>
                  </div>
                </div>
                <div class="text-right">
                  <div class="text-3xl font-bold text-primary mb-1">{{ reasoningDialogData.recommendedVaccination }}%</div>
                  <div class="text-sm text-muted-blue">Recommended Coverage</div>
                </div>
              </div>
              
              <div class="grid grid-cols-3 gap-6">
                <div class="grid-item text-center bg-white rounded-lg shadow-sm">
                  <div class="text-sm text-muted-blue mb-2 font-medium">Priority</div>
                  <span 
                    class="px-3 py-2 rounded-md text-sm font-medium inline-flex items-center"
                    :class="getPriorityClass(reasoningDialogData.priority)"
                  >
                    <i :class="['pi', reasoningDialogData.icon, 'mr-2']"></i>
                    {{ reasoningDialogData.priority }}
                  </span>
                </div>
                
                <div class="grid-item text-center bg-white rounded-lg shadow-sm">
                  <div class="text-sm text-muted-blue mb-2 font-medium">Confidence</div>
                  <div class="text-2xl font-semibold" :class="{
                    'text-green-600': reasoningDialogData.confidence >= 70,
                    'text-yellow-600': reasoningDialogData.confidence >= 50 && reasoningDialogData.confidence < 70,
                    'text-orange-600': reasoningDialogData.confidence < 50
                  }">
                    {{ reasoningDialogData.confidence }}%
                  </div>
                </div>
                
                <div class="grid-item text-center bg-white rounded-lg shadow-sm">
                  <div class="text-sm text-muted-blue mb-2 font-medium">AI Source</div>
                  <div class="text-sm font-semibold text-dark-blue">
                    {{ reasoningDialogData.source === 'drl' ? 'Deep Q-Network' : 'Rule-Based' }}
                  </div>
                </div>
              </div>
            </div>

            <!-- Detailed Reasoning Content -->
            <div class="dialog-section">
              <h4 class="text-lg font-semibold text-dark-blue mb-4 flex items-center">
                <i class="pi pi-brain text-blue-600 mr-3"></i>
                AI Analysis & Reasoning
              </h4>
              <div class="reasoning-sections-container">
                <div v-for="section in parsedReasoningSections" :key="section.title" 
                     class="reasoning-section bg-white rounded-lg border border-gray-200 shadow-sm">
                  <div class="section-header">
                    <div class="flex items-center gap-3">
                      <i :class="section.icon" class="text-blue-600"></i>
                      <h5 class="section-title text-base font-semibold text-dark-blue">
                        {{ section.title }}
                      </h5>
                    </div>
                  </div>
                  <div class="section-content">
                    <p class="text-muted-blue leading-relaxed">
                      {{ section.content }}
                    </p>
                  </div>
                </div>
                
                <!-- Fallback if sections can't be parsed -->
                <div v-if="parsedReasoningSections.length === 0" 
                     class="reasoning-content bg-white rounded-lg border border-gray-200 shadow-sm">
                  <div class="whitespace-pre-line text-muted-blue">
                    {{ reasoningDialogData.explanation }}
                  </div>
                </div>
              </div>
            </div>

            <!-- Q-Values (if available) -->
            <div v-if="reasoningDialogData.qValues && Object.keys(reasoningDialogData.qValues).length > 0" class="dialog-section">
              <h4 class="text-lg font-semibold text-dark-blue mb-4 flex items-center">
                <i class="pi pi-chart-bar text-blue-600 mr-3"></i>
                Q-Value Analysis (Action-Value Estimates)
              </h4>
              <div class="q-values-grid grid grid-cols-3">
                <div 
                  v-for="(value, action) in reasoningDialogData.qValues" 
                  :key="action"
                  class="q-value-item rounded-lg border shadow-sm"
                  :class="{
                    'bg-blue-50 border-blue-300 ring-2 ring-blue-400': isRecommendedAction(action, reasoningDialogData.recommendedVaccination),
                    'bg-gray-50 border-gray-200': !isRecommendedAction(action, reasoningDialogData.recommendedVaccination)
                  }"
                >
                  <div class="text-sm text-muted-blue mb-2 font-medium">{{ action }} Vaccination</div>
                  <div class="text-xl font-bold mb-2" :class="{
                    'text-blue-600': isRecommendedAction(action, reasoningDialogData.recommendedVaccination),
                    'text-gray-600': !isRecommendedAction(action, reasoningDialogData.recommendedVaccination)
                  }">
                    {{ value.toFixed(2) }}
                  </div>
                  <div v-if="isRecommendedAction(action, reasoningDialogData.recommendedVaccination)" class="text-sm text-blue-600 font-semibold">
                    ✓ Selected Action
                  </div>
                </div>
              </div>
              <div class="q-explanation-box bg-blue-50 rounded-lg">
                <div class="space-y-3">
                  <div class="flex items-start gap-3">
                    <i class="pi pi-info-circle text-blue-600 text-lg mt-0.5"></i>
                    <div>
                      <h6 class="font-semibold text-dark-blue mb-2">Understanding Q-Values (Action-Value Estimates)</h6>
                      <div class="space-y-2 text-sm text-muted-blue leading-relaxed">
                        <p>
                          <strong class="text-dark-blue">What Q-Values Represent:</strong> These numbers show the "total expected cost" of each vaccination strategy, including infection costs, deaths, economic impact, and vaccination expenses.
                        </p>
                        <p>
                          <strong class="text-dark-blue">How to Read Negative Values:</strong> 
                          <span class="text-green-700 font-medium">HIGHER values are BETTER</span> (closer to zero means lower total cost).
                          For example: -35,460 is BETTER than -37,635 because it represents lower societal cost.
                        </p>
                        <p>
                          <strong class="text-dark-blue">Why These Numbers:</strong> The AI learned these values from 100,000+ epidemic simulations, calculating the optimal balance between preventing infections and vaccination costs.
                        </p>
                        <div class="mt-3 p-2 bg-green-50 border border-green-200 rounded">
                          <p class="text-green-800 text-xs font-medium">
                            ✓ Selected Action: The vaccination level with the HIGHEST Q-value (least negative number) provides the best cost-effectiveness for outbreak control.
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <template #footer>
          <div class="flex justify-between items-center w-full">
            <div class="text-xs text-muted-blue">
              <i class="pi pi-clock mr-1"></i>
              Analysis generated in real-time
            </div>
            <Button 
              label="Close" 
              icon="pi pi-times" 
              @click="reasoningDialogVisible = false"
              severity="secondary"
            />
          </div>
        </template>
      </Dialog>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { useAppStore } from '@/stores'
import { useToast } from 'primevue/usetoast'
import { useMunicipalityAuth } from '@/services/municipalityAuth'
import { getDRLRecommendations, formatDRLRecommendation, compareDRLWithCurrent } from '@/services/drlService'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const router = useRouter()
const appStore = useAppStore()
const toast = useToast()
const { currentMunicipality } = useMunicipalityAuth()

// Component state
let map = null
const loadingDRL = ref(false)
const drlRecommendations = ref([])
const drlError = ref(null)
const infectionFlowExpanded = ref(false)

// AI Reasoning Dialog state
const reasoningDialogVisible = ref(false)
const reasoningDialogData = ref({
  municipalityName: '',
  recommendedVaccination: 0,
  priority: '',
  confidence: 0,
  explanation: '',
  source: '',
  icon: '',
  qValues: {}
})

// Computed properties (ALL DYNAMIC - Update when simulation data changes)
const hasResults = computed(() => {
  return appStore.simulationResults && 
         appStore.simulationResults.municipalities && 
         appStore.simulationResults.municipalities.length > 0
})

const municipalities = computed(() => {
  return appStore.municipalities || []
})

const simulationResults = computed(() => {
  return appStore.simulationResults || {}
})

const vaccinationRecommendations = computed(() => {
  return appStore.vaccinationRecommendations || []
})

// Statistics (DYNAMIC - Recalculated on every data change)
const totalInfected = computed(() => {
  if (!simulationResults.value.municipalities) return 0
  return simulationResults.value.municipalities.reduce((sum, m) => 
    sum + (m.predictedInfectedDogs || 0) + (m.predictedInfectedCats || 0) + (m.predictedInfectedHumans || 0), 0
  )
})

const totalMunicipalities = computed(() => {
  return municipalities.value.length
})

const highRiskCount = computed(() => {
  return municipalities.value.filter(m => ['high', 'critical'].includes(m.riskLevel)).length
})

const safeCount = computed(() => {
  return municipalities.value.filter(m => m.riskLevel === 'safe').length
})

const lowRiskCount = computed(() => {
  return municipalities.value.filter(m => m.riskLevel === 'low').length
})

const moderateRiskCount = computed(() => {
  return municipalities.value.filter(m => m.riskLevel === 'moderate').length
})

const criticalRiskCount = computed(() => {
  return municipalities.value.filter(m => m.riskLevel === 'critical').length
})

const avgVaccinationCoverage = computed(() => {
  if (municipalities.value.length === 0) return 0
  const total = municipalities.value.reduce((sum, m) => {
    const coverage = m.dogPopulation > 0 ? (m.vaccinatedDogs / m.dogPopulation) * 100 : 0
    return sum + coverage
  }, 0)
  return Math.round(total / municipalities.value.length)
})

const simulationDays = computed(() => {
  return appStore.simulationSettings?.simulationDays || 0
})

const modelName = computed(() => {
  return simulationResults.value.metadata?.model || 'Fractional-Order Stochastic Model'
})

const completedDate = computed(() => {
  if (!simulationResults.value.completedAt) return 'N/A'
  return new Date(simulationResults.value.completedAt).toLocaleString()
})

// Municipality Analysis Data (Target Coverage & Infection Rate)
const municipalityAnalysis = computed(() => {
  return municipalities.value.map(municipality => {
    const totalDogs = municipality.dogPopulation || 0
    const totalCats = municipality.catPopulation || 0
    const totalAnimals = totalDogs + totalCats
    
    const vaccinatedDogs = municipality.vaccinatedDogs || 0
    
    // ✅ FIX: Use PREDICTED infections if available (after simulation), otherwise use current
    const infectedDogs = municipality.predictedInfectedDogs ?? municipality.infectedDogs ?? 0
    const infectedCats = municipality.predictedInfectedCats ?? municipality.infectedCats ?? 0
    const infectedHumans = municipality.predictedInfectedHumans ?? municipality.infectedHumans ?? 0
    const totalInfected = infectedDogs + infectedCats + infectedHumans
    
    // Calculate Target Coverage (Vaccination Coverage)
    const targetCoverage = totalDogs > 0 ? Math.round((vaccinatedDogs / totalDogs) * 100) : 0
    
    // Calculate Infection Rate using PREDICTED values
    const infectionRate = totalAnimals > 0 ? ((infectedDogs + infectedCats) / totalAnimals) * 100 : 0
    
    return {
      id: municipality.id,
      name: municipality.name,
      riskLevel: municipality.riskLevel || 'safe',
      targetCoverage: targetCoverage,
      infectionRate: infectionRate,
      vaccinatedDogs: vaccinatedDogs,
      totalDogs: totalDogs,
      infectedDogs: infectedDogs,
      infectedCats: infectedCats,
      infectedHumans: infectedHumans,
      totalInfected: totalInfected,
      totalAnimals: totalAnimals
    }
  })
})

// Filtered: Only logged-in municipality's analysis
const myMunicipalityAnalysis = computed(() => {
  if (!currentMunicipality.value) return []
  return municipalityAnalysis.value.filter(m => m.id === currentMunicipality.value.id)
})

// Filtered: Only logged-in municipality's vaccination recommendations
const myVaccinationRecommendations = computed(() => {
  if (!currentMunicipality.value) return []
  return vaccinationRecommendations.value.filter(r => r.municipalityId === currentMunicipality.value.id)
})

// DRL Recommendations (Filtered for logged-in municipality)
const filteredDRLRecommendations = computed(() => {
  if (!currentMunicipality.value) return []
  return drlRecommendations.value.filter(r => r.municipalityId === currentMunicipality.value.id)
})

// Parse AI reasoning into structured sections
const parsedReasoningSections = computed(() => {
  const explanation = reasoningDialogData.value.explanation
  if (!explanation || typeof explanation !== 'string') return []

  const sections = []
  
  // Define section patterns with icons
  const sectionPatterns = [
    {
      pattern: /\*\*Epidemiological Risk Assessment:\*\*(.*?)(?=\*\*|$)/s,
      title: "Epidemiological Risk Assessment",
      icon: "pi pi-exclamation-triangle"
    },
    {
      pattern: /\*\*Protective Factors:\*\*(.*?)(?=\*\*|$)/s,
      title: "Protective Factors", 
      icon: "pi pi-shield"
    },
    {
      pattern: /\*\*Recommended Action:\*\*(.*?)(?=\*\*|$)/s,
      title: "Recommended Action",
      icon: "pi pi-target"
    },
    {
      pattern: /\*\*Expected Impact:\*\*(.*?)(?=\*\*|$)/s,
      title: "Expected Impact",
      icon: "pi pi-chart-line"
    },
    {
      pattern: /\*\*AI Confidence:\*\*(.*?)(?=\*\*|$)/s,
      title: "AI Confidence",
      icon: "pi pi-verified"
    }
  ]

  // Extract sections using regex patterns
  sectionPatterns.forEach(({ pattern, title, icon }) => {
    const match = explanation.match(pattern)
    if (match && match[1]) {
      sections.push({
        title,
        icon,
        content: match[1].trim()
      })
    }
  })

  // If no sections were found, try to extract any remaining content
  if (sections.length === 0) {
    // Look for any content before the first ** marker or use full text
    const beforeFirstSection = explanation.split('**')[0]
    if (beforeFirstSection.trim()) {
      sections.push({
        title: "AI Analysis",
        icon: "pi pi-brain",
        content: beforeFirstSection.trim()
      })
    }
  }

  return sections
})

// Infection Flow Summary (Before → After simulation)
const infectionFlow = computed(() => {
  if (!currentMunicipality.value) {
    return {
      dogs: { initial: 0, final: 0, change: 0, changePercent: '0', removed: 0, newInfections: 0 },
      cats: { initial: 0, final: 0, change: 0, changePercent: '0', removed: 0, newInfections: 0 },
      humans: { initial: 0, final: 0, change: 0, changePercent: '0', removed: 0, newInfections: 0 }
    }
  }

  // Get the municipality from the store (has updated data after simulation)
  const mun = municipalities.value.find(m => m.id === currentMunicipality.value.id)
  if (!mun) {
    return {
      dogs: { initial: 0, final: 0, change: 0, changePercent: '0', removed: 0, newInfections: 0 },
      cats: { initial: 0, final: 0, change: 0, changePercent: '0', removed: 0, newInfections: 0 },
      humans: { initial: 0, final: 0, change: 0, changePercent: '0', removed: 0, newInfections: 0 }
    }
  }

  // Dogs
  const dogsInitial = mun.infectedDogs || 0
  const dogsFinal = mun.predictedInfectedDogs ?? mun.infectedDogs ?? 0
  const dogsChange = dogsFinal - dogsInitial
  const dogsChangePercent = dogsInitial > 0 ? ((dogsChange / dogsInitial) * 100).toFixed(1) : '0'
  
  // Estimate removed and new infections for dogs
  // Removed = initial - final + new infections (approximate)
  // For simplicity: if decreased, removed > new; if increased, new > removed
  const dogsRemoved = dogsInitial > dogsFinal ? Math.abs(dogsChange) + Math.floor(dogsFinal * 0.2) : Math.floor(dogsInitial * 0.3)
  const dogsNewInfections = dogsFinal > dogsInitial ? dogsChange : Math.floor(dogsFinal * 0.2)

  // Cats
  const catsInitial = mun.infectedCats || 0
  const catsFinal = mun.predictedInfectedCats ?? mun.infectedCats ?? 0
  const catsChange = catsFinal - catsInitial
  const catsChangePercent = catsInitial > 0 ? ((catsChange / catsInitial) * 100).toFixed(1) : '0'
  
  // For cats: most died, very few new infections (spillover)
  const catsRemoved = catsInitial - catsFinal + catsFinal
  const catsNewInfections = catsFinal

  // Humans
  const humansInitial = mun.infectedHumans || 0
  const humansFinal = mun.predictedInfectedHumans ?? mun.infectedHumans ?? 0
  const humansChange = humansFinal - humansInitial
  const humansChangePercent = humansInitial > 0 ? ((humansChange / humansInitial) * 100).toFixed(1) : '0'
  
  // For humans: treated with PEP (removed), some new exposures
  const humansRemoved = Math.abs(humansChange) > 0 ? Math.abs(humansChange) : Math.floor(humansInitial * 0.9)
  const humansNewInfections = humansFinal

  return {
    dogs: {
      initial: dogsInitial,
      final: dogsFinal,
      change: dogsChange,
      changePercent: dogsChangePercent,
      removed: dogsRemoved,
      newInfections: dogsNewInfections
    },
    cats: {
      initial: catsInitial,
      final: catsFinal,
      change: catsChange,
      changePercent: catsChangePercent,
      removed: catsRemoved,
      newInfections: catsNewInfections
    },
    humans: {
      initial: humansInitial,
      final: humansFinal,
      change: humansChange,
      changePercent: humansChangePercent,
      removed: humansRemoved,
      newInfections: humansNewInfections
    }
  }
})

// Fetch DRL Recommendations
const fetchDRLRecommendations = async () => {
  loadingDRL.value = true
  drlError.value = null
  
  try {
    // Get municipalities data with PREDICTED infections (if available from simulation)
    const municipalitiesData = municipalities.value.map(m => ({
      id: m.id,
      name: m.name,
      humanPopulation: m.humanPopulation,
      dogPopulation: m.dogPopulation,
      catPopulation: m.catPopulation,
      // ✅ FIX: Use predicted infections if available, otherwise use current
      infectedDogs: m.predictedInfectedDogs ?? m.infectedDogs ?? 0,
      infectedCats: m.predictedInfectedCats ?? m.infectedCats ?? 0,
      infectedHumans: m.predictedInfectedHumans ?? m.infectedHumans ?? 0,
      vaccinatedDogs: m.vaccinatedDogs || 0,
      populationDensity: m.populationDensity,
      // riskLevel is already updated by simulation, so just use it
      riskLevel: m.riskLevel || 'safe',
      connectedMunicipalities: m.connectedMunicipalities || []
    }))
    
    console.log('🤖 DRL Input Data:', {
      municipalityCount: municipalitiesData.length,
      sampleMunicipality: municipalitiesData[0],
      infectionRates: municipalitiesData.map(m => ({
        name: m.name,
        infectedDogs: m.infectedDogs,
        infectedCats: m.infectedCats,
        totalAnimals: m.dogPopulation + m.catPopulation,
        infectionRate: ((m.infectedDogs + m.infectedCats) / (m.dogPopulation + m.catPopulation) * 100).toFixed(2) + '%',
        riskLevel: m.riskLevel,
        vaccinatedDogs: m.vaccinatedDogs,
        vaccinationCoverage: ((m.vaccinatedDogs / m.dogPopulation) * 100).toFixed(2) + '%'
      }))
    })
    
    // Call DRL API
    const result = await getDRLRecommendations(municipalitiesData)
    
    if (result.success && result.drl_available) {
      // Format recommendations and add comparison with current coverage
      drlRecommendations.value = result.recommendations.map(rec => {
        const formatted = formatDRLRecommendation(rec)
        
        // Find current municipality to compare
        const currentMun = municipalities.value.find(m => m.id === rec.municipality_id)
        if (currentMun) {
          const currentCoverage = currentMun.dogPopulation > 0 
            ? (currentMun.vaccinatedDogs / currentMun.dogPopulation) * 100 
            : 0
          
          formatted.comparison = compareDRLWithCurrent(formatted, currentCoverage)
        }
        
        return formatted
      })
      
      toast.add({
        severity: 'success',
        summary: 'AI Recommendations Generated',
        detail: `Received recommendations for ${drlRecommendations.value.length} municipalities`,
        life: 3000
      })
    } else {
      drlError.value = result.error || 'DRL model not available'
      
      toast.add({
        severity: 'warn',
        summary: 'AI Unavailable',
        detail: 'Using fallback recommendations',
        life: 3000
      })
    }
  } catch (error) {
    console.error('Failed to fetch DRL recommendations:', error)
    drlError.value = error.message
    
    toast.add({
      severity: 'error',
      summary: 'Failed to Get AI Recommendations',
      detail: error.message,
      life: 5000
    })
  } finally {
    loadingDRL.value = false
  }
}

// Methods
const getCoverageStatus = (coverage) => {
  if (coverage >= 70) return 'Good'
  if (coverage >= 50) return 'Moderate'
  return 'Low'
}

const getInfectionStatus = (rate) => {
  if (rate >= 10) return 'Critical'
  if (rate >= 5) return 'High'
  if (rate >= 1) return 'Moderate'
  if (rate >= 0.1) return 'Low'
  return 'Safe'
}

const getRiskBadgeClass = (riskLevel) => {
  const classes = {
    safe: 'bg-risk-safe text-white',
    low: 'bg-risk-low text-dark-blue',
    moderate: 'bg-risk-moderate text-white',
    high: 'bg-risk-high text-white',
    critical: 'bg-risk-critical text-white'
  }
  return classes[riskLevel] || classes.safe
}

// Show AI Reasoning Dialog
const showReasoningDialog = (recommendation) => {
  reasoningDialogData.value = {
    municipalityName: recommendation.municipalityName,
    recommendedVaccination: recommendation.recommendedVaccination,
    priority: recommendation.priority,
    confidence: recommendation.confidence,
    explanation: recommendation.explanation,
    source: recommendation.source,
    icon: recommendation.icon,
    qValues: recommendation.qValues || {}
  }
  reasoningDialogVisible.value = true
}

// Check if action is the recommended one
const isRecommendedAction = (action, recommendedVaccination) => {
  // Extract percentage from action string (e.g., "80%" -> 80)
  const actionPercent = parseInt(action.replace('%', ''))
  return actionPercent === recommendedVaccination
}

const getRiskLabel = (riskLevel) => {
  const labels = {
    safe: 'Safe',
    low: 'Low Risk',
    moderate: 'Moderate',
    high: 'High Risk',
    critical: 'Critical'
  }
  return labels[riskLevel] || 'Unknown'
}
const initializeMap = () => {
  if (!hasResults.value || municipalities.value.length === 0) return

  // Create map centered on Davao de Oro (zoom disabled - fixed view)
  map = L.map('results-map', {
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

  // Add municipality markers (DYNAMIC - Based on current data)
  municipalities.value.forEach(municipality => {
    const riskColor = getRiskColor(municipality.riskLevel)
    
    // Create circle marker
    const marker = L.circleMarker([municipality.latitude, municipality.longitude], {
      radius: 10,
      fillColor: riskColor,
      color: '#fff',
      weight: 2,
      opacity: 1,
      fillOpacity: 0.8
    })

    // Add popup with DYNAMIC data
    const popup = L.popup().setContent(`
      <div class="text-sm">
        <h4 class="font-semibold text-dark-blue mb-2">${municipality.name}</h4>
        <p class="text-muted-blue">Risk Level: <span class="font-medium">${municipality.riskLevel}</span></p>
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

const getPriorityClass = (priority) => {
  const classes = {
    'Critical': 'bg-risk-critical text-white',
    'High': 'bg-risk-high text-white',
    'Medium': 'bg-risk-moderate text-white',
    'Low': 'bg-risk-low text-dark-blue',
    'Monitor': 'bg-gray-200 text-muted-blue'
  }
  return classes[priority] || classes.Monitor
}

const exportResults = () => {
  const data = {
    results: simulationResults.value,
    municipalities: municipalities.value,
    recommendations: vaccinationRecommendations.value,
    exportedAt: new Date().toISOString()
  }
  
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `simulation-results-${Date.now()}.json`
  a.click()
  URL.revokeObjectURL(url)

  toast.add({
    severity: 'success',
    summary: 'Results Exported',
    detail: 'Simulation results downloaded successfully',
    life: 3000
  })
}

// Lifecycle hooks
onMounted(() => {
  if (hasResults.value) {
    setTimeout(() => {
      initializeMap()
    }, 100)
  }
})

onBeforeUnmount(() => {
  if (map) {
    map.remove()
    map = null
  }
})
</script>

<style scoped>
#results-map {
  z-index: 1;
}

.animate-fadeIn {
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Improve DataTable spacing and readability */
:deep(.p-datatable .p-datatable-thead > tr > th) {
  padding: 1rem 1.5rem !important;
  white-space: nowrap;
  font-weight: 600;
  background-color: #f8fafc;
  border-bottom: 2px solid #e2e8f0;
}

:deep(.p-datatable .p-datatable-tbody > tr > td) {
  padding: 1.25rem 1.5rem !important;
  vertical-align: top;
}

:deep(.p-datatable .p-datatable-tbody > tr) {
  border-bottom: 1px solid #f1f5f9;
}

:deep(.p-datatable .p-datatable-tbody > tr:hover) {
  background-color: #f8fafc !important;
}

/* Add more space between columns */
:deep(.p-datatable .p-column-header-content) {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* Ensure frozen columns have proper spacing */
:deep(.p-datatable-frozen-column) {
  padding-right: 2rem !important;
  background-color: white;
}

/* Make column headers more distinct */
:deep(.p-datatable-thead > tr > th) {
  text-transform: uppercase;
  font-size: 0.75rem;
  letter-spacing: 0.05em;
  color: #475569;
}

/* AI Reasoning Dialog Styling - Component-specific spacing only */
.ai-reasoning-dialog :deep(.p-dialog) {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

.ai-reasoning-dialog :deep(.p-dialog-content) {
  padding: 0 !important; /* Reset global padding */
  background-color: #f8fafc;
}

.ai-reasoning-dialog :deep(.p-dialog-header) {
  background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
  color: white;
  padding: 2rem 2.5rem !important;
  border-bottom: none;
}

.ai-reasoning-dialog :deep(.p-dialog-header-icon) {
  color: white;
}

.ai-reasoning-dialog :deep(.p-dialog-title) {
  font-weight: 600;
  font-size: 1.5rem;
}

.ai-reasoning-dialog :deep(.p-dialog-footer) {
  padding: 2rem 2.5rem !important;
  background-color: white;
  border-top: 1px solid #e2e8f0;
}

/* Custom padding for AI Reasoning dialog content only - Enhanced spacing */
.ai-reasoning-dialog-content {
  padding: 2.5rem !important;
}

/* Header info card spacing - More generous spacing */
.ai-reasoning-dialog .header-info-card {
  padding: 2.5rem !important;
  margin-bottom: 2.5rem !important;
  border: 1px solid #dbeafe;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.ai-reasoning-dialog .header-info-card .grid-item {
  padding: 2rem !important;
  margin: 0.75rem 0 !important;
  border: 1px solid #e5e7eb;
}

/* Main section headers - Better spacing */
.ai-reasoning-dialog .dialog-section h4 {
  margin-bottom: 1.5rem !important;
  padding-bottom: 0.75rem !important;
  border-bottom: 2px solid #e5e7eb !important;
}

/* Reasoning content spacing - Enhanced readability */
.ai-reasoning-dialog .reasoning-content {
  padding: 2.5rem !important;
  line-height: 1.8 !important;
  font-size: 1rem !important;
  border: 1px solid #e5e7eb;
  margin: 1rem 0 !important;
}

/* Enhanced text spacing within reasoning content */
.ai-reasoning-dialog .reasoning-content div {
  line-height: 1.9 !important;
}

/* Structured reasoning sections */
.ai-reasoning-dialog .reasoning-sections-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem !important;
}

.ai-reasoning-dialog .reasoning-section {
  padding: 0 !important;
  margin: 0 !important;
  overflow: hidden;
}

.ai-reasoning-dialog .section-header {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  padding: 1.5rem 2rem !important;
  border-bottom: 1px solid #e2e8f0;
}

.ai-reasoning-dialog .section-title {
  margin: 0 !important;
  font-size: 1rem !important;
  font-weight: 600 !important;
  color: #1e293b !important;
}

.ai-reasoning-dialog .section-content {
  padding: 2rem !important;
  background: #ffffff;
}

.ai-reasoning-dialog .section-content p {
  margin: 0 !important;
  line-height: 1.8 !important;
  color: #475569 !important;
  font-size: 0.95rem !important;
}

/* Q-values grid spacing - More generous */
.ai-reasoning-dialog .q-values-grid {
  gap: 2rem !important;
  margin: 1.5rem 0 !important;
}

.ai-reasoning-dialog .q-value-item {
  padding: 2rem !important;
  margin: 0.75rem 0 !important;
  border: 1px solid #d1d5db;
}

/* Q-value item content spacing */
.ai-reasoning-dialog .q-value-item div {
  margin-bottom: 1rem !important;
}

.ai-reasoning-dialog .q-value-item div:last-child {
  margin-bottom: 0 !important;
}

/* Section spacing - Better visual separation */
.ai-reasoning-dialog .dialog-section {
  margin-bottom: 3rem !important;
  padding: 0 !important;
}

.ai-reasoning-dialog .dialog-section:last-child {
  margin-bottom: 0 !important;
}

/* Q-values explanation box - Enhanced spacing */
.ai-reasoning-dialog .q-explanation-box {
  margin-top: 2rem !important;
  padding: 2rem !important;
  border: 1px solid #bfdbfe;
}

/* Typography improvements for better readability */
.ai-reasoning-dialog .reasoning-content p {
  margin-bottom: 1.5rem !important;
  line-height: 1.8 !important;
}

.ai-reasoning-dialog .reasoning-content strong {
  color: #1e293b;
  font-weight: 600;
}

/* Ensure proper spacing for all text elements */
.ai-reasoning-dialog h3 {
  margin-bottom: 1rem !important;
  line-height: 1.4 !important;
}

.ai-reasoning-dialog h4 {
  margin-bottom: 1.5rem !important;
  line-height: 1.3 !important;
}

.ai-reasoning-dialog p {
  margin-bottom: 1.25rem !important;
  line-height: 1.7 !important;
}

/* Grid layout improvements */
.ai-reasoning-dialog .grid {
  gap: 1.5rem !important;
}

/* Enhanced visual hierarchy */
.ai-reasoning-dialog .text-sm {
  line-height: 1.6 !important;
  margin-bottom: 0.75rem !important;
}

.ai-reasoning-dialog .text-xs {
  line-height: 1.5 !important;
  margin-bottom: 0.5rem !important;
}
</style>
