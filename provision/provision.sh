#!/usr/bin/env bash

# This script installs ansbile in a temporary python venv and runs the playbook.

set -euo pipefail


cd $(dirname $(readlink -f $0))

apt -y update
apt -y install python3 python3-venv

venvpath=$(mktemp -ut ansible.XXX)
python3 -m venv ${venvpath}
source ${venvpath}/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

inventory="../inventory.yml.$(hostname)"
[ -f ${inventory} ] || inventory=../inventory.yml

ansible-playbook -i ${inventory} default.yml

deactivate
rm -rf ${venvpath}
