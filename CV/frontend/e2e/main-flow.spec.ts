import { test, expect } from '@playwright/test'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const SAMPLE_PDF = path.join(__dirname, 'fixtures', 'sample.pdf')

/**
 * The main product flow from the brief: register -> create a PDF resume ->
 * upload -> publish -> an unauthenticated visitor opens the public URL and
 * sees the CV. Runs against whatever E2E_BASE_URL points to (default
 * http://localhost:5174) - see README.md for how to bring the stack up
 * first.
 */
test('register, upload a PDF, publish it, and view it as an anonymous visitor', async ({ page, browser }) => {
  const uniqueEmail = `e2e-${Date.now()}@example.com`

  await page.goto('/register')
  await page.getByLabel('Họ và tên').fill('E2E Test User')
  await page.getByLabel('Email').fill(uniqueEmail)
  await page.getByLabel('Mật khẩu').fill('correct-password-1')
  await page.getByRole('button', { name: 'Đăng ký' }).click()

  await expect(page).toHaveURL(/\/dashboard\/cvs$/)

  await page.getByTestId('create-resume-button').click()
  await page.getByTestId('new-resume-name').fill('E2E CV')
  await page.getByTestId('confirm-create-resume').click()

  await expect(page.getByTestId('resume-card')).toContainText('E2E CV')
  await page.getByTestId('resume-card').getByRole('button', { name: 'Quản lý' }).click()

  await expect(page).toHaveURL(/\/dashboard\/cvs\/.+\/edit$/)

  // QFile hides its native <input type="file"> outside the element carrying
  // our data-testid, so target it page-wide - there's only one on this page.
  await page.locator('input[type="file"]').setInputFiles(SAMPLE_PDF)
  await page.getByTestId('upload-pdf-button').click()
  await expect(page.getByTestId('version-list')).toContainText('Đang dùng')

  // Switch visibility to PUBLIC via the Quasar select popup.
  await page.getByTestId('visibility-select').click()
  await page.getByRole('option', { name: 'PUBLIC' }).click();

  await page.getByTestId('publish-button').click()
  await expect(page.getByTestId('publish-button')).toHaveCount(0)

  const publicLink = await page.getByTestId('public-link-text').innerText()
  expect(publicLink).toContain('/cv/')

  // A fresh, cookie-less browser context stands in for an anonymous visitor.
  const visitorContext = await browser.newContext()
  const visitorPage = await visitorContext.newPage()
  await visitorPage.goto(publicLink)

  await expect(visitorPage.getByTestId('public-resume-name')).toHaveText('E2E CV')
  await expect(visitorPage.getByTestId('pdf-viewer')).toBeVisible()

  await visitorContext.close()
})
