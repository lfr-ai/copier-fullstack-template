/**
 * Core Web Vitals monitoring using the `web-vitals` library.
 *
 * Tracks the five standard web vitals (web-vitals v4+):
 * - **CLS** — Cumulative Layout Shift
 * - **FCP** — First Contentful Paint
 * - **INP** — Interaction to Next Paint
 * - **LCP** — Largest Contentful Paint
 * - **TTFB** — Time to First Byte
 *
 * Usage:
 * ```ts
 * import { reportWebVitals } from '@/infrastructure/profiling';
 *
 * // Log to console in development
 * reportWebVitals(console.log);
 *
 * // Send to analytics endpoint
 * reportWebVitals((metric) => {
 *   navigator.sendBeacon('/api/v1/analytics/vitals', JSON.stringify(metric));
 * });
 * ```
 *
 * @module infrastructure/profiling/web-vitals
 */
import type { Metric } from 'web-vitals';

/** Callback invoked for each Web Vital measurement. */
export type VitalsReportFn = (metric: Metric) => void;

/**
 * Report all Core Web Vitals by dynamically importing the `web-vitals` library.
 *
 * Uses dynamic import so the library is tree-shaken in production builds
 * when profiling is disabled.
 *
 * @param onReport - Callback invoked for each measured metric.
 */
export function reportWebVitals(onReport: VitalsReportFn): void {
  if (typeof onReport !== 'function') return;

  void import('web-vitals')
    .then(({ onCLS, onFCP, onINP, onLCP, onTTFB }) => {
      onCLS(onReport);
      onFCP(onReport);
      onINP(onReport);
      onLCP(onReport);
      onTTFB(onReport);
    })
    .catch(() => {
      // web-vitals library failed to load — silently degrade
    });
}
