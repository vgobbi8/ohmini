"""Errors shared by the knowledge boundary."""

from ohmni.errors import OhmniError


class KnowledgeError(OhmniError):
    """Base class for knowledge-domain and provider failures."""


class KnowledgeValidationError(KnowledgeError):
    """A knowledge object or document is malformed."""


class KnowledgeSourceError(KnowledgeError):
    """A configured knowledge source is missing or unavailable."""


class KnowledgeProviderError(KnowledgeError):
    """A provider failed while retrieving or normalizing knowledge."""


class KnowledgeIngestionError(KnowledgeError):
    """A source could not be ingested into normalized knowledge."""
