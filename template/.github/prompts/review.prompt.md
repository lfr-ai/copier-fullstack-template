---
description: 'Perform comprehensive code review with security, performance, and architecture analysis'
name: 'review'
argument-hint: 'File path or description of changes to review'
agent: 'ask'
model: 'Claude Sonnet 4'
tools:
  [
    search/codebase,
    search/fileSearch,
    search/textSearch,
    search/usages,
    search/changes,
    read/readFile,
    read/problems,
  ]
---

# Code Review

Perform a comprehensive code review on the specified files or recent changes.

## Review Checklist

### Architecture
- [ ] Follows Clean Architecture dependency rule
- [ ] No circular imports between layers
- [ ] Appropriate layer placement

### Code Quality
- [ ] Type annotations on all public functions
- [ ] Keyword-only arguments used appropriately
- [ ] No `Final[...]` (use `@final` decorator or `UPPER_CASE` convention)
- [ ] Structured logging (no `print()` statements)
- [ ] Descriptive naming (no abbreviations)

### Security
- [ ] No SQL injection vulnerabilities
- [ ] No XSS attack vectors
- [ ] Input validation at system boundaries
- [ ] No hardcoded secrets or credentials
- [ ] Proper error handling (no stack traces leaked)

### Performance
- [ ] N+1 query patterns avoided
- [ ] Appropriate use of async/await
- [ ] No blocking I/O in async contexts
- [ ] Indexes on frequently queried columns

### Testing
- [ ] Unit tests cover new behavior
- [ ] Edge cases and error paths tested
- [ ] Factories used (not raw fixtures)
- [ ] Test names follow `test_<action>_<condition>_<result>` pattern

## Output Format

Report findings grouped by severity:
1. **Critical** — Must fix before merge
2. **Important** — Should fix before merge
3. **Minor** — Nice to have
4. **Positive** — Good patterns to highlight
