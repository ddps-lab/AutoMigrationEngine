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

def scenario2_dump(groups):
    sources = []
    for i in range(len(groups)):
        with open("ssh_scripts/inventory_" + str(groups[i]) + ".txt") as f:
            source = f.readlines()
        sources += [src.strip() for src in source]

    inventory = {
        "all": {
            "vars": {
                "ansible_user": "ubuntu",
                "ansible_ssh_common_args": "-o 'StrictHostKeyChecking=no'",
            },
            "hosts": {src: None for src in sources}
        },
    }

    # Update dynamic inventory file
    with open("ssh_scripts/inventory.json", "w") as f:
        json.dump(inventory, f)

    with open(f'ansible.log', 'w') as f:
            subprocess.run(["ansible-playbook", "ssh_scripts/process-dump.yml",
                           "-i", "ssh_scripts/inventory.json", "--forks", f"{len(groups)}"], stdout=f, stderr=f)


def scenario2_restore(groups, src, re_exp):
    destinations = []
    for i in range(len(groups)):
        # 본인을 제외한 모든 그룹의 프로세스를 복원
        if groups[i] == src:
            continue

        with open("ssh_scripts/inventory_" + str(groups[i]) + ".txt") as f:
            destination = f.readlines()
        destinations += [dst.strip() for dst in destination]

    inventory = {
        "all": {
            "vars": {
                "ansible_user": "ubuntu",
                "ansible_ssh_common_args": "-o 'StrictHostKeyChecking=no'",
            },
            "hosts": {dst: None for dst in destinations}
        },
    }

    if(re_exp):
        src = 0

    # Update dynamic inventory file
    with open("ssh_scripts/inventory.json", "w") as f:
        json.dump(inventory, f)

    with open(f'ansible.log', 'a') as f:
        subprocess.run(["ansible-playbook", "ssh_scripts/process-restore.yml",
                        "-i", "ssh_scripts/inventory.json", "-e", f"src={src}", "--forks", f"{len(groups)}"], stdout=f, stderr=f)
        
def scenario2_debug(groups, src, re_exp):
    destinations = []
    for i in range(len(groups)):
        # 본인을 제외한 모든 그룹의 프로세스를 복원
        if groups[i] == src:
            continue

        with open("ssh_scripts/inventory_" + str(groups[i]) + ".txt") as f:
            destination = f.readlines()
        destinations += [dst.strip() for dst in destination]

    inventory = {
        "all": {
            "vars": {
                "ansible_user": "ubuntu",
                "ansible_ssh_common_args": "-o 'StrictHostKeyChecking=no'",
            },
            "hosts": {dst: None for dst in destinations}
        },
    }

    if(re_exp):
        src = 0

    # Update dynamic inventory file
    with open("ssh_scripts/inventory.json", "w") as f:
        json.dump(inventory, f)

    with open(f'ansible.log', 'a') as f:
        subprocess.run(["ansible-playbook", "ssh_scripts/process-debug.yml",
                        "-i", "ssh_scripts/inventory.json", "-e", f"src={src}", "--forks", f"{len(groups)}"], stdout=f, stderr=f)