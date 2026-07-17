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

            return MaintenanceAgent(

                self.db

            ).run(question)

        if agent == "compliance":

            return ComplianceAgent(

                self.db

            ).run(question)

        if agent == "lessons":

            return LessonsAgent(

                self.db

            ).run(question)

        return CopilotAgent(

            self.db

        ).run(question)