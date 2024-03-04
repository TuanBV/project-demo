import userSchema from 'models/user';
import { ERROR } from 'utilities/message';

const passwordResetSchema = {
  type: 'object',
  required: ['password', 'confirm_password'],
  properties: {
    password: {
      ...userSchema.password,
      errorMessage: {
        minLength: ERROR.PASSWORD.REQUIRED,
        _: ERROR.PASSWORD.INVALID,
      },
    },
    new_password: {
      ...userSchema.new_password,
      errorMessage: {
        minLength: ERROR.NEW_PASSWORD.REQUIRED,
        not: ERROR.NEW_PASSWORD.NOT_EQUAL_PASSWORD,
        _: ERROR.NEW_PASSWORD.INVALID,
      },
    },
    confirm_password: {
      ...userSchema.confirm_password,
      errorMessage: {
        minLength: ERROR.CONFIRM_PASSWORD.REQUIRED,
        _: ERROR.CONFIRM_PASSWORD.EQUAL,
      },
    },
  },
  additionalProperties: false,
};

export default passwordResetSchema;
