import { render, screen } from "@testing-library/vue"
import NavBar from "@/components/navbar/NavBar.vue"
import { describe, expect, it } from "vitest"

describe("NavBar", () => {
  it('display company name', () => {
      render(NavBar)
      screen.debug()
      const companyName = screen.getByText('Boo Careers')
      expect(companyName).toBeInTheDocument()
  })

  it('displays menu items for navigation', () => {
    render(NavBar)
    screen.debug()
  })
})