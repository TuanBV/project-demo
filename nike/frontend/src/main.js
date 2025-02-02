import 'assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
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
  faClipboard
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
  faClipboard
)

const app = createApp(App)
app.component('font-awesome-icon', FontAwesomeIcon)
app.use(createPinia())
app.use(router)

app.mount('#app')
