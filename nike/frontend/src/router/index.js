import { createRouter, createWebHistory } from 'vue-router'
import routes from 'router/routes.js'
import userService from 'service/user.service'
import { useAuthStore } from 'stores/auth-store'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior() {
    return { left: 0, top: 0, behavior: 'smooth' }
  }
})

/**
 * Handle check user login
 *
 * @returns boolean
 */
const checkUserLogin = async () => {
  const user = await userService.getMe()
  return !!user
}

/**
 * Handle check authentication every time page change
 */
router.beforeEach(async (to) => {
  const auth = useAuthStore()
  let checkLogin = true
  if (!auth.isLoggedIn) {
    checkLogin = await checkUserLogin()
  }

  // Check login to access admin routes
  if (auth.getRole) {
    if (to.meta?.role !== 'admin') {
      return '/v1/admin'
    }
    return true
  }
  // Check if the user has permission to access the route
  if (!auth.getRole) {
    if (to.path === '/v1/admin/sign-in') {
      return true
    }
    if (to.path.includes(['/v1/admin'])) {
      return '/v1/admin/sign-in'
    }
  }

  // Check login to access cart
  if (!checkLogin && to.name.includes(['cart', 'sign-in', 'sign-up'])) {
    return '/sing-in'
  }
  if (to.name.includes('sign-in') && checkLogin) {
    return '/'
  }
  return true
})

export default router
