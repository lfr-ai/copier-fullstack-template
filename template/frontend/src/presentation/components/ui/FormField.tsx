/**
 * FormField — reusable form field component with React Hook Form + React Aria.
 *
 * Provides accessible label, input, description, and error message.
 * Integrates with React Hook Form's register API.
 */
import type { InputHTMLAttributes } from 'react';
import type { FieldError, UseFormRegisterReturn } from 'react-hook-form';

interface FormFieldProps extends Omit<InputHTMLAttributes<HTMLInputElement>, 'name'> {
  readonly label: string;
  readonly registration: UseFormRegisterReturn;
  readonly error?: FieldError;
  readonly description?: string;
}

export function FormField({
  label,
  registration,
  error,
  description,
  id,
  ...inputProps
}: FormFieldProps) {
  const fieldId = id ?? registration.name;
  const errorId = `${fieldId}-error`;
  const descriptionId = `${fieldId}-description`;

  return (
    <div className="flex flex-col gap-1.5">
      <label htmlFor={fieldId} className="text-sm font-medium text-gray-700 dark:text-gray-300">
        {label}
      </label>
      <input
        id={fieldId}
        aria-invalid={error ? 'true' : undefined}
        aria-describedby={
          [error ? errorId : undefined, description ? descriptionId : undefined]
            .filter(Boolean)
            .join(' ') || undefined
        }
        className={[
          'rounded-lg border px-3 py-2 text-sm shadow-sm transition-colors',
          'focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-1',
          'dark:bg-gray-900 dark:text-gray-100',
          error
            ? 'border-red-500 focus:ring-red-500'
            : 'border-gray-300 dark:border-gray-600',
        ].join(' ')}
        {...registration}
        {...inputProps}
      />
      {description && !error && (
        <p id={descriptionId} className="text-xs text-gray-500 dark:text-gray-400">
          {description}
        </p>
      )}
      {error?.message && (
        <p id={errorId} role="alert" className="text-xs text-red-600 dark:text-red-400">
          {error.message}
        </p>
      )}
    </div>
  );
}
