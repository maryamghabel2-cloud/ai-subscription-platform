# Agents Landscape Research

**Version:** v0.1.0

**Date:** 2026-07-28

**Status:** Proposed Architecture / Research - Pending Owner Approval

**Document Owner:** Product / AI Platform / Security

**Purpose:** Evaluate autonomous, multi-step agent frameworks and ready-made agent
projects for a future Agent Marketplace. This is research only. It does not
enable repositories, frameworks, credentials, remote execution, or autonomous
operations in the platform.

## 1. Executive Summary

An Agent is a constrained workflow actor that can plan or iterate across multiple
steps, use approved tools, observe results, and stop under policy. It is not the
same as a single Skill. An Agent may use Skills, but it needs stronger authority,
budget, cancellation, audit, sandbox, and human-approval controls because errors
can compound across a multi-step run.

The ecosystem offers mature orchestration frameworks and highly visible ready-made
projects. Visibility, GitHub stars, demos, benchmarks, or marketplace presence are
interest signals only. They are not proof of secure behavior, license fit,
publisher identity, privacy posture, or suitability for Persian-language users.

For this platform, first evaluation should focus on framework patterns that support
bounded state, explicit tool schemas, cancellation, checkpoints, and human gates.
Ready-made autonomous coding or browser agents should remain sandbox research
subjects, not marketplace defaults. No third-party agent should receive broad
credentials, unrestricted network access, raw private conversations, or authority
to publish, spend, contact customers, merge, deploy, or administer the platform.

Sources in this document were accessed 2026-07-28. Licenses must be re-verified
at the exact repository commit or package version selected for any future intake.

## 2. Agent Frameworks

### Evaluation Method

Maturity is a qualitative research label, not a vendor guarantee. Learning curve
reflects expected platform-team integration effort. License entries are based on
public repository metadata or official documentation at the access date; use
UNKNOWN where that could not be safely confirmed from the research source.

| Framework | Primary use | License | Maturity signal | Learning curve | Platform assessment |
|---|---|---|---|---|---|
| LangChain | LLM application composition and tools | MIT | broad ecosystem | Medium | evaluate utility layer only |
| LangGraph | Stateful agent/workflow orchestration | MIT | widely documented graph model | Medium/High | shortlist for bounded workflows |
| AutoGen | Multi-agent conversation framework | MIT | Microsoft-origin ecosystem | Medium | watchlist for controlled patterns |
| CrewAI | Role-oriented multi-agent workflows | MIT | active community visibility | Low/Medium | sandbox evaluation only |
| LlamaIndex | Data and retrieval workflows | MIT | mature RAG ecosystem | Medium | shortlist for grounded workflows |
| Auto-GPT platform | Task execution concepts | MIT, verify exact edition | visible project | Medium/High | research only; high autonomy risk |

### LangChain and LangGraph

LangChain provides abstractions for models, tools, retrieval, and application
composition. LangGraph focuses on graph-like, stateful workflows and is relevant
where the platform needs explicit state transitions, durable checkpoints, bounded
loops, and an approval node.

Potential fit: a platform-owned workflow can model a research task as explicit
nodes rather than an unconstrained agent loop. The framework does not itself
supply tenant isolation, cost control, credential policy, or safe tools.

Sources:

- https://github.com/langchain-ai/langchain
- https://github.com/langchain-ai/langgraph
- https://langchain-ai.github.io/langgraph/

### AutoGen

AutoGen is a framework for multi-agent conversations and tool-using workflows.
Its patterns can be useful for comparing delegation, handoffs, and human-in-loop
control. Multi-agent conversation should not be adopted merely because it appears
natural in a demo; it increases prompt-routing, data-sharing, loop, and cost risk.

Potential fit: research the message-boundary and approval patterns with synthetic
data. Do not allow agents to grant one another permissions or share full context.

Sources:

- https://github.com/microsoft/autogen
- https://microsoft.github.io/autogen/

### CrewAI

CrewAI presents a role/crew model for multi-agent flows. The model may help
product teams explain specialized roles, but role labels do not enforce security.
Every delegated task needs an independent permission boundary and must preserve
tenant ownership through each handoff.

Potential fit: evaluate only for developer ergonomics in a sandbox. Require
explicit tool allowlists, run limits, cancellation, and a no-self-escalation rule.

Sources:

- https://github.com/crewAIInc/crewAI
- https://docs.crewai.com/

### LlamaIndex

LlamaIndex focuses on data frameworks, retrieval, indexing, and agent-related
workflows. It is relevant to grounded knowledge and source-aware responses, not a
reason to expose raw documents or allow an agent to treat retrieved text as a
trusted instruction.

Potential fit: evaluate retrieval patterns with citations, data classification,
provenance, and prompt-injection controls. Keep original documents tenant-scoped.

Sources:

- https://github.com/run-llama/llama_index
- https://docs.llamaindex.ai/

