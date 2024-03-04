import addParamSchema from '../../models/param.js';
import { ERROR } from '../../../shared/utilities/message';

const parameterSchema = {
  type: 'object',
  required: [
    'name',
    'table',
    'column',
    'note',
  ],
  properties: {
    id: {
      type: 'string',
    },
    name: {
      ...addParamSchema.name,
      errorMessage: {
        maxLength: ERROR.PARAM.NAME.MAXLENGTH,
        minLength: ERROR.PARAM.NAME.REQUIRED,
        _: ERROR.PARAM.NAME.REQUIRED,
      },
    },
    table: {
      ...addParamSchema.table,
      errorMessage: {
        maxLength: ERROR.PARAM.TABLE.MAXLENGTH,
        minLength: ERROR.PARAM.TABLE.REQUIRED,
        _: ERROR.PARAM.TABLE.REQUIRED,
      },
    },
    column: {
      ...addParamSchema.column,
      errorMessage: {
        maxLength: ERROR.PARAM.COLUMN.MAXLENGTH,
        minLength: ERROR.PARAM.COLUMN.REQUIRED,
        _: ERROR.PARAM.COLUMN.INVALID,
      },
    },
    note: {
      ...addParamSchema.note,
      errorMessage: {
        maxLength: ERROR.NOTE.MAXLENGTH,
        _: ERROR.NOTE.INVALID,
      },
    },
  },
  additionalProperties: false,
};

export default parameterSchema;
