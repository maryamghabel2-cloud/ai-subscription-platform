# Extensibility: MCP and Skills

**Version:** v0.1.0

**Date:** 2026-07-24

**Status:** Proposed Architecture - Pending Owner, Security, Privacy, and
Compliance Approval

**Document Owner:** AI Platform Architect / Product

**Purpose:** Define extensibility concepts for Roles, Skills, MCP Connectors,
Agents, Sub-agents, hybrid naming, three-tier access model, platform as MCP
Client and Server, Skill Builder, Agent Builder and Sub-agents, security review
pipeline, marketplace, and relation to Security Agent.

**Note:** Documentation only. No real provider API calls, no secrets.

## Purpose

Establish how the platform will be extensible via Skills, MCP Connectors,
Agents, and Sub-agents with clear naming, tiered trust, and security review.

## In Scope

- Definitions of Role, Skill, MCP Connector, Agent, Sub-agent
- Hybrid naming: Persian user-facing and technical
- Three-tier access model: Internal, Verified External, User-Provided
- Platform as MCP Client and as MCP Server
- Skill Builder, Agent Builder and Sub-agents
- Security review pipeline for imported Skills and MCPs
- Marketplace and relation to Security Agent

## Out of Scope

- Actual Skill and MCP implementation and provider wiring (future, reviewed)
- Final marketplace business logic and revenue share (future Phase 8)
- Production Skill Builder and Agent Builder code (future PRs)

## Define Concepts

### Role

- Conversation style and behavior only
- Conversation-only, no tools, no autonomous actions
- Defines identity, tone, style, method, language, creativity defaults,
  response mode, model policy, memory policy, risk level, disclaimer policy
- Example: Normal Assistant, Language Tutor, Friendly Companion, Writer,
  Business Assistant, Prompt Engineer
- Extensible registry-based, adding new Role should not require changing core
  chat logic

### Skill

- A packaged capability containing instructions, prompt templates, checklists,
  output formats, optional knowledge-pack references, and lightweight workflow
  guidance
- No code execution in early phases, no network access in early phases, no
  provider secrets, highest initial trust for internal Skills
- Example: SEO checklist Skill, Product Photography Prompt Enhancer Skill,
  Career Advisor structured direct Skill

### MCP Connector

- A controlled connection to an external tool, service, dataset, or user system
  using Model Context Protocol or a compatible connector design
- Connects to GitHub, cloud storage, document systems, CRMs, databases, search
  providers, internal company APIs
- Must have least-privilege scopes, OAuth or vaulted API keys, read/write
  separation, network allowlist, rate limits, audit logs, immediate revocation

### Agent

- An execution system that can use tools, call connectors, run multi-step
  workflows, and coordinate sub-agents
- Performs work, may use tools, browse, retrieve, call APIs, process files,
  run multi-step workflows, must have permissions, budgets, safety controls,
  auditability
- Examples: Telegram Business Agent, Deep Research Agent, Immigration Research
  Agent (performs multi-step research, may browse approved current official
  government and embassy sources)

### Sub-agent

- A specialized agent used by a parent agent for a narrow task
- Inherits parent agent's permissions only when explicitly allowed
- Must not receive broad secrets, must not grant itself new permissions
- High-risk actions require human approval, publishing requires security,
  privacy, and product review

## Naming

Use hybrid naming:

- User-facing Persian:
  - تخصص‌ها، اتصال‌گرها، ایجنت‌ها
  - تخصص‌ها for Skills, اتصال‌گرها for MCP Connectors, ایجنت‌ها for Agents

- Technical:
  - Skills, MCP Connectors, Agents
  - Skill: SEO Skill, Product Photography Skill
  - MCP Connector: GitHub Connector, Google Drive Connector
  - Agent: Business Agent, Research Agent

## Three-Tier Access Model

### Tier 1 — Internal Skills

- Built by our platform, security-reviewed by us
- No code execution in early phases
- No network access in early phases
- No provider secrets
- Highest initial trust
- Versioned, with knowledge_pack_version, review date, expiry, benchmark
- Example: Prompt Enhancer Skill, Product Photography Advisor Skill

### Tier 2 — Verified External Skills and MCP Connectors

- Imported from trusted sources or partners (e.g., vetted GitHub repos, official
  partners)
- Must pass security review, license review, dependency scan, prompt injection
  testing, and sandbox validation
- Published only after approval (human approval gates for publishing, spending,
  contacting customers, pricing, config, merge, deploy, API keys, persona
  sensitive edits)
- Versioned, with source, checksum, license, review status, rollback version
- Network and tool calls restricted to approved allowlist

### Tier 3 — User-Provided Skills and MCP Connectors

