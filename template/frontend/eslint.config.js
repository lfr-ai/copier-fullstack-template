export default [
  {
    files: ['src/**/*.ts'],
    rules: {
      'no-unused-vars': 'warn',
      'no-console': 'warn',
    },
  },
  {
    ignores: ['dist/', 'node_modules/'],
  },
];
