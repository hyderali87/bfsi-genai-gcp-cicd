resource "google_secret_manager_secret" "api_key" {
  secret_id = "bfsi-api-key"

  replication {
    auto {}
  }

  depends_on = [google_project_service.services]
}

resource "google_secret_manager_secret" "current_model" {
  secret_id = "current-tuned-model"

  replication {
    auto {}
  }

  depends_on = [google_project_service.services]
}

resource "google_secret_manager_secret" "app_config" {
  secret_id = "app-config-json"

  replication {
    auto {}
  }

  depends_on = [google_project_service.services]
}

resource "google_secret_manager_secret_version" "current_model_seed" {
  secret      = google_secret_manager_secret.current_model.id
  secret_data = "gemini-2.5-flash"
}

resource "google_secret_manager_secret_version" "app_config_seed" {
  secret      = google_secret_manager_secret.app_config.id
  secret_data = jsonencode({
    temperature       = 0.2
    max_output_tokens = 1024
  })
}

resource "google_secret_manager_secret_iam_member" "runtime_model_access" {
  secret_id = google_secret_manager_secret.current_model.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.runtime.email}"
}

resource "google_secret_manager_secret_iam_member" "runtime_config_access" {
  secret_id = google_secret_manager_secret.app_config.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.runtime.email}"
}

resource "google_secret_manager_secret_iam_member" "runtime_api_key_access" {
  secret_id = google_secret_manager_secret.api_key.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.runtime.email}"
}
