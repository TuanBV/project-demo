import editTemplateSchema from '../../models/template.js';
import { ERROR } from '../../../shared/utilities/message';

const templateSchema = {
  type: 'object',
  required: [
    'title',
    'body',
    'note',
  ],
  properties: {
    id: {
      type: 'string',
    },
    title: {
      ...editTemplateSchema.title,
      errorMessage: {
        maxLength: ERROR.TEMPLATE.TITLE.MAXLENGTH,
        minLength: ERROR.TEMPLATE.TITLE.REQUIRED,
        _: ERROR.TEMPLATE.TITLE.REQUIRED,
      },
    },
    body: {
      ...editTemplateSchema.body,
      errorMessage: {
        minLength: ERROR.TEMPLATE.BODY.REQUIRED,
        _: ERROR.TEMPLATE.BODY.REQUIRED,
      },
    },
    note: {
      ...editTemplateSchema.note,
      errorMessage: {
        maxLength: ERROR.NOTE.MAXLENGTH,
        _: ERROR.NOTE.INVALID,
      },
    },
  },
  additionalProperties: false,
};

export default templateSchema;
