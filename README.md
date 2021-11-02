# Patroni Dockerfile
You can run Patroni in a docker container using this docker compose project.

The project can bootstrap a 3 node primary HA cluster and 3 node secondary standby 
HA cluster. 


## Cluster configuration

The cluster configuration can be managed by two site specific configuration files
and one config file used as defaults for both sites. 

    settings/defaults.py
    settings/primary.py
    settings/secondary.py

You can override the defaults in each of the site specific configuration files.


## Start clusters

You can start the primary and secondary commands in to independent terminal sessions.
The docker compose command will run in the foreground and output the container logs
on stdout.

    # starts the 3 node cluster primary site
    make primary

    # starts the 3 node cluster secondary site
    make secondary

Both sites expose the following ports on the docker host:
    

Primary:

    Patroni (Postgres): 0.0.0.0:5000->5000/tcp
    Postgres (direct): 0.0.0.0:5400->5432/tcp
    Patroni (REST API): 0.0.0.0:8000->8008/tcp


Secondary:

    Patroni (Postgres): 0.0.0.0:5001->5000/tcp
    Postgres (direct): 0.0.0.0:5401->5432/tcp
    Patroni (REST API): 0.0.0.0:8001->8008/tcp


## Useful commands

Show running containers

    (PatroniHA) Danzig:PatroniHA syrics$ docker ps
    CONTAINER ID   IMAGE                       COMMAND                  CREATED          STATUS          PORTS                                                                    NAMES    
    ad47160b31cd   syrics.us/patroni/cluster   "/usr/bin/python3 /e…"   44 seconds ago   Up 43 seconds                                                                            primary-node2    
    c9c5a61f1330   syrics.us/patroni/cluster   "/usr/bin/python3 /e…"   44 seconds ago   Up 43 seconds                                                                            primary-node1
    55c28f8d45ee   syrics.us/patroni/gateway   "/usr/bin/python3 /e…"   44 seconds ago   Up 43 seconds   0.0.0.0:5000->5000/tcp, 0.0.0.0:5400->5432/tcp, 0.0.0.0:8000->8008/tcp   primary-gateway 
    7bf7b80f0e08   syrics.us/patroni/cluster   "/usr/bin/python3 /e…"   44 seconds ago   Up 43 seconds                                                                            primary-node3
    
Show container logs

    docker logs primary-node2

Show patroni cluster status

    (PatroniHA) Danzig:PatroniHA syrics$ docker exec -ti primary-node1 patronictl --config-file /data/settings/patroni.yml list
    2021-11-02 12:29:21,803 - INFO - Selected new etcd server http://primary-node1:2379
    + Cluster: primary (7025946832745361466) -+---------+----+-----------+
    | Member        | Host          | Role    | State   | TL | Lag in MB |
    +---------------+---------------+---------+---------+----+-----------+
    | primary-node1 | primary-node1 | Replica | running |  1 |         0 |
    | primary-node2 | primary-node2 | Replica | running |  1 |         0 |
    | primary-node3 | primary-node3 | Leader  | running |  1 |           |


Show etcd cluster members

    (PatroniHA) Danzig:PatroniHA syrics$ docker exec -ti primary-node1 etcdctl member list
    f1b23951a525ba2: name=primary-node3 peerURLs=http://primary-node3:2380 clientURLs=http://primary-node3:2379 isLeader=false
    2fa2a421086ba24f: name=primary-node2 peerURLs=http://primary-node2:2380 clientURLs=http://primary-node2:2379 isLeader=false
    8418ac8bdc93a1e4: name=primary-node1 peerURLs=http://primary-node1:2380 clientURLs=http://primary-node1:2379 isLeader=true


