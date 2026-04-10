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

## Quality Gates

- TypeScript strict mode must remain clean
- All existing tests must remain green
- Add targeted tests for new behaviors
- Use stable selectors and deterministic mocks for e2e tests
- Keep component composition consistent with shadcn patterns
