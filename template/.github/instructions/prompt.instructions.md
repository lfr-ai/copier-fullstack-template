---
description: Guidelines for creating high-quality prompt files for GitHub Copilot
applyTo: '**/*.prompt.md'
---

# Copilot Prompt Files

## Scope and Principles

- Target audience: maintainers and contributors authoring reusable prompts for Copilot Chat.
- Goals: predictable behavior, clear expectations, minimal permissions, and portability across repos.
- Primary references: VS Code documentation on prompt files and organization-specific conventions.

## Frontmatter Requirements

Every prompt file should include YAML frontmatter:

| Field | Required | Description |
|-------|----------|-------------|
| `description` | Recommended | Short description (single sentence, actionable outcome) |
| `name` | Optional | Name shown after typing `/` in chat. Defaults to filename |
| `agent` | Recommended | Agent to use: `ask`, `edit`, `agent`, or a custom agent name |
| `model` | Optional | Language model to use. Defaults to current model |
| `tools` | Optional | List of tool/tool set names available for this prompt |
| `argument-hint` | Optional | Hint text shown in chat input to guide user interaction |

- Use consistent quoting (single quotes recommended) and one field per line
- If `tools` are specified and the current agent is `ask` or `edit`, the default agent becomes `agent`

## File Naming and Placement

- Use kebab-case filenames ending with `.prompt.md`
- Store under `.github/prompts/` unless workspace standard specifies another directory
- Filename should communicate the action (e.g., `generate-readme.prompt.md`)

## Body Structure

- Start with an `#` heading matching the prompt intent
- Recommended sections: Mission, Scope & Preconditions, Inputs, Workflow, Output Expectations, Quality Assurance
- Adjust section names to fit domain but retain flow: why -> context -> inputs -> actions -> outputs -> validation

## Input and Context Handling

- Use `${input:variableName[:placeholder]}` for required values
- Call out `${selection}`, `${file}`, `${workspaceFolder}` only when essential
- Document how to proceed when mandatory context is missing

## Tool and Permission Guidance

- Limit `tools` to the smallest set enabling the task
- List tools in preferred execution order when sequence matters
- Warn about destructive operations and include guard rails

## Instruction Tone and Style

- Write in direct, imperative sentences targeted at Copilot
- Keep sentences short and unambiguous
- Avoid idioms, humor, or culturally specific references

## Output Definition

- Specify format, structure, and location of expected results
- Include success criteria and failure triggers
- Provide validation steps reviewers can execute after running the prompt

## Quality Assurance Checklist

- [ ] Frontmatter fields are complete, accurate, and least-privilege
- [ ] Inputs include placeholders, default behaviors, and fallbacks
- [ ] Workflow covers preparation, execution, and post-processing
- [ ] Output expectations include formatting and storage details
- [ ] Validation steps are actionable
- [ ] Security, compliance, and privacy policies are current
- [ ] Prompt executes successfully in VS Code using representative scenarios

## Maintenance

- Version-control prompts alongside the code they affect
- Review prompts periodically to ensure tool lists, model requirements, and linked docs remain valid
- Extract broadly useful guidance into instruction files or shared prompt packs
