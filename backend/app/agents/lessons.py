from app.chat.chat_service import ChatService


PROMPT = """
You are a Failure Intelligence AI.

Analyze

Incident Reports

Near Misses

Audit Findings

Failure Records

Format the answer with these headings when the evidence supports them:

1. Observed pattern
2. Supporting incidents or findings
3. Operational lesson
4. Preventive recommendation
5. Evidence limitations

Treat a pattern as tentative unless multiple cited records support it. Never
invent incident frequencies or causal links.
"""


class LessonsAgent:

    def __init__(self, db):

        self.chat = ChatService(db)

    def run(self, question):
        return self.chat.ask(question, instruction=PROMPT)