### Auto-GPT

Auto-GPT is a prominent autonomous-agent project and product family. Its
visibility demonstrates demand for delegated multi-step tasks, while also
illustrating why broad autonomy needs strong boundaries and review. The exact
license, project edition, and deployment component must be verified at intake.

Potential fit: no direct adoption recommendation. Use it as a research reference
for task decomposition, observability, and failure-mode analysis.

Sources:

- https://github.com/Significant-Gravitas/AutoGPT
- https://agpt.co/

## 3. Ready-Made Autonomous Agents

### Comparison Table

| Project / category | Focus | License | Maturity signal | Main risks | Platform posture |
|---|---|---|---|---|---|
| SWE-agent | Software engineering tasks | MIT, re-verify | academic/open-source lineage | code execution, repository writes | research sandbox only |
| OpenHands | Software development agent | MIT, re-verify | active project ecosystem | shell, network, code changes | research sandbox only |
| OpenDevin name/history | Predecessor naming context | UNKNOWN | project naming changed | stale assumptions | do not select by name |
| GPT Engineer | Code generation workflow | MIT, re-verify | visible open-source project | generated code and filesystem risk | watchlist only |
| BabyAGI | Task-loop prototype concepts | MIT, re-verify | historical visibility | unbounded loop and stale patterns | reject as runtime base |
| Research agents | Search/synthesis workflows | Varies | broad category | misinformation and injection | evaluate patterns, not brands |
| Browser agents | Web interaction workflows | Varies | broad category | SSRF, action, session theft | later only |
| Data-analysis agents | Query and analysis workflows | Varies | broad category | data leakage, query mutation | later only |

### SWE-agent

SWE-agent is associated with software-engineering task execution against code
repositories. It is useful as a case study for issue-to-patch workflows, but a
coding agent can alter files, run commands, consume tokens, and create supply-chain
risk. Any evaluation must use disposable repositories, synthetic or public test
issues, isolated runners, a network allowlist, and a human review before a patch
is accepted.

Sources:

- https://github.com/SWE-agent/SWE-agent
- https://swe-agent.com/

### OpenHands and OpenDevin Naming

OpenHands is an open-source software-development agent project. "OpenDevin" is a
historical project name in this ecosystem; naming alone is insufficient to identify
a current repository, version, publisher, or license. Future intake must use an
immutable source, exact publisher identity, and exact dependency lockfiles.

Potential evaluation requires a disposable sandbox with no platform secrets, no
production source control token, no direct deployment path, and no customer data.

Sources:

- https://github.com/All-Hands-AI/OpenHands
- https://www.all-hands.dev/

### GPT Engineer

GPT Engineer is a code-generation project. Code generation can be valuable for
internal developer workflows, but a generated patch is untrusted output and must
be tested, reviewed, scanned, and approved through normal repository controls.

Source: https://github.com/AntonOsika/gpt-engineer

### BabyAGI

BabyAGI is widely referenced for task-loop and autonomous-agent concepts. It is
not a recommended runtime foundation for this platform because simple autonomous
loops can obscure stop conditions, budgets, quality controls, and delegation
boundaries. Treat it as historical research, not a marketplace candidate.

Source: https://github.com/yoheinakajima/babyagi

### Research Agents

Research-agent products vary substantially. Their common risks are source quality,
citation fabrication, prompt injection in retrieved pages, confidential query
leakage, and accidental overstatement. The platform should evaluate a bounded
research workflow with source provenance and citations rather than adopt an
unverified "research agent" repository by category label.

## 4. Security and Isolation Risks

### Third-Party Repository Intake

Every external agent repository starts untrusted. Review must identify publisher,
immutable commit or release, license, dependency lockfiles, SBOM where available,
runtime, installation command, network destinations, tools, data classes,
credentials, and write side effects.

Do not infer trust from stars, forks, downloads, social-media mentions, or an
"official" appearing README. Those are discovery signals and can be manipulated.
The applicable platform process is in
[THIRD_PARTY_AGENT_REVIEW.md](../security/THIRD_PARTY_AGENT_REVIEW.md).

### Sandbox and Container Boundaries

Agent execution should use an isolated runtime appropriate to the risk class. A
container alone is not a complete control: it needs constrained mounts, no host
Docker socket, a non-root user where applicable, resource controls, a network
deny-by-default policy, secret isolation, and observable lifecycle controls.

For high-risk code, browser, or data agents, use disposable environments and
synthetic data first. Do not mount platform source, production credentials,
customer files, or unrestricted home directories into a candidate runtime.

### Network Isolation

Default network access should be denied. Approved egress destinations must be
explicitly allowlisted, logged as metadata, and revocable. Browser automation and
web retrieval add SSRF, redirect, download, cookie, session, and prompt-injection
risk. A model must not choose arbitrary internal network destinations.

### Authority and Human Gates

