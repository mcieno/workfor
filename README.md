<p align="center">
  <img width="100%" src=".assets/logo.svg"/>
</p>
<p align="center">
  <em>Lightweight VMs for freelancers.</em>
</p>

## Requirements

WorkFor requires [multipass](https://multipass.run) installed on the host.

## Installation

Clone this repo and copy file [`.env.example`](./.env.example) into a new file
named `.env` and customize the global settings to your preference.

The entrypoint is the [`workfor`](./workfor) script, which is just a wrapper
around the multipass CLI. For convenience, consider creating an alias in your
shell RC-file (e.g., `alias wf=/path/to/workfor`).

## Launch a new VM

First things first, copy [`inventory.yml.example`](./inventory.yml.example)
and customize the provisioning configuration to your preference.

If the VM name is `something`, WorkFor will look for provisioning configuration
files `inventory.yml.something` and `inventory.yml`, in this order.

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
