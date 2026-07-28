# Skills Landscape Research

**Version:** v0.1.0

**Date:** 2026-07-28

**Status:** Proposed Architecture / Research - Pending Owner Approval

**Document Owner:** Product / AI Platform / Security

**Purpose:** Evaluate granular, non-autonomous tools and reusable capabilities for
a future Persian-first Skills Marketplace. This is research only. It does not
enable providers, publish skills, or demonstrate implementation.

## 1. Executive Summary

A Skill is a bounded capability with a defined input, output, permission model,
and failure mode. It differs from an Agent: a Skill should not independently plan
an open-ended workflow, choose an unrestricted sequence of tools, or escalate its
own permissions. A Skill may be invoked by a user, a workflow, or an approved
Agent, but its own contract should remain narrow and testable.

For this platform, the initial marketplace should favor read-only or draft-only
Skills that deliver visible value to Persian-speaking users and businesses. Skills
with publishing, spending, data export, messaging, browser control, database
mutation, or account changes need stronger approval and isolation boundaries.

The market signal is clear but not sufficient for approval: tool ecosystems make
it easy to describe callable functions, while marketplace listings make discovery
easy. Neither is security evidence. Every third-party Skill must remain untrusted
until it passes intake, source review, license review, sandboxing, and applicable
privacy review.

Primary sources, accessed 2026-07-28:

- OpenAI function calling guide: https://platform.openai.com/docs/guides/function-calling
- Anthropic tool use guide: https://docs.anthropic.com/en/docs/build-with-claude/tool-use
- LangChain tools guide: https://python.langchain.com/docs/concepts/tools/
- MCP architecture: https://modelcontextprotocol.io/docs/learn/architecture
- Existing platform extensibility policy: [EXTENSIBILITY_MCP_AND_SKILLS.md](../architecture/EXTENSIBILITY_MCP_AND_SKILLS.md)

## Skill Terminology and Ecosystem Boundaries

### Product Skill

A Product Skill is a platform-owned, bounded product capability. It has a
versioned input/output contract, permission and side-effect classification, risk
class, cost policy, evaluation evidence, owner, and lifecycle state. A Product
Skill is the platform's approval and runtime unit, regardless of whether its
implementation later uses a provider tool, an MCP connector, or an imported
package format.

### Agent Skills Package

An Agent Skills Package is a filesystem-based package following an Agent
Skills-style format. It typically contains `SKILL.md`, YAML frontmatter,
instructions, optional scripts, optional references, and optional assets.

Accepting a package format does not mean executing unreviewed scripts. Package
instructions are content to review, not authority to run code, install dependencies,
or access user data.

### Provider Tool or Function Calling

A Provider Tool or Function Calling definition is a provider-specific schema that
allows a model to request an application function. The application remains
responsible for authorization, validation, execution, and error handling. It is
not a portable Skill marketplace format, and model output never authorizes the
action by itself.

### MCP Tool

An MCP Tool is a capability exposed by an MCP Server. It is a protocol-exposed
capability, not automatically an approved Product Skill. Registry presence is
discovery evidence only. MCP intake and Skill intake must share source, license,
sandbox, permission, and security-review controls.

### Agent

An Agent is a multi-step workflow actor that may invoke approved Skills. An Agent
is not a Skill and requires stronger run, permission, budget, audit, cancellation,
and human-approval controls.

| Concept | Unit | May contain code | Autonomous planning | Discovery mechanism | Approval required |
|---|---|---|---|---|---|
| Product Skill | Platform capability | Platform-controlled | No | Platform catalog | Yes |
| Agent Skills package | Filesystem package | Optional scripts | No by format alone | Repository or package source | Yes |
| Provider tool/function | Provider schema | Application handler | No | Provider API configuration | Yes |
| MCP Tool | Server capability | Server-defined | No by protocol alone | MCP server or registry | Yes |
| Agent | Multi-step actor | May invoke code/tools | Yes, bounded | Platform catalog | Yes, stronger gates |

## Existing Skill Formats and Official Collections

The following sources are primary publisher sources and are research inputs only.
Their repositories, examples, or documentation must not be treated as a blanket
security or commercial-use approval. Access date for every entry: 2026-07-28.

### Agent Skills Open Specification

Publisher: Agent Skills community project. Source:
https://github.com/agentskills/agentskills

The project describes a portable, filesystem-oriented Skill format centered on a
`SKILL.md` file and metadata/instructions. Optional package content can include
scripts, references, and assets. Portability is a format goal, but runtime support
and safety remain host-specific. License status must be verified at the selected
path and commit before adoption.

