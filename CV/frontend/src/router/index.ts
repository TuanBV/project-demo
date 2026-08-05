import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'landing',
      component: () => import('../pages/LandingPage.vue'),
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../pages/LoginPage.vue'),
      meta: { guestOnly: true },
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../pages/RegisterPage.vue'),
      meta: { guestOnly: true },
    },
    {
      path: '/dashboard/cvs',
      name: 'dashboard-cvs',
      component: () => import('../pages/DashboardCvsPage.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/dashboard/cvs/:id/edit',
      name: 'resume-edit',
      component: () => import('../pages/ResumeEditPage.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/cv/:publicId/:slug',
      name: 'public-resume',
      component: () => import('../pages/PublicResumePage.vue'),
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('../pages/NotFoundPage.vue'),
    },
  ],
})

router.beforeEach((to) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }
  if (to.meta.guestOnly && authStore.isAuthenticated) {
    return { name: 'dashboard-cvs' }
  }
  return true
})

export { router }
