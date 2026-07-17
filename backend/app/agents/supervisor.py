import json

from app.ai.llm import llm


SUPERVISOR_PROMPT = """
You are the Supervisor of ConstructIQ AI.

Choose ONE agent.

Possible agents:

- copilot
- maintenance
- compliance
- lessons

Return ONLY JSON.

Example:

{
    "agent":"maintenance"
}
"""


class SupervisorAgent:

    @staticmethod
    def choose(question: str):

        response = llm.generate_content(

            SUPERVISOR_PROMPT + question

        )

        return json.loads(response.text)["agent"]