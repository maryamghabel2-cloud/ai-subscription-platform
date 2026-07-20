# AGENT DIRECTORY REQUIREMENTS

**Date:** 2026-07-19

## Purpose
Directory for Specialist Personas and Business Agents, and future Agent Marketplace concept.

## Persona Directory (/personas)

- Grid of cards: Name, ID, Purpose one line, Risk Level badge (Low/Med/High), Maturity badge (idea/planned/research-needed/ready-later), Credit cost
- Click → Detail page /personas/{id}
- Filters: Risk Low/Med/High, Domain, Target user
- Disclaimer banner top: "These are evidence-based assistants, not certified professionals..."

## Persona Detail (/personas/{id})

- Name, version, risk, domain, target users
- Purpose
- How it works: method
- Knowledge sources required (links)
- Prompt policy, escalation behavior
- Evaluation tests summary
- Disclaimer + safety policy link
- CTA: Try persona chat (if ready) or Join waitlist (if idea)

## Business Agents Directory (/business-agents)

- Similar cards: FAQ Agent, Lead Qualifier, Content Drafter
- Shows Telegram integration possibility

## Future Agent Marketplace (Phase 8 Idea) - Not Built

- Concept: /marketplace - user-created agents, with review
- Requirements idea: agent card, permissions manifest, approval flow for listing, rev-share

## Approval Gates

- Adding new persona to directory requires QA + red teaming + human approval
- Persona prompt changes for High risk require compliance review + human approval

## Safety

- No medical/legal/psych authority claims in cards
- Risk level visible
- Disclaimer visible
