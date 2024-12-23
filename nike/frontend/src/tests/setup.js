import { cleanup } from '@testing-library/vue';
import * as matchers from '@testing-library/jest-dom/matchers';
import { expect, afterEach } from 'vitest';

console.log(matchers);


expect.extend(matchers);

afterEach(() => {
  cleanup();
});