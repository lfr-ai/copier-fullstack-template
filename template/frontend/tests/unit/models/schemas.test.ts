/**
 * Unit tests for Zod runtime validation schemas.
 *
 * Validates that schemas correctly accept valid data
 * and reject invalid or malformed payloads.
 */
import { describe, expect, it } from 'vitest';

import {
  ApiErrorSchema,
  CreateUserSchema,
  HealthResponseSchema,
  PaginatedResponseSchema,
  UserSchema,
} from '@/models/schemas/index';

// ── User ──────────────────────────────────────────────────────────

describe('UserSchema', () => {
  it('accepts a valid user', () => {
    const result = UserSchema.safeParse({
      id: '550e8400-e29b-41d4-a716-446655440000',
      email: 'user@example.com',
      display_name: 'Alice',
      is_active: true,
    });
    expect(result.success).toBe(true);
  });

  it('rejects missing email', () => {
    const result = UserSchema.safeParse({
      id: '550e8400-e29b-41d4-a716-446655440000',
      display_name: 'Alice',
      is_active: true,
    });
    expect(result.success).toBe(false);
  });

  it('rejects invalid email format', () => {
    const result = UserSchema.safeParse({
      id: '550e8400-e29b-41d4-a716-446655440000',
      email: 'not-an-email',
      display_name: 'Alice',
      is_active: true,
    });
    expect(result.success).toBe(false);
  });

  it('rejects non-uuid id', () => {
    const result = UserSchema.safeParse({
      id: 'not-a-uuid',
      email: 'a@b.com',
      display_name: 'A',
      is_active: true,
    });
    expect(result.success).toBe(false);
  });
});

// ── CreateUser ────────────────────────────────────────────────────

describe('CreateUserSchema', () => {
  it('accepts valid creation payload', () => {
    const result = CreateUserSchema.safeParse({
      email: 'new@example.com',
      display_name: 'Bob',
      password: 'securepass123',
    });
    expect(result.success).toBe(true);
  });

  it('rejects password shorter than 8 chars', () => {
    const result = CreateUserSchema.safeParse({
      email: 'new@example.com',
      display_name: 'Bob',
      password: 'short',
    });
    expect(result.success).toBe(false);
  });

  it('rejects empty display_name', () => {
    const result = CreateUserSchema.safeParse({
      email: 'new@example.com',
      display_name: '',
      password: 'securepass123',
    });
    expect(result.success).toBe(false);
  });
});

// ── Pagination ────────────────────────────────────────────────────

describe('PaginatedResponseSchema', () => {
  const PaginatedUsers = PaginatedResponseSchema(UserSchema);

  it('accepts valid paginated response', () => {
    const result = PaginatedUsers.safeParse({
      items: [
        {
          id: '550e8400-e29b-41d4-a716-446655440000',
          email: 'a@b.com',
          display_name: 'A',
          is_active: true,
        },
      ],
      total: 1,
      offset: 0,
      limit: 10,
      has_more: false,
    });
    expect(result.success).toBe(true);
  });

  it('accepts empty items list', () => {
    const result = PaginatedUsers.safeParse({
      items: [],
      total: 0,
      offset: 0,
      limit: 10,
      has_more: false,
    });
    expect(result.success).toBe(true);
  });

  it('rejects invalid item in items array', () => {
    const result = PaginatedUsers.safeParse({
      items: [{ id: 'not-a-uuid' }],
      total: 1,
      offset: 0,
      limit: 10,
      has_more: false,
    });
    expect(result.success).toBe(false);
  });
});

// ── ApiError ──────────────────────────────────────────────────────

describe('ApiErrorSchema', () => {
  it('accepts valid error response', () => {
    const result = ApiErrorSchema.safeParse({
      detail: 'Not found',
      status_code: 404,
    });
    expect(result.success).toBe(true);
  });

  it('rejects missing detail', () => {
    const result = ApiErrorSchema.safeParse({
      status_code: 500,
    });
    expect(result.success).toBe(false);
  });
});

// ── Health ────────────────────────────────────────────────────────

describe('HealthResponseSchema', () => {
  it('accepts valid health response', () => {
    const result = HealthResponseSchema.safeParse({ status: 'healthy' });
    expect(result.success).toBe(true);
  });

  it('rejects non-string status', () => {
    const result = HealthResponseSchema.safeParse({ status: 123 });
    expect(result.success).toBe(false);
  });
});
