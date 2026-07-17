from fastapi import APIRouter, Depends

from app.schemas.user import CurrentUser
from app.auth.dependencies import get_current_user

router = APIRouter(
    prefix="/api",
    tags=["Users"],
)


@router.get("/me")
async def me(
    current_user: CurrentUser = Depends(get_current_user),
):
    return current_user