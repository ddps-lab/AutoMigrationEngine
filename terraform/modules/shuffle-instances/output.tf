output "shuffled_instance_group" {
  value = random_shuffle.shuffled.result
}

output "instance_group" {
  value = local.group[var.group_number]
}