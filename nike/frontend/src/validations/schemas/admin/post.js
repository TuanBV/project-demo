import postModel from 'models/post.js'

const postSchema = {
  type: 'object',
  required: ['title', 'status'],
  properties: {
    id: {
      ...postModel.id,
    },
    title: {
      ...postModel.title,
      errorMessage: {
        maxLength: 'Max length of title name is 256.',
        minLength: 'Title is required to enter.',
        _: 'Invalid title.',
      },
    },
    content: {
      ...postModel.content,
    },
    status: {
      ...postModel.status,
      errorMessage: {
        maximum: 'Invalid status post',
        minimum: 'Invalid status post',
        _: 'Invalid status post',
      },
    },
  },
  additionalProperties: false,
}

export default postSchema
