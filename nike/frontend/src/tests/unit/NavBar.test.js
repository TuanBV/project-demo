import { render, screen } from '@testing-library/vue'
import { createPinia, setActivePinia } from 'pinia'
import { createRouter, createMemoryHistory } from 'vue-router'
import { describe, expect, it, beforeEach } from 'vitest'
import NavBar from '@/components/user/navbar/NavBar.vue'
import routes from '@/router/routes.js'
import { useAuthStore } from '@/stores/auth-store'

const renderNavBar = () => {
  const router = createRouter({ history: createMemoryHistory(), routes })
  return render(NavBar, { global: { plugins: [router] } })
}

describe('NavBar', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('renders the main navigation categories', () => {
    renderNavBar()
    expect(screen.getByText('Men')).toBeInTheDocument()
    expect(screen.getByText('Women')).toBeInTheDocument()
    expect(screen.getByText('Sale')).toBeInTheDocument()
  })

  it('shows a sign-in link when the user is not authenticated', () => {
    renderNavBar()
    expect(screen.getByText('Sign In')).toBeInTheDocument()
    expect(screen.queryByText('Logout')).not.toBeInTheDocument()
  })

  it('shows cart/profile/logout instead of sign-in when authenticated', () => {
    renderNavBar()
    const auth = useAuthStore()
    auth.user = { email: 'user@example.com' }

    return screen.findByText('Logout').then(logoutButton => {
      expect(logoutButton).toBeInTheDocument()
      expect(screen.queryByText('Sign In')).not.toBeInTheDocument()
    })
  })
})
