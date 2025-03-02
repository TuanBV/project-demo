const productModel = {
  name: {
    type: 'string',
    maxLength: 256,
    minLength: 1
  },
  quantity: {
    type: 'integer',
    minimum: 0
  },
  price: {
    type: 'string',
    minLength: 1,
    checkNumber: true
  },
  sale_id: {
    type: 'string'
  },
  category_id: {
    type: 'string',
    minLength: 1
  },
  kind_id: {
    type: 'string',
    minLength: 1
  },
  info: {
    type: 'string',
    minLength: 1,
    maxLength: 512
  },
  weight: {
    type: 'string',
    checkNumber: true
  },
  height: {
    type: 'string',
    checkNumber: true
  }
}

export default productModel
