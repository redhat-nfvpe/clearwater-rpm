Utility Packages
================


### `clearwater-radius-auth`

### `clearwater-snmpd`

### `clearwater-cassandra`

This requires [Cassandra](http://cassandra.apache.org/), which is not included in the CentOS
repositories. You must thuss add the Cassandra repository for this package to install.

### `clearwater-monit`

Fork of [Monit](https://mmonit.com/monit/) daemon monitor, written in C. The
[service packages](service-packages.md) come with appropriate monit control files.


Installation
------------

### `clearwater-infrastructure`

Poorly named. Handles running scripts for deployment-wide installation and upgrading.

### `clearwater-auto-upgrade`


Configuration
-------------

Tools to configure a cluster of [etcd](https://github.com/coreos/etcd). All of these are written in
Python 2. Python code accesses cpp-common via CFFI.

### `clearwater-cluster-manager`

### `clearwater-queue-manager`

### `clearwater-config-manager`

### `clearwater-etcd`

### `clearwater-auto-config-generic`

### `clearwater-auto-config-aws`

### `clearwater-auto-config-docker`


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
and component diagnostics. Contains pre-configured memcached and snmpd. Contains configuration
validation (written in Python), loading, and auto-generation.

### `clearwater-splunkforwarder-fake`

Looks like splunkforwarder but does nothing.


Networking
----------

### `clearwater-tcp-scalability`

### `clearwater-secure-connections`

### `clearwater-socket-factory`
