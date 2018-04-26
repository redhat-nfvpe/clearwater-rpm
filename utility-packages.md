Utility Packages
================

### `clearwater-snmpd`

### `clearwater-radius-auth`

### `clearwater-provisioning-tools`

Provisioning CLI tools.


Configuration
-------------

### `clearwater-auto-upgrade`

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

### `clearwater-tcp-scalability`

Modifies `/etc/sysctl.conf` for increased TCP scalability.
