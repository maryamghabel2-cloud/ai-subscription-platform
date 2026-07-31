# Agent Marketplace and Agent SDK

**Version:** v0.1.0

**Date:** 2026-07-29

**Status:** Proposed Architecture - Pending Owner Approval and Implementation

**Document Owner:** Architecture / Security / Marketplace

## 1. Purpose and Status

This is proposed architecture only. Agents are autonomous multi-step, planning,
tool-chaining actors distinct from the non-autonomous Skill Store. Execution must
pass through sandbox, Policy Gateway, and audit boundaries. This does not claim an
Agent Marketplace, SDK, runtime, or sandbox is implemented.

## 2. Scope Boundary vs Skill Store

| Aspect | Skill Store | Agent Marketplace |
|---|---|---|
| Autonomy | non-autonomous | autonomous multi-step |
| Planning | no | yes |
| Tool chaining | at most 1 bounded skill | multiple tools dynamic |
| Approval model | user initiates each run | agent runs under policy and gates |
| Risk profile | lower | higher |
| Review process | prompt injection and content | full third-party agent review |

## 3. Canonical Domain Concepts

- **Agent Listing:** catalog entry describing an installable agent version.
- **Agent Manifest:** machine-readable permissions and runtime declaration.
- **Agent Version:** immutable reviewed release or checksum target.
- **Agent Execution Context:** tenant, actor, task, data scope, and policy inputs.
- **Policy Gateway:** deterministic enforcement point before every tool action.
- **Sandbox Profile:** isolated runtime and resource policy.
- **Tool Allowlist:** manifest and policy-approved callable tools.
- **Human Approval Gate:** explicit actor decision for consequential action.
- **Audit Trail:** append-only metadata evidence of decisions and actions.
- **Revocation Record:** record disabling an agent, tool, credential, or version.
- **Quarantine Record:** record isolating a suspicious listing or execution.
- **Rollback Target:** previous approved version eligible for restoration.

## 4. Agent Types and Risk Classes

| Risk Class | Examples | Approval |
|---|---|---|
| Low | read-only research, FAQ, content draft | L2 draft |
| Medium | draft with external write after approval | L3 approval write |
| High | code execution, browser, payment, external API side effects | L3 minimum, some forbidden v1 |

Risk class and autonomy level are separate. A low-risk listing does not receive
higher autonomy automatically.

## 5. Seller Developer Verification

Seller or developer verification requires identity verification, portfolio and
sample Agents, security history review, supply-chain/dependency review, and license
compatibility. Verification is not permanent approval; material updates require
re-review and may result in suspension or revocation.

## 6. Agent Manifest and Permissions

Every Agent listing declares:

- listing_id
- agent_id
- version
- author_id
- publisher_type
- risk_class
- required_tools
- read_permissions
- write_permissions
- network_access_policy (denied by default)
- data_classes_accessed
- max_cost_per_run
- max_duration
- max_iterations
- human_approval_requirements
- sandbox_profile
- license
- provenance_checksum
- security_review_status

The manifest cannot self-escalate permissions. Workspace installation requires
admin approval of declared permissions and version pinning by default.

## 7. Marketplace Discovery and Installation

Discovery supports category, risk, language, and price filters. A buyer reviews
the manifest before installation, approves permissions, and installs a reviewed
version to a workspace. Permission changes require re-approval. Listings remain
untrusted until certification and do not receive cross-workspace access.

## 8. Sandbox and Execution Environment

Every Agent runs in an isolated sandbox. Third-party code does not share a
filesystem with the core platform. Network is denied by default, with explicit
allowlists. Resource controls cover CPU, memory, disk, and time according to
approved policy. A kill switch and forced termination are required.

No secret inheritance is allowed. Agents receive only brokered, short-lived,
scoped credentials where approved. No cross-tenant data access is allowed. Sandbox
technology choice remains an Open Decision.

### Certification Prerequisites

Before an Agent can be listed, its exact version must have a provenance source,
immutable checksum, license evidence, dependency inventory, declared tools, and
sandbox profile. Evaluation uses synthetic data and no production credentials.

### Execution Preconditions

A run starts only after tenant resolution, workspace install validation, manifest
version validation, permission checks, budget reservation where applicable, and
Policy Gateway initialization. A cancelled, quarantined, suspended, or revoked
version cannot start a new run.

### Failure Boundaries

A sandbox failure must fail closed for sensitive actions. A tool denial returns a
safe policy outcome, not a bypass path. Partial results are explicitly labeled and
never treated as authorization for later actions.

## 9. Policy Gateway and Tool Allowlist

Every tool call passes through Policy Gateway. Only manifest-declared and
policy-approved tools are allowed, with runtime enforcement rather than declaration
alone. Every invocation, policy decision, cost, quota outcome, and blocked call is
recorded as metadata.

Tool results are sanitized before return to agent code. Prompt-injection defenses
and DLP apply to tool input/output. Agent code never receives direct provider keys.

> **Document continues in the next commit with: Human Approval Gates,**
> **Audit and Monitoring, Revocation, Rights and Revenue, Agent SDK,**
> **Persian Requirements, Implementation Sequence, and Open Decisions.**

### Marketplace Boundary

Catalog discovery is not runtime permission. Installing a listing binds only the
reviewed version, manifest, and approved workspace scope. Publisher reputation does
not bypass Policy Gateway or sandbox enforcement.

### Related Documents

- [AGENT_SECURITY_MODEL.md](../security/AGENT_SECURITY_MODEL.md)
- [THIRD_PARTY_AGENT_REVIEW.md](../security/THIRD_PARTY_AGENT_REVIEW.md)
- [SECURITY_AGENT_RUNTIME.md](../security/SECURITY_AGENT_RUNTIME.md)
- [PROMPT_MARKETPLACE_AND_SKILL_STORE.md](PROMPT_MARKETPLACE_AND_SKILL_STORE.md)
