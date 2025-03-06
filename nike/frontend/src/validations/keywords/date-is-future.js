import dayjs from 'utility/day'

const dateIsFuture = {
  keyword: 'dateIsFuture',
  type: 'string',
  validate: function validate(_, data) {
    if (!data) {
      return true
    }

    if (!dayjs(data).isValid()) {
      return true
    }

    const inputTimeStamp = dayjs(data).unix()
    const currentTimeStamp = dayjs().startOf('day').unix()
    if (currentTimeStamp <= inputTimeStamp) {
      return true
    }

    this.errors = [
      {
        keyword: 'dateIsFuture',
        params: { keyword: 'dateIsFuture' }
      }
    ]
    return false
  },
  errors: true
}

export default dateIsFuture
