/// <reference types="vite/client" />

/**
 * Augmented Vite environment variables.
 *
 * Only variables prefixed with `VITE_` are exposed to client code.
 * @see https://vite.dev/guide/env-and-mode#intellisense-for-typescript
 */
interface ImportMetaEnv {
  /** Current deployment environment. */
  readonly VITE_ENVIRONMENT: 'local' | 'dev' | 'test' | 'staging' | 'production';
  /** Base URL for backend API requests. */
  readonly VITE_API_BASE_URL: string;
  /** Application version injected at build time. */
  readonly VITE_APP_VERSION: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
