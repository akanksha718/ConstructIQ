RELATION_PROMPT = """
You extract relationships between industrial entities from the TEXT below.

Return ONLY valid JSON in exactly this shape:
{{
  "relationships": [
    {{
      "source": "Pump P-101",
      "relation": "CONNECTED_TO",
      "target": "Valve V-11",
      "confidence": 0.8
    }}
  ]
}}

Common relations: CONNECTED_TO, PART_OF, LOCATED_IN, MAINTAINED_BY,
GOVERNED_BY, HAS_PARAMETER, CAUSED_BY, INSPECTED_BY, OPERATED_BY.

Rules:
- source/target must be concrete entities mentioned in the text.
- confidence is a float between 0 and 1.
- If none, return {{"relationships": []}}.

TEXT:
{text}
"""