- May be created by users via Skill Builder (private draft, local validation,
  security pre-check, user testing, submission for review, approved publication,
  versioning and rollback)
- Private use may be allowed with strong restrictions (no public publication,
  no bulk, no spending without approval, audit logging)
- Public publication requires Security Agent review and human approval
- High-risk connectors (e.g., database with write access, CRM with PII, payment
  APIs) require sandbox isolation and explicit user consent
- Must not automatically become public, private draft by default

## Platform as MCP Client

The platform may connect to user-approved external tools such as:

- GitHub: repository access, issues, PRs, code search
- Cloud storage: Google Drive, Dropbox, OneDrive, S3-compatible storage
- Document systems: Notion, Confluence, Google Docs, Office 365
- CRMs: HubSpot, Salesforce, internal company CRM
- Databases: Postgres, MySQL, MongoDB, internal company databases
- Search providers: web search, internal knowledge-base search
- Internal company APIs: HR, finance, support, analytics

Controls:

- Least-privilege scopes: read-only vs read-write, minimal scopes required
- OAuth or vaulted API keys: OAuth flow with user consent, tokens encrypted at
  rest, vaulted API keys in secrets manager, no secrets in logs
- Read/write separation: read and write operations have separate permissions,
  write requires additional approval
- Network allowlist: only approved domains, IPs, no arbitrary internet unless
  explicitly allowed and reviewed
- Rate limits: per user, per connector, per tool, CONFIGURED_MCP_RATE_LIMIT placeholders
- Audit logs: all connector calls logged with metadata only by default, no raw
  sensitive content, content_fingerprint DISABLED_BY_DEFAULT
- Immediate revocation: user can revoke connector token at any time, revocation
  is immediate, audit trail, no orphaned tokens

## Platform as MCP Server

The platform may expose controlled MCP-compatible endpoints so external tools
and AI systems can use our capabilities.

### What Capabilities Will Be Exposed Externally?

- Specific Skills: e.g., SEO Skill, Product Photography Prompt Enhancer Skill,
  Career Advisor structured direct Skill (internal Skills only in early phases,
  no code execution, no network access, highest trust)
- Knowledge Bases: e.g., Persian knowledge-base search, source-grounded study
  workspace with citations, approved official-source Knowledge Base via
  Retrieval Service
- Studio Workflows: e.g., Professional Image Studio, Video Studio, Product
  Photography Studio, structured workflows for professional image and video
  creation (core revenue products, not simple Roles)
- Search: e.g., Web Search and Grounded Answers with provenance, URL/source,
  access time, trust classification, citation where appropriate
- Study Workspace retrieval: upload PDFs and docs, ask questions with citations,
  RAG attachment, file attachments
- Approved Research Agents: Deep Research Agent (multi-step research with
  citations), Immigration Research Agent (general information only, not legal
  advice, uses approved official-source Knowledge Base via Retrieval Service)
- Business workflows: FAQ, lead, support draft, content draft (draft-only
  initially, publish requires approval)

### Authentication and Scope

- External tools must authenticate using scoped API keys or OAuth:
  - API keys short-lived or rotatable, hashed, scopes, rate limits, revocable
    without disruption
  - OAuth with least-privilege scopes, user consent, tokens encrypted at rest
  - Each API key has defined scopes and rate limits, least privilege, no
    cross-user access, tenant isolation

### Out of Scope for Early Phases

- State that exposing Agent execution (especially high-risk Agents) through MCP
  Server is out of scope for early phases:
  - High-risk Agents: Evidence-Based Mental Health Information Assistant,
    Immigration Information Assistant, Legal Information Assistant, Health
    Information Assistant (risk high, requires expert review, disclaimer,
    escalation, must not claim professional authority)
  - Business Agents that perform work with tools, browse, retrieve, call APIs,
    process files, run multi-step workflows, must have permissions, budgets,
    safety controls, auditability – exposing their execution via MCP Server
    requires security, privacy, legal, owner review and is out of scope for
    early phases

### Guardrails for Exposed Capabilities

- Any exposed capability must go through the same Prompt Injection Guard and
  Output DLP that internal usage goes through:
  - Prompt Injection Guard: separation of concerns (system instructions in
    separate immutable never-user-modifiable segment, user content and retrieved
    content always treated as untrusted), structured tool calls with strict
    allowlist schema, output guardrails (AI output must never contain raw API
    keys, secrets, tokens, scanned for data-exfiltration patterns)
  - Output DLP: AI output scanned for data-exfiltration patterns before delivery,
    responses containing potential credential leaks blocked and logged without
    raw content, content_fingerprint DISABLED_BY_DEFAULT

### Raw User Data Clarification

