const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {
        path: '',
        component: () => import('pages/manager-cv/ContactCandidateList.vue'),
        name: 'contact_candidate',
        meta: {
          requiredAuth: true,
        },
      },
      {
        path: 'add-cv',
        component: () => import('pages/manager-cv/AddCV.vue'),
        name: 'add_cv',
        meta: {
          requiredAuth: true,
        },
      },
      {
        path: 'template/list',
        component: () => import('pages/settings/ListTemplate.vue'),
        name: 'list_template',
        meta: {
          requiredAuth: true,
        },
      },
      {
        path: 'param/list',
        component: () => import('pages/settings/ListParam.vue'),
        name: 'list_param',
        meta: {
          requiredAuth: true,
        },
      },
      {
        path: 'user/list',
        component: () => import('pages/user/ListUser.vue'),
        name: 'list_user',
        meta: {
          requiredAuth: true,
        },
      },
      {
        path: 'recommender',
        component: () => import('src/pages/recommenders/ListPage.vue'),
        name: 'recommender',
        meta: {
          requiresAuth: true,
        },
      },
      {
        path: 'interview-schedule',
        component: () => import('src/pages/manager-cv/InterviewSchedule.vue'),
        name: 'interview_schedule',
        meta: {
          requiredAuth: true,
        },
      },
      {
        path: 'candidate-list',
        component: () => import('src/pages/manager-cv/CandidateList.vue'),
        name: 'candidate_list',
        meta: {
          requiredAuth: true,
        },
      },
      {
        path: 'staff-list',
        component: () => import('src/pages/manager-cv/StaffList.vue'),
        name: 'staff_list',
        meta: {
          requiredAuth: true,
        },
      },
      {
        path: 'black-list',
        component: () => import('src/pages/manager-cv/BlackList.vue'),
        name: 'black_list',
        meta: {
          requiredAuth: true,
        },
      },
      {
        path: 'confirm-test',
        component: () => import('src/pages/manager-cv/ConfirmTest.vue'),
        name: 'confirm_test',
        meta: {
          requiredAuth: true,
        },
      },
      {
        path: 'invite-interview',
        component: () => import('src/pages/manager-cv/InviteInterview.vue'),
        name: 'invite_interview',
        meta: {
          requiredAuth: true,
        },
      },
      {
        path: 'candidate-assessment',
        component: () => import('src/pages/manager-cv/CandidateAssessment.vue'),
        name: 'candidate_assessment',
        meta: {
          requiredAuth: true,
        },
      },
      {
        path: 'send-results',
        component: () => import('src/pages/manager-cv/SendResults.vue'),
        name: 'send_results',
        meta: {
          requiredAuth: true,
        },
      },
      {
        path: 'update-offers',
        component: () => import('src/pages/manager-cv/UpdateOffers.vue'),
        name: 'update_offers',
        meta: {
          requiredAuth: true,
        },
      },
      {
        path: 'send-forms',
        component: () => import('src/pages/manager-cv/SendForms.vue'),
        name: 'send_forms',
        meta: {
          requiredAuth: true,
        },
      },
      {
        path: 'candidate-pass-list',
        component: () => import('src/pages/manager-cv/CandidatePassList.vue'),
        name: 'candidate_pass_list',
        meta: {
          requiredAuth: true,
        },
      },
      {
        path: 'candidate_confirm',
        component: () => import('src/pages/manager-cv/CandidateConfirm.vue'),
        name: 'candidate_confirm',
        meta: {
          requiredAuth: true,
        },
      },
      {
        path: 'setting-mail',
        component: () => import('src/pages/settings/SettingMail.vue'),
        name: 'setting_mail',
        meta: {
          requiredAuth: true,
        },
      },
    ],
  },
  {
    path: '/',
    component: () => import('layouts/AuthLayout.vue'),
    children: [
      {
        path: 'login',
        name: 'login',
        component: () => import('pages/auth/LoginPage.vue'),
        meta: {
          requiredAuth: true,
        },
      },
      {
        path: 'forgot-password',
        name: 'forgot_password',
        component: () => import('pages/auth/ForgotPassword.vue'),
        meta: {
          requiredAuth: false,
        },
      },
      {
        path: 'password-reset',
        name: 'password_reset',
        component: () => import('pages/auth/PasswordReset.vue'),
        meta: {
          requiredAuth: false,
        },
      },
      {
        path: '/form-candidate',
        component: () => import('src/pages/FormCandidate.vue'),
        name: 'form_candidate',
        meta: {
          requiredAuth: false,
        },
      },
      {
        path: '/form-success',
        component: () => import('src/pages/FormSuccess.vue'),
        name: 'form_success',
        meta: {
          requiredAuth: false,
        },
      },
    ],
  },
  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
