/** Route path constants — single source of truth for client-side routes.
 *
 * Import and use in route definitions and navigation:
 *
 *   import { ROUTES } from './router';
 */
export const ROUTES = {
  HOME: '/',
  DASHBOARD: '/dashboard',
  FORMS: '/forms',
  SETTINGS: '/settings',
  NOT_FOUND: '*',
} as const;

export type RoutePath = (typeof ROUTES)[keyof typeof ROUTES];

export const NAV_ROUTES = [
  {
    path: ROUTES.HOME,
    label: 'Home',
  },
  {
    path: ROUTES.DASHBOARD,
    label: 'Dashboard',
  },
  {
    path: ROUTES.FORMS,
    label: 'Forms',
  },
  {
    path: ROUTES.SETTINGS,
    label: 'Settings',
  },
] as const;

export type NavRoute = (typeof NAV_ROUTES)[number];
