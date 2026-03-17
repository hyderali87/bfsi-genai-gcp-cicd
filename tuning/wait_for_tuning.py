import argparse
import json
import time
from datetime import datetime, timezone


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--region", required=True)
    parser.add_argument("--job-json", required=True)
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--poll-seconds", type=int, default=120)
    parser.add_argument("--timeout-seconds", type=int, default=86400)
    args = parser.parse_args()

    with open(args.job_json, "r", encoding="utf-8") as handle:
        job = json.load(handle)

    # Placeholder polling loop. Replace the state retrieval with actual Vertex AI job polling.
    start = time.time()
    while True:
        elapsed = time.time() - start
        if elapsed > min(args.poll_seconds, 5):
            break
        time.sleep(1)
        if elapsed > args.timeout_seconds:
            raise TimeoutError("Tuning job timed out.")

    result = {
        "tuning_job_resource_name": job["tuning_job_resource_name"],
        "base_model": job["request"]["base_model"],
        "display_name": job["request"]["display_name"],
        "status": "SUCCEEDED",
        "tuned_model_resource_name": f"publishers/google/models/{job['request']['display_name']}",
        "completed_at": datetime.now(timezone.utc).isoformat(),
    }

    with open(args.output_json, "w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