An Agent cannot grant itself permissions, extend its runtime, disable its audit
trail, or bypass owner approval. The platform's canonical authority tiers apply:
low-risk reversible containment, controlled automatic containment with notification,
and human-approved high-impact actions. See
[SECURITY_AGENT_RUNTIME.md](../security/SECURITY_AGENT_RUNTIME.md).

### Required Controls

- Explicit per-run limits using CONFIGURED_AGENT_MAX_DURATION,
  CONFIGURED_AGENT_MAX_ITERATIONS, CONFIGURED_AGENT_MAX_TOOL_CALLS, and
  CONFIGURED_AGENT_MAX_COST_CREDITS.
- Cancellation requested by an authorized user or operator, with audit logging.
- Structured tool schemas and server-side validation.
- Content provenance and prompt-injection defenses for every retrieved input.
- Output DLP and metadata-only logs by default.
- Immediate credential revocation on suspected compromise.
- Human approval for publishing, spending, contact, destructive change, merge,
  deployment, secret access, and other high-impact actions.

## 5. Persian Language Adaptation

Persian capability must be evaluated as an end-to-end workflow property. A model
can produce Persian text yet still fail at right-to-left layout, mixed English
identifiers, dates, digits, code blocks, URLs, tool arguments, and entity names.

Key challenges:

- Right-to-left rendering may reorder punctuation, parentheses, identifiers, and
  embedded English/Latin text.
- Persian requests often mix transliterated product names, local business terms,
  and English API names; tool routing must not assume a single script.
- Tool arguments require strict schemas and canonical identifiers rather than
  model-inferred free text.
- Dates, currencies, addresses, and phone-like strings need localized validation
  and privacy handling.
- Evaluation must distinguish fluent Persian prose from factual correctness,
  citation quality, safe refusal, and correct tool selection.

Recommended acceptance tests include Persian-only, English-only, and mixed-script
prompts; RTL UI snapshots; schema-valid tool arguments; safe handling of ambiguous
local terms; grounded citations; and human review of consequential drafts.

## 6. Shortlist for Platform Integration

### Frameworks to Evaluate First

1. **LangGraph patterns** for explicit state, checkpoints, and approval nodes.
2. **LlamaIndex patterns** for grounded, citation-aware knowledge workflows.
3. **LangChain tool abstractions** only behind platform-owned policy wrappers.
4. **AutoGen patterns** for controlled handoffs using synthetic data.
5. **CrewAI patterns** as a usability comparison, not a permission model.

These are research shortlists, not adoption decisions. License, version, security
advisories, privacy posture, and runtime compatibility require a later intake.

### Ready-Made Agent Posture

- SWE-agent: evaluate only in an isolated software-engineering sandbox.
- OpenHands: evaluate only in a disposable environment with no sensitive mounts.
- GPT Engineer: use as a code-generation research reference, never as an
  unrestricted repository writer.
- BabyAGI: do not use as a runtime base; retain only as historical reference.
- Research-agent category: design platform-owned bounded workflows rather than
  importing an unverified autonomous project.

### Marketplace Recommendation

Build the marketplace around platform-owned manifests, sandbox execution, explicit
permissions, review records, version pinning, revocation, and evidence-based
promotion. Start with bounded internal Agents that invoke approved Skills. Defer
third-party autonomous agents until the intake and execution controls are tested
with synthetic workloads.

## Open Decisions

- Framework compatibility criteria and owner for long-term maintenance.
- CONFIGURED_AGENT_MAX_DURATION by approved agent risk class.
- CONFIGURED_AGENT_MAX_ITERATIONS and loop-detection policy.
- CONFIGURED_AGENT_MAX_TOOL_CALLS and per-tool limits.
- CONFIGURED_AGENT_MAX_COST_CREDITS and wallet reservation policy.
- Remote runner hosting, regional data handling, and enterprise isolation model.
- Persian evaluation corpus governance and human review process.
- Marketplace publisher verification and support model.
- Which agent outputs require human approval before delivery or publication.

## Related Documents

- Skills research: [SKILLS_LANDSCAPE_RESEARCH.md](SKILLS_LANDSCAPE_RESEARCH.md)
- MCP research: [MCP_BIDIRECTIONAL_ARCHITECTURE_AND_ECOSYSTEM.md](MCP_BIDIRECTIONAL_ARCHITECTURE_AND_ECOSYSTEM.md)
- Agent security: [AGENT_SECURITY_MODEL.md](../security/AGENT_SECURITY_MODEL.md)
- Runtime authority: [SECURITY_AGENT_RUNTIME.md](../security/SECURITY_AGENT_RUNTIME.md)
- Third-party review: [THIRD_PARTY_AGENT_REVIEW.md](../security/THIRD_PARTY_AGENT_REVIEW.md)
- Prompt injection defense: [PROMPT_INJECTION_DEFENSE.md](../security/PROMPT_INJECTION_DEFENSE.md)
