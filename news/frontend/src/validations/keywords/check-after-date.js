import dayjs from 'utility/day'

const checkAfterDate = {
  keyword: 'checkAfterDate',
  type: 'string',
  validate: function validate(schema, data, parentSchema, dataPath) {
    if (!data || !dataPath.rootData[schema]) {
      return true
    }
    if (!dayjs(data, 'YYYY-MM-DD', true).isValid()) {
      return false
    }
    if (dayjs(data).isBefore(dayjs(dataPath.rootData[schema]))) {
      return false
    }
    this.errors = [
      {
        keyword: 'checkAfterDate',
        params: { keyword: 'checkAfterDate' }
      }
    ]
    return true
  },
  errors: true
}

export default checkAfterDate
