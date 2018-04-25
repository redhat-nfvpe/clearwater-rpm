Utility Packages
================


### `clearwater-cassandra`

This requires [Cassandra](http://cassandra.apache.org/), which is not included in the CentOS
repositories. You must thuss add the Cassandra repository for this package to install.

### `clearwater-monit`

Fork of [Monit](https://mmonit.com/monit/) daemon monitor, written in C. The
[service packages](service-packages.md) as well as many of these utility packages come with monit
control files, and are "monit aware": if monit is installed, they will delegate service management
to monit.

### `clearwater-snmpd`

### `clearwater-radius-auth`


Installation
------------

### `clearwater-infrastructure`

Poorly named. Handles running scripts for deployment-wide installation and upgrading. These scripts
should all be in `/usr/share/clearwater/infrastructure/scripts/`.

This service generates the `/etc/clearwater/config` script, upon which many components rely.

TODO:

* Many of the scripts are still not fixed for systemd: they try to run non-LSB service commands
* These included tools are Debian-specific: `clearwater-version`, `clearwater-upgrade`.

### `clearwater-auto-upgrade`


Configuration
-------------

Tools to configure a cluster of [etcd](https://github.com/coreos/etcd). All of these are written in
Python 2. Python code accesses cpp-common via CFFI.

### `clearwater-cluster-manager`

### `clearwater-queue-manager`

### `clearwater-config-manager`

### `clearwater-etcd`

### Auto Configuration

These automatically generate `local_config` and `shared_config` for you based on querying the cloud
environment.

* `clearwater-auto-config-generic`
* `clearwater-auto-config-aws`
* `clearwater-auto-config-docker`


Testing
-------

### `clearwater-sipp`

### `clearwater-sip-stress`

### `clearwater-sip-stress-stats`

### `clearwater-sip-perf`


Logging
-------

### `clearwater-logging`

Based on [Nagios](https://www.nagios.org/),
[Sysstat](https://github.com/sysstat/sysstat), and supports [Splunk](https://www.splunk.com/).

Note that Splunk is not open source and must be installed separately. However, to allow you to
still use the logging package without Splunk installed, we provide the
clearwater-splunkforwarder-fake package.

### `clearwater-log-cleanup`

### `clearwater-diags-monitor`

The Diagnostics Monitor component is a set of bash scripts for gathering essential machine
and component diagnostics. Contains configuration validation (written in Python), loading, and
auto-generation.

### `clearwater-splunkforwarder-fake`

Looks like splunkforwarder but does nothing.


Networking
----------

### `clearwater-secure-connections`

IPsec support based on [Racoon](http://www.racoon2.wide.ad.jp/w/).

### `clearwater-socket-factory`

These systemd services provide on-demand sockets in other namespaces, specifically the management
(`clearwater-socket-factory-mgmt`) and signaling (`clearwater-socket-factory-sig`) namespaces.

### `clearwater-tcp-scalability`

Modifies `/etc/sysctl.conf` for increased TCP scalability.
