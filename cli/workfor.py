#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging
import os
import subprocess
import sys
import time

logging.basicConfig(
    datefmt='%Y-%m-%dT%H.%M.%S%z',
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.DEBUG,
)


def run(cmd: str) -> int:
    '''Runs the given subprocess in a shell and returns its exit code.'''
    with subprocess.Popen(
        cmd,
        shell=True,
        stdout=sys.stdout,
        stderr=sys.stderr,
    ) as p:
        p.communicate()
        return p.returncode


def mount(name: str) -> None:
    mount_base_path_host = os.environ.get('MOUNT_BASE_PATH_HOST') \
        or os.path.join(os.path.expanduser('~'), 'Workspaces')
    mount_base_path_guest = os.environ.get('MOUNT_BASE_PATH_GUEST') \
        or '/workspaces'

    mount_from = os.path.join(mount_base_path_host, name)
    mount_dest = f'{mount_base_path_guest}/{name}'
    os.makedirs(mount_from, exist_ok=True)

    logging.info(f'mounting {mount_from} into {name}:{mount_dest}')

    exitcode = run(f'multipass mount {mount_from} {name}:{mount_dest}')
    if exitcode != 0:
        logging.critical(f'unable to mount {mount_from} into {name}: exit code {exitcode}')


def i(name: str) -> None:
    logging.info(f'retrieving information about {name.upper()} environment')
    _ = run(f'multipass -v info {name}')


def l() -> None:
    logging.info(f'listing available environments')
    _ = run('multipass -v list')


def n(name: str, bridged: bool, cpus: int, disk: str, image: str, mem: str) -> None:
    logging.info(f'creating environment {name}: {image} OS, {cpus} vCPU, {disk}B disk, {mem}B RAM')

    exitcode = run(f'''
        multipass -v launch \
            {'--bridged' if bridged else ''} \
            -c {cpus} \
            -d {disk} \
            -m {mem}  \
            -n {name} \
            {image}
    ''')
    if exitcode != 0:
        logging.critical(f'unable to create environment: exit code {exitcode}')
        return

    exitcode = run(f'multipass mount . {name}:/mnt/wf')
    if exitcode != 0:
        logging.critical(f'unable to mount {os.getcwd()} into {name}: exit code {exitcode}')
        return

    exitcode = run(f'''
        multipass exec {name} -- sudo /mnt/wf/provision/provision.sh
    ''')
    if exitcode != 0:
        logging.critical(f'unable to provision {name}: exit code {exitcode}')
        return

    exitcode = run(f'multipass umount {name}:/mnt/wf')
    if exitcode != 0:
        logging.error(f'unable to umount {os.getcwd()} from {name}: exit code {exitcode}')

    mount(name)

    i(name)


def r(name: str) -> None:
    logging.warning(f'deleting environment {name.upper()} forever')
    time.sleep(5)  # Delaying just in case one thinks back

    exitcode = run(f'multipass -v delete {name}')
    if exitcode != 0:
        logging.critical(f'unable to delete environment: exit code {exitcode}')
        return

    exitcode = run('multipass -v purge')
    if exitcode != 0:
        logging.critical(f'unable to delete environment: exit code {exitcode}')
        return

    l()


def x(name: str) -> None:
    logging.info(f'restarting and preparing {name.upper()} environment')

    exitcode = run(f'multipass -v stop {name}')
    if exitcode != 0:
        logging.critical(f'unable to stop environment: exit code {exitcode}')
        return

    exitcode = run(f'multipass -v start {name}')
    if exitcode != 0:
        logging.critical(f'unable to start environment: exit code {exitcode}')
        return

    mount(name)

    i(name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Create and manage development environments',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    subparsers = parser.add_subparsers(
        dest='subcommand',
        title='subcommands',
        required=True,
    )

    parser_i = subparsers.add_parser(
        'i',
        description='print information about an environment',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        help='print information about an environment',
    )
    parser_i.add_argument(
        'name',
        help='name of the enviornment to show information about',
        type=str,
    )

    parser_l = subparsers.add_parser(
        'l',
        description='list all available environments',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        help='list all available environments',
    )

    parser_n = subparsers.add_parser(
        'n',
        description='create a new environment',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        help='create a new environment',
    )
    parser_n.add_argument(
        'name',
        help='name of the enviornment to launch',
        type=str,
    )
    parser_n_options = parser_n.add_argument_group('options')
    parser_n_options.add_argument(
        '--bridged',
        action='store_true',
        default=False,
        help='start the environment on bridge network',
    )
    parser_n_options.add_argument(
        '--cpus',
        default=4,
        help='number of vCPUs to assign to the environment',
        type=int,
    )
    parser_n_options.add_argument(
        '--disk',
        default='50G',
        help='amount of disk to assign to the environment',
        type=str,
    )
    parser_n_options.add_argument(
        '--image',
        default='22.04',
        help='type of image to launch',
        type=str,
    )
    parser_n_options.add_argument(
        '--mem',
        default='6G',
        help='amount of memory to assign to the environment',
        type=str,
    )

    parser_r = subparsers.add_parser(
        'r',
        description='permanently deletes an environment',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        help='permanently deletes an environment',
    )
    parser_r.add_argument(
        'name',
        help='name of the enviornment to permanently remove',
        type=str,
    )

    parser_x = subparsers.add_parser(
        'x',
        description='restart an environment and prepares the mounts',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        help='restart an environment and prepares the mounts',
    )
    parser_x.add_argument(
        'name',
        help='name of the enviornment to prepare',
        type=str,
    )

    args = vars(parser.parse_args())

    subcommand = globals().get(args.pop('subcommand'), None)
    if subcommand is None:
        raise NotImplementedError('unknown subcommand')

    subcommand(**args)
