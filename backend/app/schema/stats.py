from pydantic import BaseModel


class StatsResponse(BaseModel):

    documents_uploaded: int

    knowledge_entities: int

    equipment_tags: int

    relationships_built: int
