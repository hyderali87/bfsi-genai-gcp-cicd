from pathlib import Path


def load_system_prompt(path: str) -> str:
    prompt_path = Path(path)
    if not prompt_path.exists():
        return (
            "You are a BFSI domain assistant. Provide precise, compliant, and concise "
            "answers. Avoid unsupported claims. Ask for missing risk-critical details."
        )
    return prompt_path.read_text(encoding="utf-8")


def build_user_prompt(user_query: str, context: str | None = None) -> str:
    if context:
        return f"Context:\n{context}\n\nUser Query:\n{user_query}"
    return user_query
