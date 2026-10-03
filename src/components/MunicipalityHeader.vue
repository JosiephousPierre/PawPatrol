<template>
  <div class="bg-white border-b border-light-blue shadow-sm">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between py-4">
        <!-- Municipality Info -->
        <div class="flex items-center space-x-4">
          <div class="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center">
            <i class="pi pi-building text-primary text-xl"></i>
          </div>
          <div>
            <h2 class="text-xl font-semibold text-dark-blue">
              {{ currentMunicipality?.name || 'Unknown Municipality' }}
            </h2>
            <p class="text-sm text-muted-blue">
              {{ currentMunicipality?.region || 'Davao de Oro' }} • 
              {{ getPermissionLabel() }}
            </p>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex items-center space-x-3">
          <!-- Data Sync Status -->
          <div class="flex items-center space-x-2 px-3 py-1 bg-green-50 rounded-lg">
            <div class="w-2 h-2 bg-green-500 rounded-full"></div>
            <span class="text-xs text-green-700 font-medium">Data Synced</span>
          </div>

          <!-- Municipality Menu -->
          <Dropdown v-if="isAdmin" v-model="selectedMunicipality" :options="allMunicipalities" 
                   optionLabel="name" optionValue="id" placeholder="Switch Municipality"
                   class="w-48" @change="switchMunicipality" />

          <!-- User Menu -->
          <Menu ref="userMenu" :model="userMenuItems" :popup="true">
            <template #item="{ item }">
              <div class="flex items-center space-x-2 px-3 py-2 hover:bg-background rounded cursor-pointer"
                   @click="item.command">
                <i :class="item.icon" class="text-muted-blue"></i>
                <span class="text-dark-blue">{{ item.label }}</span>
              </div>
            </template>
          </Menu>

          <Button icon="pi pi-user" severity="secondary" outlined size="small" 
                  @click="toggleUserMenu" aria-label="User Menu" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useConfirm } from 'primevue/useconfirm'
import { useToast } from 'primevue/usetoast'
import { useMunicipalityAuth } from '@/services/municipalityAuth'
import { useAppStore } from '@/stores'

const router = useRouter()
const confirm = useConfirm()
const toast = useToast()
const { currentMunicipality, hasPermission, logout } = useMunicipalityAuth()
const appStore = useAppStore()

const userMenu = ref()
const selectedMunicipality = ref(null)

const isAdmin = computed(() => hasPermission('view_all_data'))
const allMunicipalities = computed(() => appStore.municipalities)

const getPermissionLabel = () => {
  if (hasPermission('view_all_data')) return 'Regional Administrator'
  if (hasPermission('manage_own_data')) return 'Municipality Manager'
  return 'Observer'
}

const userMenuItems = ref([
  {
    label: 'My Profile',
    icon: 'pi pi-user',
    command: () => {
      toast.add({
        severity: 'info',
        summary: 'Profile',
        detail: `Logged in as ${currentMunicipality.value?.name}`,
        life: 3000
      })
    }
  },
  {
    label: 'Data Settings',
    icon: 'pi pi-cog',
    command: () => {
      router.push('/municipalities')
    }
  },
  { separator: true },
  {
    label: 'Help & Support',
    icon: 'pi pi-question-circle',
    command: () => {
      toast.add({
        severity: 'info',
        summary: 'Support',
        detail: 'Contact Regional Health Office: (082) XXX-XXXX',
        life: 5000
      })
    }
  },
  {
    label: 'Logout',
    icon: 'pi pi-sign-out',
    command: handleLogout
  }
])

const toggleUserMenu = (event) => {
  userMenu.value.toggle(event)
}

const switchMunicipality = (municipalityId) => {
  if (!isAdmin.value) return
  
  // This would switch the admin's view to a different municipality
  // For now, just show a message
  toast.add({
    severity: 'info',
    summary: 'Municipality Switch',
    detail: `Viewing data for ${municipalityId}`,
    life: 3000
  })
}

function handleLogout() {
  confirm.require({
    message: 'Are you sure you want to logout?',
    header: 'Confirm Logout',
    icon: 'pi pi-exclamation-triangle',
    accept: () => {
      logout()
      router.push('/login')
      toast.add({
        severity: 'success',
        summary: 'Logged Out',
        detail: 'You have been successfully logged out',
        life: 3000
      })
    }
  })
}
</script>