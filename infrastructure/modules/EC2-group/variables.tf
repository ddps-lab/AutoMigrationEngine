variable "group_number" {
  type = number
}

variable "ami_id" {
  type = string
}

variable "key_name" {
  type = string
}

variable "availability_zone" {
  type = string
}

variable "instance_group" {
  type = list
}

variable "public_subnet_id" {
  type = string
}

variable "security_group_id" {
  type = string
}

variable "efs_dns_name" {
  type = string
}

variable "user" {
  type = string
}