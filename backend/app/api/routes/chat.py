from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schema.chat import ChatRequest
from app.schema.chat import ChatResponse

router = APIRouter()


@router.post("/", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
):
    # Imported lazily so optional AI/agent dependencies (Gemini, Neo4j, ...)
    # never prevent the rest of the API from starting.
    try:
        from app.agents.graph import AgentGraph
    except Exception as exc:  # pragma: no cover - optional dependency
        raise HTTPException(
            status_code=503,
            detail=f"Chat agent is not available: {exc}",
        )

    graph = AgentGraph(db)

    return graph.invoke(request.question)
