/**
 * Frontend Performance Profiling — Barrel Export.
 *
 * Provides Core Web Vitals monitoring via the `web-vitals` library.
 *
 * Call `reportWebVitals(console.log)` in your app entry point
 * (main.ts / bootstrap.tsx) to start collecting metrics.
 *
 * @module lib/profiling
 */
export { reportWebVitals, type VitalsReportFn } from './web-vitals';
