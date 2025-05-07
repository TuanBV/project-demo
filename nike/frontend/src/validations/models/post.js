const postModel = {
  id: {
    type: 'integer',
  },
  title: {
    type: 'string',
    maxLength: 256,
    minLength: 1,
  },
  content: {
    type: 'string',
  },
  status: {
    type: 'integer',
    minimum: 0,
    maximum: 2,
  },
}

export default postModel