### Anthropic Public Skills Repository

Publisher: Anthropic. Source: https://github.com/anthropics/skills

The public repository provides Skill examples and related materials. Its exact
format, required files, optional executable content, and license must be checked
at the chosen directory and revision. Anthropic document Skills such as DOCX,
PDF, PPTX, and XLSX are source-available references and must not automatically be
classified as open source or commercially reusable.

### OpenAI Public Skills Repository

Publisher: OpenAI. Source: https://github.com/openai/skills

The public repository is a primary research source for an official publisher's
Skill collection. Its required files, optional executable content, license, and
portability must be verified at the exact selected path, version, and commit.

| Ecosystem | Publisher | Format | License status | Executable content | Portability | Platform posture |
|---|---|---|---|---|---|---|
| Agent Skills spec | Agent Skills | Package with `SKILL.md` | Verify exact source | Optional scripts | Portable goal | Research only |
| Anthropic Skills | Anthropic | Skill directories | Verify path | Optional | Host varies | No automatic import |
| OpenAI Skills | OpenAI | Skill directories | Verify path | Optional | Host varies | No automatic import |

### License Boundary

Do not assume one license applies to every directory in a Skill repository.
Anthropic example Skills may use Apache-2.0 or another stated license. Anthropic
document Skills such as DOCX, PDF, PPTX, and XLSX are source-available references
and must not automatically be classified as open source or commercially reusable.
Every adopted Skill must be reviewed at the exact path, version, commit, and
license file. UNKNOWN license means HOLD or REJECT until clarified. Do not claim
commercial compatibility without exact evidence.

## Skill Package Security Boundary

- Instructions are untrusted content.
- Bundled scripts are untrusted executable code.
- References and assets may contain malicious content.
- No install-time script execution.
- No automatic dependency installation.
- No access to production secrets or user data during intake.
- Script execution only in an approved sandbox.
- Network denied by default.
- Immutable version/checksum approval.
- Re-review after any content, script, dependency, or permission change.
- Skill description text is not security evidence.

The applicable security controls are documented in
[THIRD_PARTY_AGENT_REVIEW.md](../security/THIRD_PARTY_AGENT_REVIEW.md),
[PROMPT_INJECTION_DEFENSE.md](../security/PROMPT_INJECTION_DEFENSE.md), and
[AGENT_SECURITY_MODEL.md](../security/AGENT_SECURITY_MODEL.md). This document
does not replace those controls.

## 2. High-Demand Skill Categories

### SEO and Content Operations

Candidate Skills include keyword clustering, Persian title and meta-description
drafts, internal-link suggestions, structured-content checks, citation extraction,
and search-intent classification. These are valuable because small businesses
need repeatable content operations but should review external publication.

- **User value:** faster first drafts and clearer SEO workflows.
- **Revenue value:** suitable for a paid workspace tier or credit-metered draft
  generation, subject to product approval.
- **Risk:** Medium for analysis and drafts; High for publishing or changing live
  site metadata.
- **Early posture:** draft-only, no direct CMS write access.

### Product Photography and Studio Workflows

Candidate Skills include background-removal requests, image resizing, listing
caption drafts, product attribute extraction, accessibility alt text, and quality
checklists. Media inputs may contain personal data, copyrighted material, or
sensitive business information.

- **User value:** practical marketplace and social-commerce support.
- **Revenue value:** studio credits and business workflow plans.
- **Risk:** Medium for transformations; High for likeness-sensitive edits,
  deceptive advertising, or automatic public posting.
- **Early posture:** upload-to-draft workflow with consent and clear output labels.

### Web Research and Extraction

Candidate Skills include source discovery, page-to-structured-notes conversion,
citation capture, comparison tables, and change monitoring. Web content is
untrusted input and can contain prompt injection, malicious instructions, or
misleading claims.

- **User value:** current research with traceable sources.
- **Revenue value:** research bundles and business intelligence workflows.
- **Risk:** Medium for read-only retrieval; High for browser automation or broad
  scraping that may violate terms, privacy rules, or network controls.
- **Early posture:** allowlisted search and retrieval with citations; no arbitrary
  browser actions or bypass of source restrictions.

### Database Querying and Analytics

Candidate Skills include read-only query templates, natural-language-to-reviewed
SQL drafts, dashboard explanation, schema discovery, and CSV quality checks.

