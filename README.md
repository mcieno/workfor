<p align="center">
  <img width="100%" src=".assets/logo.svg"/>
</p>
<p align="center">
  <em>Lightweight VMs for freelancers.</em>
</p>

## Requirements

WorkFor requires [OrbStack](https://orbstack.dev) installed on the host, with
the `orbctl` command available in your `PATH`.

## Installation

Clone this repo and copy file [`.env.example`](./.env.example) into a new file
named `.env` and customize the global settings to your preference.

Copy [`.rsyncignore.example`](./.rsyncignore.example) to `.rsyncignore` and
customize the exclusion patterns used by backup and restore.

The entrypoint is the [`workfor`](./workfor) script, which is just a wrapper
around the OrbStack CLI. For convenience, consider creating an alias in your
shell RC-file (e.g., `alias wf=/path/to/workfor`).

To disable automatic forwarding of VM ports to the host, run:

```sh
orbctl config set machines.forward_ports false
```

This setting applies globally to all OrbStack Linux machines.

## Launch a new VM

First things first, copy [`inventory.yml.example`](./inventory.yml.example)
and customize the provisioning configuration to your preference.

Ansible runs locally inside that VM. Host variables override shared variables.

When ready, launch and provision the new VM with

```sh
# Change "something" with the VM name of your choice.
wf n something
```

Should the provisioning fail halfway through, try re-executing it with

```sh
# Change "something" with the VM name of your choice.
wf p something
```

## Back up a workspace

Set `WF_BACKUP_PATH` in `.env` to the host directory for backups, for example:

```sh
WF_BACKUP_PATH="${HOME}/Workspaces"
```

`.rsyncignore` contains one rsync exclusion pattern per line and applies to both
backup and restore. Excluded files already in the backup are preserved.

Run `wf b something` and press <kbd>Enter</kbd> to confirm.
This mirrors `/home/ubuntu/workspace/` into `${WF_BACKUP_PATH}/something/` and
copies `/home/ubuntu/.zsh_history` alongside it.


## Restore a workspace

Run `wf w something` and press <kbd>Enter</kbd> to confirm.
This copies `${WF_BACKUP_PATH}/something/` back into `/home/ubuntu/workspace/`
and restores `.zsh_history` to the Ubuntu user's home directory.

## Configure DNS on macOS

Route `workspace.internal` and its subdomains to the VM (requires `jq`):

```sh
sudo mkdir -p /etc/resolver
vm="something"
domain="workspace.internal"
vm_ip="$(wf info "${vm}" --format=json | jq --raw-output --exit-status '.ip4 // empty')"
[[ ! -e "/etc/resolver/${domain}" ]] && (echo "nameserver ${vm_ip}" | sudo tee "/etc/resolver/${domain}")
```

Replace `something` with the VM name and `workspace.internal` with its
`dns_domain`. Rerun if the VM's IP changes.

Inspect and test the system resolver:

```sh
scutil --dns
dscacheutil -q host -a name app.workspace.internal
```
