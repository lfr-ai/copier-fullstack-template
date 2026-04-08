/**
 * Dashboard page component.
 *
 * Demonstrates TanStack Query integration for server-state fetching
 * with shadcn/ui Card and Badge components.
 */
import { useQuery } from '@tanstack/react-query';
import { apiRequest } from '@/infrastructure/api/client';
import { HealthResponseSchema } from '@/domain/models';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/presentation/components/ui/card';
import { Badge } from '@/presentation/components/ui/badge';
import { Skeleton } from '@/presentation/components/ui/skeleton';

const _HEALTH_STALE_TIME_MS = 30_000;

export function Dashboard() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['health'],
    queryFn: async () => {
      const raw = await apiRequest<unknown>('/health');
      return HealthResponseSchema.parse(raw);
    },
    staleTime: _HEALTH_STALE_TIME_MS,
  });

  return (
    <section className="flex flex-col gap-6 p-8">
      <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>

      <Card>
        <CardHeader>
          <CardTitle>Backend Health</CardTitle>
          <CardDescription>
            Real-time status of the backend API connection.
          </CardDescription>
        </CardHeader>
        <CardContent>
          {isLoading && (
            <div className="flex flex-col gap-2">
              <Skeleton className="h-4 w-24" />
              <Skeleton className="h-4 w-32" />
            </div>
          )}
          {error && (
            <Badge variant="destructive">Unable to reach backend</Badge>
          )}
          {data && (
            <Badge variant="secondary">Status: {data.status}</Badge>
          )}
        </CardContent>
      </Card>
    </section>
  );
}
