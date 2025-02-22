import imageModel from 'models/image.js'

const imageSchema = {
  type: 'object',
  required: ['file', 'file_ext', 'file_size'],
  properties: {
    file: {
      ...imageModel.file,
      errorMessage: {
        minLength: 'Min length of file is 1',
        _: 'Invalid file.'
      }
    },
    file_ext: {
      ...imageModel.file_ext,
      errorMessage: {
        enum: 'Type of file invalid.',
        _: 'Invalid file type.'
      }
    },
    file_size: {
      ...imageModel.file_size,
      errorMessage: {
        minimum: 'Minium value for file is 0.',
        maximum: 'Maximum value for file is 10485760.',
        _: 'Invalid file size.'
      }
    }
  },
  additionalProperties: false
}

export default imageSchema
