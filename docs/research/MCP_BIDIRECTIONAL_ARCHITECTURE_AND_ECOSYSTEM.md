# MCP Bidirectional Architecture and Ecosystem Research

**Version:** v0.1.0

**Date:** 2026-07-28

**Status:** Proposed Architecture / Research - Pending Owner Approval

**Document Owner:** AI Platform Architect / Security Architect / Product

**Purpose:** Research a safe, phased Model Context Protocol (MCP) strategy for
this Persian AI Workspace in both directions: consuming external MCP servers and
exposing narrowly scoped platform capabilities to external MCP clients.

**Evidence note:** This document is architecture and research, not implementation
evidence. It does not enable providers, connectors, remote endpoints, credentials,
payment operations, or external access. Code, tests, configuration, approval, and
security review are separate requirements.

## 1. Executive Summary

Model Context Protocol (MCP) is an open protocol for connecting AI applications to
external context and capabilities through a defined client/server interaction.
MCP matters to this workspace because it can make approved tools and knowledge
available without treating every integration as a bespoke agent implementation.

The product has two distinct directions:

- **Direction A, outbound:** this platform acts as an MCP Host/Client and connects
  to an external MCP Server on a user's or tenant's behalf.
- **Direction B, inbound:** this platform acts as an MCP Server and an external
  MCP Host/Client connects to selected platform capabilities.

Early phases should prioritize a small, sandboxed outbound connector path and a
separate, read-only inbound capability. They must not be presented as one shared
trust boundary. Each direction has its own authentication, consent, metering,
tenant-isolation, abuse-prevention, and revocation requirements.

Later phases may add user OAuth connections, enterprise-private connectors, and
registry publication. Early phases exclude unrestricted execution, broad data
export, payment actions, administrative actions, and any connector that cannot
meet the intake gates in this document and the linked security policies.

## 2. MCP Core Concepts

The following definitions use the terminology in the official MCP architecture
materials. Protocol details must be verified against the current specification
before implementation.

- **Host:** the AI application that coordinates one or more MCP client instances
  and supplies the user-facing experience. In Direction A, our platform is the
  host. In Direction B, a third-party desktop application, IDE, agent, or partner
  application is the host.
- **Client:** a protocol participant created by a host to maintain one connection
  to an MCP server. A client is not synonymous with an end user or tenant.
- **Server:** a program or remote service that offers MCP capabilities to clients.
  A server can expose tools, resources, prompts, and other protocol features it
  advertises during initialization.
- **Tools:** callable, schema-described actions provided by an MCP server. Tool
  execution can have side effects and therefore requires explicit policy gates.
- **Resources:** server-provided contextual data that a host/client can read or
  subscribe to according to the applicable protocol capability and authorization.
- **Prompts:** reusable, server-provided prompt templates or prompt-related
  interactions. They are not trusted instructions merely because a server offers
  them; all external content remains untrusted input.
- **Local server:** a server process running on the same device or controlled
  execution environment as its host/client. Local does not automatically mean
  trusted; its package, process arguments, filesystem access, and dependencies
  still need review.
- **Remote server:** a server reachable over a network endpoint. It adds network,
  authorization, SSRF, tenancy, availability, and data-residency considerations.
- **stdio:** the standard input/output transport commonly used for direct local
  process communication. Standard error is separate from protocol messages.
- **HTTP/SSE/streamable HTTP:** current ecosystem terminology includes legacy or
  deployed HTTP plus Server-Sent Events (SSE) integrations and Streamable HTTP.
  The current official architecture describes stdio and Streamable HTTP; the
  latter uses HTTP POST and may use SSE for streaming. Compatibility with older
  SSE endpoints is a connector-specific decision, not an assumed protocol feature.
- **Auth patterns:** local processes may have no protocol-level auth while relying
  on controlled process launch and local credentials. Remote servers may use API
  keys or OAuth. OAuth is the preferred documented pattern for protected remote
  MCP resources when applicable; exact flows, scopes, and registration are
  implementation decisions.

Primary sources, accessed 2026-07-28:

- Official architecture: https://modelcontextprotocol.io/docs/learn/architecture
- Official specification changelog: https://modelcontextprotocol.io/specification/2025-11-25/changelog
- Official registry overview: https://modelcontextprotocol.io/registry/about

UNKNOWN: exact compatibility requirements for every deployed legacy SSE server.
Each candidate must document its supported transport and protocol version during
intake.

## 3. Direction A — Platform as MCP Client

### User Journey and Consent

