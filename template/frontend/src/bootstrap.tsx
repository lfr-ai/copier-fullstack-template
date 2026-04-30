/**
 * React application bootstrap.
 *
 * Mounts the root component tree with required providers:
 * - React.StrictMode for development warnings
 * - ErrorBoundary for graceful crash recovery
 * - ThemeProvider for dark/light/system mode toggling
 * - QueryClientProvider for TanStack Query server-state management
 * - BrowserRouter for client-side routing
 * - Toaster for toast notifications (sonner)
 */
import React from 'react';
import ReactDOM from 'react-dom/client';
import { ErrorBoundary } from 'react-error-boundary';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter } from 'react-router';
import { ThemeProvider } from './presentation/components/theme-provider';
import { Toaster } from './presentation/components/ui/sonner';
import { Button } from './presentation/components/ui/button';
import { App } from './presentation/components/app';
import './presentation/styles/tailwind.css';
import './presentation/styles/main.css';

const _QUERY_STALE_TIME_MS = 5 * 60 * 1000;
const _QUERY_GC_TIME_MS = 10 * 60 * 1000;
const _QUERY_RETRY_COUNT = 2;
const _MUTATION_RETRY_COUNT = 1;

/** TanStack Query client with tuned defaults for stale time, GC, and retry. */
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: _QUERY_STALE_TIME_MS,
      gcTime: _QUERY_GC_TIME_MS,
      retry: _QUERY_RETRY_COUNT,
      refetchOnWindowFocus: false,
    },
    mutations: {
      retry: _MUTATION_RETRY_COUNT,
    },
  },
});

/** Fallback UI rendered when an unrecoverable error occurs. */
function ErrorFallback({ error, resetErrorBoundary }: { error: Error; resetErrorBoundary: () => void }) {
  return (
    <main role="alert" className="flex min-h-screen flex-col items-center justify-center gap-4 p-8 text-center">
      <h1 className="text-2xl font-bold text-destructive">Something went wrong</h1>
      <pre className="max-w-lg overflow-auto rounded-md bg-muted p-4 text-sm">{error.message}</pre>
      <Button onClick={resetErrorBoundary}>
        Try again
      </Button>
    </main>
  );
}

const rootElement = document.getElementById('root');

if (rootElement) {
  ReactDOM.createRoot(rootElement).render(
    <React.StrictMode>
      <ErrorBoundary FallbackComponent={ErrorFallback} onReset={() => queryClient.clear()}>
        <ThemeProvider defaultTheme="system" storageKey="vite-ui-theme">
          <QueryClientProvider client={queryClient}>
            <BrowserRouter>
              <App />
            </BrowserRouter>
          </QueryClientProvider>
          <Toaster />
        </ThemeProvider>
      </ErrorBoundary>
    </React.StrictMode>,
  );
}
