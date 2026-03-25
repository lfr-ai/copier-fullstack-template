---
description: Generate a CHANGELOG entry for recent changes
subtask: true
---

Generate a CHANGELOG entry based on recent changes:

$ARGUMENTS

Steps:

1. Review recent git commits: `!git log --oneline -20`
2. Categorize changes into: Added, Changed, Fixed, Removed, Security, Deprecated
3. Write entries following Keep a Changelog format
4. Reference issue/PR numbers where available

Output format:

```markdown
## [Unreleased]

### Added

- Description of new feature (#issue)

### Changed

- Description of change (#issue)

### Fixed

- Description of bugfix (#issue)
```

If no arguments are provided, analyze the diff between HEAD and the last tag.
