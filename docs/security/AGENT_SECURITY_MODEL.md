# Agent Security Model

**Version:** v0.1.0

**Date:** 2026-07-24

**Status:** Proposed Architecture - Pending Owner Approval and Implementation

**Document Owner:** Security Architect

**Purpose:** Define agent sandboxing, tool allowlists, permission boundaries,
network allowlists, budgets, human approval gates, agent isolation, and secret
isolation.

**Note:** Implementation Evidence: This documentation PR does not prove that the described controls are implemented, tested, deployed, or
production-ready. Code, automated tests, deployment evidence, and security verification remain the authoritative implementation evidence.

## Purpose

Define how Agents that perform work are secured.

## In Scope

- Agent sandboxing:
  - Agents run with least privilege, isolated from other users' data
  - No direct commit to main, no force-push, no history deletion
- Tool allowlists:
  - web_search (approved official sources for immigration)
  - file_reader, image_generation_api, telegram_send
  - knowledge_retrieval, embedding, LLM
  - Must be declared per agent in permissions and tools list
- Permission boundaries:
  - Allow, forbid, approval-required per AGENT_PERMISSION_MODEL
  - Absolutely forbidden NO-GO (ToS bypass, geographic/sanctions/KYC bypass,
    fake identities, sharing unauthorized credentials, CSAM, non-consensual
    imagery, deepfake without consent, claiming professional authority)
- Network allowlists:
  - For Deep Research and Immigration Research Agents, may browse approved
    current official government and embassy sources
  - Respect robots.txt, no scraping violating ToS
- Budgets:
  - Per execution max credits CONFIGURED_LIMIT
  - Per day max cost CONFIGURED_LIMIT
  - Per user spend limit CONFIGURED_LIMIT
  - Rate limit CONFIGURED_LIMIT
  - Exact values are Open Decisions requiring product/finance/trust review
- Human approval gates:
  - Publishing public content, spending money, contacting customers
  - Bulk Telegram broadcast, pricing/config changes, merge/deploy, API keys,
    persona sensitive edits, campaigns, refunds above threshold
- Agent isolation:
  - User data isolation (own data only), no cross-user access
  - Pseudonymous identifiers in audit logs, no raw sensitive prompts
- Secret isolation:
  - Telegram bot tokens encrypted at rest, provider keys via abstraction
  - No secret in logs, HMAC fingerprint secret protected, env-specific,
    versioned, rotatable, content_fingerprint DISABLED_BY_DEFAULT

## Per-Run Execution Limits

Require independently configurable limits for:

- Maximum execution duration: CONFIGURED_AGENT_MAX_DURATION
- Maximum iterations: CONFIGURED_AGENT_MAX_ITERATIONS
- Maximum tool calls: CONFIGURED_AGENT_MAX_TOOL_CALLS
- Maximum model tokens: CONFIGURED_LIMIT (input/output)
- Maximum credits/cost: CONFIGURED_LIMIT per run
- Maximum network requests: CONFIGURED_LIMIT
- Maximum input and output bytes: CONFIGURED_LIMIT
- Maximum files processed: CONFIGURED_LIMIT
- Cancellation deadline: CONFIGURED_LIMIT (time after which cancellation allowed)
- Hard termination deadline: CONFIGURED_LIMIT (time after which forced termination)

All limits must use CONFIGURED_* placeholders, not invented numbers.

## Loop and Runaway Prevention

Require:

- Maximum step and iteration enforcement: check against
  CONFIGURED_AGENT_MAX_ITERATIONS
- Repeated tool-call detection: same tool with same args repeatedly
- Repeated state detection: agent returns to same state without progress
- Cycle detection: state graph cycle detection
- Non-progress detection: no new information, no progress toward goal
- Budget exhaustion termination: stop when credits/cost exceeds
  CONFIGURED_LIMIT
- Timeout termination: stop when execution duration exceeds
  CONFIGURED_AGENT_MAX_DURATION
- Manual cancellation: user or admin can cancel running agent, audit logged
- Security Agent cancellation authority: Security Agent may cancel suspicious
  agent execution, apply emergency rate limits, quarantine
- Safe partial-result handling: return partial results if available, no raw
  sensitive content, audit metadata only
