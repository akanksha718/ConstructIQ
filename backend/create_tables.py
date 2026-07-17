from app.core.database import Base
from app.core.database import engine

# Import ALL models here
from app.models.document import Document
from app.models.chunk import Chunk
from app.models.entity import Entity
from app.models.relationship import Relationship
from app.models.embedding import Embedding

Base.metadata.create_all(bind=engine)

print("Database tables created successfully.")