/**
 * Settings page component.
 *
 * Demonstrates advanced form composition with multiple field types:
 * - Input, Textarea, Select, Checkbox, Radio Group, Switch
 * - React Hook Form Controller + useFieldArray
 * - Zod schema validation
 * - shadcn/ui Field component patterns (latest)
 * - Tabs for section organization
 * - Toast notifications on save
 *
 * @see https://ui.shadcn.com/docs/forms/react-hook-form
 */
import { Controller, useFieldArray } from 'react-hook-form';
import { z } from 'zod';
import { toast } from 'sonner';
import { PlusIcon, TrashIcon } from 'lucide-react';
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
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/presentation/components/ui/tabs';
import { Checkbox } from '@/presentation/components/ui/checkbox';
import { RadioGroup, RadioGroupItem } from '@/presentation/components/ui/radio-group';
import { Switch } from '@/presentation/components/ui/switch';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/presentation/components/ui/select';
import {
  Field,
  FieldContent,
  FieldDescription,
  FieldError,
  FieldGroup,
  FieldLabel,
  FieldLegend,
  FieldSeparator,
  FieldSet,
} from '@/presentation/components/ui/field';

/* ── Schemas ─────────────────────────────────────────────────── */

const _USERNAME_MIN = 3;
const _USERNAME_MAX = 32;
const _BIO_MAX = 200;
const _MAX_EMAILS = 5;

const profileSchema = z.object({
  username: z
    .string()
    .min(_USERNAME_MIN, `Username must be at least ${_USERNAME_MIN} characters.`)
    .max(_USERNAME_MAX, `Username must be at most ${_USERNAME_MAX} characters.`)
    .regex(/^[a-z0-9_]+$/, 'Only lowercase letters, numbers, and underscores.'),
  bio: z
    .string()
    .max(_BIO_MAX, `Bio must be at most ${_BIO_MAX} characters.`)
    .optional()
    .or(z.literal('')),
  language: z.string().min(1, 'Select a language.'),
  emails: z
    .array(
      z.object({
        address: z.string().email('Enter a valid email address.'),
      }),
    )
    .min(1, 'Add at least one email address.')
    .max(_MAX_EMAILS, `You can add up to ${_MAX_EMAILS} email addresses.`),
});

type ProfileFormValues = z.infer<typeof profileSchema>;

const notificationsSchema = z.object({
  plan: z.enum(['starter', 'pro', 'enterprise'], {
    required_error: 'Select a plan.',
  }),
  features: z.array(z.string()).min(1, 'Select at least one feature.'),
  emailNotifications: z.boolean(),
  twoFactor: z.boolean(),
});

type NotificationsFormValues = z.infer<typeof notificationsSchema>;

/* ── Data ────────────────────────────────────────────────────── */

const LANGUAGES = [
  { value: 'en', label: 'English' },
  { value: 'da', label: 'Danish' },
  { value: 'de', label: 'German' },
  { value: 'fr', label: 'French' },
  { value: 'es', label: 'Spanish' },
] as const;

const PLANS = [
  { id: 'starter', title: 'Starter', description: '100K tokens/month. For everyday use.' },
  { id: 'pro', title: 'Pro', description: '1M tokens/month. For advanced usage.' },
  { id: 'enterprise', title: 'Enterprise', description: 'Unlimited tokens. For teams.' },
] as const;

const FEATURES = [
  { id: 'analytics', label: 'Analytics' },
  { id: 'backup', label: 'Automated backups' },
  { id: 'priority', label: 'Priority support' },
] as const;

/* ── Profile Tab ─────────────────────────────────────────────── */

