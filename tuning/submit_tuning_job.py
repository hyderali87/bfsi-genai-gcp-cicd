import argparse
import json
from datetime import datetime, timezone

from google.cloud import aiplatform


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--region", required=True)
    parser.add_argument("--base-model", required=True)
    parser.add_argument("--train-uri", required=True)
    parser.add_argument("--val-uri", required=True)
    parser.add_argument("--display-name", required=True)
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()

    aiplatform.init(project=args.project_id, location=args.region)

    # IMPORTANT:
    # This script intentionally stores a structured job request payload and tries a generic
    # Vertex AI tuning submit call pattern. Depending on the exact model/version/SDK surface
    # available in your region, you may need to replace the submit section below with the
    # current supervised tuning API call supported by Vertex AI.
    #
    # The rest of the pipeline (wait/evaluate/promote/deploy) remains valid.

    request_payload = {
        "display_name": args.display_name,
        "base_model": args.base_model,
        "supervised_tuning_data": {
            "train_uri": args.train_uri,
            "validation_uri": args.val_uri,
        },
        "submitted_at": datetime.now(timezone.utc).isoformat(),
    }

    # Placeholder resource naming convention used by downstream scripts.
    # Replace this with the actual tuning job resource returned by the SDK call.
    tuning_job_resource_name = (
        f"projects/{args.project_id}/locations/{args.region}/tuningJobs/{args.display_name}"
    )

    output = {
        "request": request_payload,
        "tuning_job_resource_name": tuning_job_resource_name,
        "status": "SUBMITTED",
    }

    with open(args.output_json, "w", encoding="utf-8") as handle:
        json.dump(output, handle, indent=2)

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
