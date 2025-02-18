import dayjs from 'utility/day'

const checkDate = {
  keyword: 'checkDate',
  type: 'string',
  validate: function validate(schema, data) {
    if (!data) {
      return true
    }
    if (!dayjs(data, 'YYYY-MM-DD', true).isValid()) {
      return false
    }
    this.errors = [
      {
        keyword: 'checkDate',
        params: { keyword: 'checkDate' }
      }
    ]
    return true
  },
  errors: true
}

export default checkDate
