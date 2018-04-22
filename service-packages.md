Service Packages
================

These are the core systemd services that comprise a Clearwater deployment. You will usually install
them indirectly via a [node package](node-packages.md).

Importantly, though these packages install the components, they do not and cannot install the
deployment-wide requirements for the components. For example, they cannot commission required
MariaDB or Cassandra databases if those services are running on other servers.

Thus, a "complete" install of these services requires a properly configured node and the
poorly named `clearwater-infrastructure` [utility package](utility-packages.md), which will run the
appropriate scripts included in each of these packages. `clearwater-infrastructure` must be
installed separately. 

Additionally, these packages also contain monit control files, which can be used with the
optional `clearwater-monit` daemon monitor, also a [utility package](utility-packages.md).


`clearwater-astaire`
--------------------

Provides [memcached](https://memcached.org/) clustering with SNMP support. Written in C++.


`clearwater-bono`
-----------------

SIP edge proxy. Bono is actually the exact same executable as Sprout (see below) run with a
different configuration.


`clearwater-chronos`
--------------------

Distributed timer service with a HTTP API written in C++ based on
[evhtp](https://github.com/criticalstack/libevhtp) and [rapidjson](http://rapidjson.org/) for HTTP.


`clearwater-ellis`
------------------

Provisioning portal. Web backend is written in Python 2 and based on
[Tornado](http://www.tornadoweb.org/) and [SQLAlchemy](https://www.sqlalchemy.org/) over
[MySQL](https://www.mysql.com/). Web frontend based on
[Bootstrap](https://getbootstrap.com/)/[jQuery](https://jquery.com/). Python code accesses
cpp-common via [CFFI](https://cffi.readthedocs.io/).


`clearwater-homer`
------------------

XDMS. Based on Crest (see helper packages, below).

* `clearwater-homer-cassandra`


`clearwater-homestead`
----------------------

HSS cache/gateway. A Diameter/Cx and HTTP-RESTful interface to Cassandra written in C++ based on
[freeDiameter](http://www.freediameter.net/) for Diameter and evhtp and
[Thrift](http://thrift.apache.org/)/rapidjson for HTTP with memcached as the cache.

* `clearwater-homestead-cassandra`
* `clearwater-homestead-prov`
* `clearwater-homestead-prov-cassandra`

An HTTP API allows Ellis access to Homestead data. Based on Crest (see helper packages, below).


`clearwater-provisioning-tools`
-------------------------------

Provisioning CLI tools.


`clearwater-ralf`
-----------------

CTF. Similar architecture to that of Homestead (see above), but uses Diameter/Rf instead.


`clearwater-rogers`
-------------------

memcached proxy. Written in C++.


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

Application Server responsible for providing network-based call lists, written in C++ based on
evhtp and Thrift/rapidjson for HTTP with memcached as the cache.

* `clearwater-memento`
* `clearwater-memento-nginx`
* `clearwater-memento-cassandra`
