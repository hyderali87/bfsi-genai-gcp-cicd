resource "google_storage_bucket" "data_bucket" {
  name                        = var.data_bucket_name
  location                    = var.region
  force_destroy               = false
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  depends_on = [google_project_service.services]
}
