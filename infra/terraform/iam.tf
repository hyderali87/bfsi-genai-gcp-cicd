resource "google_service_account" "cloudbuild" {
  account_id   = "bfsi-cloudbuild"
  display_name = "BFSI Cloud Build SA"
}

resource "google_service_account" "runtime" {
  account_id   = "bfsi-runner"
  display_name = "BFSI Cloud Run Runtime SA"
}

locals {
  cloudbuild_roles = [
    "roles/run.admin",
    "roles/artifactregistry.writer",
    "roles/logging.logWriter",
    "roles/storage.admin",
    "roles/cloudbuild.builds.editor",
    "roles/aiplatform.user",
    "roles/secretmanager.admin",
    "roles/iam.serviceAccountUser",
  ]

  runtime_roles = [
    "roles/secretmanager.secretAccessor",
    "roles/aiplatform.user",
    "roles/logging.logWriter",
  ]
}

resource "google_project_iam_member" "cloudbuild_roles" {
  for_each = toset(local.cloudbuild_roles)
  project  = var.project_id
  role     = each.value
  member   = "serviceAccount:${google_service_account.cloudbuild.email}"

  depends_on = [google_project_service.services]
}

resource "google_project_iam_member" "runtime_roles" {
  for_each = toset(local.runtime_roles)
  project  = var.project_id
  role     = each.value
  member   = "serviceAccount:${google_service_account.runtime.email}"

  depends_on = [google_project_service.services]
}

resource "google_service_account_iam_member" "cloudbuild_act_as_runtime" {
  service_account_id = google_service_account.runtime.name
  role               = "roles/iam.serviceAccountUser"
  member             = "serviceAccount:${google_service_account.cloudbuild.email}"
}
