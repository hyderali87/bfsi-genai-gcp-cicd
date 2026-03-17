import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from google import genai

from app.prompt_builder import build_user_prompt, load_system_prompt
from app.secrets_util import access_secret_text


@dataclass
class AppConfig:
    temperature: float = 0.2
    max_output_tokens: int = 1024


def get_runtime_config() -> AppConfig:
    project_id = os.environ["PROJECT_ID"]
    secret_name = os.getenv("APP_CONFIG_SECRET_NAME", "app-config-json")
    raw = access_secret_text(project_id, secret_name)
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return AppConfig()
    return AppConfig(
        temperature=float(payload.get("temperature", 0.2)),
        max_output_tokens=int(payload.get("max_output_tokens", 1024)),
    )


def get_current_model_name() -> str:
    project_id = os.environ["PROJECT_ID"]
    secret_name = os.getenv("MODEL_SECRET_NAME", "current-tuned-model")
    model_name = access_secret_text(project_id, secret_name).strip()
    if not model_name:
        raise ValueError("Current model secret is empty.")
    return model_name


def generate_answer(user_query: str, context: Optional[str] = None) -> Dict[str, Any]:
    project_id = os.environ["PROJECT_ID"]
    region = os.environ["REGION"]

    system_prompt = load_system_prompt(
        os.getenv("SYSTEM_PROMPT_PATH", "/app/prompts/system_prompt.txt")
    )
    runtime_config = get_runtime_config()
    model_name = get_current_model_name()

    client = genai.Client(vertexai=True, project=project_id, location=region)

    response = client.models.generate_content(
        model=model_name,
        contents=build_user_prompt(user_query, context),
        config={
            "system_instruction": system_prompt,
            "temperature": runtime_config.temperature,
            "max_output_tokens": runtime_config.max_output_tokens,
        },
    )

    text = getattr(response, "text", None)
    if not text and hasattr(response, "candidates"):
        try:
            text = response.candidates[0].content.parts[0].text
        except Exception:
            text = None

    return {
        "model": model_name,
        "answer": text or "",
        "usage": getattr(response, "usage_metadata", None),
    }
