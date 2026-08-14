import unittest

from ohmni.knowledge import (
    ConstraintKnowledge,
    ConstraintStrength,
    EntityKnowledge,
    FactKnowledge,
    FormulaKnowledge,
    ProcedureKnowledge,
    RelationKnowledge,
    RuleKnowledge,
    ToolKnowledge,
)
from ohmni.knowledge.errors import KnowledgeValidationError


class KnowledgePayloadTests(unittest.TestCase):
    def test_construct_and_serialize_each_payload(self) -> None:
        payloads = [
            EntityKnowledge("component", "Device:R", aliases=("resistor",)),
            FactKnowledge("Device:R", "resistance", 1000, "ohm"),
            RelationKnowledge("R1", "instance_of", "Device:R"),
            RuleKnowledge("Reference nodes must be explicit", consequences=("Add a ground reference",)),
            ConstraintKnowledge("Resistance must be positive", ConstraintStrength.HARD, "passive_component"),
            FormulaKnowledge("fc = 1 / (2 * pi * R * C)", variables={"R": "resistance"}, units={"R": "ohm"}),
            ProcedureKnowledge("Design an RC low-pass", steps=("Choose R", "Choose C", "Validate cutoff")),
            ToolKnowledge("ngspice", capabilities=("simulate SPICE",), limitations=("does not prove PCB correctness",)),
        ]
        for payload in payloads:
            with self.subTest(payload=type(payload).__name__):
                serialized = payload.to_dict()
                self.assertIsInstance(serialized, dict)
                self.assertTrue(serialized)

    def test_procedure_steps_preserve_order(self) -> None:
        procedure = ProcedureKnowledge("goal", steps=("first", "second", "third"))
        self.assertEqual(procedure.to_dict()["steps"], ["first", "second", "third"])

    def test_constraint_strength_serializes_as_string(self) -> None:
        constraint = ConstraintKnowledge("Use a ground", ConstraintStrength.RECOMMENDATION, "simulation")
        self.assertEqual(constraint.to_dict()["strength"], "recommendation")

    def test_required_fields_are_validated(self) -> None:
        invalid = (
            lambda: EntityKnowledge("", "name"),
            lambda: FactKnowledge("subject", "", 1),
            lambda: RelationKnowledge("subject", "predicate", ""),
            lambda: RuleKnowledge(""),
            lambda: ConstraintKnowledge("statement", ConstraintStrength.HARD, ""),
            lambda: FormulaKnowledge(""),
            lambda: ProcedureKnowledge("", steps=("step",)),
            lambda: ToolKnowledge(""),
        )
        for factory in invalid:
            with self.subTest(factory=factory):
                with self.assertRaises(KnowledgeValidationError):
                    factory()


if __name__ == "__main__":
    unittest.main()
