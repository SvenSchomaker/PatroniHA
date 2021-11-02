#!/usr/bin/env python3
import os
import socket
import time
from pathlib import Path

from jinja2 import Template

TEMPLATES_DIR = '/data/templates'
CONFIG_DIR = '/data/settings'


nodes = os.environ['CLUSTER_NODES'].split(',')

cluster_nodes = [
    {'name': name, 'ip': socket.gethostbyname(name)}
    for name in nodes
]

config = {
    **os.environ,
    'CLUSTER_NODES': cluster_nodes
}


def render_config_files():
    paths = Path(TEMPLATES_DIR).glob('*.jinja2')
    for templ_file in paths:
        print(f'Reading {templ_file}')
        tm = Template(templ_file.read_text())

        rendered = tm.render(**config)
        config_file = Path(CONFIG_DIR) / templ_file.stem
        config_file.parent.mkdir(parents=True, exist_ok=True)
        print(f'Writing {config_file}')
        open(config_file, 'w').write(rendered)


def start_haproxy():
    print("++++++++++++++++++ STARTING HAPROXY ++++++++++++++++++")
    os.system('cat /data/settings/haproxy.cfg')
    os.system("/usr/sbin/haproxy -f /data/settings/haproxy.cfg &")


if __name__ == '__main__':
    render_config_files()
    start_haproxy()

    while True:
        time.sleep(2**16)