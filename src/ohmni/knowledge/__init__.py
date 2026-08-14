"""Provider-independent knowledge contracts for Ohmni.

Concrete sources such as Markdown files and KiCad libraries belong in
provider modules.  This package deliberately depends only on the standard
library and Ohmni's own knowledge errors.
"""

from .errors import KnowledgeError, KnowledgeIngestionError, KnowledgeProviderError, KnowledgeSourceError, KnowledgeValidationError
from .taxonomy import ConstraintStrength, KnowledgeFamily, KnowledgeKind
from .provenance import Authority, AuthorityLevel, EpistemicStatus, KnowledgeSource, Provenance, SourceType
from .payloads import ConstraintKnowledge, EntityKnowledge, FactKnowledge, FormulaKnowledge, ProcedureKnowledge, RelationKnowledge, RuleKnowledge, ToolKnowledge
from .items import KnowledgeItem, KnowledgePayload, KnowledgeRelationship

__all__ = [
    "KnowledgeError",
    "KnowledgeIngestionError",
    "KnowledgeProviderError",
    "KnowledgeSourceError",
    "KnowledgeValidationError",
    "ConstraintStrength",
    "KnowledgeFamily",
    "KnowledgeKind",
    "Authority",
    "AuthorityLevel",
    "EpistemicStatus",
    "KnowledgeSource",
    "Provenance",
    "SourceType",
    "ConstraintKnowledge",
    "EntityKnowledge",
    "FactKnowledge",
    "FormulaKnowledge",
    "ProcedureKnowledge",
    "RelationKnowledge",
    "RuleKnowledge",
    "ToolKnowledge",
    "KnowledgeItem",
    "KnowledgePayload",
    "KnowledgeRelationship",
]
