output "shuffled_instance_group" {
  value = random_shuffle.shuffled
}

# output "instance_group" {
#   # value = local.group[var.group_number]
#   value = local.group
# }