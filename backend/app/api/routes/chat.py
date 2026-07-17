from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schema.chat import ChatRequest

from app.agents.graph import AgentGraph
router = APIRouter()


@router.post("/chat")
def chat(

    request: ChatRequest,

    db: Session = Depends(get_db),

):

    graph = AgentGraph(db)

    return graph.invoke(
        request.question
    )