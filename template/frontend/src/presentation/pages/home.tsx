/**
 * Home page component.
 */
import { Button } from '@/presentation/components/ui/button';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/presentation/components/ui/card';
import { Badge } from '@/presentation/components/ui/badge';
import { Link } from 'react-router';
import { ROUTES } from '@/router';

export function Home() {
  return (
    <section className="flex flex-col items-center gap-8 px-6 py-16 text-center animate-in">
      <div className="flex flex-col gap-3">
        <Badge variant="secondary" className="mx-auto">
          Production-ready
        </Badge>
        <h1 className="text-4xl font-bold tracking-tight text-balance">
          Welcome
        </h1>
        <p className="max-w-lg text-lg text-muted-foreground">
          Application is running. Built with React 19, Vite, and shadcn/ui.
        </p>
      </div>

      <div className="flex gap-3">
        <Button asChild>
          <Link to={ROUTES.DASHBOARD}>Go to Dashboard</Link>
        </Button>
        <Button variant="secondary" asChild>
          <Link to={ROUTES.FORMS}>Try Forms</Link>
        </Button>
        <Button variant="outline" asChild>
          <a href="https://ui.shadcn.com" target="_blank" rel="noopener noreferrer">
            shadcn/ui Docs
          </a>
        </Button>
      </div>

      <div className="mt-8 grid w-full max-w-3xl gap-4 sm:grid-cols-3">
        <Card>
          <CardHeader>
            <CardTitle>Type-Safe</CardTitle>
            <CardDescription>
              End-to-end TypeScript with strict mode and Zod validation.
            </CardDescription>
          </CardHeader>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Accessible</CardTitle>
            <CardDescription>
              Radix UI primitives with WAI-ARIA patterns built in.
            </CardDescription>
          </CardHeader>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Themeable</CardTitle>
            <CardDescription>
              Dark mode, CSS variables, and semantic design tokens.
            </CardDescription>
          </CardHeader>
        </Card>
      </div>
    </section>
  );
}
