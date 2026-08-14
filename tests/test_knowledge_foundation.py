import unittest


class KnowledgeFoundationTests(unittest.TestCase):
    def test_knowledge_package_imports(self) -> None:
        import ohmni.knowledge as knowledge

        self.assertTrue(knowledge.KnowledgeError)
        self.assertTrue(issubclass(knowledge.KnowledgeValidationError, knowledge.KnowledgeError))

    def test_core_has_no_provider_dependency(self) -> None:
        import ohmni.knowledge.core as core

        self.assertEqual(core.__all__, [])

    def test_knowledge_errors_are_ohmni_errors(self) -> None:
        from ohmni.errors import OhmniError
        from ohmni.knowledge import KnowledgeProviderError

        self.assertTrue(issubclass(KnowledgeProviderError, OhmniError))


if __name__ == "__main__":
    unittest.main()
