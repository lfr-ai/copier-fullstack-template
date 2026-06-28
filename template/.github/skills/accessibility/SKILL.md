---
name: accessibility
description: WCAG 2.1 AA compliance and inclusive UI patterns
applyTo: "src/presentation/**/*.{ts,tsx}"
---

# Accessibility Skill (WCAG 2.1 AA)

## Purpose

Ensure all UI components meet WCAG 2.1 Level AA standards for users with
disabilities, including screen reader users, keyboard-only users, and users
with visual impairments.

## Core Principles (POUR)

| Principle | Meaning | Examples |
|-----------|---------|----------|
| **Perceivable** | Content is perceivable by all senses | Alt text, contrast, captions |
| **Operable** | UI is operable by all input methods | Keyboard nav, no time limits |
| **Understandable** | Content is understandable | Clear language, predictable UI |
| **Robust** | Works with assistive technologies | Semantic HTML, ARIA |

## Checklist

- [ ] All images have alt text (or `alt=""` for decorative)
- [ ] All form inputs have visible labels
- [ ] Error messages are announced to screen readers
- [ ] Focus order is logical
- [ ] Color contrast meets AA ratios
- [ ] Interactive elements have accessible names
- [ ] Loading states are announced
- [ ] Modal dialogs manage focus correctly
- [ ] Page has proper heading hierarchy (h1 → h2 → h3)
- [ ] Language attribute set on `<html>` element
