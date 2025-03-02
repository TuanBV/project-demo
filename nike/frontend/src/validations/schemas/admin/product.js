import productModel from 'models/product.js'

const productSchema = {
  type: 'object',
  required: ['name', 'price', 'category_id', 'quantity'],
  properties: {
    name: {
      ...productModel.name,
      errorMessage: {
        maxLength: 'Max length of product program name is 256.',
        minLength: 'Sale program name is required to enter.',
        _: 'Invalid product program name.'
      }
    },
    category_id: {
      ...productModel.category_id,
      errorMessage: {
        minLength: 'Please choose category for product.',
        _: 'Invalid product category.'
      }
    },
    kind_id: {
      ...productModel.kind_id,
      errorMessage: {
        minLength: 'Please choose kind for product.',
        _: 'Invalid product kind.'
      }
    },
    price: {
      ...productModel.price,
      errorMessage: {
        minium: 'Please enter price',
        checkNumber: 'Please enter correct format of price.',
        _: 'Invalid product price.'
      }
    },
    quantity: {
      ...productModel.quantity,
      errorMessage: {
        minium: 'Please enter correct format of quantity.',
        _: 'Invalid product quantity.'
      }
    },
    weight: {
      ...productModel.weight,
      errorMessage: {
        checkNumber: 'Please enter correct format of weight.',
        _: 'Invalid product weight.'
      }
    },
    height: {
      ...productModel.height,
      errorMessage: {
        checkNumber: 'Please enter correct format of height.',
        _: 'Invalid product height.'
      }
    },
    info: {
      ...productModel.info,
      errorMessage: {
        minLength: 'Please enter product information.',
        maxLength: 'Max characters is 512.',
        _: 'Invalid product info.'
      }
    },
    sale_id: {},
    images: {}
  },
  additionalProperties: false
}

export default productSchema
