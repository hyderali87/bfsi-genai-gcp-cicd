variable "project_id" {
  type = string
}

variable "project_number" {
  type = string
}

variable "region" {
  type    = string
  default = "us-central1"
}

variable "artifact_registry_repo" {
  type    = string
  default = "bfsi-app-repo"
}

variable "service_name" {
  type    = string
  default = "bfsi-genai-app"
}

variable "data_bucket_name" {
  type = string
}

variable "github_connection_name" {
  type    = string
  default = "github-connection"
}

variable "github_repository_name" {
  type = string
  # Example: "your-org/bfsi-genai-gcp-cicd"
}

variable "github_app_installation_id" {
  type        = string
  description = "Optional GitHub App installation id if required by your connection flow."
  default     = ""
}

variable "branch_regex" {
  type    = string
  default = "^main$"
}

variable "runtime_require_api_key" {
  type    = string
  default = "false"
}