- Clarify that being an MCP Server does not mean giving external parties access
  to raw user data:
  - No raw sensitive conversation content by default, only citations and
    boundaries, disclaimer if needed, no authority claims
  - No raw sensitive prompts, uploaded file contents, conversation text, raw AI
    responses by default in technical logs, only metadata
  - Raw content may only be retained in separate encrypted product-data store
    when required for user-facing feature per retention settings, not in
    technical audit logs
  - Cross-user leakage prohibited, tenant isolation, pseudonymous identifiers

### Controls

- Strict API key or OAuth authentication: API keys short-lived or rotatable,
  hashed, scopes, rate limits, revocable without disruption
- Scoped permissions: each API key has defined scopes and rate limits,
  least privilege, no cross-user access
- Rate limiting: per API key, per user, per endpoint, CONFIGURED_MCP_RATE_LIMIT
- Wallet/credit checks: check wallet balance, atomic credit/debit, balance never
  negative, ledger append-only, audit metadata
- Data classification boundaries: no raw sensitive conversation content by
  default, only metadata, content_fingerprint DISABLED_BY_DEFAULT
- No raw sensitive data by default: only citations and boundaries, disclaimer
  if needed, no authority claims
- Full audit trail: all MCP server calls logged with metadata, tamper-resistant,
  retention, access control
- Revocation and abuse monitoring: immediate revocation, anomaly detection,
  auto-pause on abuse, human approval for high-impact actions

## Skill Builder

Users may eventually create their own Skills.

Builder phases:

- Private draft: user creates Skill in private workspace, no public visibility,
  versioned, with display_name_fa, display_name_en, description, category,
  system_instructions, allowed_tones, safety_profile, risk_level
- Local validation: validate Skill structure, required fields, no secrets,
  no hardcoding of Role names in core logic, no claiming professional authority
- Security pre-check: secret scanning, prompt injection test, tool abuse test,
  data exfiltration test, static analysis, dependency scan if applicable
- User testing: user tests Skill in private, with own data, no public impact
- Submission for review: user submits Skill for review, provides source,
  license, checksum, description, category, risk level
- Approved publication: security review, license review, dependency scan,
  prompt injection testing, sandbox validation, human approval for high-risk,
  published only after approval
- Versioning and rollback: knowledge_pack_version, knowledge_pack_reviewed_at,
  knowledge_pack_expires_at, expert_review_required, expert_review_status,
  versioned and removable, rollback version

Private Skills must not automatically become public. Private draft by default,
public publication requires Security Agent review and human approval.

## Agent Builder and Sub-agents

Users may eventually build Agents and Sub-agents.

Rules:

- Agent Builder is later than Skill Builder: Skill Builder first, then Agent
  Builder, because Skills are simpler (no code execution in early phases, no
  network access), Agents are more complex (tools, browsing, multi-step)
- Any tool-using Agent requires security review: permissions, forbidden actions,
  approval-required actions, tools list, budget policy, safety profile, risk
  level, audit_required, rollback_plan
- Sub-agents inherit the parent agent's permissions only when explicitly allowed
  (e.g., parent allows sub-agent to use web_search but not file_reader)
- Sub-agents must not receive broad secrets: no full environment secrets, only
  specific scoped credentials they need, separate from platform, revocable
  independently, secret isolation
- High-risk actions require human approval: publishing public content, spending
  money, contacting customers, bulk messages, pricing/config changes, merge/deploy
- Publishing an Agent requires security, privacy, and product review:
  source verification, license review, dependency scan, prompt injection test,
  tool abuse test, data exfiltration test, remediation before approval,
  approved manifest, runtime isolation, re-review after every material update
  and according to CONFIGURED_EXTENSIBILITY_REVIEW_CADENCE

## Security Review Pipeline

For imported Skills and MCPs:

- Source verification: source repository and author identity confirmed, publisher
  authority, geographic/jurisdiction applicability
- License review: MIT, Apache, proprietary, compatibility, public domain,
  licensed, purchased with appropriate usage rights, legally authorized
- Checksum or signed release verification: SHA256, Sigstore, Cosign, versioned
- Dependency scan: direct and transitive dependencies, known vulnerabilities,
  SBOM generated, no critical CVE
- Prompt injection test: direct, indirect, jailbreak, tool abuse, RAG poisoning,
  data exfiltration, system-prompt disclosure
- Data exfiltration test: can the Skill or connector leak user data to external
  endpoints? Test with canary tokens, no real user data
- Tool abuse test: can the Skill or connector call unauthorized tools or exceed
  its budget via crafted input?
- Sandbox execution: isolated sandbox, no network by default, then allowlisted
  network, no access to real user data, audit logging
- Network allowlist check: only approved domains, no arbitrary internet unless
  explicitly allowed and reviewed
