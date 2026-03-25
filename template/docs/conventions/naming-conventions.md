# Naming Conventions

| Context          | Convention              | Example                          |
| ---------------- | ----------------------- | -------------------------------- |
| Python modules   | `snake_case.py`         | `user_service.py`                |
| Python packages  | `snake_case/`           | `adapters/`                      |
| TypeScript files | `kebab-case.ts`         | `web-vitals.ts`                  |
| React hooks      | `camelCase.ts`          | `useMediaQuery.ts`               |
| React components | `PascalCase.tsx`        | `UserProfile.tsx`                |
| CSS modules      | `kebab-case.module.css` | `user-profile.module.css`        |
| Shell scripts    | `kebab-case.zsh`        | `install-python.zsh`             |
| Config files     | `kebab-case`            | `.prettierrc.json`               |
| Documentation    | `UPPER-CASE.md`         | `ARCHITECTURE.md`                |
| ADRs             | `NNNN-kebab-case.md`    | `0001-hexagonal-architecture.md` |

| Context      | Convention                              | Example                                 |
| ------------ | --------------------------------------- | --------------------------------------- |
| Classes      | `PascalCase`                            | `UserService`                           |
| Functions    | `snake_case`                            | `create_user`                           |
| Methods      | `snake_case`                            | `get_by_email`                          |
| Constants    | `UPPER_SNAKE_CASE`                      | `MAX_RETRIES`                           |
| Variables    | `snake_case`                            | `user_email`                            |
| Type aliases | `PascalCase`                            | `type UserId = NewType("UserId", UUID)` |
| Protocols    | `PascalCase`                            | `UserRepository`                        |
| Enums        | `PascalCase` members `UPPER_SNAKE_CASE` | `UserRole.ADMIN`                        |
| Private      | `_leading_underscore`                   | `_validate_email`                       |

| Context      | Convention            | Example                 |
| ------------ | --------------------- | ----------------------- |
| Tables       | `snake_case` (plural) | `users`                 |
| Columns      | `snake_case`          | `created_at`            |
| Primary keys | `id` (UUID)           | `id`                    |
| Foreign keys | `<table>_id`          | `user_id`               |
| Indexes      | `ix_<table>_<column>` | `ix_users_email`        |
| Constraints  | `ck_<table>_<desc>`   | `ck_users_email_format` |

| Context         | Convention   | Example                   |
| --------------- | ------------ | ------------------------- |
| URLs            | `kebab-case` | `/api/v1/user-profiles`   |
| Path params     | `snake_case` | `/users/{user_id}`        |
| Query params    | `snake_case` | `?page_size=20`           |
| Response fields | `snake_case` | `{ "created_at": "..." }` |
