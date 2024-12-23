import { describe, it, expect } from 'vitest'

import { evenOrOdd, multiply } from '../playground.js'

describe('basic math', () => {
  describe('evenOrOdd', () => {
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

  describe('multiply', () => {
    it('multiplies two numbers together', () => {
      expect(multiply(2, 3)).toBe(6)
    })
  })
})
