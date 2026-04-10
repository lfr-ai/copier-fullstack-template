# Frontend React Stack Skill

## Scope

Apply this skill for all frontend changes under `frontend/`.

## Technology Stack

| Concern | Technology | Version |
|---------|-----------|---------|
| **Build** | Vite | 6+ |
| **Language** | TypeScript | strict mode |
| **UI Framework** | React | 19 |
| **UI Components** | shadcn/ui | Radix primitives + Tailwind CSS v4 |
| **Routing** | React Router | v7 (`react-router`) |
| **Forms** | React Hook Form + Zod | v7 + `@hookform/resolvers` |
| **Server State** | TanStack Query | v5 |
| **Client State** | Zustand | v5 |
| **Data Tables** | TanStack Table | v8 |
| **Styling** | Tailwind CSS | v4 (oklch tokens + `@theme inline`) |
| **Icons** | Lucide React | latest |
| **Toast** | Sonner | via shadcn `sonner` component |
| **Linting** | Biome | latest |
| **Testing** | Vitest + RTL + Playwright | latest |
| **Package Manager** | bun | latest |

## Non-goals

- Do NOT introduce Lit web components, Vue, Angular, or other front frameworks
- Do NOT introduce alternative routing systems unless explicitly requested
- Do NOT introduce TanStack Form (`@tanstack/react-form`) — use React Hook Form
  as the only form library
- Do NOT bypass shadcn primitives for shared controls without documented reason
- Do NOT use Jinja2 templates for frontend views

## Project Architecture

```text
frontend/src/
├── application/         # TanStack Query hooks + Zustand stores
├── domain/              # Models, Zod schemas, utility types
├── infrastructure/      # API client, config (runtime, env, registry)
├── lib/                 # Shared utilities (cn(), form helpers)
├── presentation/        # UI layer
│   ├── components/ui/   # shadcn/ui primitives (button, card, dialog, ...)
│   ├── components/      # Domain components (citation, layout)
│   ├── features/        # Feature modules (case-detail, cases, modals)
│   ├── pages/           # Route page components
│   └── providers/       # React context providers (theme)
├── router/              # React Router route definitions
└── styles/              # Tailwind CSS + shadcn theme tokens
```

## shadcn/ui Standards

### Installation

Always use the shadcn CLI — never copy-paste from documentation:

```bash
bun run shadcn add button card dialog   # Add components
bun run shadcn add --all                # Add all components
bun run shadcn search @shadcn -q "sidebar"  # Search registry
bun run shadcn docs button dialog       # Get component docs
```

### Configuration

The project `components.json` maps shadcn output paths:

```json
{
  "aliases": {
    "components": "@/presentation/components",
    "ui": "@/presentation/components/ui",
    "hooks": "@/application/hooks",
    "lib": "@/lib",
    "utils": "@/lib/utils"
  }
}
```

### Styling Rules

- **Semantic colors only**: `bg-primary`, `text-muted-foreground` — never `bg-blue-500`
- **`cn()` for class merging**: `cn("base-class", condition && "conditional-class")`
- **`gap-*` for spacing**: Use flex/grid + `gap-4`, never `space-x-4` / `space-y-4`
- **`size-*` for square dims**: `size-10` not `w-10 h-10`
- **`truncate` shorthand**: Not `overflow-hidden text-ellipsis whitespace-nowrap`
- **No manual `dark:` overrides**: Semantic tokens auto-adapt
- **No manual `z-index`**: Dialog, Sheet, Popover handle their own stacking

### Composition Rules

- **Full Card structure**: `CardHeader` / `CardTitle` / `CardDescription` / `CardContent` / `CardFooter`
- **Accessibility titles**: Dialog, Sheet always need `DialogTitle` / `SheetTitle` (use `sr-only` if hidden)
- **Items in Groups**: `SelectItem` in `SelectGroup`, `DropdownMenuItem` in `DropdownMenuGroup`
- **Tabs**: `TabsTrigger` must be inside `TabsList`
- **Avatar**: Always include `AvatarFallback`
- **Separators**: Use `Separator` not `<hr>` or `<div className="border-t">`
- **Loading**: Use `Skeleton` not custom `animate-pulse` divs
- **Status**: Use `Badge` not custom styled spans
- **Callouts**: Use `Alert` not custom styled divs
- **Toast**: Use `toast()` from `sonner`, not custom toast implementations