- No automatic unlimited retry loops: retry must have max retries
  CONFIGURED_LIMIT, backoff, human approval for high-risk retries

## Secret and Environment Isolation

Explicitly require:

- Agents never inherit the full application environment
- No full environment variable exposure (e.g., no DATABASE_URL, no SECRET_KEY,
  no provider API keys in env)
- No long-lived platform keys inside Agent runtime (only short-lived scoped
  credentials)
- Brokered, scoped, short-lived credentials: secrets manager issues short-lived
  credential for specific tool, e.g., Telegram bot token for telegram_send only
- Independent revocation: agent credential can be revoked without affecting
  platform, immediate revocation
- Default-deny secret access: agent has no secret access unless explicitly
  allowed in manifest and approved
- No secrets in prompts, outputs, logs, traces, or crash reports: no raw API
  keys, secrets, tokens, no provider secret in prompts, logs, model output,
  client code
- Secret access recorded as metadata without recording the secret itself
  (e.g., log secret_id, not secret value, audit trail)

## Structured Input, Output, and Tool Calls

Require:

- Versioned schemas: input schema version, output schema version, tool-call
  schema version, e.g., v1.0.0
- Input validation: validate input against schema before execution, reject
  unexpected fields, size and type limits
- Output validation: validate output against schema before returning to user
  or passing to next tool, reject unexpected fields
- Tool-call schema validation: tool calls must match strict allowlist schema,
  parameters validated before execution, tool output validated before passed
  back to model
- Rejection of unexpected fields: unknown fields in input/output/tool calls
  must be rejected, not ignored
- Size and type limits: max input bytes CONFIGURED_LIMIT, max output bytes
  CONFIGURED_LIMIT, type checks (string, integer, boolean, etc.)
- No arbitrary command execution from model-generated text: no shell evaluation
  of model output, no eval, no exec, no system call with model-generated args
- No shell evaluation of model output: model output must never be passed to
  shell, must be treated as untrusted
- No model output alone authorizes a sensitive action: sensitive actions
  (spending, publishing, contacting customers, deleting data) require human
  approval, not just model output
- Provenance and execution ID on structured results: result includes source,
  trust level, execution id, agent id, timestamp, not raw sensitive content

## Agent Termination and Failure Behavior

Require:

- Fail closed for unauthorized actions: if agent attempts forbidden action,
  fail closed, log security event, no partial execution of forbidden action
- Graceful cancellation where safe: cancel running agent, release resources,
  refund unused reservation if applicable, audit logged
- Forced termination where necessary: hard termination deadline
  CONFIGURED_AGENT_MAX_DURATION, kill process, no raw sensitive content in
  termination log
- Reserved credit settlement/refund behavior after failure: if agent fails
  before settlement, release reservation, no debit, idempotent; if fails after
  partial execution with provider-billed cost, apply approved refund policy
- Audit metadata without raw sensitive content: log agent_id, execution id,
  tool names, provider/model ids, token counts, cost, timestamps, approval
  records, result status, error category without sensitive content, rollback
  reference, no raw prompts

## Out of Scope

- Final budget numbers and exact permission matrix
- Implementation code (future PRs)

## Related Documents

- Security Index: [README.md](README.md)
- Agent Plugin and Execution: [../architecture/AGENT_PLUGIN_AND_EXECUTION_SYSTEM.md](../architecture/AGENT_PLUGIN_AND_EXECUTION_SYSTEM.md)
- Permission Model: [../agents/AGENT_PERMISSION_MODEL.md](../agents/AGENT_PERMISSION_MODEL.md)
- Human Approval Gates: [../agents/HUMAN_APPROVAL_GATES.md](../agents/HUMAN_APPROVAL_GATES.md)
- Logging and Monitoring: [LOGGING_AND_MONITORING.md](LOGGING_AND_MONITORING.md)

## Open Decisions

- Exact tool allowlist per agent type (business, research, Telegram, studio)
- Budget and rate limit numbers
- Approval gate thresholds
- Owner approval required

## Planned Completion Stage

Phase 1 - Agent Security

## Status Note

Proposed Architecture - Pending Owner Approval and Implementation. Implementation and verification are separate future work. Open Decisions remain
unresolved until explicitly approved.
