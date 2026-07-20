# AGENT REGISTRY

**Date:** 2026-07-19  
**Updated:** 2026-07-20 - Added 8 new agents, fixed L1/L2 consistency, added absolutely forbidden note
**Purpose:** Single source of truth for all agents (project-building, runtime, future internal).
**Count:** Project-building 28 agents (was 20).

## Project-Building Agents (28) - Active in Phase 0-2 - Mix L1 and L2

**Definitions:**
- L1: Prompt-driven external agent that returns a report or draft (no branch/PR itself)
- L2: External agent that may create a scoped branch and Pull Request (docs or code per separation of duties)
- Orchestrator is L2 but only documentation/planning PRs, not application-code PRs

| Agent ID | Name | Type | Phase Relevance | Maturity Now | Maturity Later | Notes |
|---|---|---|---|---|---|---|
| orchestrator | Orchestrator Agent | project | All | L2 (docs/planning PRs only) | L3 read-only control tower | Does NOT write product code |
| product_manager | Product Manager Agent | project | 0-2 | L1 | L2 | Returns PRDs, issue breakdowns as report/draft |
| fullstack_builder | Fullstack Builder Agent | project | 1-4 | L2 | L3 | Branch + PR for backend/frontend code |
| website_builder | Website Builder Agent | project | 1,6 | L2 | L3 | Branch + PR for landing/pages |
| devops | DevOps Agent | project | 1-4 | L2 | L3 | Branch + PR for docker/compose/CI |
| qa_security | QA/Security Agent | project | 1-4 | L2 | L3 | Branch + PR for tests, security checks |
| research | Research Agent | project | 0-7 | L1 | L3 read-only | Report/draft only |
| prompt_engineer | Prompt Engineer Agent | project | 1-3,7 | L2 | L3 | Branch + PR for prompt library |
| rag_knowledge | RAG Knowledge Agent | project | 7 | L1 | L3 | Report/draft |
| seo_content | SEO Content Agent | project | 0-3,6 | L1 | L3 draft-only | Report/draft, never auto-publish |
| growth_marketing | Growth Marketing Agent | project | 0-6 | L1 | L3 read-only + draft | Report/draft, experiment proposal |
| social_media | Social Media Agent | project | 6 | L1 | L3 draft-only | Draft posts only |
| analytics | Analytics Agent | project | 1-7 | L1 | L3 read-only | Report/draft, events spec |
| customer_success | Customer Success Agent | project | 6 | L1 | L3 draft-only | Draft replies only |
| sales_partnership | Sales/Partnership Agent | project | 6 | L1 | L2 | Report/draft outreach |
| compliance_risk | Compliance/Risk Agent | project | 0-8 | L1 | L3 read-only | Report/checklist, blocks forbidden |
| finance_unit | Finance/Unit Economics Agent | project | 0-5 | L1 | L3 read-only | Report, never price change without approval |
| supplier_scout | Supplier Scout Agent | project | 0,3,5 | L1 | L2 | Report, does NOT automate purchasing from GGSel etc - deprecated |
| app_store_aso | App Store/ASO Agent | project | 3,5 | L1 | L2 | Report/draft |
| execution_coach | Execution Coach Agent | project | All | L1 | L2 | Report, weekly plan |
| ux_product_design | UX/Product Design Agent | project | 1-3 | L2 | L3 | Branch + PR for UX flows, wireframes, design system - NEW |
| brand_visual_identity | Brand Visual Identity Agent | project | 0-3 | L1 | L2 | Report/draft brand guidelines, logo, colors, typography |
| ml_inference_engineer | ML Inference Engineer Agent | project | 3-5,7 | L2 | L3 | Branch + PR for inference wrapper, latency optimization |
| model_evaluation | Model Evaluation Agent | project | 2-5,7 | L1 | L3 | Report/draft eval strategy, datasets, metrics |
| trust_safety | Trust & Safety Agent | project | 2-7 | L1 | L3 | Report/checklist, safety framework |
| data_privacy_governance | Data Privacy Governance Agent | project | 0-7 | L1 | L3 | Report on data classification, retention, privacy |
| localization_accessibility | Localization & Accessibility Agent | project | 1-6 | L2 | L3 | Branch + PR for RTL, Persian typography, a11y |
| sre_incident_response | SRE/Incident Response Agent | project | 1-7 | L1 | L3 | Report/runbook draft, incident report |

## Runtime Product Agents (For Customers) - Planned Phase 1-7 - Mix L2/L3 Future

| Agent ID | Name | Phase | Risk | Maturity Future |
|---|---|---|---|---|
| general_chat | General Persian Chat | 1 | Low | L3 |
| prompt_enhancer | Prompt Enhancer | 1 | Low | L3 |
| persona_runtime | Specialist Persona Runtime | 2 | Medium (depends) | L3 |
| image_studio | Image Generation Studio | 3 | Medium (NSFW) | L3 |
| product_photo | Product Photography Studio | 3 | Low | L3 |
| video_gen | Video Generation | 5 | Medium (deepfake) | L3 |
| character_tool | AI Character/Influencer | 5 | High (consent) | L3 with approval |
| telegram_agent | Telegram Agent | 6 | Medium (spam) | L3 |
| business_agent | Business Agent (FAQ/lead) | 6 | Medium | L3 |
| research_rag | Research & RAG | 7 | Low | L3 |
| developer_api | Developer API Agent | 4 | Low | L3 |

## Internal Operations Agents (Future L3/L4, Draft-Only Initially)

| Agent ID | Future Purpose | Draft? | Maturity Future |
|---|---|---|---|
| seo_tech | SEO technical audit, sitemap | Yes draft | L3 draft-only |
| content_draft | Blog/topic draft | Yes draft | L3 draft-only |
| growth_reporter | Experiment report generator | Read-only + draft | L3 read-only |
| support_draft | Support answer draft | Draft, human sends | L3 draft-only |
| research_scout | Supplier/model scout report | Draft | L1/L2 report |

## Registry Schema
- ID, Name, Type (project/runtime/internal), Purpose, Phase, Maturity L0-L4 (per updated definitions), Permissions (allow/forbid/approval + absolutely forbidden), Owner (founder), Status (idea/active/archived), Risk Level, Audit Required
- Counts: Project-building 28, Runtime 11, Internal 5

See permission model and maturity model docs. No human approval may authorize absolutely forbidden actions (ToS bypass, geographic/sanctions/KYC bypass, fake identities, hiding prohibited locations, sharing/reselling unauthorized credentials/raw supplier keys).

