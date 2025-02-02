/* eslint-env node */
require('@rushstack/eslint-patch/modern-module-resolution')

module.exports = {
  root: true,
  extends: [
    'plugin:vue/vue3-essential',
    // 'plugin:vue/vue3-recommended',
    'eslint:recommended',
    '@vue/eslint-config-prettier/skip-formatting',
    'plugin:vitest-globals/recommended'
  ],
  // rules: {
  //   'max-len': [
  //     'warn',
  //     {
  //       code: 120,
  //       tabWidth: 2,
  //       comments: 120,
  //       ignoreUrls: true
  //     }
  //   ],
  //   'prettier/prettier': [
  //     'error',
  //     {
  //       printWidth: 120
  //     }
  //   ]
  // },
  parserOptions: {
    ecmaVersion: 'latest'
  },
  env: {
    'vitest-globals/env': true
  }
}
