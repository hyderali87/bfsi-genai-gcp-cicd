resource "google_artifact_registry_repository" "app_repo" {
  location      = var.region
  repository_id = var.artifact_registry_repo
  description   = "Artifact Registry for BFSI GenAI app"
  format        = "DOCKER"

  depends_on = [google_project_service.services]
}
