/**
 * HTTP API client for backend communication.
 */
import { config } from "@/infrastructure/config/env";

const API_BASE = config.apiBaseUrl;
const _HTTP_NO_CONTENT = 204;

type HttpMethod = "GET" | "POST" | "PUT" | "PATCH" | "DELETE";

interface RequestOptions {
  method?: HttpMethod;
  body?: unknown;
  headers?: Record<string, string>;
}

/**
 * Send typed HTTP request to the backend API.
 *
 * @typeParam T - Expected response type. Defaults to `void` for
 *   requests that return no body (e.g. DELETE → 204).  For typed
 *   JSON responses pass the expected type explicitly.
 * @param path - API path relative to `/api/v1`
 * @param options - Request method, body, and headers
 * @returns Parsed JSON response of type `T`, or `undefined` for empty responses
 * @throws {Error} On non-2xx HTTP status
 */
export async function apiRequest<T = void>(
  path: string,
  options: RequestOptions = {},
): Promise<T> {
  const { method = "GET", body, headers = {} } = options;

  const response = await fetch(`${API_BASE}${path}`, {
    method,
    headers: {
      ...(body ? { "Content-Type": "application/json" } : {}),
      ...headers,
    },
    body: body ? JSON.stringify(body) : undefined,
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status} ${response.statusText}`);
  }

  // 204 No Content or non-JSON — return undefined (safe when T is void)
  const contentType = response.headers.get("content-type");
  if (
    response.status === _HTTP_NO_CONTENT ||
    !contentType?.includes("application/json")
  ) {
    return undefined as unknown as T;
  }

  return response.json() as Promise<T>;
}
