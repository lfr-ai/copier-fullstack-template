type PluginContext = {
  project?: unknown;
  client?: unknown;
  $?: unknown;
  directory?: unknown;
  worktree?: unknown;
};

type ToolExecuteBeforeInput = {
  tool?: unknown;
};

type ToolExecuteBeforeOutput = {
  args?: {
    filePath?: unknown;
  };
};

type EnvProtectionHooks = {
  'tool.execute.before': (
    input: ToolExecuteBeforeInput,
    output: ToolExecuteBeforeOutput,
  ) => Promise<void>;
};

type LocalPlugin = (ctx: PluginContext) => Promise<EnvProtectionHooks>;

/**
 * Environment File Protection Plugin
 *
 * Prevents OpenCode from reading .env files that may contain secrets.
 * This is a defense-in-depth measure alongside permission rules.
 */
const ENV_FILE_RE = /^\.env(?:\..+)?$/i;
const ENV_EXAMPLE_FILE_RE = /^\.env(?:\..+)?\.example$/i;

const getFilePathArg = (output: unknown): string | null => {
  const args = (output as { args?: { filePath?: unknown } } | null)?.args;
  return typeof args?.filePath === 'string' && args.filePath.length > 0 ? args.filePath : null;
};

export const EnvProtection: LocalPlugin = async (_ctx: PluginContext) => {
  return {
    'tool.execute.before': async (
      input: ToolExecuteBeforeInput,
      output: ToolExecuteBeforeOutput,
    ) => {
      const tool = input?.tool;
      if (tool !== 'read') {
        return;
      }

      const filePath = getFilePathArg(output);
      if (!filePath) {
        return;
      }

      const fileName = filePath.split(/[\\/]/).pop() ?? '';

      // Block .env* files but allow .env.example and .env.*.example variants.
      if (ENV_FILE_RE.test(fileName) && !ENV_EXAMPLE_FILE_RE.test(fileName)) {
        throw new Error(
          `Blocked: reading ${filePath} — .env files may contain secrets. ` +
            'Use .env.example files instead.',
        );
      }
    },
  };
};
