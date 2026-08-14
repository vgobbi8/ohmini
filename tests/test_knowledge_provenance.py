import unittest

from ohmni.knowledge import (
    Authority,
    AuthorityLevel,
    EpistemicStatus,
    KnowledgeSource,
    Provenance,
    SourceType,
)
from ohmni.knowledge.errors import KnowledgeValidationError


class KnowledgeProvenanceTests(unittest.TestCase):
    def test_source_round_trip(self) -> None:
        source = KnowledgeSource(
            source_id="knowledge.manual",
            source_type=SourceType.MANUAL_MARKDOWN,
            name="Manual electronics knowledge",
            location="knowledge/formulas/rc.md",
            version="1",
            provider="markdown",
            metadata={"topic": "electronics", "api_key": "must not persist"},
        )
        restored = KnowledgeSource.from_dict(source.to_dict())
        self.assertEqual(restored, source)
        self.assertNotIn("api_key", source.to_dict()["metadata"])

    def test_authority_scope_is_retained(self) -> None:
        authority = Authority(AuthorityLevel.AUTHORITATIVE, "kicad_symbol_definition")
        self.assertEqual(authority.authority_scope, "kicad_symbol_definition")
        self.assertEqual(AuthorityLevel(authority.to_dict()["level"]), AuthorityLevel.AUTHORITATIVE)

    def test_candidate_agent_status_is_explicit(self) -> None:
        provenance = Provenance(
            source=KnowledgeSource("agent.draft", SourceType.AGENT_MEMORY, "Agent draft"),
            authority=Authority(AuthorityLevel.UNVERIFIED, "candidate_design_guidance"),
            epistemic_status=EpistemicStatus.CANDIDATE,
        )
        restored = Provenance.from_dict(provenance.to_dict())
        self.assertEqual(restored.epistemic_status, EpistemicStatus.CANDIDATE)
        self.assertEqual(restored.authority.level, AuthorityLevel.UNVERIFIED)

    def test_metadata_is_sanitized_recursively(self) -> None:
        source = KnowledgeSource(
            "source",
            SourceType.UNKNOWN,
            "Source",
            metadata={"nested": {"token": "secret", "safe": "value"}},
        )
        self.assertEqual(source.to_dict()["metadata"], {"nested": {"safe": "value"}})

    def test_blank_scope_is_rejected(self) -> None:
        with self.assertRaises(KnowledgeValidationError):
            Authority(AuthorityLevel.CURATED, " ")


if __name__ == "__main__":
    unittest.main()