function ProfileForm() {
  const form = useZodForm({
    schema: profileSchema,
    defaultValues: {
      username: '',
      bio: '',
      language: '',
      emails: [{ address: '' }],
    },
  });

  const { fields, append, remove } = useFieldArray({
    control: form.control,
    name: 'emails',
  });

  const onSubmit = (values: ProfileFormValues) => {
    toast.success('Profile saved', {
      description: `Username: ${values.username}, Language: ${values.language}`,
    });
  };

  return (
    <form noValidate onSubmit={form.handleSubmit(onSubmit)}>
      <FieldSet>
        <FieldLegend variant="label">Profile information</FieldLegend>
        <FieldDescription>
          Update your profile information below. Changes will be saved immediately.
        </FieldDescription>
        <FieldGroup>
          <Controller
            name="username"
            control={form.control}
            render={({ field, fieldState }) => (
              <Field data-invalid={fieldState.invalid || undefined}>
                <FieldLabel htmlFor={field.name}>Username</FieldLabel>
                <Input
                  {...field}
                  id={field.name}
                  autoComplete="username"
                  placeholder="ada_lovelace"
                  aria-invalid={fieldState.invalid}
                />
                <FieldDescription>
                  Lowercase letters, numbers, and underscores only.
                </FieldDescription>
                {fieldState.invalid && <FieldError errors={[fieldState.error]} />}
              </Field>
            )}
          />

          <Controller
            name="bio"
            control={form.control}
            render={({ field, fieldState }) => (
              <Field data-invalid={fieldState.invalid || undefined}>
                <FieldLabel htmlFor={field.name}>Bio</FieldLabel>
                <Textarea
                  {...field}
                  id={field.name}
                  placeholder="Tell us about yourself..."
                  className="min-h-[100px]"
                  aria-invalid={fieldState.invalid}
                />
                <FieldDescription>
                  {field.value?.length ?? 0}/{_BIO_MAX} characters
                </FieldDescription>
                {fieldState.invalid && <FieldError errors={[fieldState.error]} />}
              </Field>
            )}
          />

          <Controller
            name="language"
            control={form.control}
            render={({ field, fieldState }) => (
              <Field data-invalid={fieldState.invalid || undefined}>
                <FieldLabel htmlFor="settings-language">Preferred language</FieldLabel>
                <Select
                  name={field.name}
                  value={field.value}
                  onValueChange={field.onChange}
                >
                  <SelectTrigger
                    id="settings-language"
                    aria-invalid={fieldState.invalid}
                    className="min-w-[180px]"
                  >
                    <SelectValue placeholder="Select language" />
                  </SelectTrigger>
                  <SelectContent>
                    {LANGUAGES.map((lang) => (
                      <SelectItem key={lang.value} value={lang.value}>
                        {lang.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                <FieldDescription>
                  Used for UI localization and email communication.
                </FieldDescription>
                {fieldState.invalid && <FieldError errors={[fieldState.error]} />}
              </Field>
            )}
          />

          <FieldSeparator />

          <FieldSet>
            <FieldLegend variant="label">Email addresses</FieldLegend>
            <FieldDescription>
              Add up to {_MAX_EMAILS} email addresses where we can contact you.
            </FieldDescription>
            <FieldGroup className="gap-4">
              {fields.map((item, index) => (
                <Controller
                  key={item.id}
                  name={`emails.${index}.address`}
                  control={form.control}
                  render={({ field: controllerField, fieldState }) => (
                    <Field
                      orientation="horizontal"
                      data-invalid={fieldState.invalid || undefined}
                    >
                      <FieldContent>
                        <div className="flex items-center gap-2">
                          <Input
                            {...controllerField}
                            id={`settings-email-${index}`}
                            type="email"
                            autoComplete="email"
                            placeholder="name@example.com"
                            aria-invalid={fieldState.invalid}
                          />
                          {fields.length > 1 && (
                            <Button
                              type="button"
                              variant="ghost"
                              size="icon"
                              onClick={() => remove(index)}
                              aria-label={`Remove email ${index + 1}`}
                            >
                              <TrashIcon className="size-4" />
                            </Button>
                          )}
                        </div>
                        {fieldState.invalid && (
                          <FieldError errors={[fieldState.error]} />
                        )}
                      </FieldContent>
                    </Field>
                  )}
                />
              ))}
              <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={() => append({ address: '' })}
                disabled={fields.length >= _MAX_EMAILS}
              >
                <PlusIcon className="mr-1 size-4" />
                Add email address
              </Button>
            </FieldGroup>
          </FieldSet>
        </FieldGroup>
      </FieldSet>

      <div className="flex gap-3 pt-6">
        <Button type="submit" disabled={form.formState.isSubmitting}>
          Save profile
        </Button>
        <Button type="button" variant="outline" onClick={() => form.reset()}>
          Reset
        </Button>
      </div>
    </form>
  );
}

/* ── Notifications Tab ───────────────────────────────────────── */

function NotificationsForm() {
  const form = useZodForm({
    schema: notificationsSchema,
    defaultValues: {
      plan: undefined,
      features: [],
      emailNotifications: true,
      twoFactor: false,
    },
  });

  const onSubmit = (values: NotificationsFormValues) => {
    toast.success('Preferences saved', {
      description: `Plan: ${values.plan}, Features: ${values.features.join(', ')}`,
    });
  };

  return (
    <form noValidate onSubmit={form.handleSubmit(onSubmit)}>
      <FieldSet>
        <FieldLegend variant="label">Subscription plan</FieldLegend>
        <FieldDescription>Choose the plan that fits your needs.</FieldDescription>

        <Controller
          name="plan"
          control={form.control}
          render={({ field, fieldState }) => (
            <RadioGroup
              name={field.name}
              value={field.value}
              onValueChange={field.onChange}
              className="gap-4"
            >
              {PLANS.map((plan) => (
                <FieldLabel key={plan.id} htmlFor={`settings-plan-${plan.id}`}>
                  <Field orientation="horizontal" data-invalid={fieldState.invalid || undefined}>
                    <RadioGroupItem
                      value={plan.id}
                      id={`settings-plan-${plan.id}`}
                      aria-invalid={fieldState.invalid}
                    />
                    <FieldContent>
                      <span className="text-sm font-medium">{plan.title}</span>
                      <FieldDescription>{plan.description}</FieldDescription>
                    </FieldContent>
                  </Field>
                </FieldLabel>
              ))}
              {fieldState.invalid && <FieldError errors={[fieldState.error]} />}
            </RadioGroup>
          )}
        />
      </FieldSet>

      <FieldSeparator className="my-6" />

      <FieldSet>
        <FieldLegend variant="label">Add-ons</FieldLegend>
        <FieldDescription>
          Select additional features for your subscription.
        </FieldDescription>

        <Controller
          name="features"
          control={form.control}
          render={({ field, fieldState }) => (
            <FieldGroup data-slot="checkbox-group" className="gap-3">
              {FEATURES.map((feature) => (
                <Field
                  key={feature.id}
                  orientation="horizontal"
                  data-invalid={fieldState.invalid || undefined}
                >
                  <Checkbox
                    id={`settings-feature-${feature.id}`}
                    name={field.name}
                    checked={field.value.includes(feature.id)}
                    onCheckedChange={(checked) => {
                      const values = checked
                        ? [...field.value, feature.id]
                        : field.value.filter((v) => v !== feature.id);
                      field.onChange(values);
                    }}
                    aria-invalid={fieldState.invalid}
                  />
                  <FieldLabel
                    htmlFor={`settings-feature-${feature.id}`}
                    className="font-normal"
                  >
                    {feature.label}
                  </FieldLabel>
                </Field>
              ))}
              {fieldState.invalid && <FieldError errors={[fieldState.error]} />}
            </FieldGroup>
          )}
        />
      </FieldSet>

      <FieldSeparator className="my-6" />

      <FieldGroup>
        <Controller
          name="emailNotifications"
          control={form.control}
          render={({ field }) => (
            <Field orientation="horizontal">
              <FieldContent>
                <FieldLabel htmlFor="settings-email-notifications">
                  Email notifications
                </FieldLabel>
                <FieldDescription>
                  Receive email updates about your subscription and usage.
                </FieldDescription>
              </FieldContent>
              <Switch
                id="settings-email-notifications"
                name={field.name}
                checked={field.value}
                onCheckedChange={field.onChange}
              />
            </Field>
          )}
        />

        <Controller
          name="twoFactor"
          control={form.control}
          render={({ field }) => (
            <Field orientation="horizontal">
              <FieldContent>
                <FieldLabel htmlFor="settings-two-factor">
                  Two-factor authentication
                </FieldLabel>
                <FieldDescription>
                  Add an extra layer of security to your account.
                </FieldDescription>
              </FieldContent>
              <Switch
                id="settings-two-factor"
                name={field.name}
                checked={field.value}
                onCheckedChange={field.onChange}
              />
            </Field>
          )}
        />
      </FieldGroup>

      <div className="flex gap-3 pt-6">
        <Button type="submit" disabled={form.formState.isSubmitting}>
          Save preferences
        </Button>
        <Button type="button" variant="outline" onClick={() => form.reset()}>
          Reset
        </Button>
      </div>
    </form>
  );
}

/* ── Settings Page ───────────────────────────────────────────── */

export function Settings() {
  return (
    <section className="mx-auto flex w-full max-w-3xl flex-col gap-6 p-8">
      <div className="flex items-center justify-between gap-3">
        <h1 className="text-3xl font-bold tracking-tight">Settings</h1>
        <Badge variant="secondary">Advanced Forms</Badge>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Account settings</CardTitle>
          <CardDescription>
            Manage your profile, subscription plan, and notification preferences.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="profile">
            <TabsList>
              <TabsTrigger value="profile">Profile</TabsTrigger>
              <TabsTrigger value="notifications">Notifications</TabsTrigger>
            </TabsList>
            <TabsContent value="profile">
              <ProfileForm />
            </TabsContent>
            <TabsContent value="notifications">
              <NotificationsForm />
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </section>
  );
}
