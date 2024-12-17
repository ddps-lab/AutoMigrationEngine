terraform {
  required_providers {
    random = {
      source = "hashicorp/random"
      version = "3.4.3"
    }
  }
}

locals {
  group_list = [
    for row in csvdecode(file(var.file_path)) : row["feature groups"]
  ]

  group = [
    for group in local.group_list : 
      split(", ", group)
  ]
}