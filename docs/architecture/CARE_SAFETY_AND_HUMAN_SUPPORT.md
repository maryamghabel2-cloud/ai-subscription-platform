# Care Safety and Human Support

**Version:** v0.1.0

**Date:** 2026-07-29

**Status:** Proposed Architecture - Pending Owner Approval and Implementation

**Document Owner:** Safety / Security / Product

## 1. Purpose and Status

This proposed architecture defines care safety, mental-health information, and
human-support boundaries. It does not prove detection, handoff workflows, human
support tools, or specialist services are implemented.

It aligns safety with the Persian Content and Commerce Studio and Business Agent
Pack while keeping high-risk information, private conversations, and commercial
automation subject to stronger safeguards.

## 2. Default Mode and High-Risk Personas

Default mode for all users is Normal Assistant, not psychologist, therapist, or
advisor. High-risk specialist Personas are opt-in, versioned, and require explicit
safety profiles:

- Evidence-Based Mental Health Information Assistant
- Immigration Information Assistant
- Legal Information Assistant
- Health Information Assistant

These Personas must not claim professional authority, diagnosis, treatment, or
emergency-service capability. Search is disabled by default unless explicitly
enabled in their knowledge_base_policy.

## 3. Care Principle

- Do not abruptly terminate legitimate emotional conversations.
- Respond calmly and compassionately.
- Validate emotions without validating harmful conclusions.
- Use approved grounding and supportive language.
- Encourage connection to trusted humans and qualified professionals.
- Offer a human-support handoff.
- Avoid shame, threats, manipulation, or coercion.

Care does not mean certainty. A supportive response must retain truthful limits,
avoid dependency cues, and avoid presenting generated information as clinical,
legal, health, immigration, or financial authority.

## 4. Human Support Workflow

1. Detect safety risk level.
2. Continue supportive conversation.
3. Record only minimal non-content safety metadata by default.
4. Offer contact with a qualified human specialist.
5. Request informed consent.
6. Let the user select or approve content shared.
7. Create an encrypted, time-limited support case.
8. Restrict access using role-based access controls.
9. Record every human access in an immutable audit trail.
10. Delete or archive the support case according to approved policy.

Silent human-readable alerts containing private message text are forbidden.

## 5. No Secret Human Access Rule

No external human, bot, agent, or AI may access user conversations without an
explicit, informed, time-limited, audited, and consented workflow. The Security
Agent cannot read raw sensitive conversation content by default. Aggregate,
content-free safety events may support system monitoring.

Consent must identify scope, recipient role, purpose, and expiry. Withdrawing
consent stops future access subject to lawful preservation requirements.

## 6. High-Risk Persona Safety Profile

Every high-risk Persona requires allowed_capabilities, allowed_privacy_classes,
allowed_risk_classes, enabled, expert_review_required, safety_profile,
knowledge_base_ids, and retrieval_policy.

Search remains disabled by default for high-risk Personas unless explicitly enabled
in knowledge_base_policy. Profiles are versioned and changes require review.

## 7. Evidence-Based Framing and Disclaimer Policy

High-risk Personas use evidence-based framing and clear disclaimers. They cannot
provide diagnosis, treatment plan, prescription, or professional authority claims.
Where applicable, they cite jurisdiction, source, publication/update date, and
access date. Information must be distinguished from advice.

## 8. Crisis Resource and Escalation Policy

Country-specific crisis contacts must not be hardcoded unless verified, dated, and
regularly reviewed. Escalation follows the human support workflow. The Security
Agent may generate alerts and escalate but cannot replace emergency services.

Crisis language should receive compassionate support, encouragement to contact
local emergency or trusted human help where appropriate, and no coercive response.

## 9. Business Agent Safety Boundaries

Customer support, sales, research, and immigration research agents must not give
legal, medical, psychological, or financial advice. They use scoped tools and
approved knowledge bases, log metadata only, and require human approval gates for
high-impact actions.

L1 and L2 are the usual starting levels. L3 needs explicit approval for external
writes. L4 requires deterministic policy, audit, revocation, cancellation, budget,
and escalation. L5 is not approved by this document.

## 10. Safety Detection Signals and Monitoring

Monitor content-free or minimally necessary signals: prompt injection patterns,
self-harm or crisis language, repeated unauthorized access, abnormal spending or
tool usage, cross-tenant leakage attempts, and high-risk Persona misuse.

Signals are not diagnoses. Detection uncertainty must favor safe, respectful,
reviewable escalation rather than hidden surveillance or automatic punishment.

## 11. Audit and Immutable Trail Requirements

Every human access to a support case is recorded in an immutable audit trail.
Every escalation, consent, and handoff is metadata logged. The Security Agent
cannot disable or rewrite its audit trail or grant itself new privileges.

