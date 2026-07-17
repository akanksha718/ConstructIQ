from app.ai.client import ai_client

from app.ai.relation_prompt import RELATION_PROMPT


class RelationExtractor:

    def extract(
        self,
        text: str
    ):

        prompt = RELATION_PROMPT.format(
            text=text
        )

        return ai_client.generate_json(prompt)