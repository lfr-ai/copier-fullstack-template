

We use a **trunk-based development** workflow with short-lived feature branches.


- `feat/<description>` — new features
- `fix/<description>` — bug fixes
- `refactor/<description>` — code restructuring
- `docs/<description>` — documentation changes
- `test/<description>` — test additions/changes
- `chore/<description>` — maintenance tasks


1. Create a feature branch from `main`
2. Make small, focused commits
3. Open a Pull Request
4. Pass all CI checks
5. Get code review approval
6. Squash-merge to `main`

---


Follow [Conventional Commits](https://www.conventionalcommits.org/):

```text
type(scope): description
```

Enforced by `commitizen` pre-commit hook.

---


- Keep PRs small and focused (ideally < 400 lines changed)
- Include tests for all new functionality
- Update documentation when behavior changes
- All CI checks must pass
- At least one approval required

---


See [docs/RELEASE.md](../RELEASE.md) for the full release process.
