const checkIdentificationNumber = {
  keyword: 'checkIdentificationNumber',
  type: 'string',
  validate: function validate(schema, data) {
    if (!data) {
      return true;
    }
    if (!/^-?\d+$/.test(data)) {
      return false;
    }
    this.errors = [
      {
        keyword: 'checkIdentificationNumber',
        params: { keyword: 'checkIdentificationNumber' },
      },
    ];
    return true;
  },
  errors: true,
};

export default checkIdentificationNumber;
