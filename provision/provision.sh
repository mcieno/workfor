#! /usr/bin/env -S DEBIAN_FRONTEND=noninteractive bash -e -u -o pipefail
cd "$(dirname "$(readlink -f "$0")")"

if ! command -v apt-get >/dev/null; then
    echo "The bundled playbook requires an apt-based systemd guest." >&2
    exit 1
fi

apt -y update
apt -y install python3 python3-venv

venvpath="$(mktemp -ut provision.XXX)"
trap "rm -rf $venvpath" EXIT

python3 -m venv "${venvpath}"
source "${venvpath}/bin/activate"

pip install --upgrade pip
pip install -r requirements.txt

ansible-playbook --inventory ../inventory.yml \
    --extra-vars "workfor_machine=$(hostname)" \
    --extra-vars "workfor_user=${1:-ubuntu}" \
    default.yml

deactivate
