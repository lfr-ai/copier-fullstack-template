/**
 * Forms page component.
 *
 * Demonstrates production-ready form composition with:
 * - React Hook Form Controller API
 * - Zod schema validation
 * - shadcn/ui Field component (latest pattern)
 * - Accessible error handling and validation
 *
 * @see https://ui.shadcn.com/docs/forms/react-hook-form
 */
import { useState } from 'react';
import { Controller } from 'react-hook-form';
import { z } from 'zod';
import { useZodForm } from '@/application/hooks/use-zod-form';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/presentation/components/ui/card';
import { Button } from '@/presentation/components/ui/button';
import { Input } from '@/presentation/components/ui/input';
import { Textarea } from '@/presentation/components/ui/textarea';
import { Badge } from '@/presentation/components/ui/badge';
import {
  Field,
  FieldDescription,
  FieldError,
  FieldGroup,
  FieldLabel,
  FieldSet,
  FieldLegend,
} from '@/presentation/components/ui/field';

const contactSchema = z.object({
  name: z
    .string()
    .min(2, 'Name must be at least 2 characters.')
    .max(64, 'Name must be at most 64 characters.'),
  email: z.string().email('Enter a valid email address.'),
  message: z
    .string()
    .min(10, 'Message must be at least 10 characters.')
    .max(500, 'Message must be at most 500 characters.'),
});

type ContactFormValues = z.infer<typeof contactSchema>;

export function Forms() {
  const [submitted, setSubmitted] = useState<ContactFormValues | null>(null);

  const form = useZodForm({
    schema: contactSchema,
    defaultValues: {
      name: '',
      email: '',
      message: '',
    },
    mode: 'onBlur',
    reValidateMode: 'onChange',
  });

  const onSubmit = (values: ContactFormValues) => {
    setSubmitted(values);
  };

  return (
    <section className="mx-auto flex w-full max-w-3xl flex-col gap-6 p-8">
      <div className="flex items-center justify-between gap-3">
        <h1 className="text-3xl font-bold tracking-tight">Forms</h1>
        <Badge variant="secondary">React Hook Form + Zod</Badge>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Contact form</CardTitle>
          <CardDescription>
            Example form scaffolded with shadcn/ui Field components and typed validation.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form className="space-y-1" noValidate onSubmit={form.handleSubmit(onSubmit)}>
            <FieldSet>
              <FieldLegend variant="label">Contact details</FieldLegend>
              <FieldDescription>
                Fill in the form below to send us a message. All fields are required.
              </FieldDescription>
              <FieldGroup>
                <Controller
                  name="name"
                  control={form.control}
                  render={({ field, fieldState }) => (
                    <Field data-invalid={fieldState.invalid || undefined}>
                      <FieldLabel htmlFor={field.name}>Name</FieldLabel>
                      <Input
                        {...field}
                        id={field.name}
                        autoComplete="name"
                        placeholder="Ada Lovelace"
                        aria-invalid={fieldState.invalid}
                      />
                      <FieldDescription>Your full name as you would like to be addressed.</FieldDescription>
                      {fieldState.invalid && <FieldError errors={[fieldState.error]} />}
                    </Field>
                  )}
                />

                <Controller
                  name="email"
                  control={form.control}
                  render={({ field, fieldState }) => (
                    <Field data-invalid={fieldState.invalid || undefined}>
                      <FieldLabel htmlFor={field.name}>Email</FieldLabel>
                      <Input
                        {...field}
                        id={field.name}
                        type="email"
                        autoComplete="email"
                        placeholder="ada@example.com"
                        aria-invalid={fieldState.invalid}
                      />
                      <FieldDescription>We will only use this to respond to your inquiry.</FieldDescription>
                      {fieldState.invalid && <FieldError errors={[fieldState.error]} />}
                    </Field>
                  )}
                />

                <Controller
                  name="message"
                  control={form.control}
                  render={({ field, fieldState }) => (
                    <Field data-invalid={fieldState.invalid || undefined}>
                      <FieldLabel htmlFor={field.name}>Message</FieldLabel>
                      <Textarea
                        {...field}
                        id={field.name}
                        placeholder="Tell us what you need..."
                        className="min-h-[120px]"
                        aria-invalid={fieldState.invalid}
                      />
                      <FieldDescription>
                        Between 10 and 500 characters. Include steps to reproduce if reporting an issue.
                      </FieldDescription>
                      {fieldState.invalid && <FieldError errors={[fieldState.error]} />}
                    </Field>
                  )}
                />
              </FieldGroup>
            </FieldSet>

            <div className="flex gap-3 pt-4">
              <Button type="submit" disabled={form.formState.isSubmitting}>
                Submit
              </Button>
              <Button type="button" variant="outline" onClick={() => form.reset()}>
                Reset
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>

      {submitted && (
        <Card>
          <CardHeader>
            <CardTitle>Submitted payload</CardTitle>
            <CardDescription>
              This preview demonstrates validated values returned by React Hook Form.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <pre className="overflow-x-auto rounded-md bg-muted p-4 text-sm">
              {JSON.stringify(submitted, null, 2)}
            </pre>
          </CardContent>
        </Card>
      )}
    </section>
  );
}
