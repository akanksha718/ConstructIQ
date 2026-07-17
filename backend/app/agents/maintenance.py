from app.chat.chat_service import ChatService


PROMPT = """
You are an Industrial Maintenance Expert.

Answer using

OEM Manuals

Maintenance Records

Inspection Reports

Failure History

Provide:

1. Probable Root Cause

2. Recommended Action

3. Confidence

4. Citations

Do not hallucinate.
"""


class MaintenanceAgent:

    def __init__(self, db):

        self.chat = ChatService(db)

    def run(self, question):
        return self.chat.ask(question, instruction=PROMPT)