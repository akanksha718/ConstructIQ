from app.chat.chat_service import ChatService


class CopilotAgent:

    def __init__(self, db):

        self.chat = ChatService(db)

    def run(

        self,

        question: str,

    ):

        return self.chat.ask(question)