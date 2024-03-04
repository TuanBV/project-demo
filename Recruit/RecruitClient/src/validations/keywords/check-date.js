import dayjs from 'utilities/day';

const checkDate = {
  keyword: 'checkDate',
  type: 'string',
  validate: function validate(schema, data) {
    if (!dayjs(data, 'YYYY/MM/DD', true).isValid()) {
      return false;
    }
    this.errors = [
      {
        keyword: 'checkDate',
        params: { keyword: 'checkDate' },
      },
    ];
    return true;
  },
  errors: true,
};

export default checkDate;
