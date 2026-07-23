# ACCURACY AND CREATIVITY CONTROL

**Date:** 2026-07-23
**Status:** Architecture Definition - Documentation Only
**Purpose:** Define user-friendly label for accuracy/creativity modes, avoid "hallucination level" wording, define normalized modes, provider-neutral config layer

## User-Facing Label

- **Do NOT expose a user setting called "hallucination level."** This is technical jargon, negative framing, and confusing for users.
- **Use user-friendly label:** "Accuracy and Creativity" 
- **Persian UX concept:** "دقت و خلاقیت" - user-friendly, positive framing, understandable

## Normalized Modes

Define 3 normalized modes that are provider-neutral and user-friendly:

### 1. strict_factual
- **Persian label:** دقیق و مستند
- **Description:** Low creativity, high accuracy, factual, citation-aware
- **Low creativity**
- **No unsupported factual claims** - must not invent facts
- **Citation-aware** - must cite sources when factual claim, must disclose uncertainty if sources conflict or not found
- **Must never invent citations** - no hallucinated citations, no fake URLs, no fake publisher/dates
- **Use cases:** Research, study workspace, RAG with sources, fact-checking, when user asks for evidence-based information, high-risk personas (e.g., health information, legal information, immigration information) should default to strict_factual or balanced, not creative
- **Provider mapping:** Lower temperature, lower top_p, more deterministic

### 2. balanced
- **Persian label:** متعادل
- **Description:** General-purpose conversation, moderate creativity, helpful, balanced accuracy and creativity
- **Moderate creativity**
- **General-purpose:** Suitable for most chats, normal assistant default
- **Use cases:** General chat, business assistant, planning assistant, prompt engineer, everyday questions
- **Provider mapping:** Medium temperature, medium top_p

### 3. creative
- **Persian label:** خلاق
- **Description:** Storytelling, advertising, brainstorming, role-play, creative writing - may invent fictional elements only when task is clearly creative
- **May invent fictional elements only when the task is clearly creative:** e.g., story, ad copy, brainstorming ideas, role-play, artistic images, brand concepts - allowed to invent fictional characters, plots, slogans
- **Must never invent factual citations, legal rules, medical claims, provider prices, or current events:** Even in creative mode, must not invent factual citations (fake papers), legal rules (e.g., "According to Iranian law article 123..."), medical claims (e.g., "This drug cures..."), provider prices (e.g., "ChatGPT Plus costs $5"), or current events (e.g., "Yesterday event...") - these are always disallowed to invent, even in creative mode
- **Use cases:** Writer, editor, advertising campaign, poster, banner, social media assets, artistic images, brand concepts, storytelling, storyboard, character workflows
- **Provider mapping:** Higher temperature, higher top_p, more creative

## Role and Persona Default Modes

Each Role may recommend a default response mode:

- **Normal Assistant:** balanced (general-purpose)
- **Language Learning Companion:** balanced
- **Writer:** creative (but must not invent factual citations)
- **Editor:** balanced
- **Business Assistant:** balanced
- **Planning Assistant:** balanced
- **Prompt Engineer:** balanced
- **Career Advisor (specialist persona, medium risk):** balanced, may allow strict_factual as well, not creative (career advice should not be overly creative with fake job guarantees)
- **Sales Advisor:** balanced
- **SEO Advisor:** balanced
- **Evidence-Based Mental Health Information Assistant (high risk):** strict_factual only, not creative - must be accurate, citation-aware, no invented coping strategies
- **Immigration Information Assistant (high risk):** strict_factual only
- **Legal Information Assistant (high risk):** strict_factual only
- **Health Information Assistant (high risk):** strict_factual only

**Rule:** High-risk future specialist personas must NOT default to creative, only strict_factual or balanced, with allowed safe range restricted to strict_factual and balanced, not creative.

## User Override Within Safe Range

Users may override default response mode **only within the Role's allowed safe range**:

- Example: Normal Assistant allows ["strict_factual","balanced","creative"] - user may choose any of 3
- Example: Career Advisor allows ["strict_factual","balanced"] - user may choose strict_factual or balanced, but NOT creative (career advice should not be overly creative)
- Example: Mental Health Information Assistant allows ["strict_factual"] only - user cannot override to creative, because creative mode for mental health could be unsafe (inventing coping strategies that are not evidence-based)
- Example: Writer allows ["balanced","creative"] - may allow creative as default, but also balanced for more factual writing

**Enforcement:** UI Role selector shows allowed modes per Role, disabled options for modes not allowed. Backend validates requested mode is in Role's allowed_response_modes, rejects if not allowed with 400.

## Provider-Neutral Configuration Layer

