/**
 * Zod runtime validation schemas.
 *
 * Each schema mirrors a backend Pydantic model and provides
 * runtime type-safety for API responses on the client side.
 */

import { z } from 'zod';

const _DISPLAY_NAME_MIN = 1;
const _DISPLAY_NAME_MAX = 100;
const _PASSWORD_MIN = 8;
const _PASSWORD_MAX = 128;

export const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  display_name: z.string().min(_DISPLAY_NAME_MIN).max(_DISPLAY_NAME_MAX),
  is_active: z.boolean(),
});

export type User = z.infer<typeof UserSchema>;

export const CreateUserSchema = z.object({
  email: z.string().email(),
  display_name: z.string().min(_DISPLAY_NAME_MIN).max(_DISPLAY_NAME_MAX),
  password: z.string().min(_PASSWORD_MIN).max(_PASSWORD_MAX),
});

export type CreateUser = z.infer<typeof CreateUserSchema>;

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

export const ApiErrorSchema = z.object({
  detail: z.string(),
  status_code: z.number().int(),
});

export type ApiError = z.infer<typeof ApiErrorSchema>;

export const HealthResponseSchema = z.object({
  status: z.string(),
});

export type HealthResponse = z.infer<typeof HealthResponseSchema>;
