/**
 * Unit tests for shared utility functions.
 *
 * cn() uses clsx + tailwind-merge for class deduplication.
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

  it('merges conflicting Tailwind classes (last wins)', () => {
    expect(cn('px-2', 'px-4')).toBe('px-4');
  });

  it('supports conditional object syntax', () => {
    expect(cn('base', { active: true, hidden: false })).toBe('base active');
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
