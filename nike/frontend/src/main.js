import 'assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { createI18n } from 'vue-i18n'

const i18n = createI18n({
  locale: 'vn'
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
  faArrowLeft
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
  faArrowLeft
)

const app = createApp(App)
app.component('font-awesome-icon', FontAwesomeIcon)
app.use(createPinia())
app.use(router)
app.use(i18n)
app.mount('#app')
