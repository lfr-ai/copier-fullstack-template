# Frontend analysis summary

## Routing

- Generated projects use React + Vite stack conventions.
- Routing guidance is instruction-driven and prefers explicit router composition.

## Auth flows

- Auth flows are generated conditionally from template feature flags.
- Frontend should rely on API status semantics from backend route contracts.

## Forms

- Preferred form stack is React Hook Form + schema validation conventions.
- Biome + TypeScript rules enforce strongly typed form state.

## State management

- Server state conventions target TanStack Query patterns.
- Local state and component state patterns are controlled by strict lint rules.

## Error UX

- Error and async UX use structured conventions (error boundaries and clear states).
- Frontend linting prevents hidden anti-patterns (`noExplicitAny`).

## i18n

- No dedicated i18n framework wiring is enforced at template root yet.
- Current baseline allows iterative addition by generated project owners.

## Accessibility

- Frontend standards encourage shadcn/ui + accessible primitives.
- Biome rule domains include React/test quality checks.

## Key references

- `template/frontend/biome.json:19`
- `template/frontend/biome.json:22`
- `template/frontend/biome.json:43`
- `template/frontend/biome.json:48`