A user begins from a named connector page, such as GitHub, Drive, or Notion. The
page must explain the connector publisher, requested scopes, data classes, tool
list, cost model, retention implications, and how to revoke access. The user
selects only the scopes needed for the requested workflow and confirms consent
before credentials are issued or a connection is activated.

The platform backend, rather than browser code or an autonomous agent, owns the
connection lifecycle. It obtains or receives credentials through the approved
flow, stores only required credential material in managed secret storage, and
passes a scoped credential only to the connector invocation boundary.

### Invocation and Metering Path

1. User or approved workflow requests a connector capability.
2. Policy enforcement validates tenant, consent, scopes, connector state, and
   CONFIGURED_MCP_RATE_LIMIT.
3. The backend calls the approved MCP client adapter.
4. The adapter validates the selected tool schema and destination allowlist.
5. The backend records a pending credit/wallet reservation where a billable call
   is configured; no connector gets unrestricted wallet access.
6. The server result is classified, filtered, and returned through output DLP.
7. The result, cost metadata, and outcome are audit-recorded without raw secrets
   or raw sensitive conversation content by default.

Connector failure must produce a user-visible, actionable state: not connected,
consent expired, scope insufficient, provider unavailable, timeout, policy block,
or billing reservation unavailable. Error messages must not leak tokens, server
configuration, other tenants, or sensitive upstream content.

### Credential Storage, Revocation, and Audit

Credentials are vaulted, encrypted, separately scoped per tenant and connector,
and revocable. Environment variables, if used at runtime, are injection only and
not the source of truth. A revocation request must disable new calls immediately,
clear or invalidate the connector credential reference, and create audit metadata.

Audit metadata includes tenant pseudonym, connector identifier and version, tool
name, policy decision, timestamps, outcome category, cost metadata, and approval
reference. It excludes raw access tokens and raw sensitive content by default.

### Candidate External Categories

| Category | User value | Revenue value | Privacy | Security | Complexity | Timing | Must-pass gates |
|---|---|---|---|---|---|---|---|
| GitHub | Code and issues | Developer plan | Medium | High | Medium | early evaluation | OAuth, read-first, sandbox |
| Drive | Approved documents | Knowledge workflow | High | High | High | later | consent, DLP, tenant scope |
| Notion | Workspace pages | Team knowledge | High | High | High | later | OAuth, DLP, revocation |
| Browser automation | Bounded research | Research value | High | High | High | optional | sandbox, allowlist, approval |
| Databases | Approved analytics | Enterprise value | High | Critical | High | later | read-only, query guards, audit |
| Search | Grounded information | Research plan | Medium | Medium | Medium | early evaluation | citations, DLP, cost policy |
| DevTools | Build context | Developer value | Medium | Critical | High | later | isolated runner, approval |
| Slack | Approved work context | Team plan | High | High | High | later | OAuth, DLP, read-only |
| Telegram | Channel context | Channel value | High | High | High | later | consent, scoped credentials |

The table is a product hypothesis, not a promise to integrate any named service.
"Early evaluation" means research and a sandbox decision, not public activation.

## 4. Direction B — Platform as MCP Server

### Intended Clients and Boundary

Potential clients include Claude Desktop, Cursor, VS Code integrations, custom
agents, and approved partners. Acceptance by a client is not an endorsement of
that client, and client identity must not bypass platform tenant controls.

The platform server should use scoped API keys and/or OAuth only after the remote
hosting and authorization model is approved. Every request must resolve to a
platform tenant, user or service principal, capability scope, rate policy, and
wallet/credit policy where applicable.

### Early Exposed Capabilities

The initial server surface may expose only low-risk, policy-filtered capabilities:

- low-risk Skills with explicit schemas and no arbitrary command execution;
- prompt enhancer operations that return bounded, non-sensitive transformations;
- grounded knowledge-base or search results with citations and output filtering;
- read-only studio workflow status and approved result references.

Early scope excludes high-risk Agents, raw conversation export by default,
unrestricted tool execution, payment or withdrawal actions, administrative actions,
credential management, cross-tenant lookup, and direct filesystem or shell access.

### Inbound Request Path

1. External host/client authenticates with a scoped credential.
2. The MCP server authenticates the principal and resolves tenant context.
3. Authorization checks declared capability, object ownership, quota, and wallet
   preconditions before work is started.
4. Inputs are treated as untrusted and passed through prompt-injection defenses.
5. The bounded capability runs through backend policy and audit controls.
6. Output DLP removes or blocks disallowed sensitive data before the response.
7. Metadata-only audit records capture the request and policy outcome.

