/**
 * Property-based tests for utility functions using fast-check.
 *
 * Property-based testing validates behavior across a wide range of generated inputs,
 * catching edge cases that example-based tests might miss. Use property tests when:
 * - The function has algebraic properties (idempotence, commutativity, etc.)
 * - You want to test behavior across arbitrary valid inputs
 * - Edge cases are hard to enumerate manually
 *
 * Use example-based tests (utils.test.ts) for specific scenarios and regressions.
 */

import { test, fc } from '@fast-check/vitest';
import { cn } from '../../../src/lib/utils';

test.prop([fc.array(fc.string())])(
  'cn always returns a string',
  (classes) => {
    const result = cn(...classes);
    return typeof result === 'string';
  },
);

test.prop([fc.array(fc.string().filter((s) => !s.includes(' ')))])(
  'cn result never contains consecutive spaces',
  (classes) => {
    const result = cn(...classes);
    return !result.includes('  ');
  },
);

test.prop([
  fc.string(),
  fc.oneof(
    fc.constant(false),
    fc.constant(null),
    fc.constant(undefined),
    fc.constant(''),
  ),
  fc.string(),
])(
  'cn filters out falsy values',
  (before, falsy, after) => {
    const withFalsy = cn(before, falsy, after);
    const withoutFalsy = cn(before, after);
    return withFalsy === withoutFalsy;
  },
);

test.prop([fc.array(fc.string())])(
  'cn with empty array returns empty string',
  (classes) => {
    if (classes.length === 0) {
      return cn(...classes) === '';
    }
    return true;
  },
);

test.prop([fc.string()])(
  'cn with single non-empty string returns that string',
  (str) => {
    if (str.length > 0) {
      return cn(str) === str;
    }
    return true;
  },
);
