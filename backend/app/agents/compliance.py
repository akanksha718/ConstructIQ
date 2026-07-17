from app.chat.chat_service import ChatService


PROMPT = """
You are an Industrial Compliance Expert.

Check

Factory Act

OISD

PESO

ISO

Environmental Standards

Use ONLY supplied documents.

Provide

Compliance Status

Missing Evidence

Recommendations

Confidence

Citations
"""


class ComplianceAgent:

    def __init__(self, db):

        self.chat = ChatService(db)

    def run(

        self,

        question,

    ):

        return self.chat.ask(

            PROMPT + "\n\n" + question

        )