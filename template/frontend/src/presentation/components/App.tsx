/**
 * Root application component.
 *
 * Provides the main application layout with routing.
 * TanStack Query, Error Boundary, and Router are configured
 * in bootstrap.tsx (clean architecture: providers are external).
 */
import { Suspense, lazy } from 'react';
import { Routes, Route, Link } from 'react-router';
import { ROUTES } from '@/router';

/** Lazy-loaded route components for code-splitting. */
const HomePage = lazy(() => import('@/presentation/pages/Home'));
const DashboardPage = lazy(() => import('@/presentation/pages/Dashboard'));

/** Loading fallback for Suspense boundaries. */
function PageLoader() {
  return (
    <div className="flex min-h-[50vh] items-center justify-center" role="status">
      <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent" />
      <span className="sr-only">Loading…</span>
    </div>
  );
}

export function App() {
  return (
    <>
      <header className="site-header">
        <nav aria-label="Main navigation">
          <Link to={ROUTES.HOME} className="logo">{{ project_name }}</Link>
          <ul className="nav-links">
            <li><Link to={ROUTES.HOME}>Home</Link></li>
            <li><Link to={ROUTES.DASHBOARD}>Dashboard</Link></li>
          </ul>
        </nav>
      </header>

      <main id="main-content">
        <Suspense fallback={<PageLoader />}>
          <Routes>
            <Route path={ROUTES.HOME} element={<HomePage />} />
            <Route path={ROUTES.DASHBOARD} element={<DashboardPage />} />
          </Routes>
        </Suspense>
      </main>

      <footer className="site-footer">
        <p>&copy; {new Date().getFullYear()} {{ project_name }}</p>
      </footer>
    </>
  );
}
