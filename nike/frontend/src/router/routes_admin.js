const routes_admin = [
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
      },
      {
        path: 'user',
        name: 'admin-user',
        component: () => import('views/admin/UserView.vue'),
        meta: { role: 'admin' }
      },
      {
        path: 'category',
        name: 'admin-category',
        component: () => import('views/admin/CategoryView.vue'),
        meta: { role: 'admin' }
      },
      {
        path: 'product',
        meta: { role: 'admin' },
        children: [
          {
            path: '',
            name: 'admin-product',
            component: () => import('views/admin/product/ProductView.vue')
          },
          {
            path: 'add',
            name: 'admin-product-add',
            component: () => import('views/admin/product/ProductAddView.vue')
          }
        ]
      },
      {
        path: 'slide',
        meta: { role: 'admin' },
        children: [
          {
            path: '',
            name: 'admin-slide',
            component: () => import('views/admin/slide/SlideView.vue')
          },
          {
            path: 'add',
            name: 'admin-slide-add',
            component: () => import('views/admin/slide/SlideAddView.vue')
          }
        ]
      },
      {
        path: 'order',
        name: 'admin-order',
        component: () => import('views/admin/order/OrderView.vue'),
        meta: { role: 'admin' }
      },
      {
        path: 'blog',
        name: 'admin-blog',
        component: () => import('views/admin/HomeView.vue'),
        meta: { role: 'admin' }
      },
      {
        path: 'email',
        name: 'admin-email',
        component: () => import('views/admin/EmailView.vue'),
        meta: { role: 'admin' }
      },
      {
        path: 'sale',
        name: 'admin-sale',
        component: () => import('views/admin/SaleView.vue'),
        meta: { role: 'admin' }
      },
      {
        path: 'post',
        name: 'admin-post',
        component: () => import('views/admin/post/PostView.vue'),
        meta: { role: 'admin' }
      },
      {
        path: 'post-add',
        name: 'admin-post-add',
        component: () => import('views/admin/post/PostAddView.vue'),
        meta: { role: 'admin' }
      },
      {
        path: 'chat',
        name: 'admin-chat',
        component: () => import('views/admin/ChatView.vue'),
        meta: { role: 'admin' }
      },
      {
        path: 'setting',
        name: 'admin-setting',
        component: () => import('views/admin/SettingView.vue'),
        meta: { role: 'admin' }
      }
    ]
  },
  // admin
  {
    path: '/v1/admin/sign-in',
    name: 'admin-sign-in',
    component: () => import('components/admin/account/SignInView.vue'),
    meta: { role: 'admin' }
  },
  {
    path: '/v1/admin/forgot-password',
    name: 'admin-forgot-password',
    component: () => import('components/admin/account/ForgotPasswordView.vue'),
    meta: { role: 'admin' }
  },

  {
    path: '/v1/admin/change-password/:newPassword',
    name: 'admin-change-password',
    component: () => import('components/admin/account/ChangePasswordView.vue'),
    meta: { role: 'admin' }
  }
]
export default routes_admin
