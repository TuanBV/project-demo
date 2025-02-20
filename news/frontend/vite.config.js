import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue(), vueDevTools()],
  server: {
    port: 5001,
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      assets: fileURLToPath(new URL('./src/assets', import.meta.url)),
      components: fileURLToPath(new URL('./src/components', import.meta.url)),
      router: fileURLToPath(new URL('./src/router', import.meta.url)),
      stores: fileURLToPath(new URL('./src/stores', import.meta.url)),
      views: fileURLToPath(new URL('./src/views', import.meta.url)),
      layouts: fileURLToPath(new URL('./src/layouts', import.meta.url)),
      tests: fileURLToPath(new URL('./src/tests', import.meta.url)),
      service: fileURLToPath(new URL('./src/shared/service', import.meta.url)),
      utility: fileURLToPath(new URL('./src/shared/utility', import.meta.url)),
      composables: fileURLToPath(new URL('./src/composables', import.meta.url)),
      boot: fileURLToPath(new URL('./src/boot', import.meta.url)),
      validations: fileURLToPath(new URL('./src/validations', import.meta.url)),
      keywords: fileURLToPath(new URL('./src/validations/keywords', import.meta.url)),
      schemas: fileURLToPath(new URL('./src/validations/schemas', import.meta.url)),
      models: fileURLToPath(new URL('./src/validations/models', import.meta.url)),
    },
  },
})
