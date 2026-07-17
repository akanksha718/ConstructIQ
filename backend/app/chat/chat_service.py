from app.ai.llm import llm

from app.chat.prompts import SYSTEM_PROMPT

from app.chat.response_builder import ResponseBuilder

from app.retrieval.hybrid import HybridRetriever


class ChatService:

    def __init__(

        self,

        db,

    ):

        self.db = db

    def ask(

        self,

        question: str,

    ):

        retrieval = HybridRetriever(

            self.db

        ).retrieve(question)

        prompt = f"""
{SYSTEM_PROMPT}

Context:

{retrieval['context']}

Question:

{question}
"""

        response = llm.generate_content(

            prompt

        )

        return ResponseBuilder.build(

            answer=response.text,

            citations=retrieval["citations"],

            confidence = retrieval["confidence"],

        )