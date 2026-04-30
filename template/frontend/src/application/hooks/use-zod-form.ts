/**
 * useZodForm — React Hook Form pre-configured with Zod schema validation.
 *
 * Provides a typed `useForm` wrapper with:
 * - Zod schema validation via @hookform/resolvers
 * - Mode defaults to "onBlur" for a11y-friendly validation timing
 * - Full type inference from the Zod schema
 *
 * @example
 * ```tsx
 * const schema = z.object({ email: z.string().email() });
 * const form = useZodForm({ schema, defaultValues: { email: '' } });
 * ```
 */
import type { UseFormProps } from 'react-hook-form';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import type { z } from 'zod';

interface UseZodFormProps<TSchema extends z.ZodType>
  extends Omit<UseFormProps<z.infer<TSchema>>, 'resolver'> {
  readonly schema: TSchema;
}

export function useZodForm<TSchema extends z.ZodType>({
  schema,
  ...formProps
}: UseZodFormProps<TSchema>) {
  return useForm<z.infer<TSchema>>({
    resolver: zodResolver(schema),
    mode: 'onBlur',
    ...formProps,
  });
}
