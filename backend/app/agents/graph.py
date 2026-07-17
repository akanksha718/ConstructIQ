from app.agents.supervisor import SupervisorAgent

from app.agents.copilot import CopilotAgent

from app.agents.maintenance import MaintenanceAgent

from app.agents.compliance import ComplianceAgent

from app.agents.lessons import LessonsAgent


class AgentGraph:

    def __init__(self, db):

        self.db = db

    def invoke(

        self,

        question: str,

    ):

        agent = SupervisorAgent.choose(question)

        if agent == "maintenance":

            result = MaintenanceAgent(

                self.db

            ).run(question)
            result["agent"] = agent
            return result

        if agent == "compliance":

            result = ComplianceAgent(

                self.db

            ).run(question)
            result["agent"] = agent
            return result

        if agent == "lessons":

            result = LessonsAgent(

                self.db

            ).run(question)
            result["agent"] = agent
            return result

        result = CopilotAgent(

            self.db

        ).run(question)
        result["agent"] = "copilot"
        return result
