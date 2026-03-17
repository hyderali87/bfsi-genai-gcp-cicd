import os
from typing import Optional

from fastapi import Header, HTTPException, status

from app.secrets_util import access_secret_text


def verify_api_key(x_api_key: Optional[str] = Header(default=None)) -> None:
    require_api_key = os.getenv("REQUIRE_API_KEY", "false").lower() == "true"
    if not require_api_key:
        return

    secret_name = os.getenv("API_KEY_SECRET_NAME", "bfsi-api-key")
    project_id = os.environ["PROJECT_ID"]
    expected = access_secret_text(project_id, secret_name).strip()

    if not x_api_key or x_api_key.strip() != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key.",
        )
