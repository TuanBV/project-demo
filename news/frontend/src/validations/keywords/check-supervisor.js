const checkSupervisor = {
  keyword: 'checkSupervisor',
  type: 'array',
  validate: function validate(schema, data) {
    if (!data.length) return false;
    this.errors = [
      {
        keyword: 'checkSupervisor',
        params: { keyword: 'checkSupervisor' },
      },
    ];
    return true;
  },
  errors: true,
};

export default checkSupervisor;
