#!/usr/bin/env python3

import importlib
from pathlib import Path

import click
from jinja2 import Template

COMPOSE_TMPL = Path('docker/docker-compose.yml.jinja2')


def _import(conf):
    settings = importlib.import_module('settings.' + conf).__dict__
    return {
        k: v for k, v in settings.items() if not k.startswith('__')
    }


def _is_port_in_use(port):
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0


def _determine_port(pfrom, pto):
    for port in range(pfrom, pto):
        if not _is_port_in_use(port):
            return port


@click.group()
def compose():
    pass


@compose.command()
@click.option('--name', prompt='Cluster name', help='The name of the cluster to create.')
def cluster(name):
    environment = {
        **_import('defaults'),
        **_import(name)
    }

    # print out all variables that go into the
    # template renderer to generate the actual
    # docker compose file
    print(f'Rendering compose template for cluster {name} with vars')
    print('----------------------')
    for k, v in environment.items():
        print(f'{k}: {v}')
    print('----------------------')

    # determine the gateway port to use to expose the
    # cluster. Starting at 5000 upwards
    pt_gateway_port = _determine_port(5000, 5100)
    pg_gateway_port = _determine_port(5400, 5500)
    pt_api_gateway_port = _determine_port(8000, 8100)

    # read the template file from disc and render it
    # using the template renderer
    tm = Template(COMPOSE_TMPL.read_text())
    rendered = tm.render({
        'ENVIRONMENT': environment,
        'PG_GATEWAY_PORT': pg_gateway_port,
        'PT_GATEWAY_PORT': pt_gateway_port,
        'PT_API_GATEWAY_PORT': pt_api_gateway_port,
        **environment
    })

    # now that we have the rendered text, we write
    # the docker compose file to disc that was created
    # with the variables.
    config_file = Path(f'build/docker-compose-{name}.yml')
    config_file.parent.mkdir(parents=True, exist_ok=True)
    print(f'Writing compose file {config_file}')
    open(config_file, 'w').write(rendered)


if __name__ == '__main__':
    compose()
