resource "aws_efs_file_system" "efs" {
  creation_token = "junho-efs"
  performance_mode = "generalPurpose"
  encrypted = true

  tags = {
    Name = "junho-efs"
  }
}

resource "aws_security_group" "efs_security_group" {
  name_prefix = "efs_security_group"
  vpc_id      = aws_vpc.vpc.id

  ingress {
    from_port = 2049
    to_port   = 2049
    protocol  = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


resource "aws_efs_mount_target" "mount_target" {
  file_system_id  = aws_efs_file_system.efs.id
  subnet_id       = aws_subnet.public_subnet.id
  security_groups = [aws_security_group.efs_security_group.id]
}