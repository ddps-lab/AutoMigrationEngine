resource "aws_instance" "ec2" {
  count = length(var.instance_group)
  instance_type = var.instance_group[count.index]
  ami = var.ami_id # migration compatibility test on x86
  key_name = var.key_name
  availability_zone = var.availability_zone
  subnet_id = var.public_subnet_id
  
  vpc_security_group_ids = [
    var.security_group_id
  ]

  tags = {
    "Name" = "container-migration-test_${var.instance_group[count.index]}"
  }

  user_data = <<-EOF
            #!/bin/bash
            sleep 30
            mount -t nfs -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport ${var.efs_dns_name}:/ /home/ubuntu/migration_test/dump
            sudo chown ubuntu:ubuntu /home/ubuntu/migration_test/dump
            sudo timedatectl set-timezone 'Asia/Seoul'
            sudo hostnamectl set-hostname ${var.instance_group[count.index]}
            EOF
}


resource "null_resource" "init_inventory" {
  depends_on = [
    aws_instance.ec2
  ]

  provisioner "local-exec" {
    command = "rm ../../ssh_scripts/inventory_${var.group_number}.txt || true"
  }
}

resource "null_resource" "write_inventory" {
  count = length(var.instance_group)
  depends_on = [
    null_resource.init_inventory
  ]

  provisioner "local-exec" {
    command = "echo '${aws_instance.ec2[count.index].public_ip}' >> ../../ssh_scripts/inventory_${var.group_number}.txt"
  }
}