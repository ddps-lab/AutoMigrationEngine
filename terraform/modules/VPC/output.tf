output "vpc_id" {
  value = local.existing_vpc != null ? local.existing_vpc : aws_vpc.vpc[0].id
}

output "public_subnet_id" {
  value = local.existing_subnet != null ? local.existing_subnet : aws_subnet.public_subnet[0].id
}

output "security_group_id" {
  value = local.existing_security_group != null ? local.existing_security_group : aws_security_group.security_group[0].id
}