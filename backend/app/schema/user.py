from pydantic import BaseModel


class CurrentUser(BaseModel):
    clerk_id: str
    email: str | None = None
    role: str = "viewer"