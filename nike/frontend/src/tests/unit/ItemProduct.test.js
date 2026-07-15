import { render, screen } from '@testing-library/vue'
import { describe, expect, it } from 'vitest'
import ItemProduct from '@/components/user/product/ItemProduct.vue'

const productWithoutImages = {
  name: 'Test Product 001',
  price: 49.99,
  images: [],
}

describe('ItemProduct', () => {
  it('renders without throwing when the product has no images', () => {
    render(ItemProduct, { props: { itemProduct: productWithoutImages } })

    expect(screen.getByText('Test Product 001')).toBeInTheDocument()
  })

  it('falls back to a placeholder image instead of crashing on images[0]', () => {
    render(ItemProduct, { props: { itemProduct: productWithoutImages } })

    const img = screen.getByAltText('Test Product 001')
    expect(img.getAttribute('src')).not.toContain('undefined')
  })
})
