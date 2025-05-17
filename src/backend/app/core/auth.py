from fastapi import Depends, HTTPException, status, Request, Security
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import jwt, JWTError
from backend.app.core.config import settings
from typing import Dict, List

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login/token",  # must match your actual token generation endpoint
    scopes={
        "system": "Full system access",
        "administrador": "Permission to manage users",
        "pasajero": "Passenger permission",
        "supervisor": "Supervisor permission",
        "mantenimiento": "Maintenance permission",
        "operador": "Operator permission",
    }
)


def encode_token(payload: dict) -> str:
    """
    Encodes a JWT token using the given payload.

    Args:
        payload (dict): Data to encode in the token.

    Returns:
        str: Encoded JWT token.
    """
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def get_current_user(
    security_scopes: SecurityScopes,
    request: Request,
    token: str = Depends(oauth2_scheme)
) -> Dict[str, str]:
    """
    Extracts and verifies the current authenticated user from a JWT token.

    Args:
        security_scopes (SecurityScopes): Required scopes for the route.
        request (Request): The current request.
        token (str): The Bearer token from the header or cookie.

    Returns:
        dict: A dictionary containing the user_id and associated scopes.

    Raises:
        HTTPException: If authentication fails or token is invalid.
    """
    token_cookie = request.cookies.get("access_token")
    if token_cookie:
        token = token_cookie.replace("Bearer ", "")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        scope_string = payload.get("scope", "")
        token_scopes = scope_string.split()

        return {
            "user_id": user_id,
            "scopes": token_scopes
        }

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def verify_role(allowed_roles: List[str]):
    """
    Dependency to verify if the current user has the required role(s).

    Args:
        allowed_roles (List[str]): List of roles allowed to access the route.

    Returns:
        Callable: A dependency function that returns the current user if authorized.

    Raises:
        HTTPException: If the user does not have the required role.
    """

    def _verify(current_user: dict = Depends(get_current_user)):
        if not any(scope in allowed_roles for scope in current_user["scopes"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this route",
            )
        return current_user

    return _verify
