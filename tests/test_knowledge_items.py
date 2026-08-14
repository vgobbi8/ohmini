import unittest

from ohmni.knowledge import (
    Authority,
    AuthorityLevel,
    ConstraintKnowledge,
    ConstraintStrength,
    EntityKnowledge,
    EpistemicStatus,
    FactKnowledge,
    FormulaKnowledge,
    KnowledgeFamily,
    KnowledgeItem,
    KnowledgeKind,
    KnowledgeRelationship,
    KnowledgeSource,
    ProcedureKnowledge,
    Provenance,
    RelationKnowledge,
    RuleKnowledge,
    SourceType,
    ToolKnowledge,
)
from ohmni.knowledge.errors import KnowledgeValidationError


def _provenance() -> Provenance:
    return Provenance(
        source=KnowledgeSource("test.source", SourceType.MANUAL_MARKDOWN, "Test source"),
        authority=Authority(AuthorityLevel.CURATED, "test_fixture"),
    )


class KnowledgeItemTests(unittest.TestCase):
    def test_round_trip_each_kind(self) -> None:
        examples = (
            (KnowledgeKind.ENTITY, EntityKnowledge("component", "Device:R")),
            (KnowledgeKind.FACT, FactKnowledge("R1", "resistance", 1000, "ohm")),
            (KnowledgeKind.RELATION, RelationKnowledge("R1", "instance_of", "Device:R")),
            (KnowledgeKind.RULE, RuleKnowledge("Ground references are explicit")),
            (KnowledgeKind.CONSTRAINT, ConstraintKnowledge("R is positive", ConstraintStrength.HARD, "component")),
            (KnowledgeKind.FORMULA, FormulaKnowledge("V = I * R")),
            (KnowledgeKind.PROCEDURE, ProcedureKnowledge("Measure resistance", steps=("Connect meter", "Read value"))),
            (KnowledgeKind.TOOL, ToolKnowledge("ngspice")),
        )
        for kind, payload in examples:
            with self.subTest(kind=kind):
                item = KnowledgeItem(
                    id=f"test.{kind.value}",
                    title=f"Test {kind.value}",
                    family=kind.default_family,
                    kind=kind,
                    payload=payload,
                    provenance=_provenance(),
                    tags=("z", "electronics", "z"),
                    relationships=(KnowledgeRelationship("related_to", "test.other"),),
                )
                restored = KnowledgeItem.from_dict(item.to_dict())
                self.assertEqual(restored, item)
                self.assertEqual(KnowledgeItem.from_dict(__import__("json").loads(item.to_json())), item)

    def test_mismatched_payload_and_kind_fails(self) -> None:
        with self.assertRaises(KnowledgeValidationError):
            KnowledgeItem(
                id="test.bad",
                title="Bad item",
                family=KnowledgeFamily.DECLARATIVE,
                kind=KnowledgeKind.FACT,
                payload=EntityKnowledge("component", "Device:R"),
                provenance=_provenance(),
            )

    def test_provenance_and_status_are_retained(self) -> None:
        item = KnowledgeItem(
            id="test.candidate",
            title="Candidate",
            family=KnowledgeFamily.DECLARATIVE,
            kind=KnowledgeKind.FACT,
            payload=FactKnowledge("R1", "value", "unverified"),
            provenance=_provenance(),
            epistemic_status=EpistemicStatus.CANDIDATE,
        )
        serialized = item.to_dict()
        self.assertEqual(serialized["provenance"]["source"]["source_id"], "test.source")
        self.assertEqual(serialized["epistemic_status"], "candidate")


if __name__ == "__main__":
    unittest.main()