- **User value:** reduces friction for business reporting.
- **Revenue value:** enterprise analytics workflows.
- **Risk:** High because data may be confidential and generated queries may expose
  other tenants or mutate data.
- **Early posture:** synthetic data and read-only approved views only; no direct
  production database access.

### Calendar and Task Synchronization

Candidate Skills include availability summaries, suggested event drafts, task
extraction, agenda preparation, and conflict detection.

- **User value:** recurring personal and team productivity.
- **Revenue value:** business workspace retention.
- **Risk:** Medium for read access; High when creating, deleting, or inviting
  attendees to calendar events.
- **Early posture:** read-only summaries and user-confirmed draft events.

### Social Media and Communication

Candidate Skills include caption drafts, content calendars, comment summaries,
brand-style checking, and reply suggestions. Posting, direct messaging, or bulk
broadcasting creates reputational, policy, and consent risk.

- **User value:** practical sales and marketing operations.
- **Revenue value:** business plan differentiation.
- **Risk:** Medium for drafts; High for publishing, messaging, or bulk actions.
- **Early posture:** draft-only; separate human approval for any external post.

### Documents, Knowledge Bases, and Translation

Candidate Skills include Persian document summarization, extraction of actions,
redaction suggestions, glossary enforcement, bilingual formatting, and grounded
knowledge-base answers with citations.

- **User value:** especially high for Persian-first workflows and mixed Persian /
  English business material.
- **Revenue value:** broad individual and business utility.
- **Risk:** Medium to High depending on source classification and export scope.
- **Early posture:** tenant-scoped, citation-aware, no raw sensitive export by
default.

### Customer Support and Commerce Assistance

Candidate Skills include FAQ draft generation, product catalog normalization,
order-status explanation, support-ticket routing, and policy-compliant response
drafts. They must not impersonate a human, promise outcomes, or initiate refunds.

- **User value:** helps small teams respond consistently.
- **Revenue value:** business operations plan.
- **Risk:** Medium for drafts; High for account, refund, or payment action.
- **Early posture:** draft replies and routing recommendations only.

## 3. Tool Ecosystems

### OpenAI Function Calling

OpenAI documents function calling as a way for a model to request an application
function with a schema-defined interface. The application, not the model, decides
whether to execute the function and must validate arguments and results.

**Implication:** use explicit JSON schemas, server-side authorization, and tool
allowlists. A model-generated argument must never bypass ownership, rate, credit,
or approval checks.

Source: https://platform.openai.com/docs/guides/function-calling
Accessed: 2026-07-28.

### Anthropic Tool Use

Anthropic documents tools as schema-described capabilities supplied to a model,
with the client application responsible for executing calls and returning results.
The tool contract is useful for bounded Skills but does not remove the need for
input validation or policy enforcement.

**Implication:** tools should have a human-readable purpose, narrow parameters,
strict schemas, and explicit side-effect classification.

Source: https://docs.anthropic.com/en/docs/build-with-claude/tool-use
Accessed: 2026-07-28.

### LangChain Tools

LangChain describes tools as interfaces that an agent or chain can call. Its
abstraction can accelerate prototyping, but framework availability is not a
security boundary or a reason to allow arbitrary tools in this platform.

**Implication:** if evaluated, wrap each tool behind platform-owned authorization,
tenant isolation, audit, and timeout policies.

Source: https://python.langchain.com/docs/concepts/tools/
Accessed: 2026-07-28.

### MCP Tools, Resources, and Prompts

MCP provides a client/server protocol vocabulary for tools, resources, and
prompts. It can be one integration boundary for Skills, but a Skill is a product
contract and an MCP server is a protocol endpoint; they are not synonyms.

**Implication:** an MCP-discovered tool is untrusted until reviewed. It cannot be
installed, invoked, or given credentials simply because a registry lists it.

Source: https://modelcontextprotocol.io/docs/learn/architecture
Accessed: 2026-07-28.

### Integration Comparison

| Ecosystem | Strength | Limitation | Platform posture |
|---|---|---|---|
| OpenAI function calling | Familiar schema-based calls | Application still owns execution safety | evaluate as adapter pattern |
| Anthropic tool use | Clear tool schemas and client execution | Provider-specific integration surface | evaluate as adapter pattern |
| LangChain tools | Broad ecosystem and abstractions | Framework tool is not a trust signal | sandboxed evaluation only |
| MCP | Interoperable client/server boundary | Registry discovery is not approval | controlled connector boundary |
| Internal Skills | Product-owned contracts | Requires lifecycle investment | preferred early foundation |

