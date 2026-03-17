import argparse
import json
from pathlib import Path


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if stripped:
                rows.append(json.loads(stripped))
    return rows


def heuristic_eval(rows: list[dict]) -> float:
    if not rows:
        return 0.0

    passed = 0
    for row in rows:
        target = row.get("output", "")
        if len(target.split()) >= 8:
            passed += 1
    return passed / len(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--region", required=True)
    parser.add_argument("--model-json", required=True)
    parser.add_argument("--validation-file", required=True)
    parser.add_argument("--min-pass-rate", type=float, required=True)
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()

    with open(args.model_json, "r", encoding="utf-8") as handle:
        model_meta = json.load(handle)

    rows = load_jsonl(Path(args.validation_file))
    pass_rate = heuristic_eval(rows)
    passed = pass_rate >= args.min_pass_rate

    result = {
        "model": model_meta["tuned_model_resource_name"],
        "pass_rate": pass_rate,
        "threshold": args.min_pass_rate,
        "passed": passed,
    }

    with open(args.output_json, "w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2)

    print(json.dumps(result, indent=2))

    if not passed:
        raise SystemExit(
            f"Evaluation gate failed. pass_rate={pass_rate:.3f}, required={args.min_pass_rate:.3f}"
        )


if __name__ == "__main__":
    main()
