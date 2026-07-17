from fastapi import Header
from fastapi import HTTPException
from fastapi import Depends
import jwt

from app.auth.clerk import verify_token


async def get_current_user(
    authorization: str = Header(...)
):

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    token = authorization.replace("Bearer ", "")

    try:

        payload = await verify_token(token)

        return payload

    except jwt.InvalidTokenError:

        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )


async def require_admin(
    user=Depends(get_current_user)
):

    role = (
        user.get("metadata", {}).get("role")
        or user.get("publicMetadata", {}).get("role")
        or user.get("public_metadata", {}).get("role")
        or user.get("unsafeMetadata", {}).get("role")
    )

    if role != "admin":

        raise HTTPException(
            status_code=403,
            detail="Admin only"
        )

    return user