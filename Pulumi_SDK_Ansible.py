import * as pulumi from "@pulumi/pulumi";
import * as ansible from "./ansible";

const hosts = new ansible.InventoryHosts("my-hosts", {
    hosts: ["web1", "web2"],
    vars: {
        ansible_user: "ubuntu",
        ansible_private_key_file: "/path/to/private/key",
    },
});

const playbook = new ansible.Playbook("my-playbook", {
    inventory: hosts.id,
    playbook: "/path/to/playbook.yml",
    vars: {
        db_password: "mysecretpassword",
    },
});

export const output = pulumi.all([hosts.hosts, playbook.playbook]).apply(([h, p]) => `Hosts: ${h.join(", ")}\nPlaybook: ${p}`);


import * as pulumi from "@pulumi/pulumi";
import * as ansible from "@pulumi/ansible";

const inventory = new ansible.DynamicInventory("my-inventory", {
    hosts: pulumi.output(host.privateIp),
});

const playbook = new ansible.Playbook("my-playbook", {
    inventory: inventory.id,
    playbook: "path/to/playbook.yml",
});
