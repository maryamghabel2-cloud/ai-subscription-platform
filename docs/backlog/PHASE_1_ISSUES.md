# PHASE 1 ISSUES - Core MVP

**Milestone:** Phase 1 Core MVP

## ISSUE-1-01: Backend Auth - User Model, JWT, Register/Login/Me

- **Title:** Implement auth endpoints
- **Purpose:** Working auth skeleton
- **Owner Agent Type:** Fullstack Builder
- **Dependencies:** Phase 0
- **Acceptance Criteria:** POST /auth/register creates user (email unique, bcrypt), POST /auth/login returns JWT, GET /auth/me requires JWT and returns user, tests pass, no secrets, password hashed, alembic migration exists, docker compose up works
- **Priority:** P0
- **Phase Label:** phase-1
- **Risk Level:** Medium (auth security)

## ISSUE-1-02: Backend Chat Echo Endpoint Protected

- **Title:** POST /chat protected echo Hello {message}
- **Purpose:** Prove auth + working route for future AI
- **Owner:** Fullstack Builder
- **Dependencies:** 1-01
- **Acceptance:** POST /chat requires JWT, returns Hello {message}, 401 without token, test
- **Priority:** P0
- **Phase:** phase-1
- **Risk:** Low

## ISSUE-1-03: Frontend Landing + Auth Pages

- **Title:** Next.js 14 landing, login, register, dashboard with chat box
- **Purpose:** Public landing + protected dashboard
- **Owner:** Website Builder + Fullstack Builder
- **Dependencies:** 1-01
- **Acceptance:** / public, /login form calls /auth/login stores token localStorage, /register calls register, /dashboard protected redirects to /login if 401, ChatBox calls /chat with JWT interceptor, axios client, tailwind
- **Priority:** P0
- **Phase:** phase-1
- **Risk:** Low

## ISSUE-1-04: Docker Compose Dev Ready

- **Title:** docker-compose.yml postgres + backend + frontend
- **Purpose:** One command run
- **Owner:** DevOps
- **Dependencies:** 1-01, 1-03
- **Acceptance:** docker compose up --build runs postgres:15-alpine, backend uvicorn reload, frontend npm dev, ports 5432:5432, 8000:8000, 3000:3000, env file from .env.example, alembic upgrade head works inside container, README quick start works
- **Priority:** P0
- **Phase:** phase-1
- **Risk:** Low

## ISSUE-1-05: Wallet Mock Display

- **Title:** Wallet mock UI (no real payment)
- **Purpose:** Show credit concept
- **Owner:** Fullstack Builder
- **Dependencies:** 1-01
- **Acceptance:** Dashboard shows wallet 100 credits mock, no real purchase, no crypto, clearly marked mock
- **Priority:** P1
- **Phase:** phase-1
- **Risk:** Low
