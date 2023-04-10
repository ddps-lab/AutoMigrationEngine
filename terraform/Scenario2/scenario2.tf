provider "aws" {
  profile = "default"
  region  = var.region
}

module "shuffle_instances" {
  source    = "../modules/shuffle-instances"
  file_path = "../CPU Feature Visualization - simplized aws group(core).csv"
}

module "vpc" {
  source            = "../modules/VPC"
  resource_prefix   = var.resource_prefix
  availability_zone = var.availability_zone
}

module "efs" {
  count = 1
  source            = "../modules/EFS"
  resource_prefix   = var.resource_prefix
  group_number      = count.index
  vpc_id            = module.vpc.vpc_id
  public_subnet_id  = module.vpc.public_subnet_id
  security_group_id = aws_security_group.efs_security_group.id
}


module "ec2" {
  count                   = length(var.group)
  source                  = "../modules/EC2-group"
  group_number            = count.index
  shuffled_instance_group = module.shuffle_instances.shuffled_instance_group[var.group[count.index]].result
  ami_id                  = var.ami_id
  key_name                = var.key_name
  availability_zone       = var.availability_zone
  public_subnet_id        = module.vpc.public_subnet_id
  security_group_id       = aws_security_group.ec2_security_group.id
  efs_dns_name            = module.efs[0].efs_dns_name

  depends_on = [
    module.shuffle_instances,
    module.efs
  ]
}