## 4. Relevance to a Persian-First Workspace

Persian-first value is not only translation. It includes right-to-left presentation,
local business wording, mixed Persian/English source handling, culturally suitable
marketing drafts, and careful handling of Iran-related legal, sanctions, payment,
and service-availability constraints.

High-value early research targets are:

1. Persian SEO drafts and content-quality checks.
2. Product listing photography and caption drafts.
3. Grounded research with Persian summaries and source citations.
4. Document extraction, bilingual glossary checks, and redaction suggestions.
5. Customer-support response drafts with explicit review before sending.
6. Calendar, task, and business-admin summaries without automatic writes.

The platform must not imply that a language Skill provides legal, immigration,
medical, financial, tax, or professional advice. For Persian right-to-left output,
acceptance tests should cover Unicode normalization, mixed-direction punctuation,
numerals, dates, link rendering, copy/paste behavior, and accessible layout.

## 5. Risk Classification

| Class | Typical access | Examples | Required posture |
|---|---|---|---|
| Low | Local transformation or public read | formatting, summarization, alt text | schema validation, audit metadata |
| Medium | Tenant-scoped read or draft write | KB search, caption draft, calendar draft | consent, tenant checks, DLP |
| High | External write, secrets, private data, money | posting, database write, messaging | human approval, scoped auth, sandbox |
| Forbidden early | Irreversible or privileged action | withdrawals, admin grants, raw export | do not expose |

Read access is not automatically low risk. Reading a private conversation,
customer database, or credential store is high risk even when no mutation occurs.
Write access is not automatically prohibited, but it requires an explicit action
contract, user confirmation, idempotency, rollback planning where possible, and
an audit record.

## 6. Integration Recommendations for Our Platform

### Recommended Foundations

- Define a platform Skill manifest with owner, version, source, input/output
  schema, side-effect class, data classes, scopes, cost policy, and revocation
  state.
- Route every Skill through backend authorization rather than client-side direct
  provider calls.
- Separate draft generation from public publication, direct messaging, spending,
  and other consequential actions.
- Use managed secret storage for connector credentials and issue only scoped,
  short-lived runtime references where approved.
- Meter external calls with documented credit reservation and reconciliation;
  use CONFIGURED_SKILL_EXECUTION_TIMEOUT and CONFIGURED_SKILL_MAX_CALLS where
  future operational policy needs values.
- Record metadata-only audit events and apply output DLP before user or external
  client delivery.

### Candidate Sequence

1. Internal text and document Skills with no external write path.
2. Grounded search/retrieval Skill with source policy and citations.
3. Media draft Skills with consent and content-safety checks.
4. One read-only, low-risk external connector after full intake.
5. User-confirmed draft creation for calendar or social content only after the
   authorization and revocation experience is proven.

### Security and Product Gates

Every imported or marketplace Skill must follow the existing controls in
[THIRD_PARTY_AGENT_REVIEW.md](../security/THIRD_PARTY_AGENT_REVIEW.md) and
[PROMPT_INJECTION_DEFENSE.md](../security/PROMPT_INJECTION_DEFENSE.md). It must
not receive unrestricted network access, full environment variables, raw secrets,
or cross-tenant data.

### Open Questions

- Which skills justify a marketplace listing versus an internal workflow?
- Which providers are legally and commercially available for intended users?
- What owner-approved credit model applies to each external call type?
- Which Skills can be evaluated with synthetic data first?
- What is CONFIGURED_SKILL_EXECUTION_TIMEOUT for each approved risk class?
- What is CONFIGURED_SKILL_MAX_CALLS for an approved execution?

## Related Documents

- MCP research: [MCP_BIDIRECTIONAL_ARCHITECTURE_AND_ECOSYSTEM.md](MCP_BIDIRECTIONAL_ARCHITECTURE_AND_ECOSYSTEM.md)
- Extensibility policy: [EXTENSIBILITY_MCP_AND_SKILLS.md](../architecture/EXTENSIBILITY_MCP_AND_SKILLS.md)
- Agent security: [AGENT_SECURITY_MODEL.md](../security/AGENT_SECURITY_MODEL.md)
- Third-party review: [THIRD_PARTY_AGENT_REVIEW.md](../security/THIRD_PARTY_AGENT_REVIEW.md)
- Prompt injection defense: [PROMPT_INJECTION_DEFENSE.md](../security/PROMPT_INJECTION_DEFENSE.md)
