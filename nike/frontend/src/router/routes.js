const routes = [
  {
    path: '/',
    name: 'layout',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {
        path: '',
        name: 'home',
        component: () => import('views/product/HomeView.vue')
      },
      {
        path: 'new-featured',
        name: 'new-featured',
        component: () => import('views/product/NewFeaturedView.vue')
      },
      {
        path: 'blog',
        name: 'blog',
        component: () => import('views/product/BlogView.vue')
      },
      {
        path: 'product/:type1?/:type2?/:type3?',
        name: 'product',
        component: () => import('views/product/ProductView.vue')
      },
      {
        path: 'cart',
        name: 'cart',
        component: () => import('views/product/CartView.vue'),
        meta: { requiresAuth: true }
      }
    ]
  },
  {
    path: '/v1/admin/',
    name: 'layout-admin',
    component: () => import('layouts/AdminLayout.vue'),
    children: [
      {
        path: '',
        name: 'home-admin',
        component: () => import('views/admin/HomeView.vue'),
        meta: { role: 'admin' }
      }
    ]
  },
  // product
  {
    path: '/sign-in',
    name: 'sign-in',
    component: () => import('components/account/SignInView.vue')
  },
  {
    path: '/forgot-password',
    name: 'forgot-password',
    component: () => import('components/account/ForgotPasswordView.vue')
  },
  {
    path: '/sign-up',
    name: 'sign-up',
    component: () => import('components/account/SignUpView.vue')
  },
  // admin
  {
    path: '/v1/admin/sign-in',
    name: 'admin-sign-in',
    component: () => import('components/account/AdminSignInView.vue'),
    meta: { role: 'admin' }
  },
  {
    path: '/:catchAll(.*)',
    name: 'Not Found',
    component: () => import('components/page-error/NotFound.vue')
  }
]
export default routes
