/**
 * Lightweight reactive stores for cross-component state.
 *
 * Usage:
 * - React: wrap with `useSyncExternalStore(themeStore.subscribe, themeStore.get)`
 * - Lit: use a `ReactiveController` that calls `themeStore.subscribe`
 */

type Theme = 'light' | 'dark' | 'system';

const THEME_KEY = 'app-theme';

function getInitialTheme(): Theme {
  if (typeof window === 'undefined') return 'system';
  return (localStorage.getItem(THEME_KEY) as Theme | null) ?? 'system';
}

let _theme: Theme = getInitialTheme();
const _listeners = new Set<(theme: Theme) => void>();

export const themeStore = {
  get(): Theme {
    return _theme;
  },

  set(next: Theme): void {
    _theme = next;
    localStorage.setItem(THEME_KEY, next);
    _listeners.forEach((fn) => fn(next));
  },

  subscribe(fn: (theme: Theme) => void): () => void {
    _listeners.add(fn);
    return () => _listeners.delete(fn);
  },

  /** Resolve 'system' to the actual OS preference. */
  resolved(): 'light' | 'dark' {
    if (_theme !== 'system') return _theme;
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  },
} as const;
