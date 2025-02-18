import saleModel from 'models/sale.js'

const saleSchema = {
  type: 'object',
  required: ['name', 'discount'],
  properties: {
    name: {
      ...saleModel.name,
      errorMessage: {
        maxLength: 'Max length of sale program name is 256.',
        minLength: 'Sale program name is required to enter.',
        _: 'Invalid sale program name.'
      }
    },
    discount: {
      ...saleModel.discount,
      errorMessage: {
        minimum: 'Minimum value for discount is 0.',
        minLength: 'Maximum value for discount is 100.',
        _: 'Invalid discount.'
      }
    },
    file: {
      ...saleModel.file,
      errorMessage: {
        minLength: 'Min length of file is 1',
        _: 'Invalid file.'
      }
    },
    file_ext: {
      ...saleModel.file_ext,
      errorMessage: {
        enum: 'Type of file invalid.',
        _: 'Invalid file type.'
      }
    },
    file_size: {
      ...saleModel.file_size,
      errorMessage: {
        minimum: 'Minium value for file is 0.',
        maximum: 'Maximum value for file is 10485760.',
        _: 'Invalid file size.'
      }
    },
    start_date: {
      ...saleModel.start_date,
      errorMessage: {
        pattern: 'start_date',
        checkDate: 'Format of start date invalid!',
        dateIsFuture: 'Start date must be greater than or equal to current date.',
        _: 'Invalid start date.'
      }
    },
    end_date: {
      ...saleModel.end_date,
      errorMessage: {
        pattern: 'start_date',
        checkDate: 'Format of start date invalid.',
        dateIsFuture: 'End date must be greater than or equal to current date.',
        checkAfterDate: 'End date is greater than start date.',
        _: 'Invalid end date.'
      }
    }
  },
  additionalProperties: false
}

export default saleSchema
