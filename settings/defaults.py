CLUSTER = None
CLUSTER_NODES = None
CLUSTER_GATEWAY = None

PATRONI_LOG_LEVEL = 'INFO'
POSTGRESQL_LOG_LEVEL = 'DEBUG'
ETCD_LOG_LEVEL = 'error'
HAPROXY_LOG_LEVEL = 'warning'

# Standby configuration that points a secondary
# cluster to the primary cluster for replication
PATRONI_STANDBY_PRIMARY_LEADER = None  # hostname / ip of primary site leader or empty if not replicated from primary
PATRONI_STANDBY_PRIMARY_LEADER_SLOT_NAME = None  # try "patroni" which is the default in the settings docs

# Replication settings that we assume make the
# biggest difference in terms of fail / success
# of cross site streaming replication
#
# NOTE: WAL_LEVEL -> In releases prior to 9.6, this
# parameter also allowed the values archive and hot_standby.
# These are still accepted but mapped to replica.
PATRONI_WAL_LEVEL = 'replica'
PATRONI_WAL_KEEP_SEGMENTS = 1024
PATRONI_WAL_MAX_SENDERS = 8
PATRONI_WAL_MAX_REPLICATION_SLOTS = 8

# General password setup
PATRONI_RESTAPI_USERNAME = 'restapi'
PATRONI_RESTAPI_PASSWORD = 'password'
PATRONI_ADMIN_USERNAME = 'admin'
PATRONI_ADMIN_PASSWORD = 'password'
PATRONI_REPLICATION_USERNAME = 'replicator'
PATRONI_REPLICATION_PASSWORD = 'password'
PATRONI_SUPERUSER_USERNAME = 'postgres'
PATRONI_SUPERUSER_PASSWORD = 'password'
PATRONI_REWIND_USERNAME = 'rewind'
PATRONI_REWIND_PASSWORD = 'password'
