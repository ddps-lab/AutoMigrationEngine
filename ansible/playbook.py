#!/usr/bin/env python

import subprocess
import time
import json

with open("inventory.txt") as f:
    hosts = f.readlines()
hosts = [host.strip() for host in hosts]

print(hosts)

inventory = {
    "src": {
        "hosts": {
            hosts[0]: None,
        },
    },
    "dst": {
        "hosts": {
            host: None for host in hosts[1:]
        },
    },
}

start_time = time.time()
for _ in range(len(inventory["dst"]["hosts"]) + len(inventory["src"]["hosts"])):
    # Run playbook with current inventory

    # Swap hosts
    src_hosts = list(inventory["src"]["hosts"].keys())
    dst_hosts = list(inventory["dst"]["hosts"].keys())

    inventory["dst"]["hosts"][src_hosts[0]] = inventory["src"]["hosts"].pop(src_hosts[0])
    inventory["src"]["hosts"][dst_hosts[0]] = inventory["dst"]["hosts"].pop(dst_hosts[0])

    # Update dynamic inventory file
    with open("inventory.json", "w") as f:
        json.dump(inventory, f)


    subprocess.run(["ansible-playbook", "playbook.yml", "-i", "inventory.json"])

    # break
    # Wait for some time before running the playbook again
    time.sleep(5)

end_time = time.time()
total_time = end_time - start_time
print("total execution time: {:.2f}".format(total_time))