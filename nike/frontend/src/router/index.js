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
  if (to.fullPath.includes('v1/admin')) {
    document.title = 'Page Admin'
  }
  let checkLogin = await checkUserLogin()

  // Check if the account login is admin
  if (auth.getRole) {
    if (to.meta?.role !== 'admin') {
      return '/v1/admin'
    }
  } else {
    // Access to the screen requires login: Cart, Profile
    if (!checkLogin && ['cart', 'profile'].includes(to.name)) {
      return '/sign-in'
    }
    if (['sign-in', 'sign-up'].includes(to.name) && checkLogin) {
      return '/'
    }
    // Access to admin screen then error
    if (to.meta?.role === 'admin' && checkLogin) {
      return '/404'
    }
  }
  // Not log in and directory is '/v1/admin/sign-in'
  if (!checkLogin && to.path === '/v1/admin/sign-in') {
    return true
  }
  // Not log in and access to directory admin
  if (!checkLogin && to.meta?.role === 'admin') {
    return '/v1/admin/sign-in'
  }
  return true
})

export default router
