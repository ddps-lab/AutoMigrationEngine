resource "aws_instance" "test" {
  count = length(var.instance_group)
  instance_type = var.shuffled_instance_group[count.index]
  ami = "ami-0c7a974f58b92cfc6" # migration compatibility test on x86
  key_name = "junho_us"
  availability_zone = "us-west-2a"
  subnet_id = var.public_subnet_id
  
  vpc_security_group_ids = [
    var.security_group_id
  ]

  tags = {
    "Name" = "container-migration-test_${var.shuffled_instance_group[count.index]}"
  }

  user_data = <<-EOF
            #!/bin/bash
            mount -t nfs -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport ${var.efs_dns_name}:/ /home/ec2-user/podman/dump
            sudo chown ec2-user:ec2-user /home/ec2-user/podman/dump
            sudo timedatectl set-timezone 'Asia/Seoul'
            sudo hostnamectl set-hostname ${var.shuffled_instance_group[count.index]}
            EOF
}


resource "null_resource" "init_inventory" {
  depends_on = [
    aws_instance.test
  ]

  provisioner "local-exec" {
    command = "rm ../ansible/inventory_${var.group_number}.txt || true"
  }
}

resource "null_resource" "write_inventory" {
  count = length(var.instance_group)
  depends_on = [
    null_resource.init_inventory
  ]

  provisioner "local-exec" {
    command = "echo '${aws_instance.test[count.index].public_ip}' >> ../ansible/inventory_${var.group_number}.txt"
  }
}