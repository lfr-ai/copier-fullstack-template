/**
 * Runtime environment configuration.
 *
 * All values are sourced from Vite's {@link import.meta.env} which reads
 * from `.env`, `.env.local`, `.env.[mode]`, and `.env.[mode].local` files
 * at build time.  Only variables prefixed with `VITE_` are exposed.
 *
 * @see https://vite.dev/guide/env-and-mode
 */

/** Supported deployment environments. */
export type AppEnvironment = 'local' | 'dev' | 'test' | 'staging' | 'prod';

/** Typed environment configuration object. */
export interface AppConfig {
  /** Current deployment environment. */
  readonly environment: AppEnvironment;
  /** Base URL for backend API requests (no trailing slash). */
  readonly apiBaseUrl: string;
  /** Whether the app is running in a production build. */
  readonly isProd: boolean;
  /** Whether the app is running in development mode. */
  readonly isDev: boolean;
  /** Application version string (injected at build time). */
  readonly appVersion: string;
}

function resolveEnvironment(): AppEnvironment {
  const raw = import.meta.env.VITE_ENVIRONMENT ?? 'local';
  const allowed: ReadonlySet<AppEnvironment> = new Set([
    'local',
    'dev',
    'test',
    'staging',
    'prod',
  ]);
  if (allowed.has(raw as AppEnvironment)) {
    return raw as AppEnvironment;
  }
  console.warn(`[config] Unknown VITE_ENVIRONMENT "${raw}", falling back to "local".`);
  return 'local';
}

/**
 * Singleton application configuration derived from build-time env vars.
 *
 * Import this wherever you need environment-aware behaviour:
 * ```ts
 * import { config } from '@/config/env';
 * if (config.isDev) { ... }
 * ```
 */
export const config: AppConfig = Object.freeze({
  environment: resolveEnvironment(),
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL ?? '/api/v1',
  isProd: import.meta.env.PROD,
  isDev: import.meta.env.DEV,
  appVersion: import.meta.env.VITE_APP_VERSION ?? '0.0.0-dev',
});
