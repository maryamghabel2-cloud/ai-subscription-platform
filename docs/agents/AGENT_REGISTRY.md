# AGENT REGISTRY

**Date:** 2026-07-19  
**Purpose:** Single source of truth for all agents (project-building, runtime, future internal).

## Project-Building Agents (20) - Active in Phase 0-2

| Agent ID | Name | Type | Phase Relevance | Maturity Now | Maturity Later |
|---|---|---|---|---|---|
| orchestrator | Orchestrator Agent | project | All | L2 | L3 |
| product_manager | Product Manager Agent | project | 0-2 | L2 | L2 |
| fullstack_builder | Fullstack Builder Agent | project | 1-4 | L2 | L3 |
| website_builder | Website Builder Agent | project | 1,6 | L2 | L3 |
| devops | DevOps Agent | project | 1-4 | L1 | L3 |
| qa_security | QA/Security Agent | project | 1-4 | L2 | L3 |
| research | Research Agent | project | 0-7 | L1 | L3 |
| prompt_engineer | Prompt Engineer Agent | project | 1-3,7 | L2 | L3 |
| rag_knowledge | RAG Knowledge Agent | project | 7 | L1 | L3 |
| seo_content | SEO Content Agent | project | 0-3,6 | L1 | L3 (draft-only) |
| growth_marketing | Growth Marketing Agent | project | 0-6 | L2 | L3 |
| social_media | Social Media Agent | project | 6 | L1 | L3 (draft-only) |
| analytics | Analytics Agent | project | 1-7 | L1 | L3 |
| customer_success | Customer Success Agent | project | 6 | L1 | L3 (draft-only) |
| sales_partnership | Sales/Partnership Agent | project | 6 | L1 | L2 |
| compliance_risk | Compliance/Risk Agent | project | 0-8 | L2 | L3 |
| finance_unit | Finance/Unit Economics Agent | project | 0-5 | L1 | L3 (read-only) |
| supplier_scout | Supplier Scout Agent | project | 0,3,5 | L1 | L2 |
| app_store_aso | App Store/ASO Agent | project | 3,5 | L1 | L2 |
| execution_coach | Execution Coach Agent | project | All | L1 | L2 |

## Runtime Product Agents (For Customers) - Planned Phase 1-7

| Agent ID | Name | Phase | Risk |
|---|---|---|---|
| general_chat | General Persian Chat | 1 | Low |
| prompt_enhancer | Prompt Enhancer | 1 | Low |
| persona_runtime | Specialist Persona Runtime | 2 | Medium (depends) |
| image_studio | Image Generation Studio | 3 | Medium (NSFW) |
| product_photo | Product Photography Studio | 3 | Low |
| video_gen | Video Generation | 5 | Medium (deepfake) |
| character_tool | AI Character/Influencer | 5 | High (consent) |
| telegram_agent | Telegram Agent | 6 | Medium (spam) |
| business_agent | Business Agent (FAQ/lead) | 6 | Medium |
| research_rag | Research & RAG | 7 | Low |
| developer_api | Developer API Agent | 4 | Low |

## Internal Operations Agents (Future L3/L4, Draft-Only Initially)

| Agent ID | Future Purpose | Draft? |
|---|---|---|
| seo_tech | SEO technical audit, sitemap | Yes draft |
| content_draft | Blog/topic draft | Yes draft |
| growth_reporter | Experiment report generator | Read-only + draft |
| support_draft | Support answer draft | Draft, human sends |
| research_scout | Supplier/model scout report | Draft |

## Registry Schema
- ID, Name, Type (project/runtime/internal), Purpose, Phase, Maturity L0-L4, Permissions (allow/forbid/approval), Owner (founder), Status (idea/active/archived), Risk Level, Audit Required

See permission model and maturity model docs.
