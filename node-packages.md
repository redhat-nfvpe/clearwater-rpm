Node Packages
=============

These are the packages that most users will use.

These represent "nodes" in the Clearwater architecture. A single high-level package contains
the minimum required to run the node. For the most part these are meta-packages that in turn require
the [actual services](service-packages.md) as well as some [utilities](utility-packages.md).

It is possible to install multiple nodes on a single server. Indeed, you can install all of them on
one server to create an "all-in-one" deployment.


Composite Nodes (priority 10)
-----------------------------

* `clearwater-node-dime` (Diameter)
    * `clearwater-node-homestead` (HSS cache/gateway)
    * `clearwater-node-ralf` (CTF)
* `clearwater-node-vellum` (storage)
    * `clearwater-node-chronos`
    * `clearwater-node-memcached`
    * `clearwater-node-cassandra`
    * `clearwater-etcd` (TODO: cluster and queue managers?)


Base Nodes (priority 20)
------------------------

* `clearwater-node-bono` (SIP edge proxy) 
    * `clearwater-sprout-libs`
* `clearwater-node-ellis` (provisioning portal)
    * `clearwater-ellis`
    * `clearwater-prov-tools`
* `clearwater-node-homer` (XDMS)
* `clearwater-node-homestead` (HSS cache/gateway)
    * `clearwater-homestead`
    * `clearwater-homestead-prov`
* `clearwater-node-ralf` (CTF)
* `clearwater-node-sprout` (SIP router)


Plugin Nodes (priority 80)
--------------------------

* `clearwater-node-memento`


Sub-Nodes (priority 90)
-----------------------

* `clearwater-node-cassandra` (database)
* `clearwater-node-chronos` (distributed timer)
* `clearwater-node-memcached` (cache)
    * `clearwater-memcached`
    * `clearwater-astaire` (memcached clustering)
    * `clearwater-rogers` (memcached proxy)
