# BFSI GenAI App on GCP (GitHub → Cloud Build → Vertex AI → Cloud Run)

This project bootstraps a **fully automated CI/CD + LLM tuning flow** for a BFSI application on GCP.

## What it includes

- **FastAPI** inference app for Cloud Run
- **Cloud Build** pipelines:
  - `cloudbuild.app.yaml` for application CI/CD
  - `cloudbuild.train.yaml` for dataset validation, Vertex AI tuning, evaluation, model promotion, and redeploy
- **Vertex AI** tuning helper scripts
- **Terraform** for GCP infrastructure
- **Sample BFSI training data**
- **GitHub Actions not required**; GitHub only acts as source repository for Cloud Build triggers

## Reference architecture

GitHub push  
→ Cloud Build trigger  
→ validate dataset / code  
→ submit Vertex AI tuning job  
→ wait for completion  
→ run evaluation gate  
→ update current model reference in Secret Manager  
→ build and deploy Cloud Run service

## Important notes

1. **No manual execution after bootstrap**: once the project, IAM, repo connection, and triggers are created, pushes to GitHub drive the pipeline automatically.
2. **One-time bootstrap still exists**: GitHub connection and GCP project bootstrap are first-time setup tasks.
3. **Tuning API surface changes over time**: `tuning/submit_tuning_job.py` is structured so you can swap the exact SDK call if your chosen Gemini tuning method changes slightly by region/model/version.
4. **This repository is intentionally modular**: you can adapt it to:
   - Gemini supervised tuning on Vertex AI
   - an open model fine-tuning/deployment path
   - RAG + fine-tuned response style hybrid design

## Expected repository layout

```text
bfsi-genai-gcp-cicd/
├── app/
├── infra/terraform/
├── prompts/
├── training_data/
├── tuning/
├── cloudbuild.app.yaml
├── cloudbuild.train.yaml
├── Dockerfile
└── README.md
```

## Bootstrap sequence

### 1) Create the Terraform backend bucket
Create a GCS bucket for Terraform state and then update `infra/terraform/terraform.tfvars`.

### 2) Update terraform variables
Edit `infra/terraform/terraform.tfvars.example` and save it as `terraform.tfvars`.

### 3) Apply Terraform
From `infra/terraform/`:

```bash
terraform init
terraform plan
terraform apply
```

### 4) Configure GitHub connection
Terraform creates the connection/repository resource definitions. Depending on your org policy, the **GitHub App installation/authorization** may still require a one-time approval in GitHub.

### 5) Push code
Push to the configured branch. Cloud Build triggers handle the rest automatically.

## Trigger strategy

### Trigger A: training pipeline
Use this trigger for changes under:
- `training_data/**`
- `prompts/**`
- `tuning/**`
- `cloudbuild.train.yaml`

### Trigger B: app pipeline
Use this trigger for changes under:
- `app/**`
- `Dockerfile`
- `requirements.txt`
- `cloudbuild.app.yaml`

## Required secrets

Terraform creates these Secret Manager secrets:
- `bfsi-api-key`
- `current-tuned-model`
- `app-config-json`

Populate values after bootstrap if needed.

## Environment variables used by the app

- `PROJECT_ID`
- `REGION`
- `MODEL_SECRET_NAME`
- `APP_CONFIG_SECRET_NAME`
- `API_KEY_SECRET_NAME`
- `REQUIRE_API_KEY`
- `SYSTEM_PROMPT_PATH`

## High-level deployment flow

### App pipeline
1. Run unit/import checks
2. Build Docker image
3. Push to Artifact Registry
4. Deploy Cloud Run revision

### Train pipeline
1. Validate JSONL dataset
2. Upload dataset to GCS
3. Submit Vertex AI tuning job
4. Wait for completion
5. Run evaluation gate
6. Update `current-tuned-model` Secret Manager secret
7. Build/deploy Cloud Run using the new model reference

## How the app selects the model

At runtime, Cloud Run reads the **current tuned model name** from Secret Manager. This means the app always points to the latest promoted model without hardcoding model IDs in source.

## Suggested production improvements

- Add a **manual approval** step before prod deployment using separate branches/environments
- Add **Vertex AI evaluation** or custom safety evaluation over BFSI golden datasets
- Add **Cloud Deploy** for environment promotion
- Add **BigQuery** for prompt/response audit
- Add **DLP** or PII masking
- Add **VPC egress**, **private service access**, and **CMEK** as needed
- Add **binary authorization / artifact signing**
- Add **SAST/DAST** if your SDLC requires it

## Sample commands for local testing

```bash
pip install -r app/requirements.txt
uvicorn app.main:app --reload --port 8080
```

## Files you should customize first

- `infra/terraform/terraform.tfvars`
- `training_data/train.jsonl`
- `training_data/val.jsonl`
- `prompts/system_prompt.txt`
- `tuning/submit_tuning_job.py`
