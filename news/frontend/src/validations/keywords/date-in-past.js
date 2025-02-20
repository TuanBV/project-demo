import dayjs from 'utilities/day';

const dateMustBeInPast = {
  keyword: 'dateMustBeInPast',
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

    if (currentTimeStamp > timeStamp && !dayjs().isSame(dayjs(data), 'day')) {
      return true;
    }

    this.errors = [
      {
        keyword: 'dateMustBeInPast',
        params: { keyword: 'dateMustBeInPast' },
      },
    ];
    return false;
  },
  errors: true,
};

export default dateMustBeInPast;
