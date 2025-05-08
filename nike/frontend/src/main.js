import 'assets/main.css'
import 'aos/dist/aos.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { createI18n } from 'vue-i18n'
import en from './locales/en.json'
import vi from './locales/vi.json'

import AOS from 'aos'

const i18n = createI18n({
  locale: 'vi', // Default languages
  fallbackLocale: 'en',
  messages: {
    en,
    vi,
  },
})

import {
  faSearch,
  faSignOut,
  faCartShopping,
  faUser,
  faBars,
  faClose,
  faPlus,
  faArrowRight,
  faArrowLeft,
  faAngleRight,
  faAngleLeft,
  faSpinner,
  faBoxArchive,
  faBlog,
  faGear,
  faRightToBracket,
  faImage,
  faEdit,
  faPowerOff,
  faAdd,
  faEnvelope,
  faFileCirclePlus,
  faEye,
  faPercent,
  faClipboard,
  faList,
  faCloudArrowUp,
  faFolderOpen,
  faCheckCircle,
  faComments,
  faEyeSlash,
  faCaretUp,
  faCaretDown,
} from '@fortawesome/free-solid-svg-icons'
library.add(
  faSearch,
  faSignOut,
  faCartShopping,
  faUser,
  faBars,
  faClose,
  faPlus,
  faArrowRight,
  faArrowLeft,
  faAngleRight,
  faAngleLeft,
  faSpinner,
  faBoxArchive,
  faBlog,
  faGear,
  faRightToBracket,
  faImage,
  faEdit,
  faPowerOff,
  faAdd,
  faEnvelope,
  faFileCirclePlus,
  faEye,
  faPercent,
  faClipboard,
  faList,
  faCloudArrowUp,
  faFolderOpen,
  faCheckCircle,
  faComments,
  faEyeSlash,
  faCaretUp,
  faCaretDown
)

const app = createApp(App)
AOS.init()
app.component('font-awesome-icon', FontAwesomeIcon)
app.use(createPinia())
app.use(router)
app.use(i18n)
app.mount('#app')
