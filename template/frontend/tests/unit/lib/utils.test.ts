/**
 * Unit tests for shared utility functions.
 *
 * Moved from co-located src/lib/utils.test.ts to follow
 * the centralized tests/unit/ convention.
 */
import { describe, it, expect } from 'vitest';
import { cn, formatDate } from '../../../src/lib/utils';

describe('cn', () => {
  it('joins class names', () => {
    expect(cn('a', 'b', 'c')).toBe('a b c');
  });

  it('filters falsy values', () => {
    expect(cn('a', false, null, undefined, 'b')).toBe('a b');
  });

  it('returns empty string for no classes', () => {
    expect(cn()).toBe('');
  });

  it('handles single class', () => {
    expect(cn('only')).toBe('only');
  });

  it('handles all falsy', () => {
    expect(cn(false, null, undefined)).toBe('');
  });
});

describe('formatDate', () => {
  it('formats a Date object', () => {
    const result = formatDate(new Date('2024-01-15'));
    expect(result).toContain('2024');
  });

  it('formats an ISO string', () => {
    const result = formatDate('2024-06-01');
    expect(result).toContain('2024');
  });
});
