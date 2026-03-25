/// <reference types="vite/client" />

/**
 * Augmented Vite environment variables.
 *
 * Only variables prefixed with `VITE_` are exposed to client code.
 * @see https://vite.dev/guide/env-and-mode#intellisense-for-typescript
 */
interface ImportMetaEnv extends Readonly<import('vite').ImportMetaEnv> {
  /** Current deployment environment. */
  readonly VITE_ENVIRONMENT: 'local' | 'dev' | 'test' | 'staging' | 'prod';
  /** Base URL for backend REST API requests. */
  readonly VITE_API_BASE_URL: string;
  /** URL for backend GraphQL endpoint. */
  readonly VITE_GRAPHQL_URL: string;
  /** Application version injected at build time. */
  readonly VITE_APP_VERSION: string;
}
