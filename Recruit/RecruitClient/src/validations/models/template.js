const editTemplateSchema = {
  title: {
    type: 'string',
    maxLength: 256,
    minLength: 1,
  },
  body: {
    type: 'string',
    minLength: 1,
  },
  note: {
    type: 'string',
    maxLength: 256,
  },
};

export default editTemplateSchema;
