CLUSTER = 'secondary'
CLUSTER_NODES = 'secondary-node1,secondary-node2,secondary-node3'
CLUSTER_GATEWAY = 'secondary-gateway'

# Standby configuration that points a secondary
# cluster to the primary cluster for replication
PATRONI_STANDBY_PRIMARY_LEADER = 'primary-gateway'
#PATRONI_STANDBY_PRIMARY_LEADER_SLOT_NAME = ''  # try "patroni" which is the default in the settings docs
