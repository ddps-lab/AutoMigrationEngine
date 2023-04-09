data "aws_vpcs" "existing_vpcs" {
  filter {
    name = "tag:Name"
    values = ["junhoVPC"]
  }
}

data "aws_subnets" "existing_subnets"{
  filter {
    name = "tag:Name"
    values = ["junhoSubnet"]
  }
}

data "aws_security_groups" "existing_security_groups"{
  filter {
    name = "tag:Name"
    values = ["junhoSecurity_group"]
  }
}

locals {
  existing_vpc = length(data.aws_vpcs.existing_vpcs.ids) > 0 ? data.aws_vpcs.existing_vpcs.ids[0] : null
  existing_subnet = length(data.aws_subnets.existing_subnets.ids) > 0 ? data.aws_subnets.existing_subnets.ids[0] : null
  existing_security_group = length(data.aws_security_groups.existing_security_groups.ids) > 0 ? data.aws_security_groups.existing_security_groups.ids[0] : null
}

resource "aws_vpc" "vpc" {
  count = local.existing_vpc == null ? 1 : 0

  cidr_block = "172.31.0.0/16"
  enable_dns_hostnames = true

  tags = {
    Name = "junhoVPC"
  }
}

resource "aws_subnet" "public_subnet" {
  count = local.existing_subnet == null ? 1 : 0
  vpc_id = local.existing_vpc == null ? aws_vpc.vpc[0].id : data.aws_vpcs.existing_vpcs.id

  availability_zone = "us-west-2a"
  cidr_block = "172.31.1.0/24"
  enable_resource_name_dns_a_record_on_launch = true
  map_public_ip_on_launch = true

  tags = {
    Name = "junhoSubnet"
  }
}

resource "aws_internet_gateway" "igw" {
  count = local.existing_vpc == null ? 1 : 0
  vpc_id = local.existing_vpc == null ? aws_vpc.vpc[0].id : data.aws_vpcs.existing_vpcs.id

  tags = {
    Name = "junhoIgw"
  }
}

resource "aws_route_table" "route_table" {
  count = local.existing_vpc == null ? 1 : 0
  vpc_id = local.existing_vpc == null ? aws_vpc.vpc[0].id : data.aws_vpcs.existing_vpcs.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw[0].id
  }

  tags = {
    Name = "junhoRoute_table"
  }
}

resource "aws_security_group" "security_group" {
  name_prefix = "junhoSecurity_group"

  count = local.existing_vpc == null ? 1 : 0
  vpc_id = aws_vpc.vpc[0].id

  ingress {
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port = 8888
    to_port = 8888
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port = 0
    to_port = 0
    protocol = -1
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "junhoSecurity_group"
  }
}

resource "aws_route_table_association" "route_table_association" {
  count = local.existing_vpc == null ? 1 : 0

  subnet_id = aws_subnet.public_subnet[0].id
  route_table_id = aws_route_table.route_table[0].id
}