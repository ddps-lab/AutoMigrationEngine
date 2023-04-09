provider "aws" {
  profile = "default"
  region = "us-west-2"
}

variable "group_number" {
  type = number
}

module "shuffle_instances" {
  source = "../modules/shuffle-instances"
  group_number = var.group_number
  file_path = "../CPU Feature Visualization - simplized aws group(core).csv"
}

module "vpc" {
  source = "../modules/VPC"
}

module "s3" {
  source = "../modules/S3"
}

module "efs" {
  source = "../modules/EFS-for-senario1"
  group_number = var.group_number
  vpc_id = module.vpc.vpc_id
  public_subnet_id = module.vpc.public_subnet_id
  security_group_id = module.vpc.security_group_id
}

module "ec2" {
  source = "../modules/EC2"
  group_number = var.group_number
  shuffled_instance_group = module.shuffle_instances.shuffled_instance_group
  instance_group = module.shuffle_instances.instance_group
  public_subnet_id = module.vpc.public_subnet_id
  security_group_id = module.vpc.security_group_id
  efs_dns_name = module.efs.efs_dns_name
}