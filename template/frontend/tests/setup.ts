/**
 * @module tests/setup
 *
 * Vitest global setup file executed before every test suite.
 *
 * Responsibilities:
 * - Clears the DOM and resets mocks after each test.
 * - Stubs browser APIs unavailable in happy-dom
 *   (`matchMedia`, `IntersectionObserver`, `ResizeObserver`).
 * - Provides {@link mockApiSuccess} and {@link mockApiError}
 *   helpers for declarative `fetch` stubbing.
 */

import { afterEach, vi } from 'vitest';

// ── DOM cleanup + mock reset ───────────────────────────────────
afterEach(() => {
  document.body.replaceChildren();
  vi.clearAllMocks();
});

// ── Browser API stubs ──────────────────────────────────────────

Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation((query: string) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
});

if (typeof globalThis.IntersectionObserver === 'undefined') {
  globalThis.IntersectionObserver = class IntersectionObserver {
    readonly root = null;
    readonly rootMargin = '';
    readonly thresholds: readonly number[] = [];
    observe = vi.fn();
    unobserve = vi.fn();
    disconnect = vi.fn();
    takeRecords(): IntersectionObserverEntry[] {
      return [];
    }
  } as unknown as typeof globalThis.IntersectionObserver;
}

if (typeof globalThis.ResizeObserver === 'undefined') {
  globalThis.ResizeObserver = class ResizeObserver {
    observe = vi.fn();
    unobserve = vi.fn();
    disconnect = vi.fn();
  } as unknown as typeof globalThis.ResizeObserver;
}

// ── Shared test utilities ──────────────────────────────────────

/** Create a mock successful fetch response. */
export function mockApiSuccess<T>(data: T): void {
  globalThis.fetch = vi.fn().mockResolvedValue(
    new Response(JSON.stringify(data), {
      status: 200,
      headers: { 'Content-Type': 'application/json' },
    }),
  );
}

/** Create a mock error fetch response. */
export function mockApiError(status: number, message: string): void {
  globalThis.fetch = vi.fn().mockResolvedValue(
    new Response(JSON.stringify({ detail: message }), {
      status,
      headers: { 'Content-Type': 'application/json' },
    }),
  );
}
