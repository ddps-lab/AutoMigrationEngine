provider "aws" {
  profile = "default"
  region = "us-west-2"
}

variable "group_number" {
  type = number
}

module "shuffle_instances" {
  source = "./shuffle-instances"
  group_number = var.group_number
}

module "vpc" {
  source = "./VPC"
}

module "s3" {
  source = "./S3"
}

module "efs" {
  source = "./EFS"
  group_number = var.group_number
  vpc_id = module.vpc.vpc_id
  public_subnet_id = module.vpc.public_subnet_id
  security_group_id = module.vpc.security_group_id
}

module "ec2" {
  source = "./EC2"
  group_number = var.group_number
  shuffled_instance_group = module.shuffle_instances.shuffled_instance_group
  instance_group = module.shuffle_instances.instance_group
  public_subnet_id = module.vpc.public_subnet_id
  security_group_id = module.vpc.security_group_id
  efs_dns_name = module.efs.efs_dns_name
}