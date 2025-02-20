const routes = [
  {
    path: '/',
    name: 'layout',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {
        path: '',
        name: 'home',
        component: () => import('views/HomeView.vue'),
      },
      // {
      //   path: 'new-featured',
      //   name: 'new-featured',
      //   component: () => import('views/user/NewFeaturedView.vue'),
      // },
      // {
      //   path: 'blog',
      //   name: 'blog',
      //   component: () => import('views/user/BlogView.vue'),
      // },
      {
        path: 'product/:type1?/:type2?/:type3?',
        name: 'product',
        component: () => import('views/ProductView.vue'),
      },
      // {
      //   path: 'cart',
      //   name: 'cart',
      //   component: () => import('views/user/CartView.vue'),
      //   meta: { requiresAuth: true },
      // },
      // {
      //   path: 'profile',
      //   name: 'profile',
      //   component: () => import('views/user/ProfileView.vue'),
      //   meta: { requiresAuth: true },
      // },
    ],
  },
  // product
  {
    path: '/sign-in',
    name: 'sign-in',
    component: () => import('views/user/account/SignInView.vue'),
  },
  // {
  //   path: '/forgot-password',
  //   name: 'forgot-password',
  //   component: () => import('components/user/account/ForgotPasswordView.vue'),
  // },
  // {
  //   path: '/change-password/:newPassword',
  //   name: 'change-password',
  //   component: () => import('components/user/account/ChangePasswordView.vue'),
  // },
  // {
  //   path: '/sign-up',
  //   name: 'sign-up',
  //   component: () => import('components/user/account/SignUpView.vue'),
  // },
  {
    path: '/:catchAll(.*)',
    name: 'Not Found',
    component: () => import('components/common/page-error/NotFound.vue'),
  },
]
export default routes
