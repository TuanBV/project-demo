const saleModel = {
  name: {
    type: 'string',
    maxLength: 256,
    minLength: 1
  },
  discount: {
    type: 'number',
    minimum: 0,
    maximum: 100
  },
  file: { type: 'string', minLength: 1 },
  file_ext: { type: 'string', enum: ['jpg', 'png', 'jpeg'] },
  file_size: { type: 'integer', minimum: 0, maximum: 10485760 },
  start_date: {
    type: 'string',
    // pattern: '^(\\d{4})-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$',
    checkDate: true,
    dateIsFuture: true
  },
  end_date: {
    type: 'string',
    // pattern: '^(\\d{4})-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$',
    checkDate: true,
    dateIsFuture: true,
    checkAfterDate: 'start_date'
  }
}

export default saleModel
