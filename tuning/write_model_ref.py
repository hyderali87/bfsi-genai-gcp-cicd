import argparse
import json

from google.cloud import secretmanager


def add_secret_version(project_id: str, secret_name: str, payload: str) -> None:
    client = secretmanager.SecretManagerServiceClient()
    parent = f"projects/{project_id}/secrets/{secret_name}"
    client.add_secret_version(
        request={"parent": parent, "payload": {"data": payload.encode("utf-8")}}
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--secret-name", required=True)
    parser.add_argument("--model-json", required=True)
    args = parser.parse_args()

    with open(args.model_json, "r", encoding="utf-8") as handle:
        model_meta = json.load(handle)

    model_name = model_meta["tuned_model_resource_name"]
    add_secret_version(args.project_id, args.secret_name, model_name)
    print(f"Promoted model '{model_name}' into secret '{args.secret_name}'.")


if __name__ == "__main__":
    main()
