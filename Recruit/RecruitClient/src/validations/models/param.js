const addParamSchema = {
  name: {
    type: 'string',
    maxLength: 50,
    minLength: 1,
  },
  table: {
    type: 'string',
    maxLength: 50,
    minLength: 1,
  },
  column: {
    type: 'string',
    minLength: 1,
    maxLength: 50,
  },
  note: {
    type: 'string',
    maxLength: 256,
  },
};

export default addParamSchema;
