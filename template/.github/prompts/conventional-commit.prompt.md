---
description: Prompt and workflow for generating conventional commit messages
tools: ['run_in_terminal', 'get_terminal_output']
---


Follow the Conventional Commits specification to create standardized, descriptive commit messages.


1. Run `git status` to review changed files.
2. Run `git diff --cached` to inspect staged changes.
3. Construct the commit message using the structure below.
4. Execute the commit command in the terminal.


```
type(scope): description

[optional body]

[optional footer(s)]
```


| Type | Description |
|---|---|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, missing semicolons, etc. |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `perf` | Performance improvement |
| `test` | Adding missing or correcting existing tests |
| `build` | Changes to build system or dependencies |
| `ci` | CI configuration changes |
| `chore` | Other changes that don't modify src or test files |
| `revert` | Reverts a previous commit |


```
feat(parser): add ability to parse arrays
fix(ui): correct button alignment
docs: update README with usage instructions
refactor: improve performance of data processing
chore: update dependencies
feat!: send email on registration (BREAKING CHANGE: email service required)
```


- **type**: Must be one of the allowed types
- **scope**: Optional but recommended for clarity
- **description**: Required, use imperative mood ("add", not "added")
- **body**: Optional, use for additional context
- **footer**: Use for breaking changes or issue references


```bash
git commit -m "type(scope): description"
```
