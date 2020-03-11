module.exports = {
  roots: ['<rootDir>/tests'],
  transform: {
    '\\.(ts|tsx)?$': 'babel-jest',
    '.+\\.scss$': 'jest-css-modules-transform',
  },
  testMatch: ['<rootDir>/tests/**/?(*.)test.{ts,tsx}'],
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json', 'node'],
  testPathIgnorePatterns: ['/node_modules/', '/public/'],
};
