from app.ai.client import ai_client

from app.ai.prompts import ENTITY_PROMPT


class EntityExtractor:

    def extract(
        self,
        text: str
    ):

        prompt = ENTITY_PROMPT.format(
            text=text
        )

        return ai_client.generate_json(prompt)