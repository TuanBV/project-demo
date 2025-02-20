import dayjs from 'utilities/day';

const dateMustBeNowOrPast = {
  keyword: 'dateMustBeNowOrPast',
  type: 'string',
  validate: function validate(_, data) {
    if (!data) {
      return true;
    }

    if (!dayjs(data).isValid()) {
      return true;
    }

    const timeStamp = dayjs(data).unix();
    const currentTimeStamp = dayjs().unix();
    if (currentTimeStamp >= timeStamp) {
      return true;
    }

    this.errors = [
      {
        keyword: 'dateMustBeNowOrPast',
        params: { keyword: 'dateMustBeNowOrPast' },
      },
    ];
    return false;
  },
  errors: true,
};

export default dateMustBeNowOrPast;