Audit records identify actor role, purpose, case scope, timestamp, policy decision,
and outcome without default inclusion of raw private content.

## 12. Privacy and Data Minimization in Safety Cases

Support cases are encrypted and time-limited. Raw sensitive conversation content is
shared only with explicit user consent and only to the minimum necessary extent.
Support case data is deleted or archived according to approved policy. No secret
human access to conversations is permitted.

### Operational Safety Constraints

- Safety labels must not be shown as diagnoses.
- Risk signals require policy context before action.
- Users must receive understandable handoff choices.
- Support access is limited to approved case scope.
- Case access expires when consent or assignment expires.
- Human support staff cannot export unrelated conversation history.
- Support staff actions require role-appropriate training records.
- Specialist availability must not be implied when unavailable.
- The platform must not promise emergency response times.
- Automated summaries are reviewable aids, not authoritative case records.
- Escalation metadata must avoid unnecessary sensitive details.
- Safety workflows must support user cancellation where lawful.
- A declined handoff does not end a compassionate conversation.
- Business agents must surface uncertainty rather than fabricate advice.
- High-risk retrieval sources require provenance and review.
- Persona configuration must not silently expand risk classes.
- Content moderation decisions require auditable policy reasons.
- Likeness and impersonation concerns require separate consent review.
- Creator marketplace disputes do not grant access to private chat memory.
- Customer support context must remain tenant and customer scoped.

### Human Support Case Boundaries

- A support case has a purpose-bound access scope.
- A case has an owner role and expiry metadata.
- Case attachments follow the media asset privacy boundary.
- Case notes are not training data by default.
- Provider data handling requires separate disclosure.
- Case closure records outcome category, not unnecessary raw content.
- Reopening a case requires a new authorized workflow.
- Emergency resources are informational, not a substitute for local services.
- Enterprise administrators do not gain raw support-case access by default.
- Security monitoring receives aggregate signals unless consented access exists.

### Persona Review Expectations

- Review allowed capabilities before each profile release.
- Review retrieval policy before enabling external search.
- Review disclaimer language for clarity and locale.
- Review source freshness for jurisdiction-sensitive information.
- Review refusal and redirect behavior for harmful requests.
- Review Persian language tone for compassion and non-coercion.
- Review mixed RTL/LTR display for resource and contact information.
- Review agent handoff boundaries before business deployment.
- Review audit coverage for every consent and access transition.
- Review deletion behavior for support-case and conversation references.

### Testing Expectations

- Test consent withdrawal during an active support case.
- Test that a human cannot access an unassigned case.
- Test case expiry and access revocation.
- Test cross-tenant support-case denial.
- Test transcript and attachment minimization.
- Test audit records for consent and human access.
- Test high-risk Persona search-disabled defaults.
- Test prompt injection in attached content.
- Test L3 approval requirements for external business actions.
- Test that L4 policy constraints remain deterministic.
- Test user-visible handling of unavailable human support.
- Test deletion and archive policy transitions after case closure.

### Deployment Preconditions

- Owner approval for the relevant safety profile.
- Security approval for access and audit controls.
- Privacy approval for consent and minimization behavior.
- Legal review where jurisdiction-specific information is involved.
- Trained human-support role assignment before any handoff offering.

## 13. Proposed Implementation PR Sequence

1. High-risk Persona safety profile schema.
2. Care Principle and disclaimer templates.
3. Human support case model and encrypted storage.
4. Safety detection signals and metadata logging.
5. Human handoff workflow API.
6. Consent and audit trail enforcement.
7. Business Agent safety boundaries enforcement.
8. Security Agent escalation rules.
9. UI for memory controls and safety handoff later.

Each future PR requires tests, privacy review, security review, and rollback plans.

## 14. Open Decisions

- Exact crisis resource list and verification process.
- Minors and children policy.
- Legal review cadence for high-risk Personas.
- Support case retention and deletion policy.
- Encryption algorithm and key management for support cases.
- Thresholds for safety detection signals.
- Enterprise versus individual safety policy differences.
- Integration with future Trust & Safety team.

### Related Documents

- [ROLE_AND_PERSONA_SYSTEM.md](ROLE_AND_PERSONA_SYSTEM.md)
- [ROLE_PERSONA_AGENT_BOUNDARIES.md](ROLE_PERSONA_AGENT_BOUNDARIES.md)
- [PROMPT_INJECTION_DEFENSE.md](../security/PROMPT_INJECTION_DEFENSE.md)
- [AGENT_SECURITY_MODEL.md](../security/AGENT_SECURITY_MODEL.md)
- [SECURITY_AGENT_RUNTIME.md](../security/SECURITY_AGENT_RUNTIME.md)

