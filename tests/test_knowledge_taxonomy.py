import json
import unittest

from ohmni.knowledge import ConstraintStrength, KnowledgeFamily, KnowledgeKind


class KnowledgeTaxonomyTests(unittest.TestCase):
    def test_enum_values_are_stable_and_json_serializable(self) -> None:
        self.assertEqual(KnowledgeFamily.DECLARATIVE.value, "declarative")
        self.assertEqual(KnowledgeKind.ENTITY.value, "entity")
        self.assertEqual(ConstraintStrength.RECOMMENDATION.value, "recommendation")
        self.assertEqual(json.loads(json.dumps(KnowledgeKind.FACT)), "fact")

    def test_enum_values_round_trip(self) -> None:
        for family in KnowledgeFamily:
            self.assertIs(KnowledgeFamily.from_value(family.value), family)
        for kind in KnowledgeKind:
            self.assertIs(KnowledgeKind.from_value(kind.value), kind)
        for strength in ConstraintStrength:
            self.assertIs(ConstraintStrength.from_value(strength.value), strength)

    def test_default_family_mapping(self) -> None:
        expected = {
            KnowledgeKind.ENTITY: KnowledgeFamily.DECLARATIVE,
            KnowledgeKind.FACT: KnowledgeFamily.DECLARATIVE,
            KnowledgeKind.RELATION: KnowledgeFamily.DECLARATIVE,
            KnowledgeKind.RULE: KnowledgeFamily.DECLARATIVE,
            KnowledgeKind.CONSTRAINT: KnowledgeFamily.DECLARATIVE,
            KnowledgeKind.FORMULA: KnowledgeFamily.DECLARATIVE,
            KnowledgeKind.PROCEDURE: KnowledgeFamily.PROCEDURAL,
            KnowledgeKind.TOOL: KnowledgeFamily.OPERATIONAL,
        }
        self.assertEqual({kind: kind.default_family for kind in KnowledgeKind}, expected)

    def test_invalid_enum_values_are_rejected(self) -> None:
        for enum_type in (KnowledgeFamily, KnowledgeKind, ConstraintStrength):
            with self.subTest(enum_type=enum_type):
                with self.assertRaises(ValueError):
                    enum_type.from_value("not-a-valid-value")
                with self.assertRaises(ValueError):
                    enum_type.from_value(" ")


if __name__ == "__main__":
    unittest.main()
