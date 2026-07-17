
import jwt

from jwt import PyJWKClient

from app.core.config import settings


JWKS_URL = settings.CLERK_JWKS_URL

jwk_client = PyJWKClient(JWKS_URL)


async def verify_token(token: str):

    signing_key = jwk_client.get_signing_key_from_jwt(token)

    payload = jwt.decode(
        token,
        signing_key.key,
        algorithms=["RS256"],
        issuer=settings.CLERK_ISSUER,
        options={
            "verify_aud": False
        },
    )

    return payload