/**
 * TypeScript type definitions.
 *
 * Pure interfaces and types — no runtime dependencies.
 * Types with Zod schemas (User, ApiError, HealthResponse) are inferred
 * from ../schemas/index.ts and re-exported via ../index.ts.
 * Only types without a Zod equivalent live here.
 */

/** Paginated API response envelope. */
export interface PaginatedResponse<T> {
  readonly items: readonly T[];
  readonly total: number;
  readonly offset: number;
  readonly limit: number;
  readonly has_more: boolean;
}
