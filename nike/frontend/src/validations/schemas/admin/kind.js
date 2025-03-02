import kindModel from 'models/kind.js'

const kindSchema = {
  type: 'object',
  required: ['name'],
  properties: {
    name: {
      ...kindModel.name,
      errorMessage: {
        maxLength: 'Max length of kind name is 256.',
        minLength: 'Kind name is required to enter.',
        _: 'Invalid kind name.'
      }
    }
  },
  additionalProperties: false
}

export default kindSchema
