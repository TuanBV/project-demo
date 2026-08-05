import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vitest/config'
import vue from '@vitejs/plugin-vue'
import { quasar, transformAssetUrls } from '@quasar/vite-plugin'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue({
      template: { transformAssetUrls },
    }),
    quasar({
      sassVariables: 'src/quasar-variables.sass',
    }),
  ],
  resolve: {
    alias: {
      // Required by @quasar/vite-plugin's sassVariables option, which
      // imports this path as-is from Quasar's own (aliased) source sass.
      src: fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    port: 5174,
  },
  test: {
    environment: 'jsdom',
    globals: true,
    // e2e/** are Playwright specs (different runner, different `test`
    // import) - Vitest's default include glob would otherwise try to run
    // them too.
    exclude: ['**/node_modules/**', '**/dist/**', 'e2e/**'],
  },
})
