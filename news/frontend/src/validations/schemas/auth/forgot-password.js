import userSchema from 'models/user';
import { ERROR } from 'utilities/message';

const forgotPasswordSchema = {
  type: 'object',
  required: ['email'],
  properties: {
    email: {
      ...userSchema.mail,
      errorMessage: {
        maxLength: ERROR.EMAIL.MAXLENGTH,
        minLength: ERROR.EMAIL.REQUIRED,
        _: ERROR.EMAIL.INVALID,
      },
    },
  },
  additionalProperties: false,
};

export default forgotPasswordSchema;
