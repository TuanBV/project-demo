import userSchema from 'models/user';
import { ERROR } from 'utilities/message';
import { cloneDeep } from 'lodash';

const newUserChema = cloneDeep(userSchema);
delete newUserChema.new_password.not;
const passwordResetSchema = {
  type: 'object',
  required: ['new_password', 'confirm_password'],
  properties: {
    new_password: {
      ...newUserChema.new_password,
      errorMessage: {
        minLength: ERROR.PASSWORD.REQUIRED,
        _: ERROR.PASSWORD.INVALID,
      },
    },
    confirm_password: {
      ...newUserChema.confirm_password,
      errorMessage: {
        minLength: ERROR.CONFIRM_PASSWORD.REQUIRED,
        _: ERROR.CONFIRM_PASSWORD.EQUAL,
      },
    },
  },
  additionalProperties: false,
};

export default passwordResetSchema;
