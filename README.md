<p align="center">
  <img width="100%" src=".assets/logo.svg"/>
</p>
<p align="center">
  <em>Create and manage multiple isolated development environments.</em>
</p>

## Installation

Workfor requires [multipass](https://multipass.run) to be installed on the host.

The entrypoint is the [`workfor`](./workfor) wrapper script, which will start a
Python CLI. Hence, make sure [Python](https://www.python.org) is installed in
your system.

Now, copy [`.env.example`](./.env.example) into a new file named `.env` and
customize the settings to your preference.

| Option name             | Description                                                                                                                                | Default value  |
|-------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|----------------|
| `MOUNT_BASE_PATH_HOST`  | Path on the host machine from where folders will be mounted into the environments. Workfor will be create one folder for each environment. | `~/Workspaces` |
| `MOUNT_BASE_PATH_GUEST` | Path on the environment where folders will be mounted.                                                                                     | `/workspace`   |

Make sure everyhing works by running `./workfor -h`. If you see the command
usage, then you're all set 🚀.

**Note:** a time saving idea would be to add an alias to the Workfor entrypoint.
Something like this: `alias wf=/path/to/workfor`.

## Create an environment

When creating a new environment, the very first thing to do is configuring it.

If the environment is named `something`, Workfor will look for configuration
files `inventory.yml.something` and `inventory.yml`, in this
order.

You can take a cue from [`inventory.yml.example`](./inventory.yml.example).

When ready, you can start and provision the environment with Workfor (try
running `wf n -h`).

**Note:** it looks like multipass isn't great at preserving mounts between reboots.
Use `wf x` to restart an environment and remount its workspace.
