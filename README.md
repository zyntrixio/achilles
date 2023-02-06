# Achilles

An Ansible Playbook designed to replace the Fury, Nebula, Jarvis, and Wanda cookbooks

## Why are we moving from Chef?

Chef/Cinc requires the use of a Chef Server, this has a monthly cost of ~$128/month, while the motivation for moving to ansible is not financial in nature, it is a factor worth mentioning

The main features we use from the Chef Servers are Inventory and Configuration Storage, Ansible can bring these at zero cost by using Azure Key Vault for Configuration and Secret Management, and Azure Resource Management for inventory.

The intention is to use GitHub Actions to execute every 60 minutes to ensure all infrastructure is in spec.


## Project Setup
1. Install Poetry: `curl -sSL https://install.python-poetry.org | python3 -`
2. Run Ansible: `poetry run ./run.sh`

### Local Development

#### Install Asnible

Install Asnible with `brew install ansible`

#### SSH Config Setup

The `~/.ssh/config` needs to be setup with the following:

```
Host bastion
    HostName ssh.uksouth.bink.sh
    User chris_pressland
    Port 22
    IdentityFile ~/.ssh/id_ed25519

Host *.uksouth.bink.host *.prod.uksouth.bink.host *.staging.uksouth.bink.host *.dev.uksouth.bink.host *.sandbox.uksouth.bink.host *.core.uksouth.bink.host
    ProxyJump bastion
    User chris_pressland
    IdentityFile ~/.ssh/id_ed25519
```

Check you can access all hosts via: `ansible all -i hosts -m ping`
Run all playbooks on all hosts via: `ansible-playbook -i hosts site.yaml`
Run all playbooks on specific hosts: `ansible-playbook -i hosts -l datawarehouse site.yaml`

### Continious Integration

TODO: Needs to be added
