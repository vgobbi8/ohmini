# Ohmni TCC — Knowledge Engine Research References

This document consolidates the research references discussed for the Ohmni Knowledge Engine, including direct publisher/proceedings links and DOI or arXiv links where available.

---

## Most important for the TCC Knowledge Engine

### 1. Davis, Shrobe & Szolovits (1993) — Knowledge Representation

**DAVIS, Randall; SHROBE, Howard; SZOLOVITS, Peter.** What Is a Knowledge Representation? *AI Magazine*, v. 14, n. 1, p. 17–33, 1993.

**In-text citation:** `(DAVIS; SHROBE; SZOLOVITS, 1993)`

**Why it matters for Ohmni:**  
Main theoretical reference for justifying a task-oriented knowledge representation composed of explicit concepts, relations, rules, and other structures useful for reasoning.

**Links:**
- Publisher / article: https://onlinelibrary.wiley.com/doi/10.1609/aimag.v14i1.1029
- MIT-hosted full text: https://groups.csail.mit.edu/medg/ftp/psz/k-rep.html
- DOI: https://doi.org/10.1609/aimag.v14i1.1029

---

### 2. Li et al. (2024) — Declarative and Procedural Knowledge

**LI, Zhuoqun; LIN, Hongyu; LU, Yaojie; XIANG, Hao; HAN, Xianpei; SUN, Le.** Meta-Cognitive Analysis: Evaluating Declarative and Procedural Knowledge in Datasets and Large Language Models. In: *Proceedings of the 2024 Joint International Conference on Computational Linguistics, Language Resources and Evaluation (LREC-COLING 2024)*. Torino: ELRA and ICCL, 2024. p. 11222–11228.

**In-text citation:** `(LI et al., 2024)`

**Why it matters for Ohmni:**  
Useful for grounding the explicit distinction between **declarative knowledge** and **procedural knowledge** in a context involving large language models.

**Links:**
- ACL Anthology: https://aclanthology.org/2024.lrec-main.980/
- PDF: https://aclanthology.org/2024.lrec-main.980.pdf
- arXiv: https://arxiv.org/abs/2403.09750

---

### 3. Nguyen et al. (2026) — Structured Procedural Knowledge

**NGUYEN, Thanh-Son; YANG, Hong; NEOH, Tzeh Yuan; ZHANG, Hao; YEO KEAT, Ee; FERNANDO, Basura.** PKR-QA: A Benchmark for Procedural Knowledge Reasoning with Knowledge Module Learning. *Proceedings of the AAAI Conference on Artificial Intelligence*, v. 40, n. 29, p. 24549–24557, 2026.

**In-text citation:** `(NGUYEN et al., 2026)`

**Why it matters for Ohmni:**  
Supports representing procedural knowledge explicitly and reasoning over structured procedural information.

**Links:**
- AAAI: https://ojs.aaai.org/index.php/AAAI/article/view/39638
- DOI: https://doi.org/10.1609/aaai.v40i29.39638

---

### 4. Xu et al. (2026) — Rule Knowledge

**XU, Zijie; KE, Wenjun; WANG, Peng; LI, Guozheng; NI, Qingjian; LIU, Jiajun; SHANG, Ziyu; ZHOU, Jing.** Benchmarking and Enhancing Rule Knowledge-Driven Reasoning of Large Language Models. *Proceedings of the AAAI Conference on Artificial Intelligence*, v. 40, n. 40, p. 34187–34195, 2026.

**In-text citation:** `(XU et al., 2026)`

**Why it matters for Ohmni:**  
Particularly useful for justifying **rules** as explicit knowledge resources and for discussing how LLMs reason when supplied with rule knowledge rather than relying only on examples.

**Links:**
- AAAI: https://ojs.aaai.org/index.php/AAAI/article/view/40714
- DOI: https://doi.org/10.1609/aaai.v40i40.40714

---

### 5. Alexander et al. (1986) — Knowledge Engineering and Ontological Analysis

**ALEXANDER, James H.; FREILING, Michael J.; SHULMAN, Sheryl J.; STALEY, Jeffery L.; REHFUSS, Steven; MESSICK, Steven L.** Knowledge Level Engineering: Ontological Analysis. In: *Proceedings of the Fifth National Conference on Artificial Intelligence (AAAI-86)*. Philadelphia: AAAI Press, 1986. p. 963–968.

**In-text citation:** `(ALEXANDER et al., 1986)`

**Why it matters for Ohmni:**  
Supports the broader knowledge-engineering view in which a domain is modeled through explicit knowledge elements, a knowledge base, and procedures used to reason over that knowledge.

**Links:**
- AAAI archive: https://www.aaai.org/Library/AAAI/1986/aaai86-159.php
- Alternate AAAI archive host: https://vvvvw.aaai.org/Library/AAAI/1986/aaai86-159.php

---

## Knowledge augmentation / retrieval architecture

### 6. Liang et al. (2024) — Knowledge Augmented Generation (KAG)

**LIANG, Lei et al.** KAG: Boosting LLMs in Professional Domains via Knowledge Augmented Generation. *arXiv*, 2024. arXiv:2409.13731.

**In-text citation:** `(LIANG et al., 2024)`

**Why it matters for Ohmni:**  
Highly relevant because it discusses professional-domain knowledge, expert rules, numerical relationships, structured knowledge, and links between structured representations and original textual chunks instead of relying exclusively on vector similarity.

**Links:**
- arXiv: https://arxiv.org/abs/2409.13731
- PDF: https://arxiv.org/pdf/2409.13731
- DOI for arXiv record: https://doi.org/10.48550/arXiv.2409.13731

---

### 7. Lewis et al. (2020) — Retrieval-Augmented Generation

