# Ponytail Audit — copier-fullstack-template

Comprehensive over-engineering audit. Ranked by lines/complexity removed.

## Findings

### Critical — Unconditional AI scaffolding (YAGNI)

| Tag | Finding | Replacement | Path |
|-----|---------|-------------|------|
| `yagni:` | 18 AI interface files always generated regardless of `use_ai` flag | Make conditional (`.py.jinja` with `{% if use_ai %}`) | `core/interfaces/{chain,crewai,agent_*,mcp_*,tool,prompt_template,evaluator,guardrail,knowledge_graph,observability,workflow_engine,llm,embedding,retriever,reranker,vector_store}.py` |
| `yagni:` | MCP entities always generated | Conditional on `use_mcp` | `core/entities/mcp.py` |
| `yagni:` | `__init__.py` barrel re-exports 7 interfaces unconditionally | Make AI-only exports conditional | `core/interfaces/__init__.py` |

### High — Empty/speculative structure

| Tag | Finding | Replacement | Path |
|-----|---------|-------------|------|
| `delete:` | 4 empty template subdirs | Nothing — empty dirs are noise | `frontend/src/presentation/templates/{components,layouts,pages,partials}/` |
| `delete:` | 2 empty component subdirs | Nothing | `frontend/src/presentation/components/{common,layout}/` |
| `yagni:` | Full Specification pattern with And/Or/Not combinators | Keep `base.py` only if specs exist; otherwise delete dir | `core/specifications/base.py` |
| `yagni:` | `core/types.py` — single `UserId = NewType(...)` line | Inline where used or put in `constants.py` | `core/types.py` |

### Medium — Over-abstraction

| Tag | Finding | Replacement | Path |
|-----|---------|-------------|------|
| `done:` | Removed CQRS `CommandHandler` ABC | Handlers are plain classes with `async def handle()` | `application/commands/base.py.jinja` (deleted) |
| `done:` | Removed CQRS `QueryHandler` ABC | Handlers are plain classes with `async def handle()` | `application/queries/base.py` (deleted) |
| `done:` | Removed `BaseService` (2 fields, no logic) | Inlined `self._uow` and service logger state | `application/services/base.py.jinja` (deleted) |
| `shrink:` | `utils/crypto_utils.py` — 2 one-liner stdlib wrappers | Inline `secrets.token_urlsafe()` / `hashlib.sha256()` at call site | `utils/crypto_utils.py` |
| `shrink:` | `utils/file_utils.py` — 3 trivial stdlib wrappers | Inline where used | `utils/file_utils.py` |
| `shrink:` | `utils/json_utils.py` — `AppJSONEncoder` wrapping stdlib json | Use Pydantic's JSON serialization (already a dep) | `utils/json_utils.py` |
| `native:` | `infrastructure/profiling/` — 3 files of dev tooling baked into template | Move to conditional or `tools/` dir | `infrastructure/profiling/` |

### Low — Config/docs bloat

| Tag | Finding | Replacement | Path |
|-----|---------|-------------|------|
| `delete:` | README.md in 5+ internal backend dirs | Remove from generated output (dev context belongs in instructions) | `core/README.md`, `application/README.md`, etc. |
| `shrink:` | `.github/instructions/` (16) + `.claude/rules/` (20) heavy overlap | Consolidate into single source of truth | Root config |
| `shrink:` | `.github/skills/` (16) + `.claude/skills/` (14) duplication | Single skill definition, symlink or generate the other | Skills dirs |
| `delete:` | `frontend/src/lib/utils.ts` `sleep()` function | Nothing — YAGNI in production frontend | `frontend/src/lib/utils.ts` |
| `yagni:` | `core/enums/` with 7 separate files | Consolidate into 1-2 files | `core/enums/` |

## Net estimate

`net: ~40 files made conditional, 6 empty dirs removed, 7 dead files deleted, 1 Jinja bug fixed.`
`Minimal render (use_ai=false, use_auth=false) now generates ~60% fewer domain files.`

## Implementation Plan (priority order)

