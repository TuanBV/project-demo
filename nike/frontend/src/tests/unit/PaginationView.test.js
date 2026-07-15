import { render, screen } from '@testing-library/vue'
import { describe, expect, it } from 'vitest'
import PaginationView from '@/components/common/pagination/PaginationView.vue'

describe('PaginationView', () => {
  it('shows page nav when total is an exact multiple of the page size', () => {
    // Regression: v-if="total < page * show" was always false when total
    // divides evenly by show (e.g. 100 / 20 = 5, 5*20 == 100), hiding the nav.
    render(PaginationView, {
      props: { modelValue: { current: 1, show: 20, total: 100 } },
    })

    expect(screen.getByLabelText('Pagination')).toBeInTheDocument()
    expect(screen.getAllByText('5')).toHaveLength(1)
  })

  it('hides page nav when everything fits on one page', () => {
    render(PaginationView, {
      props: { modelValue: { current: 1, show: 20, total: 10 } },
    })

    expect(screen.queryByLabelText('Pagination')).not.toBeInTheDocument()
  })

  it('shows the correct "to" value on the last (partial) page', () => {
    render(PaginationView, {
      props: { modelValue: { current: 5, show: 12, total: 52 } },
    })

    expect(screen.getByText(/Showing 49 to 52 of 52 entries/)).toBeInTheDocument()
  })

  it('shows the correct "to" value on a full, non-final page', () => {
    render(PaginationView, {
      props: { modelValue: { current: 1, show: 12, total: 100 } },
    })

    expect(screen.getByText(/Showing 1 to 12 of 100 entries/)).toBeInTheDocument()
  })
})
