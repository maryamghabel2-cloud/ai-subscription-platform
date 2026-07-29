# MCP, Skills, and Agents v1 Decisions

**Version:** v0.1.0

**Date:** 2026-07-28

**Status:** Proposed Decision Record - Pending Owner Approval

**Document Owner:** Product / AI Platform / Security

## 1. Purpose and Decision Status

This record converts completed MCP, Skills, and Agents research into product
planning decisions. It does not approve production implementation, dependency
adoption, external activation, credentials, OAuth, or provider connections.

Owner approval is required before this status changes to Accepted. Security
approval remains required in each implementation PR, along with relevant privacy,
legal, architecture, and product review.

## 2. Canonical Terminology

- **MCP Host:** application that coordinates MCP client connections and user flow.
- **MCP Client:** protocol participant created by a host to connect to one server.
- **MCP Server:** program or service exposing protocol capabilities to clients.
- **Product Skill:** bounded platform capability with versioned contracts, owner,
  permissions, risk class, evaluation evidence, and lifecycle state.
- **Agent Skills Package:** filesystem package, commonly with `SKILL.md`, metadata,
  instructions, and optional scripts, references, or assets.
- **MCP Tool:** capability exposed by an MCP Server through the protocol.
- **Agent:** multi-step workflow actor that may invoke approved Skills.
- **Persona:** product behavior and policy context that can narrow capability use.

These terms are not synonyms. Package acceptance does not approve code execution;
an MCP Tool is not automatically an approved Product Skill; an Agent has stronger
authority, budget, audit, cancellation, and approval requirements.

## 3. MCP Direction

Adopt Client-first sequencing. Design a narrow Server contract in parallel as
documentation only. Do not expose a public MCP Server until tenant isolation,
scoped auth, metering, audit, revocation, prompt-injection defense, and output DLP
are proven through separately approved implementation evidence.

## 4. MCP Client Evaluation Order

1. Sandbox MCP client abstraction using synthetic data.
2. GitHub read-only connector evaluation.
3. Search/Grounding connector evaluation.
4. One document connector: Drive OR Notion.
5. One enterprise/private knowledge connector later.

This is an evaluation sequence, not vendor approval, activation, or a promise to
support any named connector.

## 5. MCP Server v1 Boundary

Allowed for evaluation:

- Read-only grounded knowledge lookup with citations.
- Bounded Prompt Enhancer.
- Read-only Studio job status.
- Read-only approved result references.
- One schema-defined low-risk internal Skill.

Forbidden in v1:

- Payment or withdrawal.
- Wallet signing.
- Admin operations.
- Raw secret access.
- Raw conversation export by default.
- Arbitrary command execution.
- Unrestricted browsing.
- Cross-tenant search.
- High-risk Agent execution.

## 6. Early Product Skill Shortlist

### 1. Persian-aware Web Search and Citation Assistant

- **Integration mode:** internal Product Skill.
- **v1 permission boundary:** approved search/retrieval only; no authenticated
  browsing or arbitrary browser control.
- **Required security gate:** source policy, prompt-injection defense, citations,
  output DLP, and configured cost controls.
- **Out of scope:** arbitrary browser control and provider account access.

### 2. Product Photography Prompt Enhancer

- **Integration mode:** internal Product Skill.
- **v1 permission boundary:** draft transformations and prompts only.
- **Required security gate:** consent, image safety review, and output policy.
- **Out of scope:** deceptive edits and automatic marketplace publication.

### 3. SEO and Landing-page Content Brief

- **Integration mode:** internal Product Skill.
- **v1 permission boundary:** reviewable draft content only.
- **Required security gate:** no direct CMS write scope and citations for research.
- **Out of scope:** automatic publishing and ranking guarantees.

### 4. GitHub Read-only Code Review Assistant

- **Integration mode:** external MCP connector.
- **v1 permission boundary:** read-only approved repository context.
- **Required security gate:** scoped OAuth, repository allowlist, audit, and no
  merge, deploy, workflow-dispatch, or secret access.
- **Out of scope:** pull-request writes and administrative repository actions.

