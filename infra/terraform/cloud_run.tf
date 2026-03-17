resource "google_cloud_run_v2_service" "app" {
  name     = var.service_name
  location = var.region

  template {
    service_account = google_service_account.runtime.email
    containers {
      image = "${var.region}-docker.pkg.dev/${var.project_id}/${var.artifact_registry_repo}/${var.service_name}:bootstrap"
      env {
        name  = "PROJECT_ID"
        value = var.project_id
      }
      env {
        name  = "REGION"
        value = var.region
      }
      env {
        name  = "MODEL_SECRET_NAME"
        value = google_secret_manager_secret.current_model.secret_id
      }
      env {
        name  = "APP_CONFIG_SECRET_NAME"
        value = google_secret_manager_secret.app_config.secret_id
      }
      env {
        name  = "API_KEY_SECRET_NAME"
        value = google_secret_manager_secret.api_key.secret_id
      }
      env {
        name  = "REQUIRE_API_KEY"
        value = var.runtime_require_api_key
      }
      env {
        name  = "SYSTEM_PROMPT_PATH"
        value = "/app/prompts/system_prompt.txt"
      }
    }
  }

  depends_on = [
    google_project_service.services,
    google_service_account.runtime,
    google_secret_manager_secret.current_model,
    google_secret_manager_secret.app_config,
    google_secret_manager_secret.api_key,
  ]
}

resource "google_cloud_run_v2_service_iam_member" "public_invoker" {
  project  = var.project_id
  location = var.region
  name     = google_cloud_run_v2_service.app.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
