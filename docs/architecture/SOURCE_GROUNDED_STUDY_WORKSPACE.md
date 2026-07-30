# Source-Grounded Study Workspace

**Version:** v0.1.0

**Date:** 2026-07-29

**Status:** Proposed Architecture - Pending Owner Approval and Implementation

**Document Owner:** Architecture / Research / Product

## 1. Purpose and Status

- Proposed architecture only; it does not prove RAG, vector stores, document processing, embeddings, or providers are implemented.

- It supports learners, researchers, business knowledge, and future Deep Research workflows.


## 2. Supported Use Cases

- | Use Case | User | Sources | Output |

- |---|---|---|---|

- | Student research and study | Learner | Notes and PDFs | Study notes |

- | Legal/immigration research | Researcher | Dated sources | Cited information |

- | Business knowledge Q&A | Workspace member | FAQs/catalogs | Grounded answer |

- | Market and competitor research | Business user | Approved sources | Comparison |

- | Academic paper analysis | Researcher | Papers | Outline |

- | Document comparison | User | Multiple versions | Differences |

- | Personal knowledge base | Individual | Private documents | Cited recall |


## 3. Canonical Domain Concepts

- Source: uploaded document, URL reference, or knowledge-base entry.

- Source Version: immutable captured revision.

- Source Chunk: addressable source fragment.

- Chunk Embedding: derived retrieval representation.

- Source Citation: exact document, chunk, and version reference.

- Trust Classification: source provenance and review category.

- Processing Status: ingestion lifecycle metadata.


## 4. Source and Document Model

- Require source ownership and tenant isolation.

- Track versions and processing metadata.

- Deletion cascades to chunks, embeddings, and indexes.

- No cross-tenant source sharing.

- Citations reference exact source, chunk, and version.

- Raw source content must not enter technical logs.


## 5. Workspace and Notebook Model

- Workspace: personal or business scope.

- Notebook: permissioned collection of research work.

- Source Collection: selected sources for a question.

- Research Question: versioned user inquiry.

- Study Session: bounded learning interaction.

- Require scoped access and explicit project sharing.

- Business workspace and personal workspace remain separate.


## 6. Grounded Q&A and Citation Model

- Answers cite document ID, chunk ID, and version.

- Unsupported answers state not found in provided sources.

- Do not silently use general model knowledge to fill gaps.

- Citation confidence is metadata.

- Show source-grounded versus general knowledge distinctly.


## 7. Source-Only Mode

- Source-Only Mode explicitly permits only provided sources.

- No general LLM knowledge fill-in is permitted.

- Unsupported questions are explicitly flagged.

- Every factual claim requires a citation.

- Mode changes are visible to users and auditable as metadata.


## 8. Study and Learning Outputs

- Summary

- Study notes

- Flashcards

- Quiz questions

- Source comparison

- Timeline extraction

- Research outline

- Concept map (future)

- Audio overview (future)


## 9. Persian Document Handling

- Require Persian PDF/text extraction quality.

- Require RTL rendering in outputs.

- Support mixed Persian/English documents.

- Use Persian citation formatting.

- Account for Persian legal and regulatory document context.

- Review OCR uncertainty and mixed-script identifiers.


## 10. Privacy, Retention, and Deletion

- Source documents are sensitive assets.

- Use CONFIGURED_SOURCE_RETENTION.

- Use CONFIGURED_EMBEDDING_RETENTION.

- Delete embeddings when a source is deleted.

- Workspace deletion cascades.

- Disclose provider retention for embedding/OCR services.


## 11. Safety and Trust Boundaries

- Legal, immigration, and medical sources do not confer professional advice.

- High-risk sources require appropriate disclaimers.

- Mitigate prompt injection via document content.

- OCR and extracted text are untrusted input.

- Source content does not authorize system actions.


## 12. Deep Research Agent Integration Point

- Study Workspace is a retrieval foundation for Deep Research Agent.

- Research Agent may request sources, search, and return citations.

- It follows source-only mode and citation rules.

- It must not fabricate citations.

- Autonomy starts at L2 draft.


## 13. Billing and Usage Hooks

- Embedding cost per source ingestion.

- Retrieval cost per query.

- Output generation cost.

- Reserve/settle model reference.

- No billing implementation here.


## 14. Proposed Implementation PR Sequence

- 1. source/document metadata model

- 2. chunk and embedding pipeline stub

- 3. workspace and notebook model

- 4. grounded Q&A API

- 5. citation model and rendering

- 6. source-only mode enforcement

- 7. study output generators

- 8. Persian document extraction adapter

- 9. source deletion and embedding cascade

- 10. Deep Research Agent retrieval integration later


## 15. Open Decisions

- vector store choice

- embedding model choice

- OCR provider

- chunk size and overlap strategy

- citation confidence threshold

- URL source crawling policy

- knowledge base sharing between tenants

- audio overview provider

- Deep Research Agent activation timeline

### Related Documents

- [MULTIMODAL_MEDIA_ASSET_AND_JOB_FOUNDATION.md](MULTIMODAL_MEDIA_ASSET_AND_JOB_FOUNDATION.md)
- [MEMORY_RETENTION_AND_USER_CONTROLS.md](MEMORY_RETENTION_AND_USER_CONTROLS.md)
- [PROMPT_INJECTION_DEFENSE.md](../security/PROMPT_INJECTION_DEFENSE.md)
