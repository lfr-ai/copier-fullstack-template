/**
 * Root application component.
 *
 * Provides the main application layout with routing.
 * TanStack Query, Error Boundary, ThemeProvider, and Router are
 * configured in bootstrap.tsx (clean architecture: providers are external).
 */
import { Suspense, lazy } from 'react';
import { Routes, Route, Link, NavLink } from 'react-router';
import { NAV_ROUTES, ROUTES } from '@/router';
import { Separator } from '@/presentation/components/ui/separator';
import { Skeleton } from '@/presentation/components/ui/skeleton';
import { buttonVariants } from '@/presentation/components/ui/button';
import { ModeToggle } from '@/presentation/components/mode-toggle';
import { cn } from '@/lib/utils';

/** Lazy-loaded route components for code-splitting. */
const HomePage = lazy(() =>
  import('@/presentation/pages/home').then((module) => ({
    default: module.Home,
  })),
);
const DashboardPage = lazy(() =>
  import('@/presentation/pages/dashboard').then((module) => ({
    default: module.Dashboard,
  })),
);
const FormsPage = lazy(() =>
  import('@/presentation/pages/forms').then((module) => ({
    default: module.Forms,
  })),
);
const SettingsPage = lazy(() =>
  import('@/presentation/pages/settings').then((module) => ({
    default: module.Settings,
  })),
);
const NotFoundPage = lazy(() =>
  import('@/presentation/pages/not-found').then((module) => ({
    default: module.NotFound,
  })),
);

/** Loading fallback for Suspense boundaries. */
function PageLoader() {
  return (
    <div className="flex min-h-[50vh] flex-col items-center justify-center gap-4" role="status">
      <Skeleton className="size-8 rounded-full" />
      <Skeleton className="h-4 w-48" />
      <span className="sr-only">Loading page...</span>
    </div>
  );
}

export function App() {
  return (
    <>
      <header className="sticky top-0 z-40 border-b border-border bg-background/95 backdrop-blur supports-backdrop-filter:bg-background/60">
        <nav aria-label="Main navigation" className="mx-auto flex max-w-5xl items-center justify-between px-6 py-3">
          <Link to={ROUTES.HOME} className="text-lg font-bold text-primary no-underline">
            {{ project_name }}
          </Link>
          <div className="flex items-center gap-6">
            <ul className="flex list-none gap-4">
              {NAV_ROUTES.map((route) => (
                <li key={route.path}>
                  <NavLink
                    to={route.path}
                    end
                    className={({ isActive }) =>
                      cn(
                        buttonVariants({ variant: 'ghost', size: 'sm' }),
                        isActive && 'bg-accent text-accent-foreground',
                      )
                    }
                  >
                    {route.label}
                  </NavLink>
                </li>
              ))}
            </ul>
            <ModeToggle />
          </div>
        </nav>
      </header>

      <main id="main-content">
        <Suspense fallback={<PageLoader />}>
          <Routes>
            <Route path={ROUTES.HOME} element={<HomePage />} />
            <Route path={ROUTES.DASHBOARD} element={<DashboardPage />} />
            <Route path={ROUTES.FORMS} element={<FormsPage />} />
            <Route path={ROUTES.SETTINGS} element={<SettingsPage />} />
            <Route path={ROUTES.NOT_FOUND} element={<NotFoundPage />} />
          </Routes>
        </Suspense>
      </main>

      <Separator className="mt-16" />
      <footer className="py-6 text-center text-sm text-muted-foreground">
        <p>&copy; {new Date().getFullYear()} {{ project_name }}</p>
      </footer>
    </>
  );
}
