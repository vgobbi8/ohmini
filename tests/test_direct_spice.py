from __future__ import annotations

import unittest

from ohmni.generation.contracts import CircuitGenerationRequest
from ohmni.generation.direct_spice import DEFAULT_SYSTEM_PROMPT, DirectSpiceGenerator
from ohmni.generation.errors import GenerationError
from ohmni.model.contracts import FakeModelBackend, ModelResponse


class DirectSpiceGeneratorTests(unittest.TestCase):
    def test_generator_uses_expected_prompt_shape(self) -> None:
        def response(request):
            self.assertEqual(request.system_prompt, DEFAULT_SYSTEM_PROMPT)
            self.assertIn("Requirement:", request.prompt)
            return ModelResponse(
                content="```spice\nV1 in 0 5\nR1 in out 1k\nC1 out 0 1u\n.end\n```",
                metadata={"k": "v"},
            )

        backend = FakeModelBackend(response)
        generator = DirectSpiceGenerator(backend=backend)
        circuit = generator.generate(CircuitGenerationRequest(requirement="RC low-pass filter"))
        self.assertEqual(circuit.netlist, "V1 in 0 5\nR1 in out 1k\nC1 out 0 1u\n.end\n")
        self.assertEqual(circuit.raw_model_response.startswith("```spice"), True)
        self.assertEqual(circuit.model_metadata["k"], "v")

    def test_prose_only_response_rejected(self) -> None:
        backend = FakeModelBackend("Here is your netlist, but no netlist is present.")
        generator = DirectSpiceGenerator(backend=backend)
        with self.assertRaises(GenerationError):
            generator.generate(CircuitGenerationRequest(requirement="RC filter"))

    def test_blank_response_rejected(self) -> None:
        backend = FakeModelBackend("   ")
        generator = DirectSpiceGenerator(backend=backend)
        with self.assertRaises(GenerationError):
            generator.generate(CircuitGenerationRequest(requirement="RC filter"))


if __name__ == "__main__":
    unittest.main()
