# Phase 1 Implementation Backlog

## Completed or Validation Required
- Database/migration, authentication/session, wallet/ledger, and sandbox payment foundations: validate current code; do not rebuild without evidence.

## Ordered Work
1. Stabilize backend configuration and PostgreSQL migration path.
2. Validate secure cookie-based authentication; authentication tokens are forbidden in browser localStorage.
3. Build clean RTL frontend skeleton without reseller pages.
4. Add provider abstraction and Persian streaming chat.
5. Add wallet usage reserve/settle integration.
6. Add Prompt Enhancer.
7. Add Instagram Caption Generator.

Each item requires a focused PR, tests, and rollback approach.