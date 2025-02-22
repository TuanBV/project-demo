const imageModel = {
  file: { type: 'string', minLength: 1 },
  file_ext: { type: 'string', enum: ['jpg', 'png', 'jpeg'] },
  file_size: { type: 'integer', minimum: 0, maximum: 10485760 }
}

export default imageModel
