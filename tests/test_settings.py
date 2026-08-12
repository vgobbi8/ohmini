from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from ohmni.config.settings import Settings, SettingsError


class SettingsTests(unittest.TestCase):
    def test_valid_fake_settings(self) -> None:
        settings = Settings.from_env(
            {
                "OHMNI_MODEL_BACKEND": "fake",
                "OHMNI_MODEL_PROVIDER": "fake",
                "OHMNI_MODEL": "fake-model",
                "OHMNI_MODEL_TIMEOUT_SECONDS": "12",
                "OHMNI_GENERATOR": "direct_spice",
                "OHMNI_VALIDATORS": "ngspice",
                "OHMNI_NGSPICE_EXECUTABLE": "ngspice",
                "OHMNI_OUTPUT_DIR": "runs",
            },
            cwd=Path.cwd(),
        )
        self.assertEqual(settings.model_backend, "fake")
        self.assertEqual(settings.config_snapshot()["model"], "fake-model")
        self.assertNotIn("api_key", repr(settings))

    def test_invalid_backend(self) -> None:
        with self.assertRaises(SettingsError):
            Settings.from_env(
                {
                    "OHMNI_MODEL_BACKEND": "unknown",
                    "OHMNI_MODEL_PROVIDER": "fake",
                    "OHMNI_MODEL": "m",
                }
            )

    def test_incompatible_provider(self) -> None:
        with self.assertRaises(SettingsError):
            Settings.from_env(
                {
                    "OHMNI_MODEL_BACKEND": "api",
                    "OHMNI_MODEL_PROVIDER": "codex",
                    "OHMNI_MODEL": "m",
                    "OPENAI_API_KEY": "x",
                }
            )

    def test_google_api_settings(self) -> None:
        settings = Settings.from_env(
            {
                "OHMNI_MODEL_BACKEND": "api",
                "OHMNI_MODEL_PROVIDER": "google",
                "OHMNI_MODEL": "gemini-2.5-flash",
                "GOOGLE_API_KEY": "secret",
            }
        )
        self.assertEqual(settings.model_provider, "google")
        self.assertEqual(settings.api_key, "secret")
        self.assertNotIn("secret", settings.config_snapshot().__repr__())

    def test_harness_google_does_not_need_api_key(self) -> None:
        settings = Settings.from_env(
            {
                "OHMNI_MODEL_BACKEND": "harness",
                "OHMNI_MODEL_PROVIDER": "agy",
                "OHMNI_MODEL": "Gemini 3.6 Flash (Low)",
            }
        )
        self.assertEqual(settings.model_provider, "agy")

    def test_blank_model_rejected(self) -> None:
        with self.assertRaises(SettingsError):
            Settings.from_env(
                {
                    "OHMNI_MODEL_BACKEND": "fake",
                    "OHMNI_MODEL_PROVIDER": "fake",
                    "OHMNI_MODEL": "",
                }
            )

    def test_timeout_rejected(self) -> None:
        with self.assertRaises(SettingsError):
            Settings.from_env(
                {
                    "OHMNI_MODEL_BACKEND": "fake",
                    "OHMNI_MODEL_PROVIDER": "fake",
                    "OHMNI_MODEL": "m",
                    "OHMNI_MODEL_TIMEOUT_SECONDS": "0",
                }
            )

    def test_empty_validators_rejected(self) -> None:
        with self.assertRaises(SettingsError):
            Settings.from_env(
                {
                    "OHMNI_MODEL_BACKEND": "fake",
                    "OHMNI_MODEL_PROVIDER": "fake",
                    "OHMNI_MODEL": "m",
                    "OHMNI_VALIDATORS": "",
                }
            )

    def test_blank_output_dir_rejected(self) -> None:
        with self.assertRaises(SettingsError):
            Settings.from_env(
                {
                    "OHMNI_MODEL_BACKEND": "fake",
                    "OHMNI_MODEL_PROVIDER": "fake",
                    "OHMNI_MODEL": "m",
                    "OHMNI_OUTPUT_DIR": "",
                }
            )


if __name__ == "__main__":
    unittest.main()
