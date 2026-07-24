# Agent Security Model

**Purpose:** Define security model for Agents that perform work with tools, browsing, and external APIs.

**Status:** Draft - Structure Only

**Note:** This is a structure-only stub. Final agent security model will be completed in later PRs.

## Scope

This document will cover:

- Agent vs Role distinction: Agent performs work with tools, must have permissions, budgets, safety controls, auditability
- Permission model: allowed, forbidden, approval-required, absolutely forbidden NO-GO
- Tool allowlisting: web_search, file_reader, image_generation_api, telegram_send, etc. must be declared per agent
- Budget and rate limiting: per execution, per day, per user, symbolic CONFIGURED_LIMIT placeholders
- Input/output validation for tool calls
- Audit logging: metadata only by default, no raw sensitive prompts, content_fingerprint DISABLED_BY_DEFAULT, fingerprint_method APPROVED_KEYED_HMAC_ONLY_IF_REQUIRED
- Approval gates: publishing, spending, contacting customers, bulk messages, pricing, config, merge, deploy require human approval
- Rollback and error handling

Final policy will require security and engineering review.

## Linkage

- Security Index: [README.md](README.md)
- Agent Plugin and Execution: [../architecture/AGENT_PLUGIN_AND_EXECUTION_SYSTEM.md](../architecture/AGENT_PLUGIN_AND_EXECUTION_SYSTEM.md)
- Agent Permission Model: [../agents/AGENT_PERMISSION_MODEL.md](../agents/AGENT_PERMISSION_MODEL.md)

## Status

Draft - Structure Only. Will be completed later.
