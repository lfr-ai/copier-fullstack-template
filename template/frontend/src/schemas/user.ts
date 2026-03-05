/**
 * User Zod validation schemas matching backend Pydantic models.
 */
import { z } from 'zod';

export const CreateUserSchema = z.object({
  email: z.string().email().min(5).max(255),
  display_name: z.string().min(1).max(100),
  password: z.string().min(8).max(128),
});

export const UserSchema = z.object({
  id: z.number().positive(),
  email: z.string().email(),
  display_name: z.string(),
  is_active: z.boolean(),
});

export type CreateUser = z.infer<typeof CreateUserSchema>;
export type User = z.infer<typeof UserSchema>;
