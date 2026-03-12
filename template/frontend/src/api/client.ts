/**
 * HTTP API client for backend communication.
 */
import { config } from '@/config/env';

const API_BASE = config.apiBaseUrl;

type HttpMethod = 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';

interface RequestOptions {
  method?: HttpMethod;
  body?: unknown;
  headers?: Record<string, string>;
}

/**
 * Send typed HTTP request to the backend API.
 *
 * @param path - API path relative to `/api/v1`
 * @param options - Request method, body, and headers
 * @returns Parsed JSON response cast to `T`
 * @throws {Error} On non-2xx HTTP status
 */
export async function apiRequest<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const { method = 'GET', body, headers = {} } = options;

  const response = await fetch(`${API_BASE}${path}`, {
    method,
    headers: {
      ...(body ? { 'Content-Type': 'application/json' } : {}),
      ...headers,
    },
    body: body ? JSON.stringify(body) : undefined,
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status} ${response.statusText}`);
  }

  return response.json() as Promise<T>;
}
