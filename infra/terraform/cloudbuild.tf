# NOTE:
# The exact GitHub connection flow can vary based on org controls and current API behavior.
# This configuration gives you the Terraform structure for a Cloud Build v2 connection + repository
# and trigger setup. You may still need one-time GitHub-side authorization.

resource "google_cloudbuildv2_connection" "github" {
  location = var.region
  name     = var.github_connection_name

  github_config {
    app_installation_id = var.github_app_installation_id != "" ? tonumber(var.github_app_installation_id) : null
    authorizer_credential {
      oauth_token_secret_version = google_secret_manager_secret_version.github_pat.id
    }
  }

  depends_on = [google_project_service.services]
}

resource "google_secret_manager_secret" "github_pat" {
  secret_id = "github-pat"

  replication {
    auto {}
  }

  depends_on = [google_project_service.services]
}

resource "google_secret_manager_secret_version" "github_pat" {
  secret      = google_secret_manager_secret.github_pat.id
  secret_data = "REPLACE_ME"
}

resource "google_cloudbuildv2_repository" "repo" {
  location          = var.region
  name              = "bfsi-genai-repo"
  parent_connection = google_cloudbuildv2_connection.github.name
  remote_uri        = "https://github.com/${var.github_repository_name}.git"
}

resource "google_cloudbuild_trigger" "app_trigger" {
  name            = "bfsi-app-trigger"
  description     = "App deploy trigger"
  filename        = "cloudbuild.app.yaml"
  service_account = google_service_account.cloudbuild.id

  repository_event_config {
    repository = google_cloudbuildv2_repository.repo.id
    push {
      branch = var.branch_regex
    }
  }

  included_files = [
    "app/**",
    "prompts/**",
    "Dockerfile",
    "cloudbuild.app.yaml",
  ]

  substitutions = {
    _REGION                 = var.region
    _AR_REPO                = var.artifact_registry_repo
    _SERVICE_NAME           = var.service_name
    _RUNTIME_SA             = google_service_account.runtime.email
    _MODEL_SECRET_NAME      = google_secret_manager_secret.current_model.secret_id
    _APP_CONFIG_SECRET_NAME = google_secret_manager_secret.app_config.secret_id
    _API_KEY_SECRET_NAME    = google_secret_manager_secret.api_key.secret_id
    _REQUIRE_API_KEY        = var.runtime_require_api_key
  }

  depends_on = [google_cloudbuildv2_repository.repo]
}

resource "google_cloudbuild_trigger" "train_trigger" {
  name            = "bfsi-train-trigger"
  description     = "Dataset/tuning trigger"
  filename        = "cloudbuild.train.yaml"
  service_account = google_service_account.cloudbuild.id

  repository_event_config {
    repository = google_cloudbuildv2_repository.repo.id
    push {
      branch = var.branch_regex
    }
  }

  included_files = [
    "training_data/**",
    "tuning/**",
    "prompts/**",
    "cloudbuild.train.yaml",
  ]

  substitutions = {
    _REGION                 = var.region
    _DATA_BUCKET            = google_storage_bucket.data_bucket.name
    _BASE_MODEL             = "gemini-2.5-flash"
    _TUNING_JOB_PREFIX      = "bfsi-tuning-job"
    _MIN_PASS_RATE          = "0.80"
    _AR_REPO                = var.artifact_registry_repo
    _SERVICE_NAME           = var.service_name
    _RUNTIME_SA             = google_service_account.runtime.email
    _MODEL_SECRET_NAME      = google_secret_manager_secret.current_model.secret_id
    _APP_CONFIG_SECRET_NAME = google_secret_manager_secret.app_config.secret_id
    _API_KEY_SECRET_NAME    = google_secret_manager_secret.api_key.secret_id
    _REQUIRE_API_KEY        = var.runtime_require_api_key
  }

  depends_on = [google_cloudbuildv2_repository.repo]
}
