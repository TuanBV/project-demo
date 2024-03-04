const checkRequired = {
  keyword: 'checkRequired',
  type: 'string',
  validate: function validate(schema, data) {
    if (!data) {
      return false;
    }
    this.errors = [
      {
        keyword: 'checkRequired',
        params: { keyword: 'checkRequired' },
      },
    ];
    return true;
  },
  errors: true,
};

export default checkRequired;
