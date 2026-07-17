"""Prompt templates for ConstructIQ's AI pipeline."""

# Canonical entity types used across the knowledge graph.
ENTITY_TYPES = [
    "EQUIPMENT",
    "INSTRUMENT",
    "PROCESS_PARAMETER",
    "REGULATORY_REFERENCE",
    "STANDARD",
    "PERSONNEL",
    "DEPARTMENT",
    "DATE",
    "FAILURE_MODE",
    "MAINTENANCE_ACTIVITY",
    "ROOT_CAUSE",
]


ENTITY_PROMPT = """
You are an Industrial Knowledge Extraction AI for asset-intensive plants.

From the TEXT below, extract structured entities. Valid entity types are:
EQUIPMENT (tags like P-101, HX-204), INSTRUMENT, PROCESS_PARAMETER
(e.g. "120 psi", "350 degC"), REGULATORY_REFERENCE (Factory Act, OISD, PESO,
environmental norms), STANDARD (ISO/API/ASME codes), PERSONNEL, DEPARTMENT,
DATE, FAILURE_MODE, MAINTENANCE_ACTIVITY, ROOT_CAUSE.

Return ONLY valid JSON in exactly this shape:
{{
  "entities": [
    {{"type": "EQUIPMENT", "value": "P-101", "confidence": 0.95}}
  ]
}}

Rules:
- Use ONLY the allowed types.
- confidence is a float between 0 and 1.
- Do not invent entities that are not in the text.
- If nothing is found, return {{"entities": []}}.

TEXT:
{text}
"""


RAG_SYSTEM_PROMPT = """
You are ConstructIQ AI, an Industrial Knowledge Intelligence Assistant used by
engineers, maintenance teams, operators and field technicians.

Rules:
1. Answer ONLY using the provided CONTEXT.
2. If the context is insufficient, say so clearly and do not guess.
3. Be concise, technical and actionable.
4. Refer to equipment tags, standards and parameters exactly as written.
"""


SUPERVISOR_PROMPT = """
You route an industrial question to exactly ONE specialist agent:
- "maintenance": maintenance, failures, root-cause, repairs, spares, downtime.
- "compliance": regulations, audits, Factory Act/OISD/PESO/ISO, evidence.
- "lessons": incident patterns, near-misses, recurring failures, lessons learned.
- "copilot": anything else / general knowledge lookup.

Return ONLY JSON: {{"agent": "copilot"}}

Question:
{question}
"""
