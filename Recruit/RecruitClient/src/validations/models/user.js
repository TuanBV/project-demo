const userSchema = {
  mail: {
    type: 'string',
    maxLength: 256,
    minLength: 1,
    pattern: '^[A-Za-z0-9_!#$%&*+/=?`\'{|}~^.-]+@[A-Za-z0-9.-]+$',
  },
  password: {
    type: 'string',
    minLength: 1,
    pattern: '^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]{8,64}$',
  },
  new_password: {
    type: 'string',
    minLength: 1,
    maxLength: 64,
    pattern: '^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]{8,64}$',
    not: {
      const: {
        $data: '1/password',
      },
    },
  },
  confirm_password: {
    type: 'string',
    minLength: 1,
    maxLength: 64,
    const: {
      $data: '1/new_password',
    },
  },
};

export default userSchema;
