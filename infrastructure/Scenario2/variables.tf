variable "region" {
  type    = string
  default = "us-west-2"
}

variable "resource_prefix" {
  type    = string
  default = "migration"
}

variable "availability_zone" {
  type    = string
  default = "us-west-2a"
}

variable "ami_id" {
  type    = string
  default = "ami-0dc15ee8b0d70d4d4"
}

variable "key_name" {
  type    = string
  default = "junho_us"
}

variable "group" {
  type = list
}
