resource "aws_spot_instance_request" "spot_ec2" {
  count = length(var.instance_group)
  spot_price       = var.spot_price
  instance_type    = var.instance_group[count.index]
  ami              = var.ami_id
  key_name         = var.key_name
  availability_zone = var.availability_zone
  subnet_id        = var.public_subnet_id

  vpc_security_group_ids = [
    var.security_group_id
  ]

  user_data = <<-EOF
              #!/bin/bash
              sleep 60
              mount -t nfs -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport ${var.efs_dns_name}:/ /home/${var.user}/migration_test/dump
              sudo chown ${var.user}:${var.user} /home/${var.user}/migration_test/dump
              sudo timedatectl set-timezone 'Asia/Seoul'
              sudo hostnamectl set-hostname migration-test-${var.instance_group[count.index]}
              EOF

  wait_for_fulfillment = true

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_ec2_tag" "spot_instance_tag" {
  count = length(aws_spot_instance_request.spot_ec2)

  resource_id = aws_spot_instance_request.spot_ec2[count.index].spot_instance_id
  key         = "Name"
  value       = "migration-test(spot)_${var.instance_group[count.index]}"
}


resource "null_resource" "spot_init_inventory" {
  depends_on = [
    aws_spot_instance_request.spot_ec2
  ]

  provisioner "local-exec" {
    command = "rm ../../ssh_scripts/inventory_${var.group_number}.txt || true"
  }
}

resource "null_resource" "spot_write_inventory" {
  count = length(var.instance_group)
  depends_on = [
    null_resource.spot_init_inventory
  ]

  provisioner "local-exec" {
    when    = create
    command = "echo '${element(aws_spot_instance_request.spot_ec2.*.public_ip, count.index)}' >> ../../ssh_scripts/inventory_${var.group_number}.txt"
  }
}
