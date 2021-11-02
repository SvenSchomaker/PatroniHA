#!/usr/bin/env python3
import atexit
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
    'CLUSTER_NODES': cluster_nodes,
    'ETCD_INITIAL_CLUSTER': ','.join([f'{node}=http://{node}:2380' for node in nodes])
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


def start_etcd():
    print("++++++++++++++++++ STARTING ETCD ++++++++++++++++++")
    os.system('cat /data/settings/etcd.yml')
    os.system("/usr/bin/etcd --config-file /data/settings/etcd.yml &")


def start_patroni():
    print("++++++++++++++++++ STARTING PATRONI ++++++++++++++++++")
    os.system('cat /data/settings/patroni.yml')
    os.system("mkdir -p /data/patroni/data "
              "&& cp /data/settings/patroni.yml /data/patroni "
              "&& chown -R postgres:postgres /data/patroni"
              "&& chmod 0750 /data/patroni/data")
    os.system('rm /data/patroni/data/*.lock 2>/dev/null')
    os.system("sudo -u postgres /usr/bin/patroni /data/patroni/patroni.yml &")


def stop_patroni():
    print("++++++++++++++++++ STOPPING PATRONI ++++++++++++++++++")
    os.system("killall -SIGTERM patroni")
    os.system("killall -SIGTERM postgres")


if __name__ == '__main__':
    render_config_files()

    start_haproxy()
    start_etcd()
    start_patroni()

    atexit.register(stop_patroni),

    while True:
        time.sleep(2**16)