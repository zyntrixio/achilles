#!/usr/bin/env bash

export ANSIBLE_CALLBACK_PLUGINS="$(python3 -m ara.setup.callback_plugins)"
ansible-playbook site.yaml -i hosts -l all:!ara