**LEWIS, Patrick; PEREZ, Ethan; PIKTUS, Aleksandra; PETRONI, Fabio; KARPUKHIN, Vladimir; GOYAL, Naman; KÜTTLER, Heinrich; LEWIS, Mike; YIH, Wen-tau; ROCKTÄSCHEL, Tim; RIEDEL, Sebastian; KIELA, Douwe.** Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. In: *Advances in Neural Information Processing Systems 33 (NeurIPS 2020)*. 2020.

**In-text citation:** `(LEWIS et al., 2020)`

**Why it matters for Ohmni:**  
Foundational RAG reference. For Ohmni, it primarily grounds the use of external retrievable knowledge rather than depending only on knowledge encoded in model parameters.

**Links:**
- NeurIPS: https://neurips.cc/virtual/2020/public/poster_6b493230205f780e1bc26945df7481e5.html
- arXiv: https://arxiv.org/abs/2005.11401
- PDF: https://arxiv.org/pdf/2005.11401

---

### 8. Hwang et al. (2025) — Source Reliability in RAG

**HWANG, Jeongyeon; PARK, Junyoung; PARK, Hyejin; KIM, Dongwoo; PARK, Sangdon; OK, Jungseul.** Retrieval-Augmented Generation with Estimation of Source Reliability. In: *Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing (EMNLP 2025)*. Suzhou, China: Association for Computational Linguistics, 2025. p. 34279–34303.

**In-text citation:** `(HWANG et al., 2025)`

**Why it matters for Ohmni:**  
Useful for motivating provenance, source reliability, and concepts such as `source`, `authority`, or `authority_scope`, since retrieval relevance alone does not imply source reliability.

**Links:**
- ACL Anthology: https://aclanthology.org/2025.emnlp-main.1738/
- PDF: https://aclanthology.org/2025.emnlp-main.1738.pdf
- DOI: https://doi.org/10.18653/v1/2025.emnlp-main.1738
- Original arXiv version: https://arxiv.org/abs/2410.22954

> **Note:** An earlier version of this bibliography cited the 2024 arXiv preprint. A peer-reviewed EMNLP 2025 version is now available and should be preferred in the TCC bibliography.

---

## Agent-memory papers

These are relevant references, but they should **not** be used as the primary theoretical basis of the Ohmni Knowledge Engine. They are better suited to a future agent-memory or experience-learning subsystem.

### 9. Xu et al. (2025) — A-Mem

**XU, Wujiang; LIANG, Zujie; MEI, Kai; GAO, Hang; TAN, Juntao; ZHANG, Yongfeng.** A-Mem: Agentic Memory for LLM Agents. In: *Advances in Neural Information Processing Systems 38 (NeurIPS 2025)*. 2025.

**In-text citation:** `(XU et al., 2025)`

**Why it matters for Ohmni:**  
Potentially useful for a future subsystem in which agents retain, organize, and retrieve knowledge derived from previous design experiences.

**Links:**
- NeurIPS proceedings: https://proceedings.neurips.cc/paper_files/paper/2025/hash/19909c36f51abc4856b4560aff3d36d6-Abstract-Conference.html
- arXiv: https://arxiv.org/abs/2502.12110
- PDF: https://arxiv.org/pdf/2502.12110

---

### 10. Cao et al. (2026) — Dynamic Procedural Memory

**CAO, Zouying; DENG, Jiaji; YU, Li; ZHOU, Weikang; LIU, Zhaoyang; DING, Bolin; ZHAO, Hai.** Remember Me, Refine Me: A Dynamic Procedural Memory Framework for Experience-Driven Agent Evolution. In: *Findings of the Association for Computational Linguistics: ACL 2026*. San Diego, California, United States: Association for Computational Linguistics, 2026. p. 16803–16822.

**In-text citation:** `(CAO et al., 2026)`

**Why it matters for Ohmni:**  
Relevant if Ohmni later allows agents to derive, retain, refine, and reuse procedural knowledge from previous circuit-design attempts.

**Links:**
- ACL Anthology: https://aclanthology.org/2026.findings-acl.829/
- PDF: https://aclanthology.org/2026.findings-acl.829.pdf
- DOI: https://doi.org/10.18653/v1/2026.findings-acl.829
- arXiv: https://arxiv.org/abs/2512.10696

---

## Suggested citation grouping for the Ohmni Knowledge Engine

For the section that introduces the structured knowledge representation itself, the strongest initial group is:

`(DAVIS; SHROBE; SZOLOVITS, 1993; LI et al., 2024; NGUYEN et al., 2026; XU et al., 2026)`

These references support the chain:

**Knowledge representation → declarative/procedural knowledge → structured procedural knowledge → explicit rule-based reasoning.**

For the architecture that retrieves and combines external knowledge, add:

`(LEWIS et al., 2020; LIANG et al., 2024)`

For provenance and source reliability:

`(HWANG et al., 2025)`

For future agent memory and experience learning:

`(XU et al., 2025; CAO et al., 2026)`

---

## Proposed Ohmni knowledge taxonomy motivated by these references

```text
Knowledge
│
├── Declarative Knowledge
│   ├── Entity / Concept
│   ├── Fact
│   ├── Relation
│   ├── Rule
│   ├── Constraint
│   └── Formula
│
├── Procedural Knowledge
│   └── Procedure
│       ├── prerequisites
│       ├── inputs
│       ├── steps
│       └── expected outputs
│
└── Operational / Meta Knowledge
    ├── Tool capability
    ├── Applicability
    ├── Source
    ├── Authority
    └── Version
```

The taxonomy above is an **Ohmni-specific engineering design informed by the cited literature**. The cited works motivate structured knowledge representation and distinctions such as declarative, procedural, and rule knowledge; they do not prescribe this exact taxonomy.
