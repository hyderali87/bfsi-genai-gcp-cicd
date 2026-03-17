import argparse
import json
from pathlib import Path


REQUIRED_KEYS = {"input", "output"}


def validate_jsonl(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    errors = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                errors.append(f"Line {line_no}: empty line not allowed")
                continue
            try:
                row = json.loads(stripped)
            except json.JSONDecodeError as exc:
                errors.append(f"Line {line_no}: invalid JSON: {exc}")
                continue

            missing = REQUIRED_KEYS - row.keys()
            if missing:
                errors.append(f"Line {line_no}: missing keys {sorted(missing)}")
                continue

            if not isinstance(row["input"], str) or not row["input"].strip():
                errors.append(f"Line {line_no}: input must be a non-empty string")

            if not isinstance(row["output"], str) or not row["output"].strip():
                errors.append(f"Line {line_no}: output must be a non-empty string")

    if errors:
        joined = "\n".join(errors[:50])
        raise ValueError(f"Dataset validation failed:\n{joined}")

    print(f"Validation passed for {path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    args = parser.parse_args()
    validate_jsonl(Path(args.file))


if __name__ == "__main__":
    main()