No raw sensitive user data is exposed by default. Any future exception needs a
separate data-classification decision, explicit tenant authorization, a documented
workflow, and applicable human approval.

## 5. Ecosystem Landscape Research

### Sources and Research Method

This is a dated landscape summary, not a security endorsement or a live market
measurement. Registry listings, stars, install indicators, and mentions are
interest or discoverability signals only. They are not security evidence, proof of
publisher identity, or proof that a server is safe to connect.

Primary sources, accessed 2026-07-28:

- Official MCP site and architecture: https://modelcontextprotocol.io/docs/learn/architecture
- Official MCP Registry, preview status: https://modelcontextprotocol.io/registry/about
- Official registry announcement: https://blog.modelcontextprotocol.io/posts/2025-09-08-mcp-registry-preview/
- Official registry source: https://github.com/modelcontextprotocol/registry
- Official/reference servers source: https://github.com/modelcontextprotocol/servers
- Community catalog: https://github.com/punkpeye/awesome-mcp-servers
- Community registry/catalog: https://smithery.ai/
- Community catalog: https://mcpservers.org/
- Community catalog: https://mcpmarket.com/

The official registry describes itself as preview and warns that breaking changes
or data resets can occur before general availability. Therefore registry metadata
must be captured with source URL, version, effective date when provided, and
access date during intake.

### Landscape Table

| MCP / Category | Source | Demand signal | License | Runtime | Data access | Risk | Fit | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| MCP architecture | Official site | Standard source | UNKNOWN | Protocol | N/A | Medium | foundation | shortlist-early |
| Official Registry | Official registry | Central metadata; preview | UNKNOWN | Web/API | Metadata | Medium | discovery | shortlist-early |
| Reference servers | Official servers repo | Official examples | Repo-specific | Mixed | Varies | Medium | learning | watchlist |
| GitHub remote server | GitHub repo | Official publisher | Repo-specific | Remote | Code/issues | High | dev workflow | shortlist-early |
| Source control | Vendor servers | Repeated category | Varies | Mixed | Code/issues | High | high fit | shortlist-early |
| Google Drive | Registry/catalogs | Common connector | Varies | Mixed | Documents | High | knowledge | later |
| Notion | Registry/catalogs | Common connector | Varies | Mixed | Pages | High | knowledge | later |
| Filesystem | Official servers repo | Reference category | Repo-specific | Local | Local files | Critical | sandbox | later |
| Fetch/web | Official servers repo | Reference category | Repo-specific | Mixed | Web content | High | research | watchlist |
| Search | Registry/catalogs | Common category | Varies | Remote | Queries/results | Medium | research | shortlist-early |
| Databases | Registry/catalogs | Enterprise category | Varies | Mixed | Structured data | Critical | enterprise | later |
| Browser automation | Registry/catalogs | Agent-tool category | Varies | Mixed | Browser/session | Critical | bounded use | later |
| Slack | Registry/catalogs | Team category | Varies | Remote | Messages/files | High | later team | later |
| DevTools | Registry/catalogs | Developer category | Varies | Mixed | Build systems | Critical | isolated use | later |
| Smithery | smithery.ai | Discovery surface | Platform-specific | Web | Metadata | Medium | cross-check | watchlist |
| awesome-mcp-servers | punkpeye list | Community curation | Repo-specific | N/A | Metadata | Medium | research | watchlist |
| mcpservers.org | mcpservers.org | Community catalog | Platform-specific | Web | Metadata | Medium | cross-check | watchlist |
| MCP Market | mcpmarket.com | Community catalog | Platform-specific | Web | Metadata | Medium | cross-check | watchlist |

Language/runtime trend: the ecosystem is not limited to one language. Official
registry discussion material notes JavaScript/TypeScript and Python alongside Go,
Rust, Java, and C#. This is a qualitative observation, not a measured ranking.
Runtime must be evaluated per candidate because package format and isolation vary.

## 6. Trust, Security, and Intake

All external MCP servers start untrusted. A registry entry, repository star,
installation instruction, marketplace placement, or vendor claim is not approval.
This document complements, and does not replace, the existing third-party intake
policy in [THIRD_PARTY_AGENT_REVIEW.md](../security/THIRD_PARTY_AGENT_REVIEW.md).

The intake package requires publisher identity, source URL, immutable version or
checksum, license, runtime, transport, authentication method, requested tools,
permissions, network destinations, data classifications, dependency lockfiles or
SBOM where available, and operational ownership.

