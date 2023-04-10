provider "aws" {
  profile = "default"
  region = "us-west-2"
}

module "shuffle_instances" {
  source = "../modules/shuffle-instances"
  file_path = "../CPU Feature Visualization - simplized aws group(core).csv"
}

module "vpc" {
  source = "../modules/VPC"
  resource_prefix = "migration"
  availability_zone = "us-west-2a"
}

module "efs" {
  count = 10
  source = "../modules/EFS"
  resource_prefix = "migration"
  group_number = count.index
  vpc_id = module.vpc.vpc_id
  public_subnet_id = module.vpc.public_subnet_id
}


module "ec2" {
  count = 10
  source = "../modules/EC2"
  group_number = count.index
  shuffled_instance_group = module.shuffle_instances.shuffled_instance_group[count.index].result
  ami_id = "ami-0c7a974f58b92cfc6"
  key_name = "junho_us"
  availability_zone = "us-west-2a"
  public_subnet_id = module.vpc.public_subnet_id
  security_group_id = module.vpc.security_group_id
  efs_dns_name = module.efs[count.index].efs_dns_name

  depends_on = [
    module.shuffle_instances
  ]
}