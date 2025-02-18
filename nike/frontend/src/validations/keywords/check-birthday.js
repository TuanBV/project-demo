import dayjs from 'utilities/day'

const checkBirthday = {
  keyword: 'checkBirthday',
  type: 'string',
  validate: function validate(schema, data) {
    if (dayjs(data, 'YYYY/MM/DD', true).isValid()) {
      const timeCurrent = dayjs.getDate().unix()
      const timeInput = dayjs(data).unix()

      if (timeInput > timeCurrent) {
        return false
      }
    }
    this.errors = [
      {
        keyword: 'checkBirthday',
        params: { keyword: 'checkBirthday' }
      }
    ]
    return true
  },
  errors: true
}

export default checkBirthday
