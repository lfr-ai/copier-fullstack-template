/**
 * Zod runtime validation schemas.
 *
 * Each schema mirrors a backend Pydantic model and provides
 * runtime type-safety for API responses on the client side.
 */

import { z } from 'zod';

// ── User ──────────────────────────────────────────────────────────

export const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  display_name: z.string().min(1).max(100),
  is_active: z.boolean(),
});

export type User = z.infer<typeof UserSchema>;

export const CreateUserSchema = z.object({
  email: z.string().email(),
  display_name: z.string().min(1).max(100),
  password: z.string().min(8).max(128),
});

export type CreateUser = z.infer<typeof CreateUserSchema>;

// ── Pagination ────────────────────────────────────────────────────

/**
 * Build paginated response schema for a given item schema.
 *
 * @param itemSchema - Zod schema for individual items
 * @returns Zod schema wrapping items in pagination envelope
 */
export const PaginatedResponseSchema = <T extends z.ZodTypeAny>(itemSchema: T) =>
  z.object({
    items: z.array(itemSchema),
    total: z.number().int().nonnegative(),
    offset: z.number().int().nonnegative(),
    limit: z.number().int().positive(),
    has_more: z.boolean(),
  });

// ── API Error ─────────────────────────────────────────────────────

export const ApiErrorSchema = z.object({
  detail: z.string(),
  status_code: z.number().int(),
});

export type ApiError = z.infer<typeof ApiErrorSchema>;

// ── Health ────────────────────────────────────────────────────────

export const HealthResponseSchema = z.object({
  status: z.string(),
});

export type HealthResponse = z.infer<typeof HealthResponseSchema>;
