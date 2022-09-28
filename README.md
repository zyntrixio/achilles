# achilles

An Ansible Playbook designed to replace the Fury, Nebula, Jarvis, and Wanda cookbooks

## Why are we moving from Chef?

Chef/Cinc requires the use of a Chef Server, this has a monthly cost of ~$128/month, while the motivation for moving to ansible is not financial in nature, it is a factor worth mentioning

The main features we use from the Chef Servers are Inventory and Configuration Storage, Ansible can bring these at zero cost by using Azure Key Vault for Configuration and Secret Management, and Azure Resource Management for inventory.

The intention is to use GitHub Actions to execute every 60 minutes to ensure all infrastructure is in spec.


## Project Setup

### Local Development

Needs to be added 

### Continious Integration

Needs to be added 


Needs to write out the required SSH key to `~/.ssh/id_rsa`

Needs to write out the require SSH config to `~/.ssh/config`
