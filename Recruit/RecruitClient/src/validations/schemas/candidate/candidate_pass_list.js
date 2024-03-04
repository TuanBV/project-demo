import { ERROR } from '../../../shared/utilities/message';

const templateCandidatePassSchema = {
  type: 'object',
  properties: {
    id: {
      type: 'integer',
    },
    candidate_id: {
      type: 'integer',
    },
    title: {
      type: 'string',
      maxLength: 256,
      errorMessage: {
        maxLength: ERROR.TITLE_MAIL.MAXLENGTH,
        _: ERROR.NOTE.INVALID,
      },
    },
    body: {
      type: 'string',
    },
    list_email_cc: {
      type: 'array',
    },
  },
  additionalProperties: false,
};

export default templateCandidatePassSchema;
