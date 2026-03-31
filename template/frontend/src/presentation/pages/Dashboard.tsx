/**
 * Dashboard page component.
 *
 * Demonstrates TanStack Query integration for server-state fetching.
 */
import { useQuery } from '@tanstack/react-query';
import { apiRequest } from '@/infrastructure/api/client';
import { HealthResponseSchema } from '@/domain/models';

const _HEALTH_STALE_TIME_MS = 30_000;

export default function Dashboard() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['health'],
    queryFn: async () => {
      const raw = await apiRequest<unknown>('/health');
      return HealthResponseSchema.parse(raw);
    },
    staleTime: _HEALTH_STALE_TIME_MS,
  });

  return (
    <section className="p-8">
      <h1 className="mb-6 text-3xl font-bold">Dashboard</h1>

      <section className="stat-card" aria-label="Backend health status">
        <h2 className="mb-2 text-lg font-semibold">Backend Health</h2>
        {isLoading && <p className="text-secondary">Checking…</p>}
        {error && <p className="text-error">Unable to reach backend.</p>}
        {data && (
          <p className="text-success font-medium">
            Status: {data.status}
          </p>
        )}
      </section>
    </section>
  );
}
