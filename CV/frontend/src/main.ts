import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { Quasar, Notify } from 'quasar'

import '@quasar/extras/material-icons/material-icons.css'
import 'quasar/src/css/index.sass'
import './style.css'

import App from './App.vue'
import { router } from './router'
import { useAuthStore } from './stores/auth'

const app = createApp(App)

app.use(createPinia())
app.use(Quasar, {
  plugins: { Notify },
})
app.use(router)

// Restore the session from the HttpOnly refresh cookie (if any) before the
// router resolves the first navigation, so route guards see the correct
// authenticated state instead of bouncing to /login on every page reload.
const authStore = useAuthStore()
authStore
  .tryRestoreSession()
  .finally(() => app.mount('#app'))