- Secret access review: Does Skill or connector access secrets? No provider
  secrets in prompts, logs, model output, client code, secrets come only from
  approved secrets manager
- Risk classification: low, medium, high, high-risk requires expert review,
  disclaimer, escalation, must not claim professional authority
- Human approval for high-risk items: human approval gates for publishing,
  spending, contacting customers, pricing, config, merge, deploy, API keys,
  persona sensitive edits

## Marketplace

- Internal Skills launch first: platform-built Skills, security-reviewed, no
  code execution in early phases, no network access, highest initial trust
- Verified external Skills may be listed later: imported from trusted sources
  or partners, must pass security review, license review, dependency scan,
  prompt injection testing, sandbox validation, published only after approval
- User-submitted Skills require approval before publication: private draft,
  local validation, security pre-check, user testing, submission for review,
  approved publication, versioning and rollback, private must not automatically
  become public
- Revenue share is not active in early phases: no cash payouts, no rev-share
  without legal, tax, KYC, finance, owner approval
- Early rewards may use platform credits, badges, or visibility: e.g.,
  promotional credits capped by CONFIGURED_MARKETPLACE_PROMOTIONAL_CREDIT_REWARD,
  badges, featured listing
- Cash payouts require future legal, tax, KYC, finance, and owner approval:
  no cash payouts without legal review, tax review, KYC, finance and owner
  approval, versioned config

## Relation to Security Agent

Security Agent may:

- block publication of a Skill or connector that fails security review
- quarantine a Skill that shows anomalous behavior, prompt injection signals,
  data exfiltration signals
- disable a connector that is compromised, misbehaving, or abused
- revoke a connector token that is compromised or leaked
- open a security incident and escalate to human operators
- require human review for high-risk public releases
- roll back a version to previous known good version

Security Agent must not silently approve high-risk public releases without
human review: high-risk Skills and connectors (e.g., database write access, CRM
with PII, payment APIs) require human approval, audit trail, no auto-approval
without human review for high-risk.

## Related Documents

- Security Index: [../security/README.md](../security/README.md)
- Security Architecture: [../security/SECURITY_ARCHITECTURE.md](../security/SECURITY_ARCHITECTURE.md)
- Prompt Injection Defense: [../security/PROMPT_INJECTION_DEFENSE.md](../security/PROMPT_INJECTION_DEFENSE.md)
- Agent Security Model: [../security/AGENT_SECURITY_MODEL.md](../security/AGENT_SECURITY_MODEL.md)
- Third-Party Agent Review: [../security/THIRD_PARTY_AGENT_REVIEW.md](../security/THIRD_PARTY_AGENT_REVIEW.md)
- Security Agent Runtime: [../security/SECURITY_AGENT_RUNTIME.md](../security/SECURITY_AGENT_RUNTIME.md)
- Role and Persona System: [ROLE_AND_PERSONA_SYSTEM.md](ROLE_AND_PERSONA_SYSTEM.md)
- Agent Plugin and Execution: [AGENT_PLUGIN_AND_EXECUTION_SYSTEM.md](AGENT_PLUGIN_AND_EXECUTION_SYSTEM.md)
- Role Persona Agent Boundaries: [ROLE_PERSONA_AGENT_BOUNDARIES.md](ROLE_PERSONA_AGENT_BOUNDARIES.md)
- Multi-Provider Routing: [MULTI_PROVIDER_MODEL_ROUTING.md](MULTI_PROVIDER_MODEL_ROUTING.md)

## Open Decisions

- Exact Skill and MCP Connector schema and field types
- Three-tier access model thresholds and trust levels
- Platform as MCP Client: supported external tools and scopes and allowlists
- Platform as MCP Server: exposed endpoints and scopes and rate limits and
  wallet/credit checks and data classification boundaries
- Skill Builder phases and validation and security pre-check
- Agent Builder and Sub-agents inheritance and permissions and secret isolation
- Security review pipeline tooling and checklist and approval workflow
- Marketplace launch phases and revenue share and reward types and legal review
- Relation to Security Agent: blocking, quarantine, disabling, revocation,
  incident escalation, human review for high-risk releases
- Owner, security, privacy, legal, and compliance approval required for all

## Planned Completion Stage

Phase 1 - Extensibility (Internal Skills first, Verified External later,
User-Provided with restrictions, Marketplace future)

## Status Note

Proposed Architecture - Pending Owner, Security, Privacy, and Compliance
Approval. This document is proposed architecture. It does not prove that the described controls, integrations, providers, wallet-login flows, MCP exposure, or search behavior are implemented, tested, deployed, or production-ready. Implementation requires separate code, tests, configuration, owner approval, and security review.
No real provider API calls in this PR.