### MCP/Skills Workflow

- Use shadcn MCP server (configured in `.vscode/mcp.json`) for AI-assisted discovery
- Use `shadcn docs <component>` to get documentation URLs before generating code
- Use `shadcn search` to find components before writing custom UI
- Use `shadcn add --dry-run` and `--diff` to preview updates safely

## React Router Standards

- Centralize all routes in `src/router/routes.tsx`
- Use layout routes with `<Outlet>` for shell composition (e.g., `AppShell`)
- Use `useParams()` for route parameters
- Use `useNavigate()` for programmatic navigation
- Use `<Link>` / `<NavLink>` for declarative navigation
- Use `<Navigate>` for redirects
- Include a wildcard `*` route for not-found UI

```tsx
import { Route, Routes, Navigate, Outlet } from "react-router";

export function AppRoutes() {
  return (
    <Routes>
      <Route element={<AppShell />}>
        <Route index element={<Navigate to="/cases" replace />} />
        <Route path="cases" element={<CasesPage />} />
        <Route path="cases/:caseId" element={<CaseDetailPage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Route>
    </Routes>
  );
}
```

## React Hook Form + Zod Standards

React Hook Form is mandatory for form state and validation integration in this
repository.

- Define Zod schemas as single source of truth for validation
- Wire through `zodResolver` from `@hookform/resolvers/zod`
- Always provide explicit `defaultValues` (never `undefined`)
- Use shadcn `Form` / `FormField` / `FormItem` / `FormLabel` / `FormControl` / `FormMessage`
- Keep validation mode explicit (`mode: "onBlur"` or `mode: "onChange"`) for UX consistency

```tsx
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Form, FormField, FormItem, FormLabel, FormControl, FormMessage } from "@/presentation/components/ui/form";
import { Input } from "@/presentation/components/ui/input";
import { Button } from "@/presentation/components/ui/button";

const schema = z.object({
  name: z.string().min(1, "Required"),
  email: z.string().email("Invalid email"),
});

type FormValues = z.infer<typeof schema>;

function MyForm({ onSubmit }: { onSubmit: (values: FormValues) => void }) {
  const form = useForm<FormValues>({
    resolver: zodResolver(schema),
    defaultValues: { name: "", email: "" },
    mode: "onBlur",
  });

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="flex flex-col gap-4">
        <FormField
          control={form.control}
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Name</FormLabel>
              <FormControl><Input {...field} /></FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit" disabled={form.formState.isSubmitting}>
          Submit
        </Button>
      </form>
    </Form>
  );
}
```

## TanStack Query Standards

- Define query keys in `src/application/hooks/query-keys.ts`
- One hook file per domain entity: `use-cases.ts`, `use-customers.ts`, etc.
- Use `useQuery` for reads, `useMutation` for writes
- Invalidate related queries after mutations
- Set appropriate `staleTime` and `retry` in QueryClient defaults

## Zustand Standards

- Use ONLY for client-side UI state (modals, filters, pagination, search terms)
- Server state belongs in TanStack Query, NOT in Zustand
- Use `devtools` middleware in development
- Keep stores minimal and single-responsibility

## Toast Notifications

Use `toast()` from `sonner` — never custom toast implementations:

```tsx
import { toast } from "sonner";

toast.success("Case created successfully");
toast.error("Failed to process");
toast.info("Processing...");
toast.warning("Missing fields");
toast.promise(asyncOperation(), {
  loading: "Processing...",
  success: "Done!",
  error: "Failed",
});
```

## Registry Constants

Import from `@/infrastructure/config/registry` — never hardcode route/field names:

```tsx
import { Routes, StatusText, StatusCode } from "@/infrastructure/config/registry";
```

## Quality Gates

- TypeScript strict mode must remain clean
- All existing tests must remain green
- Add targeted tests for new behaviors
- Use stable selectors and deterministic mocks for e2e tests
- Keep component composition consistent with shadcn patterns
