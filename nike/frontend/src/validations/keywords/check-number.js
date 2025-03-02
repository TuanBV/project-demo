const checkNumber = {
  keyword: 'checkNumber',
  type: 'string',
  validate: function validate(schema, data) {
    if (!/^-?\d*(\.\d+)?$/.test(data.trim()) || parseFloat(data) < 0) {
      return false
    }
    this.errors = [
      {
        keyword: 'checkNumber',
        params: { keyword: 'checkNumber' }
      }
    ]
    return true
  },
  errors: true
}

export default checkNumber
