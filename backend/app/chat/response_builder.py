class ResponseBuilder:

    @staticmethod
    def build(

        answer: str,

        citations,

        confidence: float,

    ):

        return {

            "answer": answer,

            "confidence": confidence,

            "citations": citations,

        }