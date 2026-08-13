# 29 — Research Grounding

The implementation should not claim that the Ohmni taxonomy is prescribed by the literature. It is an Ohmni-specific engineering representation informed by research on knowledge representation, declarative/procedural knowledge, rule reasoning, retrieval, and source reliability.

## Key theoretical chain

```text
Knowledge representation
    ↓
explicit concepts and relations useful for reasoning
    ↓
declarative vs procedural knowledge
    ↓
explicit rules / structured procedures
    ↓
external knowledge retrieval and augmentation
    ↓
provenance / source reliability
```

## Main references

See `references/knowledge-engine-references.md` for the full bibliography and links.

Primary grounding:

- Davis, Shrobe & Szolovits (1993), *What Is a Knowledge Representation?*
- Li et al. (2024), declarative and procedural knowledge in LLMs
- Nguyen et al. (2026), procedural knowledge reasoning
- Xu et al. (2026), rule knowledge-driven reasoning
- Alexander et al. (1986), knowledge-level engineering
- Liang et al. (2024), KAG
- Lewis et al. (2020), RAG
- Hwang et al. (2025), source reliability in RAG

## TCC framing

A suitable claim is:

> Ohmni adopts a lightweight task-oriented knowledge representation that makes domain-relevant entities, facts, relations, constraints, formulas, procedures, and tool capabilities explicit. The representation is designed for electronic circuit design but is not intrinsically limited to electronics; other domains may define their own relevant concepts, relationships, rules, and procedures while reusing the same knowledge-engine architecture.
