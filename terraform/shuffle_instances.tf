terraform {
  required_providers {
    random = {
      source = "hashicorp/random"
    }
  }
}

provider "random" {}

locals {
  group_list = [
    for row in csvdecode(file("CPU Feature Visualization - simplized aws group(core).csv")) : row["feature groups"]
  ]

  group = [
    for group in local.group_list : 
      split(", ", group)
  ]
}

variable "group_number" {
  type = number
}

resource "random_shuffle" "shuffled" {
  input = local.group[var.group_number]
}

output "shuffled_list" {
  value = random_shuffle.shuffled.result
}
