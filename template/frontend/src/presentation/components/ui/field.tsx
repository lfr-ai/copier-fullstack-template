/**
 * Field component for composing accessible form fields.
 *
 * Provides label, description, error, and grouping primitives
 * designed for use with React Hook Form and Zod validation.
 *
 * @see https://ui.shadcn.com/docs/components/field
 */
import * as React from 'react';

import { cn } from '@/lib/utils';

/* ── FieldSet ──────────────────────────────────────────────── */

function FieldSet({
  className,
  ...props
}: React.ComponentProps<'fieldset'>) {
  return (
    <fieldset
      data-slot="field-set"
      className={cn('space-y-4', className)}
      {...props}
    />
  );
}

/* ── FieldLegend ───────────────────────────────────────────── */

function FieldLegend({
  className,
  variant = 'legend',
  ...props
}: React.ComponentProps<'legend'> & {
  readonly variant?: 'legend' | 'label';
}) {
  return (
    <legend
      data-slot="field-legend"
      className={cn(
        variant === 'label'
          ? 'text-sm font-medium leading-none'
          : 'text-base font-semibold leading-none',
        className,
      )}
      {...props}
    />
  );
}

/* ── FieldGroup ────────────────────────────────────────────── */

function FieldGroup({
  className,
  ...props
}: React.ComponentProps<'div'>) {
  return (
    <div
      data-slot="field-group"
      className={cn('flex flex-col gap-6', className)}
      {...props}
    />
  );
}

/* ── Field ─────────────────────────────────────────────────── */

function Field({
  className,
  orientation = 'vertical',
  ...props
}: React.ComponentProps<'div'> & {
  readonly orientation?: 'vertical' | 'horizontal' | 'responsive';
}) {
  return (
    <div
      data-slot="field"
      role="group"
      className={cn(
        'group space-y-2',
        orientation === 'horizontal' &&
          'flex items-center gap-3 space-y-0',
        orientation === 'responsive' &&
          'flex flex-col gap-2 @sm/field-group:flex-row @sm/field-group:items-center @sm/field-group:gap-3 @sm/field-group:space-y-0',
        'data-[invalid]:text-destructive',
        className,
      )}
      {...props}
    />
  );
}

/* ── FieldContent ──────────────────────────────────────────── */

function FieldContent({
  className,
  ...props
}: React.ComponentProps<'div'>) {
  return (
    <div
      data-slot="field-content"
      className={cn('flex flex-col gap-1', className)}
      {...props}
    />
  );
}

/* ── FieldLabel ────────────────────────────────────────────── */

function FieldLabel({
  className,
  ...props
}: React.ComponentProps<'label'>) {
  return (
    <label
      data-slot="field-label"
      className={cn(
        'text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 group-data-[invalid]:text-destructive',
        className,
      )}
      {...props}
    />
  );
}

/* ── FieldTitle ────────────────────────────────────────────── */

function FieldTitle({
  className,
  ...props
}: React.ComponentProps<'p'>) {
  return (
    <p
      data-slot="field-title"
      className={cn('text-sm font-medium leading-none', className)}
      {...props}
    />
  );
}

/* ── FieldDescription ──────────────────────────────────────── */

function FieldDescription({
  className,
  ...props
}: React.ComponentProps<'p'>) {
  return (
    <p
      data-slot="field-description"
      className={cn('text-sm text-muted-foreground text-pretty', className)}
      {...props}
    />
  );
}

/* ── FieldSeparator ────────────────────────────────────────── */

function FieldSeparator({
  className,
  ...props
}: React.ComponentProps<'div'>) {
  return (
    <div
      data-slot="field-separator"
      role="separator"
      className={cn('border-t', className)}
      {...props}
    />
  );
}

/* ── FieldError ────────────────────────────────────────────── */

function FieldError({
  className,
  errors,
  children,
  ...props
}: React.ComponentProps<'p'> & {
  readonly errors?: ReadonlyArray<{ message?: string } | undefined>;
}) {
  const messages = errors
    ?.map((e) => e?.message)
    .filter((m): m is string => Boolean(m));

  if (!messages?.length && !children) return null;

  if (messages && messages.length > 1) {
    return (
      <ul
        data-slot="field-error"
        className={cn('text-sm font-medium text-destructive', className)}
        role="alert"
        {...props}
      >
        {messages.map((msg) => (
          <li key={msg}>{msg}</li>
        ))}
      </ul>
    );
  }

  return (
    <p
      data-slot="field-error"
      className={cn('text-sm font-medium text-destructive', className)}
      role="alert"
      {...props}
    >
      {messages?.[0] ?? children}
    </p>
  );
}

export {
  Field,
  FieldContent,
  FieldDescription,
  FieldError,
  FieldGroup,
  FieldLabel,
  FieldLegend,
  FieldSeparator,
  FieldSet,
  FieldTitle,
};
