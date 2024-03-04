import mailSchema from 'models/mail';
import { ERROR } from 'utilities/message';

const candidateMailSchema = {
  type: 'object',
  required: [
    'title',
    'candidate_email',
    'body',
  ],
  properties: {
    title: {
      ...mailSchema.title,
      errorMessage: {
        maxLength: ERROR.TITLE_MAIL.MAXLENGTH,
        _: ERROR.TITLE_MAIL.REQUIRED,
      },
    },
    candidate_email: {
      ...mailSchema.email,
      errorMessage: {
        maxLength: ERROR.EMAIL.MAXLENGTH,
        minLength: ERROR.EMAIL.REQUIRED,
        _: ERROR.EMAIL.INVALID,
      },
    },
    body: {
      ...mailSchema.body,
      errorMessage: {
        _: ERROR.BODY_MAIL.REQUIRED,
      },
    },
    receiver_cc0: {
      ...mailSchema.email,
      errorMessage: {
        maxLength: ERROR.EMAIL.MAXLENGTH,
        minLength: ERROR.EMAIL.REQUIRED,
        _: ERROR.EMAIL.INVALID,
      },
    },
    receiver_cc1: {
      ...mailSchema.email,
      errorMessage: {
        maxLength: ERROR.EMAIL.MAXLENGTH,
        minLength: ERROR.EMAIL.REQUIRED,
        _: ERROR.EMAIL.INVALID,
      },
    },
    receiver_cc2: {
      ...mailSchema.email,
      errorMessage: {
        maxLength: ERROR.EMAIL.MAXLENGTH,
        minLength: ERROR.EMAIL.REQUIRED,
        _: ERROR.EMAIL.INVALID,
      },
    },
    attach_file: {
      ...mailSchema.attach_file,
    },
  },
  additionalProperties: false,
};

export default candidateMailSchema;
