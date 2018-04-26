Service Packages
================

These are the core systemd services that comprise a Clearwater deployment. You will usually install
them indirectly via a [node package](node-packages.md).

Importantly, though these packages install the services, they do not and cannot install the
deployment-wide requirements for them to run properly. For example, they cannot commission required
MariaDB or Cassandra databases if those services are running on other servers.

Thus, a "complete" install of these services requires a properly configured node *as well as* the
poorly named `clearwater-infrastructure`, which will run the appropriate scripts included in each of
these packages.

Additionally, these packages also contain monit control files, which can be used with the
optional `clearwater-monit` daemon monitor.

Note that the services themselves are named without the `clearwater-` prefix. e.g:

    systemctl status sprout.service


`clearwater-astaire`
--------------------

Provides [memcached](https://memcached.org/) clustering with SNMP support. Written in C++.


`clearwater-bono`
-----------------

SIP edge proxy. Bono is actually the exact same executable as Sprout (see below) run with a
different configuration.


`clearwater-cassandra`
----------------------

This requires [Cassandra](http://cassandra.apache.org/), which is not included in the CentOS
repositories. You must thus add the Cassandra repository for this package to install.


`clearwater-chronos`
--------------------

Distributed timer service. Used by Sprout and Ralf. HTTP API written in C++ based on
[evhtp](https://github.com/criticalstack/libevhtp) and [rapidjson](http://rapidjson.org/) for HTTP.


`clearwater-clustering`
-----------------------

[Services](http://www.projectclearwater.org/using-etcd-in-project-clearwater-part-ii/) to manage
clusters of Cassandra, memcached, Chronos, and Sprout. Every node that is part of the cluster must
be running these services. The cluster information is stored in etcd.
 
Each service that needs to make use clustering must install plugins, written in Python, under
the appropriate directories. These plugins are in charge of reconfiguring and restarting the local
services accordingly.

All of these services are written in Python 2. Python code accesses cpp-common via CFFI.

TODO:

* Many of the plugins are still not fixed for systemd: they try to run non-LSB service commands

### `clearwater-cluster-manager`

Tracks additions to and removals from the clusters. Plugins are in
`/usr/share/clearwater/clearwater-cluster-manager/plugins`.

To temporarily stop a cluster manager (and keep it from restarting): 

    touch /etc/clearwater/no\_cluster\_manager
    systemctl stop clearwater-cluster-manager.service

### `clearwater-config-manager`

Tracks changes to shared configurations. Plugins are in
`/usr/share/clearwater/clearwater-config-manager/plugins`. Though these plugins *could* change the
configurations and restart services directly, having all services in the cluster down at the same
time could lead to general failure. Thus, changes are put in a queue and are executed in order by
the `clearwater-queue-manager` (see below).

To temporarily stop the config manager (and keep it from restarting): 

    touch /etc/clearwater/no\_config\_manager
    systemctl stop clearwater-config-manager.service

### `clearwater-queue-manager`

Plugins are in
`/usr/share/clearwater/clearwater-queue-manager/plugins`.


`clearwater-ellis`
------------------

Provisioning portal. Optional. Web backend is written in Python 2 and based on
[Tornado](http://www.tornadoweb.org/) and [SQLAlchemy](https://www.sqlalchemy.org/) over
[MySQL](https://www.mysql.com/). Web frontend based on
[Bootstrap](https://getbootstrap.com/)/[jQuery](https://jquery.com/). Python code accesses
cpp-common via [CFFI](https://cffi.readthedocs.io/).


`clearwater-etcd`
-----------------

See [etcd](https://github.com/coreos/etcd).


`clearwater-homer`
------------------

XDMS. Stores MMTEL setting for users using an XCAP interface. Based on Crest (see
[helper packages](helper-packages.md).

* `clearwater-homer-cassandra`


`clearwater-homestead`
----------------------

HSS cache/gateway. Used by Sprout to authenticate users and retrieve their profiles. A Diameter/Cx
and HTTP-RESTful interface to Cassandra written in C++ based on
[freeDiameter](http://www.freediameter.net/) for Diameter and evhtp and
[Thrift](http://thrift.apache.org/)/rapidjson for HTTP with memcached as the cache.


* `clearwater-homestead-cassandra`
* `clearwater-homestead-prov`
* `clearwater-homestead-prov-cassandra`

An HTTP API allows Ellis access to Homestead data. Based on Crest (see helper packages, below).


`clearwater-infrastructure`
---------------------------

Poorly named. Handles running scripts for deployment-wide installation and upgrading. Such scripts
should all be in `/usr/share/clearwater/infrastructure/scripts/`.

Note that unlike the other services it is *not* a long-running daemon: it must be restarted in order
to do its work.

This service generates the `/etc/clearwater/config` script upon which many components rely.

TODO:

* These included tools are Debian-specific: `clearwater-version`, `clearwater-upgrade`


`clearwater-ralf`
-----------------

CTF. Used by Sprout and Bono to report billable events. Similar architecture to that of Homestead
(see above), but uses Diameter/Rf instead.


`clearwater-rogers`
-------------------

memcached proxy. Written in C++.


`clearwater-monit`
------------------

Fork of [Monit](https://mmonit.com/monit/) daemon monitor, written in C. Many of these service
packages come with monit control files, and are "monit aware": if monit is installed, they will
delegate service management to monit.


`clearwater-socket-factory`
---------------------------

These systemd services provide on-demand sockets in other namespaces.

* `clearwater-socket-factory-mgmt`
* `clearwater-socket-factory-sig`


`clearwater-sprout`
-------------------

SIP router. Written in C++ based on [PJSIP](http://www.pjsip.org/),
[WebSocket++](https://www.zaphoyd.com/websocketpp), and [curl](https://curl.haxx.se/).

### Sprout Plugins

* `clearwater-sprout-plugin-scscf`
* `clearwater-sprout-plugin-icscf`
* `clearwater-sprout-plugin-bgcf`

### Sprout Application Server (AS) plugins

* `clearwater-sprout-as-plugin-mmtel`
* `clearwater-sprout-as-plugin-gemini`
* `clearwater-sprout-as-plugin-memento`
* `clearwater-sprout-as-plugin-call-diversion`
* `clearwater-sprout-as-plugin-mangelwurzel`

### Memento

Application Server for Sprout responsible for providing network-based call lists, written in C++
based on evhtp and Thrift/rapidjson for HTTP with memcached as the cache.

* `clearwater-memento`
* `clearwater-memento-nginx`
* `clearwater-memento-cassandra`