A candidate must pass source and license review, dependency and supply-chain
analysis, static and dynamic analysis where safe, prompt-injection testing, tool
abuse testing, data-exfiltration testing, sandbox evaluation, and owner approval.
Network access is deny-by-default and then limited to approved destinations.

Least privilege applies to credentials, tool scopes, data objects, execution time,
cost, network destinations, and output size. Connectors must be re-reviewed after
a material version, permission, tool, network, publisher, license, or data-class
change. Suspected compromise requires immediate revocation or disablement.

Security Agent monitoring signals for MCP abuse include repeated authorization
failures, unexpected tool schemas, credential misuse, abnormal call rates, unusual
cost, cross-tenant attempts, prompt-injection indicators, unexpected egress, and
output data-exfiltration indicators. Actions remain bounded by the canonical
Security Agent authority model in [SECURITY_AGENT_RUNTIME.md](../security/SECURITY_AGENT_RUNTIME.md).

All inbound and outbound content is untrusted input unless a policy explicitly
classifies it otherwise. Apply the defenses in
[PROMPT_INJECTION_DEFENSE.md](../security/PROMPT_INJECTION_DEFENSE.md), including
separation of instructions from data, structured tool calls, output guardrails,
provenance handling, and relevant regression tests.

## 7. Product Decisions for Our App

### 1. Direction Recommendation

Recommend **Client-first, with a narrowly designed Server contract in parallel as
documentation only**. Client-first creates immediate user value from carefully
chosen integrations and teaches the product how consent, metering, audit, and
revocation work. A public server should follow only after the platform can expose
a small read-only capability with reliable tenant isolation and output DLP.

### 2. First Five Client Categories to Evaluate

1. GitHub source-control context, read-first and narrowly scoped.
2. Search/grounding connector with citation and retention review.
3. One document connector category, either Drive or Notion, after privacy review.
4. Official/reference fetch capability in a sandboxed research environment.
5. One internal or enterprise-private knowledge connector only after tenancy and
   data-classification requirements are proven.

This is an evaluation order, not a commitment to any vendor server.

### 3. First Five Server Capabilities to Design

1. Read-only grounded knowledge lookup with citations.
2. Bounded prompt enhancement with no raw sensitive context by default.
3. Read-only studio workflow status.
4. Read-only approved studio result references.
5. One low-risk, schema-defined internal Skill with no spending, publishing, or
   external contact capability.

### 4. Never Expose in v1

Do not expose payment, withdrawal, wallet signing, administration, raw secrets,
raw conversation export by default, arbitrary command execution, unrestricted
browsing, cross-tenant search, user-management changes, or high-risk Agent actions.

### 5. Skills and Agents Are Not MCP Synonyms

A **Skill** is a bounded reusable platform capability. An **Agent** is a workflow
actor that may reason, select tools, and need stronger limits and approval gates.
An **MCP Connector** is a protocol integration boundary. An MCP server may expose
a low-risk Skill, but that does not make every Skill an MCP server or make an
Agent safe to expose. See [EXTENSIBILITY_MCP_AND_SKILLS.md](../architecture/EXTENSIBILITY_MCP_AND_SKILLS.md)
and [AGENT_SECURITY_MODEL.md](../security/AGENT_SECURITY_MODEL.md).

## 8. Open Decisions

- Remote hosting model for our MCP server, including tenancy and region design.
- OAuth provider choice, scopes, consent UX, and token lifecycle.
- Monetization and credit handling for external MCP calls.
- Enterprise-private MCP connectors and private registry model.
- Whether and when to publish our server in an external registry.
- SLA and support boundary for third-party clients connecting to us.
- CONFIGURED_MCP_RATE_LIMIT and connector-specific quota policy.
- CONFIGURED_MCP_TOKEN_LIFETIME and credential-rotation policy.
- Client compatibility matrix and supported protocol versions.
- Privacy, retention, and data-residency requirements per connector.

## 9. Phased Implementation Roadmap

### Phase MCP-0 — Research Complete

**Objective:** Approve or revise this architecture research.

**In scope:** sources, threat model, intake gates, candidate categories, and
product decisions.

**Out of scope:** code, credentials, endpoints, registry publication, or provider
activation.

**Dependencies:** owner, product, security, privacy, and legal review.

**Risks:** source drift and unclear product ownership.

**Acceptance:** approved decisions are recorded; contradictions are resolved or
explicitly tracked.

