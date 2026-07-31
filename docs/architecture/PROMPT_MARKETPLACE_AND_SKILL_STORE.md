# Prompt Marketplace and Skill Store

**Version:** v0.1.0

**Date:** 2026-07-29

**Status:** Proposed Architecture - Pending Owner Approval and Implementation

**Document Owner:** Marketplace / Product / Security

## 1. Purpose and Status

- Proposed architecture only; no marketplace, payment, review, or frontend is implemented.

- This store is distinct from Agent Marketplace (5D). Assets are non-autonomous and execution always rests with the human user.


## 2. Scope Boundary vs Agent Marketplace

| Aspect | Prompt Marketplace (this doc) | Agent Marketplace (5D) |

|---|---|---|

| Autonomy | non-autonomous | autonomous / multi-step |

| Planning | none | yes |

| Tool use | at most one bounded call | multiple calls |

| Approval model | user runs manually | Agent runs steps under policy |

| Risk profile | lower | higher |

| Review | injection + content review | full agent review |

- Skills may invoke one bounded platform tool, but the user initiates execution. Skills must not autonomously chain tools or plan.


## 3. Canonical Domain Concepts

- Prompt Template

- Product Skill Listing

- Workflow Template

- Skill Manifest

- Author Profile

- Version

- License

- Compatibility Requirement

- Purchase Record

- Install Record

- Usage Log Reference

- Review


## 4. Asset Types and Categories

- Chat prompt template

- Role/Persona template

- Image generation prompt pack

- Product photography prompt pack

- Video prompt pack

- Ad script prompt pack

- Instagram caption pack

- SEO brief pack

- Landing page copy pack

- Business FAQ template

- Study/notebook template

- Workflow templates such as Product Launch Instagram Kit

- Persian buyer categories include fashion, beauty, food, decor, digital services, real estate, clinic admin, and education creators.


## 5. Seller Types and Verification

- Platform first-party has highest trust.

- Verified Persian prompt engineer/creator requires identity evidence.

- Business consultant/agency requires verified business identity.

- Community contributor has limited trust.

- Factors include identity, portfolio quality, samples, and compliance history.


## 6. Buyer Journey and Discovery

- Browse by category, industry, language, and price.

- Use Persian-first search.

- Preview sample inputs/outputs.

- Use ratings and reviews.

- Install to workspace, not the whole platform.

- Support free, paid, subscription, and try-before-buy where feasible.


## 7. Skill Manifest and Compatibility

- id

- version

- author

- language fa/en/both

- asset_type

- category

- model compatibility families

- required capabilities

- optional Brand Kit fields

- required inputs and expected outputs

- risk_class

- content_class

- localization notes

- change log

- Manifest is machine-readable and human-reviewable.


## 8. Prompt Injection and Content Safety Review

- All listings pass automated prompt-injection scans.

- Test system-instruction hijack, output DLP, unsafe content, and persona escalation.

- Block professional medical/legal/financial/psychological advice claims.

- Review Persian content samples.

- Store never trusts a listing until reviewed.

- Updates trigger re-review.


## 9. Rights, License, and Reuse Model

- Author must own or have rights.

- Licenses may cover personal use, single business, agency reuse, or white-label higher tier.

- No scraped copyrighted content.

- Handle trademarks carefully.

- Attach rights records to purchase.


## 10. Pricing, Free Tier, and Revenue Share

- Free assets

- one-time purchase

- subscription pack

- credit-priced usage

- author revenue share

- platform commission

- refund policy for defective assets

- promotional/featured slots

- Exact pricing and commission remain Open Decisions.


## 11. Autonomy Levels and Execution Boundary

| Action | Level | Notes |

|---|---|---|

| Browse listings | L1 | Read-only |

| Preview sample output | L1 | Read-only |

| Install to workspace | L3 | Explicit user approval |

| Run prompt template | L2 | Draft output |

| One bounded tool call | L2 or L3 | Side-effect class decides |

| Auto chain or scheduling | Not allowed | Belongs to Agents |

| Account settings | Forbidden | — |

| Money or external message | Forbidden here | Requires L3 elsewhere |

- Skills must not plan chains, run without user click, or bypass Safety, Injection Defense, or DLP.


## 12. Ratings, Reviews, and Fraud Protection

- Verified purchase reviews

- text and star ratings

- review moderation

- fake review detection

- author response limits

- delisting for violations

- appeals process


## 13. Version, Update, and Deprecation Policy

- semver-style listing version

- change log

- pin-to-version option

- security quarantine, suspension, or revocation response

- deprecation window

- compatibility warnings

- author withdrawal with notice


## 14. Privacy, Isolation, and Audit

- Author never sees buyer prompts/outputs.

- Buyer data is isolated per workspace.

