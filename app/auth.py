from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from .config import settings

api_key_header_scheme = APIKeyHeader(name="x-api-key", auto_error=False)

def get_api_key(api_key_header: str = Security(api_key_header_scheme)):
    if not api_key_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Falta la API Key (x-api-key).",
        )
    if api_key_header == settings.master_key:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="No autorizado. La llave es incorrecta."
    )
