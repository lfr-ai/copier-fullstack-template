/**
 * Unit tests for the HTTP API client.
 */
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { apiRequest } from '../../../src/api/client';

describe('apiRequest', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('makes a GET request by default', async () => {
    const mockData = { id: 1, name: 'test' };
    globalThis.fetch = vi.fn().mockResolvedValue(
      new Response(JSON.stringify(mockData), {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
      }),
    );

    const result = await apiRequest('/users');

    expect(fetch).toHaveBeenCalledWith(
      '/api/v1/users',
      expect.objectContaining({ method: 'GET' }),
    );
    expect(result).toEqual(mockData);
  });

  it('sends JSON body for POST requests', async () => {
    globalThis.fetch = vi.fn().mockResolvedValue(
      new Response(JSON.stringify({ id: 1 }), {
        status: 201,
        headers: { 'Content-Type': 'application/json' },
      }),
    );

    await apiRequest('/users', {
      method: 'POST',
      body: { name: 'test' },
    });

    expect(fetch).toHaveBeenCalledWith(
      '/api/v1/users',
      expect.objectContaining({
        method: 'POST',
        body: JSON.stringify({ name: 'test' }),
      }),
    );
  });

  it('throws on non-ok response', async () => {
    globalThis.fetch = vi
      .fn()
      .mockResolvedValue(
        new Response('Not Found', { status: 404, statusText: 'Not Found' }),
      );

    await expect(apiRequest('/nonexistent')).rejects.toThrow('API error: 404');
  });
});