**Problem:** Different providers use different sampling parameters:
- OpenAI: temperature, top_p, presence_penalty, frequency_penalty, etc.
- Anthropic: temperature, top_p, top_k, etc.
- Google: temperature, top_p, top_k, etc.
- Local models: various parameters

**Solution:** Provider-neutral config layer that maps normalized modes (strict_factual, balanced, creative) to provider-specific parameters.

**Example Mapping (conceptual, not hardcoded in code yet - for documentation, actual mapping in code later):**

```python
ACCURACY_CREATIVITY_MODES = {
    "strict_factual": {
        "description": "Low creativity, high accuracy",
        "openai": {"temperature": 0.2, "top_p": 0.9},
        "anthropic": {"temperature": 0.1, "top_p": 0.9, "top_k": 40},
        "google": {"temperature": 0.2, "top_p": 0.8, "top_k": 40}
    },
    "balanced": {
        "description": "General-purpose",
        "openai": {"temperature": 0.7, "top_p": 0.95},
        "anthropic": {"temperature": 0.7, "top_p": 0.95, "top_k": 0},
        "google": {"temperature": 0.7, "top_p": 0.9, "top_k": 0}
    },
    "creative": {
        "description": "Storytelling, advertising, brainstorming",
        "openai": {"temperature": 1.0, "top_p": 1.0},
        "anthropic": {"temperature": 1.0, "top_p": 0.95, "top_k": 0},
        "google": {"temperature": 1.0, "top_p": 0.95, "top_k": 0}
    }
}
```

**Benefits:**
- User selects friendly label "Accuracy and Creativity" / "دقت و خلاقیت" with 3 modes, not technical "hallucination level" or raw temperature values
- Core chat logic uses normalized modes, not provider-specific parameters directly - adding new provider does not require changing core logic, only adding mapping in config layer
- Role's allowed_response_modes restricts which normalized modes user can choose, ensuring safety for high-risk personas
- Provider abstraction layer translates normalized modes to provider-specific parameters

**Storage:**
- User preference: user_role_preferences table with response_mode field (strict_factual, balanced, creative)
- Role registry: default_response_mode and allowed_response_modes fields per Role (already in ROLE_AND_PERSONA_SYSTEM.md)
- Audit log: logs which mode was used per response (for evaluation)

## Safety

- **Never invent citations:** Even in creative mode, must never invent factual citations (fake papers, fake URLs, fake publisher/dates). Citation-aware, no hallucinated citations - tested in PERSONA_QA_AND_RED_TEAMING.md
- **Never invent legal rules, medical claims, provider prices, current events:** Even in creative mode, these are always disallowed to invent. Creative mode may invent fictional elements only when task is clearly creative (story, ad, brainstorming, role-play, artistic images, brand concepts), not factual domains
- **High-risk personas restricted to strict_factual and balanced, not creative:** To avoid unsafe creative invention for health/legal/immigration
- **Must disclose uncertainty:** In strict_factual mode, if sources conflict or not found, must disclose uncertainty, not invent
- **Human approval for persona prompt changes, especially high-risk:** Per HUMAN_APPROVAL_GATES

## Persian UX

- **Label:** "دقت و خلاقیت" - user-friendly, positive, understandable, not technical jargon "سطح توهم"
- **Modes Persian:**
  - strict_factual: "دقیق و مستند" - توضیح: کمترین خلاقیت، بیشترین دقت، بدون ادعای بدون پشتوانه، با ذکر منبع، اعلام عدم قطعیت
  - balanced: "متعادل" - توضیح: مناسب برای گفتگوی روزمره، تعادل دقت و خلاقیت
  - creative: "خلاق" - توضیح: داستان‌نویسی، تبلیغات، طوفان فکری، نقش‌آفرینی - فقط زمانی که وظیفه واضحاً خلاقانه است می‌تواند عناصر داستانی اختراع کند، هرگز نباید استناد واقعی، قوانین حقوقی، ادعاهای پزشکی، قیمت ارائه‌دهندگان، یا رویدادهای جاری را اختراع کند
- **UI:** Slider or 3 buttons with Persian labels and descriptions, default mode per Role, user can override within allowed safe range
- **First-use onboarding:** Ask user what Accuracy and Creativity mode they prefer, explain difference

## Linkage

- Role and Persona System: ROLE_AND_PERSONA_SYSTEM.md (default_response_mode, allowed_response_modes fields)
- Persona Framework: ../personas/PERSONA_FRAMEWORK.md (evidence standard, citation requirements)
- Agent Plugin and Execution: AGENT_PLUGIN_AND_EXECUTION_SYSTEM.md (provider abstraction)
- Provider Abstraction: PROVIDER_ABSTRACTION_STRATEGY.md
- Evaluation: PERSONA_EVALUATION_STRATEGY.md (accuracy and hallucination metrics per mode)