### Phase MCP-1 — Client Abstraction and One Sandbox Connector

**Objective:** Define an internal client adapter and evaluate one non-sensitive
sandbox connector.

**In scope:** adapter interface, allowlist, schema validation, audit metadata,
and a synthetic-data test environment.

**Out of scope:** user OAuth, production tenant data, public server endpoint.

**Dependencies:** secure runtime, secrets manager, sandbox, and test plan.

**Risks:** supply-chain compromise, unexpected tool behavior, and SSRF.

**Acceptance:** connector passes intake, sandbox, prompt-injection, and revocation
tests with no real user credentials.

### Phase MCP-2 — OAuth Connect Flow for One Low-Risk Connector

**Objective:** Add consent and scoped authorization for one approved connector.

**In scope:** consent screen, approved scopes, vaulted credential reference,
revocation, and user-visible errors.

**Out of scope:** broad document export, write scopes, and multi-connector rollout.

**Dependencies:** MCP-1 acceptance and OAuth design approval.

**Risks:** overbroad consent, token leakage, and tenant confusion.

**Acceptance:** consent, scope reduction, token revocation, and tenant-isolation
tests pass.

### Phase MCP-3 — Metering, Audit, and Revocation UI

**Objective:** Make connector calls observable and financially bounded.

**In scope:** credit reservation, cost metadata, audit views, revocation UI, and
CONFIGURED_MCP_RATE_LIMIT enforcement.

**Out of scope:** payment actions through MCP.

**Dependencies:** wallet policy, audit storage, and support workflow.

**Risks:** incorrect billing, data-heavy logs, and delayed revocation.

**Acceptance:** simulated failures preserve tenant isolation and record only
approved metadata.

### Phase MCP-4 — One Low-Risk MCP Server Capability

**Objective:** Expose one read-only, schema-defined platform capability.

**In scope:** scoped authentication, tenant checks, output DLP, rate policy, and
one client compatibility test.

**Out of scope:** high-risk Agents, raw conversations, and write operations.

**Dependencies:** inbound authorization model and security review.

**Risks:** client confusion, data exposure, and abusive automation.

**Acceptance:** authorization, negative tenant tests, output DLP, and revocation
tests pass before any external access.

### Phase MCP-5 — Registry and External Developer Documentation

**Objective:** Decide whether to publish metadata for an approved server.

**In scope:** registry evidence, developer documentation, support boundary, and
versioning policy.

**Out of scope:** declaring marketplace listing as a security endorsement.

**Dependencies:** stable capability contract, legal review, and owner approval.

**Risks:** stale metadata, unsupported clients, and discovery-driven abuse.

**Acceptance:** a publication decision, review date, and incident/revocation plan
are approved before listing.

## 10. Relation to Existing Documentation

This research complements [EXTENSIBILITY_MCP_AND_SKILLS.md](../architecture/EXTENSIBILITY_MCP_AND_SKILLS.md).
That document establishes platform extensibility concepts, access tiers, the
platform-as-client and platform-as-server intent, and baseline review controls.
This document adds a bidirectional boundary model, dated ecosystem research,
candidate-evaluation method, phased roadmap, and explicit product sequencing.

### Documentation Drift

No contradiction is intentionally introduced. The following items require owner
review before implementation because they are more detailed than existing prose:

- The external registry landscape is fragmented, and official registry preview
  status means metadata must not be treated as durable approval evidence.
- Legacy SSE compatibility must be assessed per connector while Streamable HTTP
  remains the current official remote transport description.
- Client-first sequencing is a recommendation, not a replacement for the existing
  statement that the platform can act as both an MCP client and server.
- Candidate network, identity, payment, wallet, and high-risk Agent policies
  remain governed by their respective architecture and security documents.

## Related Documents

- Extensibility: [EXTENSIBILITY_MCP_AND_SKILLS.md](../architecture/EXTENSIBILITY_MCP_AND_SKILLS.md)
- Agent Security Model: [AGENT_SECURITY_MODEL.md](../security/AGENT_SECURITY_MODEL.md)
- Third-Party Agent Review: [THIRD_PARTY_AGENT_REVIEW.md](../security/THIRD_PARTY_AGENT_REVIEW.md)
- Prompt Injection Defense: [PROMPT_INJECTION_DEFENSE.md](../security/PROMPT_INJECTION_DEFENSE.md)
- Security Agent Runtime: [SECURITY_AGENT_RUNTIME.md](../security/SECURITY_AGENT_RUNTIME.md)
