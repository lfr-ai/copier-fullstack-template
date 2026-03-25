"""Extraction prompt templates — entity, relation, and triplet extraction.

FIXME: All constants in this module are currently unused scaffolding.
Import and wire them into extraction pipelines or remove the module.
"""

from __future__ import annotations

TRIPLET_EXTRACTION_PROMPT = (
    "Extract all knowledge graph triplets from the following text.\n\n"
    "Text:\n{text}\n\n"
    "Return a JSON array of triplets, each with:\n"
    '- "subject": the entity or concept\n'
    '- "predicate": the relationship\n'
    '- "object": the related entity or concept\n\n'
    "Example:\n"
    '[{{"subject": "Python", "predicate": "is_a", "object": "programming language"}}]\n\n'
    "Triplets:"
)

ENTITY_EXTRACTION_PROMPT = (
    "Extract all named entities from the following text. "
    "Categorize each entity by type.\n\n"
    "Text:\n{text}\n\n"
    "Return a JSON array of entities, each with:\n"
    '- "name": the entity name\n'
    '- "type": one of PERSON, ORGANIZATION, LOCATION, DATE, CONCEPT, TECHNOLOGY, EVENT\n'
    '- "description": brief description from context\n\n'
    "Entities:"
)

RELATION_EXTRACTION_PROMPT = (
    "Given these entities:\n{entities}\n\n"
    "And this text:\n{text}\n\n"
    "Extract all relationships between the entities.\n\n"
    "Return a JSON array of relationships, each with:\n"
    '- "source": source entity name\n'
    '- "target": target entity name\n'
    '- "relation": the relationship type\n'
    '- "confidence": confidence score 0.0-1.0\n\n'
    "Relationships:"
)
