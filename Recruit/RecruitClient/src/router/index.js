import useMixin from 'mixins/common.js';
import { POSITION_ID } from 'src/shared/utilities/const';
import { route } from 'quasar/wrappers';
import {
  createRouter, createMemoryHistory, createWebHistory, createWebHashHistory,
} from 'vue-router';
import { useAuthStore } from 'stores/auth-store';
import { useAppStore } from 'stores/app-store';
import { candidateStore } from 'stores/candidate-store';
import userService from 'services/user.service';
import candidateService from 'services/candidate.service';
import routes from './routes';

/*
 * If not building with SSR mode, you can
 * directly export the Router instantiation;
 *
 * The function below can be async too; either use
 * async/await or return a Promise which resolves
 * with the Router instance.
 */

export default route(() => {
  let createHistory = null;
  if (process.env.SERVER) {
    createHistory = createMemoryHistory;
  } else if (process.env.VUE_ROUTER_MODE === 'history') {
    createHistory = createWebHistory;
  } else {
    createHistory = createWebHashHistory;
  }

  const Router = createRouter({
    scrollBehavior: () => ({ left: 0, top: 0 }),
    routes,

    // Leave this as is and make changes in quasar.conf.js instead!
    // quasar.conf.js -> build -> vueRouterMode
    // quasar.conf.js -> build -> publicPath
    history: createHistory(process.env.VUE_ROUTER_BASE),
  });

  /**
   * Handle check user login
   *
   * @returns boolean
   */
  const checkUserLogin = async () => {
    const user = await userService.getMe();
    return !!user;
  };

  /**
   * Handle check token access form candidate
   *
   * @returns boolean
   */
  const checkTokenFormCandidate = async () => {
    const query = window.location.href.split('?');
    if (query.length > 1 && query[1].length > 0) {
      const urlParams = new URLSearchParams(`?${query[1]}`);
      if (urlParams.has('token')) {
        const token = urlParams.get('token');
        const candidate = await candidateService.getFormCandidate(token);
        if (candidate) {
          const { setCandidate } = candidateStore();
          setCandidate(candidate);
          return true;
        }
      }
    }
    return false;
  };

  /**
   * Handle check token forgot password
   *
   * @returns boolean
   */
  const checkTokenForgotPassword = () => {
    const query = window.location.href.split('?');
    if (query.length > 1 && query[1].length > 0) {
      const urlParams = new URLSearchParams(`?${query[1]}`);
      if (urlParams.has('token')) {
        const token = urlParams.get('token');
        return userService.checkTokenForgotPassword(token);
      }
    }
    return false;
  };

  /**
   * Handle check authentication every time page change
   */
  Router.beforeEach(async (to) => {
    const { isLoggedIn, user } = useAuthStore();
    const { setCurrentRouterName } = useAppStore();
    setCurrentRouterName(to.name);
    if (!to.meta.requiredAuth) {
      if (to.name === 'form_candidate') {
        if (!await checkTokenFormCandidate()) {
          return '/404';
        }
      } else if (to.name === 'password_reset') {
        // check token
        if (!await checkTokenForgotPassword()) {
          return '/404';
        }
      }
      return true;
    }

    let checkLogin = true;
    if (!isLoggedIn) {
      checkLogin = await checkUserLogin();
    }

    if (!checkLogin) {
      if (to.name !== 'login') {
        return '/login';
      }
      return true;
    }

    if (to.name === 'login'
      || (to.name !== 'add_cv' && [POSITION_ID.INTERN, POSITION_ID.COLLABORATORS, POSITION_ID.STAFF].includes(user.position_id))) {
      return '/add-cv';
    }

    const { countRecord } = useMixin();
    countRecord();

    return true;
  });

  return Router;
});
