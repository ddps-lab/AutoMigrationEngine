import subprocess
import time
import json


def scenario1(group_number):
    with open("ssh_scripts/inventory_" + group_number + ".txt") as f:
        hosts = f.readlines()
    hosts = [host.strip() for host in hosts]

    inventory = {
        "all": {
            "vars": {
                "ansible_user": "ubuntu",
                "ansible_ssh_common_args": "-o 'StrictHostKeyChecking=no'",
            },
            "hosts": {},
        },

        "src": {
            "hosts": {
                hosts[0]: None
            }
        },
        "dst": {
            "hosts": {
                host: None for host in hosts[1:]
            }
        }
    }

    start_time = time.time()
    for _ in range(len(inventory["dst"]["hosts"]) + len(inventory["src"]["hosts"])):
        # Run playbook with current inventory

        # Swap hosts
        src_hosts = list(inventory["src"]["hosts"].keys())
        dst_hosts = list(inventory["dst"]["hosts"].keys())

        inventory["dst"]["hosts"][src_hosts[0]
                                  ] = inventory["src"]["hosts"].pop(src_hosts[0])
        inventory["src"]["hosts"][dst_hosts[0]
                                  ] = inventory["dst"]["hosts"].pop(dst_hosts[0])

        # Update dynamic inventory file
        with open("ssh_scripts/inventory_" + group_number + ".json", "w") as f:
            json.dump(inventory, f)

        with open(f'group{group_number}.log', 'a') as f:
            subprocess.run(["ansible-playbook", "ssh_scripts/without-container.yml", "-i",
                           "ssh_scripts/inventory_" + group_number + ".json"], stdout=f, stderr=f)

        time.sleep(5)

    end_time = time.time()
    total_time = end_time - start_time
    print(f"group{group_number} total execution time: {total_time}")


def scenario2(src, dst):
    with open("ssh_scripts/inventory_" + str(src) + ".txt") as f:
        sources = f.readlines()
    sources = [src.strip() for src in sources]

    destinations = []
    for i in range(len(dst)):
        with open("ssh_scripts/inventory_" + str(dst[i]) + ".txt") as f:
            dst_group = f.readlines()
        destinations += [dst.strip() for dst in dst_group]

    inventory = {
        "all": {
            "vars": {
                "ansible_user": "ubuntu",
                "ansible_ssh_common_args": "-o 'StrictHostKeyChecking=no'",
            },
            "hosts": {},
        },

        "src": {
            "hosts": {
                sources[0]: None
            }
        },
        "dst": {
            "hosts": {
                dst: None for dst in destinations
            }
        }
    }

    start_time = time.time()
    for i in range(len(sources)):
        # Run playbook with current inventory

        # Swap src
        inventory["src"]["hosts"] = sources[i]

        # Update dynamic inventory file
        with open("ssh_scripts/inventory.json", "w") as f:
            json.dump(inventory, f)

        with open(f'ansible.log', 'a') as f:
            subprocess.run(["ansible-playbook", "ssh_scripts/without-container.yml",
                           "-i", "ssh_scripts/inventory.json"], stdout=f, stderr=f)

        time.sleep(5)

    end_time = time.time()
    total_time = end_time - start_time
    print("total execution time: {:.2f}".format(total_time))
