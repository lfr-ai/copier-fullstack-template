---
name: shadcn-ui
description: shadcn/ui component conventions and composition patterns
applyTo: "src/presentation/**/*.{ts,tsx}"
---

# shadcn/ui Conventions

## Purpose

Enforce consistent usage of shadcn/ui components following the new-york style
variant with Tailwind CSS v4 and Radix UI primitives.

## Adding Components

```bash
task ui:add -- button card dialog
```

## Style Rules

- No inline styles; use Tailwind utility classes.
- Compose class names with `cn()` helpers.
- Prefer Radix-backed primitives for accessibility.
- Ensure icon-only controls expose accessible names.

## Configuration

`components.json` defines style variant, css path, aliases, and icon library.
