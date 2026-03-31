/**
 * Debounce hook for rate-limiting rapid value changes.
 */
import { useEffect, useState } from 'react';

const _DEFAULT_DEBOUNCE_MS = 300;

export function useDebounce<T>(value: T, delay = _DEFAULT_DEBOUNCE_MS): T {
  const [debounced, setDebounced] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debounced;
}
