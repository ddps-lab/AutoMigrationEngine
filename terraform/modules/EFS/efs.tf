resource "aws_efs_file_system" "efs" {
  creation_token = "${var.resource_prefix}_efs_${var.group_number}"
  performance_mode = "generalPurpose"
  encrypted = true

  tags = {
    Name = "${var.resource_prefix}_efs_${var.group_number}"
  }
}

resource "aws_efs_mount_target" "mount_target" {
  file_system_id  = aws_efs_file_system.efs.id
  subnet_id = var.public_subnet_id
  security_groups = [var.security_group_id]
}
