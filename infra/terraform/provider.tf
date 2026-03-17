terraform {
  required_version = ">= 1.6.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0"
    }
  }

  backend "gcs" {
    bucket = "REPLACE_TF_STATE_BUCKET"
    prefix = "bfsi-genai-gcp-cicd/state"
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}
