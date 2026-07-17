import json

from app.ai.llm import llm
from app.ai.prompts import INDUSTRIAL_EXTRACTION_PROMPT
from app.ai.llm import llm

class KnowledgeExtractor:

    PROMPT = """
You are an Industrial Knowledge Extraction AI.

Extract:

1. Equipment
2. Instruments
3. Process Parameters
4. Standards
5. Departments
6. People
7. Dates
8. Failure Modes
9. Maintenance Activities
10. Relationships

Return ONLY JSON.
"""

    def extract(

        self,

        chunk: str,

    ):

        response = llm.generate_content(
            INDUSTRIAL_EXTRACTION_PROMPT + chunk
        )

        return json.loads(

            response.text

        )