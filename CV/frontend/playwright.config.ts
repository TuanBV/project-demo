import { defineConfig, devices } from '@playwright/test'

/**
 * E2E tests assume the full stack (postgres, minio, backend, frontend) is
 * already running - see README.md's "Running the E2E tests" section. This
 * config does not try to orchestrate docker-compose itself, since spinning
 * up a database + object storage from a test runner is fragile; a plain
 * `docker compose up -d` beforehand is simpler and matches how a human
 * would actually verify the same flow.
 */
export default defineConfig({
  testDir: './e2e',
  fullyParallel: false,
  retries: 0,
  reporter: 'list',
  use: {
    baseURL: process.env.E2E_BASE_URL ?? 'http://localhost:5174',
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
})