### 5. Document Summarization and Extraction

- **Integration mode:** internal Product Skill.
- **v1 permission boundary:** tenant-scoped reading and bounded extraction.
- **Required security gate:** file scanning, tenant isolation, output DLP, and no
  raw export by default.
- **Out of scope:** cross-tenant retrieval and unrestricted sharing.

## 7. Agent Framework Evaluation

These are evaluation candidates, not adopted dependencies.

Primary evaluation:

- LangGraph for state, checkpoint, and approval patterns.
- PydanticAI for typed contracts.
- LlamaIndex for retrieval and citation patterns.

Secondary research:

- LangChain tool abstractions behind platform policy wrappers.
- AutoGen handoff patterns in a synthetic-data sandbox.

Do not introduce multiple overlapping Agent frameworks into production without an
Architecture Decision Record and dependency-cost analysis.

## 8. Ready-Made Agent Policy

No ready-made autonomous Agent is approved for product runtime v1. SWE-agent,
OpenHands, Aider, GPT Engineer, AutoGPT, and similar projects remain research or
watchlist candidates only.

Any evaluation requires a disposable sandbox, synthetic data, no production
credentials, network allowlist, no merge or deploy authority, and human review of
every consequential output.

## 9. Deferred or Rejected Capabilities

Defer:

- Social auto-publishing.
- Payment write actions.
- Arbitrary browser control.
- Arbitrary script execution.
- Autonomous customer contact.
- Autonomous deployment.
- Third-party Agent Marketplace.

Reject for v1:

- Cross-tenant search.
- Unrestricted shell.
- Secret inheritance.
- Automatic spending.
- Autonomous PR merge.
- Raw private conversation access by default.

## 10. Implementation Dependency Order

Future work should use small implementation PRs:

1. MCP client interface and synthetic test server.
2. Connector manifest and intake schema.
3. OAuth and credential-vault abstraction.
4. One read-only connector.
5. MCP metering, audit, and revocation.
6. Internal Product Skill registry.
7. First bounded Persian Skill.
8. Agent framework evaluation spike.
9. One bounded internal Agent workflow.
10. Public MCP Server proof-of-concept later.

Core product MVP work may proceed before these integrations. Each item requires its
own acceptance criteria, security review, and owner decision.

## 11. Owner Approval Checklist

- [ ] MCP Client-first sequencing accepted.
- [ ] Initial connector order accepted.
- [ ] MCP Server v1 boundary accepted.
- [ ] Five early Skills accepted.
- [ ] Agent framework evaluation order accepted.
- [ ] No ready-made runtime Agent in v1 accepted.
- [ ] Deferred/rejected list accepted.
- [ ] Implementation sequencing accepted.

## 12. Open Decisions

- Drive versus Notion as first document connector.
- GitHub connector timing.
- OAuth implementation choice.
- MCP hosting model.
- Public registry publication timing.
- LangGraph versus PydanticAI spike order.
- Skill monetization.
- Connector credit and metering policy.

## Related Documents

- MCP research: [MCP_BIDIRECTIONAL_ARCHITECTURE_AND_ECOSYSTEM.md](../research/MCP_BIDIRECTIONAL_ARCHITECTURE_AND_ECOSYSTEM.md)
- Skills research: [SKILLS_LANDSCAPE_RESEARCH.md](../research/SKILLS_LANDSCAPE_RESEARCH.md)
- Agents research: [AGENTS_LANDSCAPE_RESEARCH.md](../research/AGENTS_LANDSCAPE_RESEARCH.md)
- Extensibility: [EXTENSIBILITY_MCP_AND_SKILLS.md](../architecture/EXTENSIBILITY_MCP_AND_SKILLS.md)
- Agent security: [AGENT_SECURITY_MODEL.md](../security/AGENT_SECURITY_MODEL.md)
- Third-party review: [THIRD_PARTY_AGENT_REVIEW.md](../security/THIRD_PARTY_AGENT_REVIEW.md)
- Prompt injection: [PROMPT_INJECTION_DEFENSE.md](../security/PROMPT_INJECTION_DEFENSE.md)
