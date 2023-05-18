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
  default = "ami-0a5f407c50b1500a5"
}

variable "key_name" {
  type    = string
  default = "junho_us"
}
