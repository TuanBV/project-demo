import routes_admin from 'router/routes_admin.js'
import routes_user from 'router/routes_user.js'

const routes = [
  ...routes_user,
  ...routes_admin,
  {
    path: '/:catchAll(.*)',
    name: 'Not Found',
    component: () => import('components/common/page-error/NotFound.vue')
  }
]
export default routes
