import recommenderModel from 'models/recommender';
import { ERROR } from 'utilities/message';

const recommenderSchema = {
  type: 'object',
  required: [
    'fullname',
    'email',
    'birthday',
    'full_address',
    'place_issued_identification',
    'identification_number',
    'date_issued_identification',
    'telephone_no',
  ],
  properties: {
    fullname: {
      ...recommenderModel.fullname,
      errorMessage: {
        maxLength: ERROR.FULLNAME.MAXLENGTH,
        _: ERROR.FULLNAME.REQUIRED,
      },
    },
    email: {
      ...recommenderModel.email,
      errorMessage: {
        maxLength: ERROR.EMAIL.MAXLENGTH,
        minLength: ERROR.EMAIL.REQUIRED,
        _: ERROR.EMAIL.INVALID,
      },
    },
    birthday: {
      ...recommenderModel.birthday,
      errorMessage: {
        minLength: ERROR.BIRTHDAY.REQUIRED,
        dateMustBeInPast: ERROR.BIRTHDAY.IN_PAST,
        _: ERROR.BIRTHDAY.INVALID,
      },
    },
    full_address: {
      ...recommenderModel.full_address,
      errorMessage: {
        maxLength: ERROR.FULL_ADDRESS.MAXLENGTH,
        _: ERROR.FULL_ADDRESS.REQUIRED,
      },
    },
    place_issued_identification: {
      ...recommenderModel.place_issued_identification,
      errorMessage: {
        maxLength: ERROR.PLACE_ISSUED_IDENTIFICATION.MAXLENGTH,
        _: ERROR.PLACE_ISSUED_IDENTIFICATION.REQUIRED,
      },
    },
    identification_number: {
      ...recommenderModel.identification_number,
      errorMessage: {
        minLength: ERROR.IDENTIFICATION_NUMBER.REQUIRED,
        _: ERROR.IDENTIFICATION_NUMBER.INVALID,
      },
    },
    date_issued_identification: {
      ...recommenderModel.date_issued_identification,
      errorMessage: {
        minLength: ERROR.DATE_ISSUED_IDENTIFICATION.REQUIRED,
        dateMustBeInPast: ERROR.DATE_ISSUED_IDENTIFICATION.IN_PAST,
        _: ERROR.DATE_ISSUED_IDENTIFICATION.INVALID,
      },
    },
    telephone_no: {
      ...recommenderModel.telephone_no,
      errorMessage: {
        minLength: ERROR.TELEPHONE_NO.REQUIRED,
        _: ERROR.TELEPHONE_NO.INVALID,
      },
    },
  },
  additionalProperties: false,
};

export default recommenderSchema;
