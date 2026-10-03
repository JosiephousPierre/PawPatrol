import { createRouter, createWebHistory } from 'vue-router'
import { useMunicipalityAuth } from '@/services/municipalityAuth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'landing',
      component: () => import('@/pages/LandingPage.vue')
    },
    {
      path: '/login',
      name: 'municipality-login',
      component: () => import('@/pages/MunicipalityLogin.vue')
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('@/layouts/AppLayout.vue'),
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          name: 'dashboard-home',
          component: () => import('@/pages/DashboardPage.vue')
        },
        {
          path: '/municipalities',
          name: 'municipalities',
          component: () => import('@/pages/MunicipalityManagement.vue'),
          meta: { requiresAuth: true }
        },
        {
          path: '/simulation',
          name: 'simulation',
          component: () => import('@/pages/SimulationPage.vue'),
          meta: { requiresAuth: true }
        },
        {
          path: '/results',
          name: 'results',
          component: () => import('@/pages/ResultsPage.vue'),
          meta: { requiresAuth: true }
        },
        {
          path: '/predictive-analysis',
          name: 'predictive-analysis',
          component: () => import('@/pages/PredictiveAnalysisPage.vue'),
          meta: { requiresAuth: true }
        },
        {
          path: '/cost-estimation',
          name: 'cost-estimation',
          component: () => import('@/pages/CostEstimationPage.vue'),
          meta: { requiresAuth: true }
        },
        {
          path: '/about',
          name: 'about',
          component: () => import('@/pages/AboutPage.vue'),
          meta: { requiresAuth: true }
        }
      ]
    }
  ]
})

// Navigation guard for municipality authentication
router.beforeEach((to, from, next) => {
  const { isAuthenticated, restoreSession } = useMunicipalityAuth()
  
  // Try to restore session from localStorage
  if (!isAuthenticated.value) {
    restoreSession()
  }
  
  // Routes that require authentication
  if (to.meta.requiresAuth) {
    if (!isAuthenticated.value) {
      // Redirect to municipality login
      next('/login')
      return
    }
  }
  
  // Redirect authenticated users from login page
  if (to.name === 'municipality-login' && isAuthenticated.value) {
    next('/dashboard')
    return
  }
  
  next()
})

export default router