# Changelog

All notable documentation and planning changes.

## 2026-07-19 — Phase 0 Foundation Merged
- Merged PR #2 into main (merge commit e4ad2f1)
- Added 105 documentation files (~7,800 lines)
- Established Agent Operating System (28 project-building agents: 19 L1 + 9 L2, 11 runtime agents, 5 internal agents)
  - L1 (19): Analytics, App Store/ASO, Brand Visual Identity, Compliance/Risk, Customer Success, Data Privacy Governance, Execution Coach, Finance/Unit Economics, Growth Marketing, Model Evaluation, Product Manager, RAG Knowledge, Research, Sales/Partnership, SEO Content, Social Media, SRE/Incident Response, Supplier Scout, Trust & Safety — report/draft only, NO branch/PR
  - L2 (9): DevOps, Fullstack Builder, Localization & Accessibility, ML Inference Engineer, Orchestrator (docs/planning PRs only), Prompt Engineer, QA/Security, UX/Product Design, Website Builder — may create scoped branch + PR
- Defined 8-phase roadmap (0 Foundation, 1 Core MVP, 2 Personas, 3 Image Studio, 4 API Platform, 5 Video & Character Tools, 6 Telegram & Business Agents, 7 Research & RAG, 8 Agent Marketplace idea)
- Added 7 governance documents:
  - docs/architecture/SYSTEM_CONTEXT.md
  - docs/architecture/PROVIDER_ABSTRACTION_STRATEGY.md
  - docs/architecture/DATA_CLASSIFICATION_AND_RETENTION.md
  - docs/evaluation/MODEL_EVALUATION_STRATEGY.md
  - docs/evaluation/PERSONA_EVALUATION_STRATEGY.md
  - docs/safety/TRUST_AND_SAFETY_FRAMEWORK.md
  - docs/research/SOURCE_QUALITY_POLICY.md
- Added 8 new specialist project agents: UX/Product Design (L2), Brand Visual Identity (L1), ML Inference Engineer (L2), Model Evaluation (L1), Trust & Safety (L1), Data Privacy Governance (L1), Localization & Accessibility (L2), SRE/Incident Response (L1)
- Created product vision (PRODUCT_VISION, BUSINESS_MODEL, USER_PERSONAS), persona system with evidence-based framework (mandatory fields: source hierarchy, evidence grade, publisher, dates, geographic scope, last review, conflicting handling, min primary sources, expert reviewer, citation requirements, benchmark, accuracy/hallucination metrics, knowledge-pack version, expiry), initial backlog 14 personas
- Created growth system (growth loops, SEO 6 clusters, content engine draft→human publish, launch plan, experiment backlog, referral ideas, social, landing strategy)
- Created website IA (15 pages) + requirements, ops (workflow, branching, labels, milestones, DoD with HttpOnly Secure SameSite, release, runbook, reporting), backlog (epics + 8 issue lists), GitHub templates (7 issue + PR template)
- Updated README to reflect Persian AI platform roadmap, deprecated reseller, links to MASTER_ROADMAP and AGENT_OPERATING_SYSTEM
- Legacy shared-account resale model officially deprecated and archived to branch archive/legacy-code-2026-07-19
- Safety: Added ABSOLUTELY FORBIDDEN / NO-GO section (ToS bypass, geographic/sanctions/KYC bypass, fake identities, hiding prohibited locations, credential sharing) with statement No human approval may authorize these actions. Orchestrator separation of duties enforced (docs/planning PRs only).
- Auth security: HttpOnly cookies Secure SameSite Lax/Strict short-lived sessions CSRF, no localStorage JWT
- Persian-first baseline: RTL, Persian nav, forms, error messages, typography, mobile-first required in Phase 1
- No application source code modified, no secrets, no deploy
