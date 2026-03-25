/** Route path constants — single source of truth for client-side routes.
 *
 * Import and use in route definitions and navigation:
 *
 *   import { ROUTES } from './router';
 */
export const ROUTES = {
  HOME: '/',
  DASHBOARD: '/dashboard',
  NOT_FOUND: '*',
} as const;

export type RoutePath = (typeof ROUTES)[keyof typeof ROUTES];
