
## Single VM Setup

Template:
```ini
# This inventory describe a HA typology with stacked etcd (== same nodes as control plane)
# and 3 worker nodes
# See https://docs.ansible.com/ansible/latest/inventory_guide/intro_inventory.html
# for tips on building your # inventory

# Configure 'ip' variable to bind kubernetes services on a different ip than the default iface
# We should set etcd_member_name for etcd cluster. The node that are not etcd members do not need to set the value,
# or can set the empty string value.
[kube_control_plane]
# node1 ansible_host=95.54.0.12  # ip=10.3.0.1 etcd_member_name=etcd1
# node2 ansible_host=95.54.0.13  # ip=10.3.0.2 etcd_member_name=etcd2
# node3 ansible_host=95.54.0.14  # ip=10.3.0.3 etcd_member_name=etcd3

[etcd:children]
kube_control_plane

[kube_node]
# node4 ansible_host=95.54.0.15  # ip=10.3.0.4
# node5 ansible_host=95.54.0.16  # ip=10.3.0.5
# node6 ansible_host=95.54.0.17  # ip=10.3.0.6
```

Setup:
```ini
# This inventory describe a HA typology with stacked etcd (== same nodes as control plane)
# and 3 worker nodes
# See https://docs.ansible.com/ansible/latest/inventory_guide/intro_inventory.html
# for tips on building your # inventory

# Configure 'ip' variable to bind kubernetes services on a different ip than the default iface
# We should set etcd_member_name for etcd cluster. The node that are not etcd members do not need to set the value,
# or can set the empty string value.
[kube_control_plane]
node1 ansible_host=localhost  ip=10.3.0.1 etcd_member_name=etcd1
# node2 ansible_host=95.54.0.13  # ip=10.3.0.2 etcd_member_name=etcd2
# node3 ansible_host=95.54.0.14  # ip=10.3.0.3 etcd_member_name=etcd3

[etcd:children]
kube_control_plane

[kube_node]
node4 ansible_host=95.54.0.15  ip=10.3.0.4
# node5 ansible_host=95.54.0.16  # ip=10.3.0.5
# node6 ansible_host=95.54.0.17  # ip=10.3.0.6
```

```ini
[all]
localhost ansible_connection=local ansible_host=127.0.0.1 ip=127.0.0.1 ansible_become=true

[kube_control_plane]
localhost

[kube_node]
localhost

[etcd]
localhost

[k8s_cluster:children]
kube_control_plane
kube_node
```

```ini
[all]
localhost ansible_connection=local ip=127.0.0.1

[kube_control_plane]
localhost

[etcd]
localhost

[kube_node]
localhost

[k8s_cluster:children]
kube_control_plane
kube_node

[calico_rr]

[vault]
```

## Run Kubespray


```ini
[all]
node1   ansible_connection=local ansible_host=<your-ip> ip=<your-ip>
node2   ansible_connection=local ansible_host=<your-ip> ip=<your-ip>
[kube-master]
node1
# We don't want node2 to act as master
# node2
[kube-node]
node1
node2
[etcd]
node1
# We don't want node2 to run etcd
# node2
[k8s-cluster:children]
kube-node   
kube-master
[calico-rr]
```