### Phase 1 — Make AI interfaces conditional ✅ DONE
1. ✅ Renamed 18 `.py` → conditional with `{% if use_ai/rag/agents/mcp/crewai/kg %}` guards
2. ✅ Made `core/entities/mcp.py` conditional on `use_mcp`
3. ✅ Fixed `core/interfaces/__init__.py` to conditionally export
4. ✅ Made entities conditional: user, conversation, embedding, document, retrieval, workflow, knowledge_graph
5. ✅ Made value objects conditional: model_config, embedding_config, chunk_metadata, retrieval_config, email
6. ✅ Made application services, DTOs, mappers conditional
7. ✅ Made API routes conditional: users, agents, workflows, ai, conversations, documents, knowledge_graph
8. ✅ Made infrastructure persistence user files conditional
9. ✅ Made core domain_services, events, specifications conditional on use_auth
10. ✅ Fixed router.py.jinja to conditionally import/register routes
11. ✅ Fixed container.py.jinja to conditionally import/use UserService
12. ✅ Made user tests conditional on use_auth

### Phase 2 — Delete empty/speculative structure ✅ DONE
1. ✅ Removed empty frontend dirs (templates/*, common/, layout/)
2. ✅ Removed 6 internal README.md files from backend dirs
3. ✅ Removed `sleep()` from frontend utils

### Phase 3 — Simplify over-abstractions ✅ DONE
1. ✅ Merged `core/types.py` (`UserId` NewType) into `core/constants.py`
2. ✅ Made AI enums conditional
3. ✅ Removed CQRS base abstractions (`application/commands/base.py.jinja`,
	`application/queries/base.py`) and simplified handlers to plain classes
4. ✅ Removed service base abstraction (`application/services/base.py.jinja`)
	and deleted obsolete abstraction-only unit tests

### Phase 4 — Bug fixes (discovered during audit) ✅ DONE
1. ✅ Fixed Jinja syntax error in `litellm_router.py.jinja` (`${%s}` → `{% raw %}...{% endraw %}`)

### Phase 5 — Config alignment — INTENTIONAL DUPLICATION
- `.github/instructions/` and `.claude/rules/` serve different tools (Copilot vs Claude Code)
- Consolidating would break tool compatibility — accepted as necessary duplication

### Phase 6 — Utils wrapper deletion pass ✅ DONE
1. ✅ Deleted unused stdlib-wrapper modules from backend template:
	- `utils/crypto_utils.py`
	- `utils/file_utils.py`
	- `utils/json_utils.py`
2. ✅ Verified no in-template references remained before deletion.
3. ✅ Re-ran `task verify-all` successfully after deletion.

### Phase 7 — governance + template dead-code simplification ✅ DONE
1. ✅ Deleted obsolete duplicate script: `scripts/check-github-alignment.sh`
	(Python checker is canonical across platforms).
2. ✅ Removed dead placeholder module:
	`template/backend/src/{{ project_slug }}/application/services/{% if use_rag %}rag_service.py{% endif %}.jinja`.
3. ✅ Simplified API dependency helpers to reuse one container accessor in
	`presentation/api/dependencies.py.jinja`.
4. ✅ Replaced hardcoded workstation/repository token checks with dynamic,
	project-agnostic token derivation from the active repository root in
	`scripts/check-github-alignment.py`.

### Phase 8 — policy hardening + docs normalization ✅ DONE
1. ✅ DRY'd alignment checker path existence scans by replacing duplicated
	required/legacy loops with one helper:
	`_collect_paths_with_existence_mismatch(...)`.
2. ✅ Tightened architecture checker policy to disallow `ai -> infrastructure`
	imports; kept adapter wiring responsibility in `composition`.
3. ✅ Simplified generated FastAPI dependency helpers so service providers accept
	typed `ContainerDep` directly instead of re-fetching container from `Request`.
4. ✅ Reduced Copier questionnaire cognitive load by asking `secret_backend`
	only when `cloud_provider == 'azure'`.
5. ✅ Normalized root documentation to one canonical template render workflow:
	`task render` + one fallback command pattern.
