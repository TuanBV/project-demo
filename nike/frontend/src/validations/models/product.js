const productModel = {
  name: {
    type: 'string',
    maxLength: 256,
    minLength: 1
  },
  quantity: {
    type: 'integer'
  },
  price: {
    type: 'number'
  },
  sale: {
    type: 'number'
  },
  category_id: {
    type: 'integer'
  }
}

export default productModel
