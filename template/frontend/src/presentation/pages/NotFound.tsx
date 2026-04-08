/**
 * Not-found page component.
 *
 * Rendered when no route match exists.
 */
import { Link } from 'react-router';
import { ROUTES } from '@/router';
import { Button } from '@/presentation/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/presentation/components/ui/card';

export function NotFound() {
  return (
    <section className="mx-auto flex min-h-[60vh] w-full max-w-3xl items-center justify-center px-6 py-16">
      <Card className="w-full max-w-lg">
        <CardHeader>
          <CardTitle className="text-3xl tracking-tight">404 — Page not found</CardTitle>
          <CardDescription>
            This route does not exist. Check the URL or return to the homepage.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Button asChild>
            <Link to={ROUTES.HOME}>Back to Home</Link>
          </Button>
        </CardContent>
      </Card>
    </section>
  );
}
