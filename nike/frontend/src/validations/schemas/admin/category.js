import categoryModel from 'models/category.js'

const categorySchema = {
  type: 'object',
  required: ['name'],
  properties: {
    name: {
      ...categoryModel.name,
      errorMessage: {
        maxLength: 'Max length of category name is 256.',
        minLength: 'Category name is required to enter.',
        _: 'Invalid category name.'
      }
    }
  },
  additionalProperties: false
}

export default categorySchema
