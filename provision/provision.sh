#! /usr/bin/env -S DEBIAN_FRONTEND=noninteractive bash -e -u -o pipefail
cd "$(dirname "$(readlink -f "$0")")"

apt -y update
apt -y install python3 python3-venv

venvpath="$(mktemp -ut provision.XXX)"
trap "rm -rf $venvpath" EXIT

python3 -m venv "${venvpath}"
source "${venvpath}/bin/activate"

pip install --upgrade pip
pip install -r requirements.txt

inventory="../inventory.yml.$(hostname)"
[ -f ${inventory} ] || inventory="../inventory.yml"

ansible-playbook -i "${inventory}" default.yml

deactivate
