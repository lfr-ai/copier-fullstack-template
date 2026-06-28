---
name: playwright
description: End-to-end testing with Playwright for user journeys and accessibility
applyTo: "tests/e2e/**/*.{ts,tsx}"
---

# Playwright E2E Testing Skill

## Purpose

Write and maintain end-to-end tests that verify critical user journeys,
accessibility compliance, and cross-browser behavior using Playwright.

## Locator Priority

1. `page.getByRole()` — semantic role + accessible name
2. `page.getByLabel()` — form controls by label
3. `page.getByText()` — visible text content
4. `page.getByPlaceholder()` — input placeholders
5. `page.getByTestId()` — last resort

## Running Tests

```bash
task test:e2e
task test:e2e:headed
task test:e2e:install
```
