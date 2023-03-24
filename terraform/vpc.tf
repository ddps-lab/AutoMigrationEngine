resource "aws_vpc" "vpc" {
  cidr_block = "172.31.0.0/16"
  enable_dns_hostnames = true
  
  tags = {
    Name = "junhoVPC"
  }
}

resource "aws_subnet" "public_subnet" {
  vpc_id     = aws_vpc.vpc.id
  cidr_block = "172.31.1.0/24"
  enable_resource_name_dns_a_record_on_launch = true
  map_public_ip_on_launch = true

  tags = {
    Name = "junhoSubnet"
  }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.vpc.id

  tags = {
    Name = "junhoIgw"
  }
}

resource "aws_route_table" "route_table" {
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "junhoRoute_table"
  }
}

resource "aws_security_group" "security_group" {
  name_prefix = "junhoSecurity_group"
  vpc_id = aws_vpc.vpc.id

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
}

resource "aws_route_table_association" "route_table_association" {
  subnet_id      = aws_subnet.public_subnet.id
  route_table_id = aws_route_table.route_table.id
}