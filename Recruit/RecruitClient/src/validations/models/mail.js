import userSchema from './user';

const mailSchema = {
  title: {
    type: 'string',
    maxLength: 256,
    minLength: 1,
  },
  email: { ...userSchema.mail },
  body: {
    type: 'string',
    minLength: 1,
  },
  attach_file: {
    type: 'object',
    properties: {
      file_size: {
        type: 'string',
      },
      file_ext: {
        type: 'string',
      },
    },
  },
};

export default mailSchema;