- Author receives aggregate usage metadata only.

- No cross-workspace leakage.

- Audit install, run, and update metadata.

- No raw inputs/outputs in author telemetry.


## 15. Persian-First and Localization Requirements

- Persian listings are first-class.

- Persian search.

- Persian-only, English-only, bilingual filters.

- RTL preview rendering.

- Persian caption/hashtag samples.

- Local business categories.

- Persian community moderation.


## 16. Proposed Implementation PR Sequence

- 1. listing metadata and manifest schema

- 2. author profile and verification

- 3. catalog and search API

- 4. install/uninstall workspace model

- 5. prompt execution binding

- 6. single-tool binding

- 7. offline injection/content review

- 8. ratings model

- 9. purchase/license record

- 10. pricing hooks

- 11. featured section

- 12. payment later

- 13. payout later

- 14. frontend later



### Workflow Template Boundary

A Workflow Template in this Store is declarative, predefined, human-initiated,
non-planning, non-autonomous, bounded to approved Product Skills, unable to create
hidden loops or unlimited retries, unable to invoke arbitrary external networks,
and unable to perform external side effects without separate L3 approval. A
template requiring autonomous planning, dynamic multi-tool chaining, background
scheduling, self-directed retries, or multi-step authority belongs to the Agent
Marketplace, not this Store.

### Executable Package Boundary

Prompt templates contain no executable scripts. Product Skill listings reference
platform-approved capabilities rather than shipping arbitrary executable code.
Bundled scripts, binaries, install hooks, arbitrary dependencies, and automatic
package installation are out of scope for Store v1. Future executable Agent Skills
packages require exact-version license review, provenance/checksum verification,
dependency and supply-chain review, sandbox evaluation, permission review, and
human approval. See [THIRD_PARTY_AGENT_REVIEW.md](../security/THIRD_PARTY_AGENT_REVIEW.md)
and [AGENT_SECURITY_MODEL.md](../security/AGENT_SECURITY_MODEL.md).

### Listing Lifecycle

Listing states are draft, submitted, automated_review, manual_review,
changes_requested, approved, published, suspended, deprecated, and delisted. Only
approved listings may be published. Suspended or delisted listings cannot be newly
installed; existing installs may be disabled for immediate security risk. Suspension
or delisting reason is audit metadata, and appeals do not automatically restore
publication.

### Manifest Requirements

Every Product Skill listing includes listing_id, skill_id, version, author_id,
publisher_type, asset_type, category, language, input_schema, output_schema,
model_compatibility, required_capabilities, required_data_classes, permission_scope,
side_effect_class, autonomy_ceiling, bounded_tool_reference, network_access_policy,
cost_class, estimate_supported, risk_class, content_class, safety_profile,
license_identifier, license_evidence_path, provenance_source, immutable_checksum,
security_review_status, review_version, minimum_platform_version, dependencies,
localization_notes, and change_log.

A listing references at most one approved bounded platform Tool in v1.
network_access_policy defaults to denied. A listing cannot increase its own
permissions. Permission and cost changes require explicit workspace re-approval.
Manifest data is machine-readable and human-reviewable.

### Installation and Update Policy

Before install, the buyer/workspace admin sees permissions, side-effect class,
autonomy ceiling, bounded Tool reference, data classes, network policy, cost class,
license, publisher identity, reviewed version, and checksum. Explicit approval is
required. Buyers may pin to a reviewed version. Content or permission changes do
not silently activate. Permission, cost, license, network, Tool, and data-access
changes require re-approval. Security response may quarantine, suspend, or revoke
a vulnerable version without silently replacing behavior with materially different
content. Rollback to the previous approved version is supported. Install and update
history is auditable.

### Related Documents

- [SKILLS_LANDSCAPE_RESEARCH.md](../research/SKILLS_LANDSCAPE_RESEARCH.md)
- [MCP_SKILLS_AGENTS_V1_DECISIONS.md](../product/MCP_SKILLS_AGENTS_V1_DECISIONS.md)
- [EXTENSIBILITY_MCP_AND_SKILLS.md](EXTENSIBILITY_MCP_AND_SKILLS.md)
- [THIRD_PARTY_AGENT_REVIEW.md](../security/THIRD_PARTY_AGENT_REVIEW.md)
- [AGENT_SECURITY_MODEL.md](../security/AGENT_SECURITY_MODEL.md)
- [PROMPT_INJECTION_DEFENSE.md](../security/PROMPT_INJECTION_DEFENSE.md)

## 17. Open Decisions

- commission rate

- refund terms

- payout method

- verification and KYC

- underage author policy

- Persian moderation staffing

- category taxonomy

- try-before-buy quota

- premium credit multipliers

- takedown appeal

- white-label reuse

