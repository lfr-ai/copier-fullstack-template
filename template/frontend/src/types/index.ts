/**
 * @module types
 *
 * Shared TypeScript utility types used across the frontend.
 *
 * Keep framework-agnostic types here; framework-specific types
 * belong in their respective directories (e.g. `components/`).
 *
 * API types (ApiError, PaginatedResponse) live in `models/` — do not
 * duplicate them here.
 */

/** Make selected keys required while keeping the rest unchanged. */
export type WithRequired<T, K extends keyof T> = T & Required<Pick<T, K>>;

/** Branded / nominal type helper for type-safe IDs. */
export type Brand<T, B extends string> = T & { readonly __brand: B };

export type UserId = Brand<string, 'UserId'>;
