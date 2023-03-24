provider "aws" {
  profile = "default"
  region = "us-west-2"
}

# output "example_output" {
#   value = local.group
# }

# resource "aws_s3_bucket" "test" {
#   bucket = "migration-compatibility"
#   acl    = "private"

#   tags = {
#     Name = "migration-compatibility"
#   }
# }

resource "aws_instance" "test" {
  count = 1
  # instance_type = local.group[var.group_number][count.index]
  instance_type = random_shuffle.shuffled.result[count.index]
  ami = "ami-0ca7246571049ab83" # migration compatibility test on x86
  key_name = "junho_us"
  subnet_id = aws_subnet.public_subnet.id
  
  # vpc_security_group_ids = [ "sg-073b11e4e427053f1" ] # junho
  vpc_security_group_ids = [
    aws_security_group.security_group.id
  ]

  tags = {
    "Name" = "container-migration-test_${random_shuffle.shuffled.result[count.index]}"
  }

  provisioner "local-exec" {
    command = "echo '${aws_instance.test[count.index].public_ip}' > ../ansible/inventory.txt"
  }

  depends_on = [
    aws_security_group.security_group
  ]
}