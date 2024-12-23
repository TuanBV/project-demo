import { describe, it, expect } from 'vitest'

import { evenOrOdd } from '../playground.js'

describe('basic math', () => {
  describe('When number is even', () => {
    it('indicates the number is even', () => {
      expect(evenOrOdd(4)).toBe('Even')
    })
  })
  describe('When number is odd', () => {
    it('indicates the number is even', () => {
      expect(evenOrOdd(5)).toBe('Odd')
    })
  })
})
