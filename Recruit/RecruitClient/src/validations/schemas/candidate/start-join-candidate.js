import { ERROR } from 'utilities/message';
import candidateModel from 'models/candidate';

const startJoinSchema = {
  type: 'object',
  required: [
    'start_join_date',
  ],
  properties: {
    start_join_date: {
      ...candidateModel.start_join_date,
      errorMessage: {
        dateIsFuture: ERROR.START_JOIN_DATE.IS_FUTURE,
        _: ERROR.START_JOIN_DATE.REQUIRED,
      },
    },
  },
  additionalProperties: false,
};

export default startJoinSchema;
