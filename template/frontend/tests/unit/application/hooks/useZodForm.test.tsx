import { act, renderHook } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { z } from 'zod';
import { useZodForm } from '../../../../src/application/hooks/use-zod-form';

describe('useZodForm', () => {
  it('applies zod validation through resolver', async () => {
    const schema = z.object({
      name: z.string().min(2, 'Name is too short'),
    });

    const { result } = renderHook(() =>
      useZodForm({
        schema,
        defaultValues: {
          name: '',
        },
      }),
    );

    await act(async () => {
      await result.current.trigger('name');
    });

    expect(result.current.formState.errors.name?.message).toBe('Name is too short');
  });
});
