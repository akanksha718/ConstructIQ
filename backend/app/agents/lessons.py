from app.chat.chat_service import ChatService


PROMPT = """
You are a Failure Intelligence AI.

Analyze

Incident Reports

Near Misses

Audit Findings

Failure Records

Return

Patterns

Repeated Failures

Recommendations

Confidence

Citations
"""


class LessonsAgent:

    def __init__(self, db):

        self.chat = ChatService(db)

    def run(

        self,

        question,

    ):

        return self.chat.ask(

            PROMPT + "\n\n" + question

        )