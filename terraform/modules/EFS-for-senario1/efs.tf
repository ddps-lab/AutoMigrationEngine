resource "aws_efs_file_system" "efs" {
  creation_token = "junho_efs_${var.group_number}"
  performance_mode = "generalPurpose"
  encrypted = true

  tags = {
    Name = "junho-efs"
  }
}

resource "aws_security_group" "efs_security_group" {
  name_prefix = "efs_security_group_${var.group_number}"

  vpc_id = var.vpc_id

  ingress {
    from_port = 2049
    to_port   = 2049
    protocol  = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_efs_mount_target" "mount_target" {
  file_system_id  = aws_efs_file_system.efs.id
  subnet_id = var.public_subnet_id
  security_groups = [var.security_group_id]
}
