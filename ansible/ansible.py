#!/usr/bin/env python

import subprocess
import time
import json

with open("inventory.txt") as f:
    hosts = f.readlines()
hosts = [host.strip() for host in hosts]

print(hosts)


# Initial inventory
inventory = {
    "src": {
        "hosts": [hosts[0]],
    },
    "dst": {
        "hosts": hosts[1:],
    },
}

for _ in range(len(inventory["dst"]["hosts"]) + len(inventory["src"]["hosts"])):
    # Run playbook with current inventory
    # subprocess.run(["ansible-playbook", "playbook.yml", "-i", "inventory.json"])
    print(inventory)

    # Swap hosts
    src_hosts = inventory["src"]["hosts"]
    dst_hosts = inventory["dst"]["hosts"]
    print(src_hosts)
    print(dst_hosts)
    inventory["dst"]["hosts"].append(inventory["src"]["hosts"].pop(0))
    inventory["src"]["hosts"].append(inventory["dst"]["hosts"].pop(0))

    # Update dynamic inventory file
    with open("inventory.json", "w") as f:
        json.dump(inventory, f)

    # Wait for some time before running the playbook again
    time.sleep(5)
