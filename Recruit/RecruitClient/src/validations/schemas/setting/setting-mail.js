import userSchema from 'models/user';
import { ERROR } from 'utilities/message';

const settingMailHanoiSchema = {
  type: 'object',
  required: ['mail_hanoi', 'password_hanoi'],
  properties: {
    mail_hanoi: {
      ...userSchema.mail,
      errorMessage: {
        maxLength: ERROR.EMAIL.MAXLENGTH,
        minLength: ERROR.EMAIL.REQUIRED,
        _: ERROR.EMAIL.INVALID,
      },
    },
    password_hanoi: {
      type: 'string',
      minLength: 1,
      errorMessage: {
        minLength: ERROR.PASSWORD.REQUIRED,
        _: ERROR.PASSWORD.INVALID,
      },
    },
    office: {
      type: 'string',
    },
  },
  additionalProperties: false,
};

const settingMailHueSchema = {
  type: 'object',
  required: ['mail_hue', 'password_hue'],
  properties: {
    mail_hue: {
      ...userSchema.mail,
      errorMessage: {
        maxLength: ERROR.EMAIL.MAXLENGTH,
        minLength: ERROR.EMAIL.REQUIRED,
        _: ERROR.EMAIL.INVALID,
      },
    },
    password_hue: {
      type: 'string',
      minLength: 1,
      errorMessage: {
        minLength: ERROR.PASSWORD.REQUIRED,
        _: ERROR.PASSWORD.INVALID,
      },
    },
    office: {
      type: 'string',
    },
  },
  additionalProperties: false,
};

export default { settingMailHanoiSchema, settingMailHueSchema };
