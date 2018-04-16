Build Architecture
------------------

Each RPM spec is devoted to a single git repository and most generate several RPMs. A crucial design
feature is a preference is to include and build specific versions of C/C++ libraries rather than use
those packaged for the operating system. It adds much complexity to the build process, but it does
ensure stability, though at the cost of losing security fixes provided by the operating system. This
preference is applied inconsistently: e.g. Sprout builds its own libcurl, while Ralf/Homestead use
the operating system's.

### clearwater-astaire

Astaire provides [memcached](https://memcached.org/) clustering with SNMP support, and Rogers
is a memcached proxy. Both are written in C++.

### clearwater-chronos

Chronos is a distributed timer service with a HTTP API written in C++ based on
[evhtp](https://github.com/criticalstack/libevhtp) and [rapidjson](http://rapidjson.org/) for HTTP.

### clearwater-crest

Contains Homer (XDMS) and Homestead's provisioning API (note that Homestead itself is in its own
spec). Both are based on Crest: a custom, extensible HTTP-RESTful interface to
[Cassandra](http://cassandra.apache.org/) written in Python 2, based on
[Zope](http://www.zope.org/)/[Cyclone](http://cyclone.io/)/[Twisted](https://twistedmatrix.com/).
Python code accesses cpp-common via [CFFI](https://cffi.readthedocs.io/).

### clearwater-ellis

Contains Ellis (provisioning portal). Web application and CLI tools. Web backend is written in
Python 2 and based on [Tornado](http://www.tornadoweb.org/) and
[SQLAlchemy](https://www.sqlalchemy.org/) over [MySQL](https://www.mysql.com/). Web frontend based
on [Bootstrap](https://getbootstrap.com/)/[jQuery](https://jquery.com/). Python code accesses
cpp-common via [CFFI](https://cffi.readthedocs.io/).

### clearwater-etcd

Contains tools to configure a cluster of [etcd](https://github.com/coreos/etcd), comprising
the Cluster Manager, Config Manager, and Queue Manager. All of these are written in Python 2.
Python code accesses cpp-common via CFFI.

### clearwater-homestead

Contains Homestead (HSS cache/gateway), a Diameter/Cx and HTTP-RESTful interface to Cassandra
written in C++ based on [freeDiameter](http://www.freediameter.net/) for Diameter and evhtp and
[Thrift](http://thrift.apache.org/)/rapidjson for HTTP with memcached as the cache.

### clearwater-infrastructure

Clearwater's miscellany. Contains Vellum (storage) and Dime (Ralf + Homestead) meta-packages.
Contains the Diagnostics Monitor component is a set of bash scripts for gathering essential machine
and component diagnostics. Contains pre-configured memcached and snmpd. Contains configuration
validation (written in Python), loading, and auto-generation. There already is an effort in this
repository to create RPMs.

### clearwater-logging

Clearwater's logging is based on [Nagios](https://www.nagios.org/) and
[Sysstat](https://github.com/sysstat/sysstat).

### clearwater-memento

Contains Memento (Application Server responsible for providing network-based call lists), written
in C++ based on evhtp and Thrift/rapidjson for HTTP with memcached as the cache.

### clearwater-monit

Fork of [Monit](https://mmonit.com/monit/) daemon monitor, written in C.

### clearwater-nginx

[Nginx](https://www.nginx.com/) (as a dependency, not a fork) with Clearwater-specific
configurations.

### clearwater-ralf

Contains Ralf (CTF). Similar architecture to that of Homestead, but uses Diameter/Rf instead. (The
two repositories might be better off combined.)

### clearwater-sprout

Contains Sprout (SIP router), Bono (SIP edge proxy/loadbalancer), and several Sprout plugins. Also
includes forks of [restund](http://www.creytiv.com/restund.html) (STUN/TURN server) and
[SIPp](http://sipp.sourceforge.net/) (SIP stress testing). Sprout and Bono are in fact the same
executable, just with different configurations, based on [PJSIP](http://www.pjsip.org/),
[WebSocket++](https://www.zaphoyd.com/websocketpp), and [curl](https://curl.haxx.se/). SIPp
provides Ruby gems for integration with Rake. Note that this is the biggest spec of the bunch
and takes an especially long time to build.
