output "cloudbuild_service_account" {
  value = google_service_account.cloudbuild.email
}

output "runtime_service_account" {
  value = google_service_account.runtime.email
}

output "artifact_registry_repo" {
  value = google_artifact_registry_repository.app_repo.id
}

output "data_bucket" {
  value = google_storage_bucket.data_bucket.name
}

output "cloud_run_service_name" {
  value = google_cloud_run_v2_service.app.name
}
