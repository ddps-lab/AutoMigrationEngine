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
  default = "us-west-2c"
}

variable "ami_id" {
  type    = string
  default = "ami-0efd66d45ae09013b"
}

variable "key_name" {
  type    = string
  default = "junho_us"
}

variable "group" {
  type = list
}
