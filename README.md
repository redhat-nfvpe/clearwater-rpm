RPM Packaging for Clearwater IMS
================================

INCOMPLETE! WORK IN PROGRESS!

The [Clearwater IMS](https://www.projectclearwater.org/) is officially packaged for Ubuntu 14.04.
Here we are re-packaging it for RHEL, CentOS, and other RPM-based Linux distributions. We support
the x86_64 platform only.


How To Build
------------

The build scripts are all under `scripts`.

First run `fetch-sources` to download the sources and archive them in the `SOURCES` directory. (Note:
we must use git to fetch them, because the repositories are designed with many git submodules,
which are not packaged in GitHub's release tarballs. Also note that these submodules are tied to
specific commits, which unfortunately do not match their git release tags. In short, this is the
only way to get the correct and complete source tarball.)

You then have a few options for building the RPMs:

1. Are you on CentOS or RHEL? Then just run `scripts/build/build`. (The requirements are documented in
   the scripts.)
2. Or, use our included [Vagrant](https://www.vagrantup.com/) configuration to quickly bring up a
   CentOS virtual machine. Just run `vagrant up`, and then `vagrant ssh` to login. The directories are
   conveniently shared with the host operating system. (Note that you may need the VirtualBox Guest
   Additions. Install them automatically via a plugin: `vagrant plugin install vagrant-vbguest`.)
3. On other Linuxes, use [mock](https://github.com/rpm-software-management/mock) to emulate CentOS
   in a chroot environment. For this, run `scripts/build/mock-build`. Note that mock will use up a lot of
   space in `/var/lib/mock` while running, so you may want to mount that directory somewhere spacious.
   Also see
   [here](https://marcin.juszkiewicz.com.pl/2016/04/15/how-to-speed-up-mock/) and
   [here](http://miroslav.suchy.cz/blog/archives/2015/05/28/increase_mock_performance_-_build_packages_in_memory/index.html)
   for some tips to speed up mock.

Once the build process starts, go make yourself a cup of tea, because it's going to take a while
(25 minutes on a 6-core workstation). Though the Clearwater build scripts are not very friendly to
concurrency (`make --jobs`) we've enabled concurrent builds in the sub-modules, and that has helped
a lot (cut down from 60 minutes).

When finished (phew!) your RPMs will be available under `RPMS/x86_64`.

You can also build individual spec files by providing the name as an argument, for example:
`build-rpms clearwater-ellis`.

Also useful may be the `validate-install` script, which skips the `%prepare` and `%build` sections in the
spec file.

All scripts capture their output into log files into the `logs` directory. If you're using mock
there will be extra logs under `RPMS/x86_64`.


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

Contains Homer (XDMS) and Homestead's provisioning server (note that Homestead itself is in its own
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


How To Use
----------

TODO

Because there are so many interdependencies, it's best to put the RPMs in a repository. The
`install-local-repository` script will do it locally, using the filesystem. Make sure to re-run it if you
rebuild any of the RPMs. You can then use `yum install` for any of the components, e.g.
`yum install clearwater-sprout`.

### Required

*Before* installing any Clearwater component, make sure you have `/etc/clearwater/local_config` and
`/etc/clearwater/shared_config`. The clearwater-auto-config-* packages come with templates for these
files.

Sprout (SIP router)

Homer (XDMS)

Vellum (Store)

Dime = Homestead (HSS) + Ralf (CTF) 

### Optional

Ellis (provisioning portal)

Bono (SIP edge proxy)