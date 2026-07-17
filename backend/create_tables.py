from app.core.database import Base
from app.core.database import engine

# Import ALL models so they are registered on the metadata.
import app.models  # noqa: F401

Base.metadata.create_all(bind=engine)

print("Database tables created successfully.")
