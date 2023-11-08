variable "region" {
  type    = string
  default = "us-west-2"
  # default = "us-east-1"
}

variable "resource_prefix" {
  type    = string
  default = "migration"
}

variable "availability_zone" {
  type    = string
  default = "us-west-2c"
  # default = "us-east-1a"
}

variable "ami_id" {
  type    = string
  default = "ami-0f319b2f53e9ace9d"
  # default = "ami-005eef97af395dc92" us-east-1
}

variable "key_name" {
  type    = string
  default = "junho_us"
}

variable "group" {
  type = list
}

variable "user" {
  type    = string
  default = "ubuntu"
}