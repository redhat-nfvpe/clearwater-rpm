Name:          clearwater-infrastructure
Version:       129
Release:       1%{?dist}
License:       GPLv3+
URL:           https:/github.com/Metaswitch/clearwater-infrastructure

Source0:       %{name}-%{version}.tar.bz2
BuildRequires: make python-virtualenv
BuildRequires: zeromq-devel boost-devel
BuildRequires: systemd

# Note: zeromq-devel requires epel-release

%global debug_package %{nil}

Summary:       Clearwater - Infrastructure
Requires:      zeromq python-setuptools
Requires:      dnsmasq ntp gnutls-utils curl redhat-lsb-core
AutoReq:       no
%{?systemd_requires}

# Note: We actually require python-virtualenv, too, but unfortunately the version in epel-7 is too
# old (its included pip is too old), so we will install it manually in the postinst scriptlet,
# which is why we are requiring python-setuptools here instead

%package -n clearwater-memcached
Summary:       Clearwater - memcached
Requires:      memcached
AutoReq:       no
#Requires:      clearwater-infrastructure clearwater-monit

%package -n clearwater-tcp-scalability
Summary:       Clearwater - TCP Scalability
AutoReq:       no

%package -n clearwater-secure-connections
Summary:       Clearwater - Secure Connections
Requires:      racoon2 ipsec-tools
AutoReq:       no

%package -n clearwater-snmpd
Summary:       Clearwater - snmpd
Requires:      net-snmp
AutoReq:       no
#Requires:      clearwater-infrastructure clearwater-monit

%package -n clearwater-diags-monitor
Summary:       Clearwater - Diagnostics Monitor
Requires:      inotify-tools sysstat gzip iotop
AutoReq:       no
#Requires:      clearwater-infrastructure clearwater-monit

%package -n clearwater-socket-factory
Summary:       Clearwater - Socket Factory
Requires:      boost
AutoReq:       no
#Requires:      clearwater-infrastructure

%package -n clearwater-auto-config-aws
Summary:       Clearwater - Auto-config AWS
AutoReq:       no

%package -n clearwater-auto-config-docker
Summary:       Clearwater - Auto-config Docker
AutoReq:       no

%package -n clearwater-auto-config-generic
Summary:       Clearwater - Auto-config Generic
AutoReq:       no

%package -n clearwater-log-cleanup
Summary:       Clearwater - Log Cleanup
AutoReq:       no

%package -n clearwater-auto-upgrade
Summary:       Clearwater - Auto-upgrade
AutoReq:       no

%package -n clearwater-radius-auth
Summary:       Clearwater - RADIUS Authentication
Requires:      pam_radius
AutoReq:       no

%package -n clearwater-vellum
Summary:       Clearwater - Vellum
AutoReq:       no

%package -n clearwater-dime
Summary:       Clearwater - Dime
AutoReq:       no
#Requires:      clearwater-infrastructure clearwater-monit clearwater-memcached

%description
Common infrastructure

%description -n clearwater-memcached
memcached configured for Clearwater

%description -n clearwater-tcp-scalability
TCP scalability improvements

%description -n clearwater-secure-connections
Secure connections between regions

%description -n clearwater-snmpd
SNMP service for CPU, RAM, and I/O statistics

%description -n clearwater-diags-monitor
Diagnostics monitor and bundler

%description -n clearwater-socket-factory
Enables other processes to establish connections using a different network namespace

%description -n clearwater-auto-config-aws
Auto-configuration tool for AWS

%description -n clearwater-auto-config-docker
Auto-configuration tool for Docker

%description -n clearwater-auto-config-generic
Generic auto-configuration tool

%description -n clearwater-log-cleanup
Prevent Sprout/Bono log files from growing too large

%description -n clearwater-auto-upgrade
Automatic upgrade

%description -n clearwater-radius-auth
RADIUS authentication

%description -n clearwater-vellum
Storage node

%description -n clearwater-dime
HTTP-to-Rf/Cx gateway node

%prep
%setup

%build
# CentOS's virtualenv requires a newer version of setuptools
sed --in-place 's/"setuptools==24"/"setuptools==39.0.1"/' clearwater-infrastructure/PyZMQ/Makefile

make MAKE="make --jobs=$(nproc)"

%install
# See: debian/clearwater-infrastructure.install
mkdir --parents %{buildroot}%{_initrddir}/
mkdir --parents %{buildroot}/etc/
mkdir --parents %{buildroot}/usr/
mkdir --parents %{buildroot}/usr/share/clearwater/infrastructure/eggs/
mkdir --parents %{buildroot}/usr/share/clearwater/bin/
mkdir --parents %{buildroot}/usr/share/clearwater/infrastructure/.wheelhouse/
cp --recursive clearwater-infrastructure/etc/* %{buildroot}/etc/
cp --recursive clearwater-infrastructure/usr/* %{buildroot}/usr/
install --mode=755 debian/clearwater-infrastructure.init.d %{buildroot}%{_initrddir}/clearwater-infrastructure
cp --recursive clearwater-infrastructure/PyZMQ/eggs/pyzmq* %{buildroot}/usr/share/clearwater/infrastructure/eggs/
cp build/bin/bracket-ipv6-address %{buildroot}/usr/share/clearwater/bin/
cp build/bin/ipv6-to-hostname %{buildroot}/usr/share/clearwater/bin/
cp build/bin/is-address-ipv6 %{buildroot}/usr/share/clearwater/bin/
cp build/bin/issue-alarm %{buildroot}/usr/share/clearwater/bin/
cp .wheelhouse/* %{buildroot}/usr/share/clearwater/infrastructure/.wheelhouse/

# See: debian/clearwater-memcached.install
mkdir --parents %{buildroot}/usr/share/clearwater/clearwater-cluster-manager/plugins/
install --mode=755 debian/clearwater-memcached.init.d %{buildroot}%{_initrddir}/clearwater-memcached
cp --recursive clearwater-memcached/* %{buildroot}/
sed --in-place s/invoke-rc.d/service/g %{buildroot}/usr/share/clearwater/infrastructure/install/clearwater-memcached.postinst # patch
cp modules/clearwater-etcd-plugins/clearwater_memcached/memcached_plugin.py %{buildroot}/usr/share/clearwater/clearwater-cluster-manager/plugins/
cp modules/clearwater-etcd-plugins/clearwater_memcached/memcached_utils.py %{buildroot}/usr/share/clearwater/clearwater-cluster-manager/plugins/
touch %{buildroot}/etc/memcached.conf # missing!

# See: debian/clearwater-tcp-scalability.install
cp --recursive clearwater-tcp-scalability/* %{buildroot}/

# See: debian/clearwater-secure-connections.install
install --mode=755 debian/clearwater-secure-connections.init.d %{buildroot}%{_initrddir}/clearwater-secure-connections
cp --recursive clearwater-secure-connections/* %{buildroot}/

# See: debian/clearwater-snmpd.install
cp --recursive clearwater-snmpd/* %{buildroot}/

# See: debian/clearwater-diags-monitor.install
install --mode=755 debian/clearwater-diags-monitor.init.d %{buildroot}%{_initrddir}/clearwater-diags-monitor
cp --recursive clearwater-diags-monitor/* %{buildroot}/

# See: debian/clearwater-socket-factory.install
mkdir --parents %{buildroot}/etc/init/
cp clearwater-socket-factory/clearwater_socket_factory %{buildroot}/usr/share/clearwater/bin/
cp clearwater-socket-factory/clearwater-socket-factory-common %{buildroot}/usr/share/clearwater/bin/
cp clearwater-socket-factory/clearwater-socket-factory-mgmt-wrapper %{buildroot}/usr/share/clearwater/bin/
cp clearwater-socket-factory/clearwater-socket-factory-sig-wrapper %{buildroot}/usr/share/clearwater/bin/
cp clearwater-socket-factory/clearwater-socket-factory-mgmt.conf %{buildroot}/etc/init/
cp clearwater-socket-factory/clearwater-socket-factory-sig.conf %{buildroot}/etc/init/

mkdir --parents %{buildroot}%{_unitdir}/
cp debian/clearwater-socket-factory-mgmt.service %{buildroot}%{_unitdir}/
cp debian/clearwater-socket-factory-sig.service %{buildroot}%{_unitdir}/

# See: debian/clearwater-auto-config-aws.install
mkdir --parents %{buildroot}/usr/share/clearwater-auto-config/bin/
install --mode=755 debian/clearwater-auto-config-aws.init.d %{buildroot}%{_initrddir}/clearwater-auto-config-aws
cp --recursive clearwater-auto-config/* %{buildroot}/
cp clearwater-infrastructure/usr/share/clearwater/infrastructure/install/common %{buildroot}/usr/share/clearwater-auto-config/bin/

# See: debian/clearwater-auto-config-docker.install
mkdir --parents %{buildroot}/usr/share/clearwater/clearwater-auto-config-docker/bin/
install --mode=755 debian/clearwater-auto-config-docker.init.d %{buildroot}%{_initrddir}/clearwater-auto-config-docker
cp --recursive clearwater-auto-config/* %{buildroot}/
cp build/bin/bracket-ipv6-address %{buildroot}/usr/share/clearwater/clearwater-auto-config-docker/bin/
cp build/bin/is-address-ipv6 %{buildroot}/usr/share/clearwater/clearwater-auto-config-docker/bin/

# See: debian/clearwater-auto-config-generic.install
mkdir --parents %{buildroot}/usr/share/clearwater/clearwater-auto-config-generic/bin/
install --mode=755 debian/clearwater-auto-config-generic.init.d %{buildroot}%{_initrddir}/clearwater-auto-config-generic
cp --recursive clearwater-auto-config/* %{buildroot}/
cp build/bin/bracket-ipv6-address %{buildroot}/usr/share/clearwater/clearwater-auto-config-generic/bin/
cp build/bin/is-address-ipv6 %{buildroot}/usr/share/clearwater/clearwater-auto-config-generic/bin/
cp clearwater-infrastructure/usr/share/clearwater/infrastructure/install/common %{buildroot}/usr/share/clearwater-auto-config/bin/

# See: debian/clearwater-log-cleanup.install
cp --recursive clearwater-log-cleanup/* %{buildroot}/

# See: clearwater-auto-upgrade
install --mode=755 debian/clearwater-auto-upgrade.init.d %{buildroot}%{_initrddir}/clearwater-auto-upgrade

# See: debian/clearwater-radius-auth.install
cp --recursive clearwater-radius-auth/* %{buildroot}/

# See: debian/velum.install
cp --recursive vellum/* %{buildroot}/

# See: debian/dime.install
cp --recursive dime/* %{buildroot}/

# TODO: /usr/share/clearwater/bin/clearwater-version is Debian-specific

%files
%{_initrddir}/clearwater-infrastructure
/usr/bin/clearwater-upgrade
/usr/share/clearwater/bin/alarms.py
/usr/share/clearwater/bin/clearwater-check-config
/usr/share/clearwater/bin/ent_log.py
/usr/share/clearwater/bin/reload_fallback_ifcs_xml
/usr/share/clearwater/bin/clearwater-version
/usr/share/clearwater/bin/poll-sip
/usr/share/clearwater/bin/restart_node_processes
/usr/share/clearwater/bin/check-uptime
/usr/share/clearwater/bin/generic_create_diameterconf
/usr/share/clearwater/bin/poll-http
/usr/share/clearwater/bin/clearwater-show-config
/usr/share/clearwater/bin/reload_dns_json
/usr/share/clearwater/bin/sync_alarms.py
/usr/share/clearwater/bin/process-stability
/usr/share/clearwater/bin/reload_shared_ifcs_xml
/usr/share/clearwater/bin/run-in-signaling-namespace
/usr/share/clearwater/bin/poll-tcp
/usr/share/clearwater/bin/cw-flag
/usr/share/clearwater/bin/stop_or_abort
/usr/share/clearwater/bin/set_ntp_server
/usr/share/clearwater/infrastructure/bin/bash.bashrc
/usr/share/clearwater/infrastructure/bin/set_snmp_community
/usr/share/clearwater/infrastructure/bin/set_log_level
/usr/share/clearwater/infrastructure/install/clearwater-infrastructure.prerm
/usr/share/clearwater/infrastructure/install/clearwater-infrastructure.postinst
/usr/share/clearwater/infrastructure/install/common
/usr/share/clearwater/infrastructure/migration-utils/migrate_local_config
/usr/share/clearwater/infrastructure/migration-utils/switch_to_migrated_config
/usr/share/clearwater/infrastructure/migration-utils/configlint.py*
/usr/share/clearwater/infrastructure/migration-utils/migrate_shared_config
/usr/share/clearwater/infrastructure/scripts/namespace
/usr/share/clearwater/infrastructure/scripts/sas_socket_factory
/usr/share/clearwater/infrastructure/scripts/1hosts
/usr/share/clearwater/infrastructure/scripts/hostname
/usr/share/clearwater/infrastructure/scripts/node_identity
/usr/share/clearwater/utils/cassandra_enabled
/usr/share/clearwater/utils/logging.bash
/usr/share/clearwater/utils/check-root-permissions
/usr/share/clearwater/utils/init-utils.bash
/usr/share/clearwater/infrastructure/eggs/
/usr/share/clearwater/bin/bracket-ipv6-address
/usr/share/clearwater/bin/ipv6-to-hostname
/usr/share/clearwater/bin/is-address-ipv6
/usr/share/clearwater/bin/issue-alarm
/usr/share/clearwater/infrastructure/.wheelhouse/
/etc/dnsmasq.d/dnsmasq.clearwater.conf
/etc/monit/run_logged
/etc/monit/conf.d/node.monit
%ghost /etc/clearwater/config

%files -n clearwater-memcached
%{_initrddir}/clearwater-memcached
/usr/share/clearwater/bin/poll_memcached.sh
/usr/share/clearwater/bin/reload_memcached_users
/usr/share/clearwater/infrastructure/alarms/memcached_alarms.json
/usr/share/clearwater/infrastructure/conf/memcached_11211.monit
/usr/share/clearwater/infrastructure/install/clearwater-memcached.postinst
/usr/share/clearwater/infrastructure/install/clearwater-memcached.prerm
/usr/share/clearwater/infrastructure/monit_uptime/check-memcached-uptime
/usr/share/clearwater/infrastructure/scripts/memcached
/usr/share/clearwater/node_type.d/90_memcached
/usr/share/clearwater/clearwater-cluster-manager/plugins/memcached_plugin.py*
/usr/share/clearwater/clearwater-cluster-manager/plugins/memcached_utils.py*
/etc/clearwater/secure-connections/memcached.conf
/etc/memcached.conf

%files -n clearwater-tcp-scalability
/usr/share/clearwater/infrastructure/install/clearwater-tcp-scalability.postinst
/usr/share/clearwater/infrastructure/install/clearwater-tcp-scalability.prerm
/etc/sysctl.conf.clearwater

%files -n clearwater-secure-connections
%{_initrddir}/clearwater-secure-connections
/usr/share/clearwater/infrastructure/install/clearwater-secure-connections.postinst
/usr/share/clearwater/infrastructure/install/clearwater-secure-connections.prerm
/etc/clearwater/secure-connections/plain-local.conf
/etc/racoon/racoon.conf.clearwater-secure-connections

%files -n clearwater-snmpd
/usr/share/clearwater/conf/snmpd.monit
/usr/share/clearwater/infrastructure/install/clearwater-snmpd.postinst
/usr/share/clearwater/infrastructure/install/clearwater-snmpd.prerm
/usr/share/clearwater/infrastructure/scripts/snmpd
/etc/snmp/snmpd.conf.clearwater-snmpd

%files -n clearwater-diags-monitor
%{_initrddir}/clearwater-diags-monitor
/usr/share/clearwater/bin/clearwater_diags_monitor
/usr/share/clearwater/bin/compress_core_file
/usr/share/clearwater/bin/gather_diags
/usr/share/clearwater/bin/gather_diags_and_report_location
/usr/share/clearwater/clearwater-diags-monitor/conf/clearwater-diags-monitor.monit
/usr/share/clearwater/infrastructure/install/clearwater-diags-monitor.postinst
/usr/share/clearwater/infrastructure/install/clearwater-diags-monitor.prerm
/etc/clearwater/diags-monitor/core_pattern
/etc/cron.d/clearwater-iotop
/etc/cron.d/clearwater-sysstat
/etc/logrotate.d/clearwater-diags-monitor
/etc/logrotate.d/clearwater-iotop

%files -n clearwater-socket-factory
/usr/share/clearwater/bin/clearwater_socket_factory
/usr/share/clearwater/bin/clearwater-socket-factory-common
/usr/share/clearwater/bin/clearwater-socket-factory-mgmt-wrapper
/usr/share/clearwater/bin/clearwater-socket-factory-sig-wrapper
%{_unitdir}/clearwater-socket-factory-mgmt.service
%{_unitdir}/clearwater-socket-factory-sig.service
/etc/init/clearwater-socket-factory-mgmt.conf
/etc/init/clearwater-socket-factory-sig.conf

%files -n clearwater-auto-config-aws
%{_initrddir}/clearwater-auto-config-aws
/usr/share/clearwater-auto-config/bin/init-functions
/usr/share/clearwater-auto-config/bin/common
/etc/clearwater/local_config
/etc/clearwater/shared_config

%files -n clearwater-auto-config-docker
%{_initrddir}/clearwater-auto-config-docker
/usr/share/clearwater-auto-config/bin/init-functions
/usr/share/clearwater/clearwater-auto-config-docker/bin/bracket-ipv6-address
/usr/share/clearwater/clearwater-auto-config-docker/bin/is-address-ipv6
/etc/clearwater/local_config
/etc/clearwater/shared_config

%files -n clearwater-auto-config-generic
%{_initrddir}/clearwater-auto-config-generic
/usr/share/clearwater-auto-config/bin/init-functions
/usr/share/clearwater/clearwater-auto-config-generic/bin/bracket-ipv6-address
/usr/share/clearwater/clearwater-auto-config-generic/bin/is-address-ipv6
/usr/share/clearwater-auto-config/bin/common
/etc/clearwater/local_config
/etc/clearwater/shared_config

%files -n clearwater-log-cleanup
/usr/share/clearwater/bin/log_cleanup.py*

%files -n clearwater-auto-upgrade
%{_initrddir}/clearwater-auto-upgrade

%files -n clearwater-radius-auth
/usr/share/clearwater/infrastructure/scripts/clearwater-radius-auth
/usr/share/clearwater-radius-auth/bin/disable-radius-authentication
/usr/share/clearwater-radius-auth/bin/enable-radius-authentication
/etc/libnss-ato.conf.TEMPLATE

%files -n clearwater-vellum
/usr/share/clearwater/node_type.d/10_vellum

%files -n clearwater-dime
/usr/share/clearwater/node_type.d/10_dime

%post
# See: debian/clearwater-infrastructure.links
set -e
ln --symbolic /usr/share/clearwater/bin/gather_diags /usr/bin/cw-gather_diags
ln --symbolic /usr/share/clearwater/bin/gather_diags_and_report_location /usr/bin/cw-gather_diags_and_report_location
ln --symbolic /usr/share/clearwater/bin/sync_alarms.py /usr/bin/cw-sync_alarms
ln --symbolic /usr/share/clearwater/bin/restart_node_processes /usr/bin/cw-restart_node_processes
ln --symbolic /usr/share/clearwater/bin/run-in-signaling-namespace /usr/sbin/cw-run_in_signaling_namespace
ln --symbolic /usr/share/clearwater/infrastructure/bin/set_snmp_community /usr/sbin/cw-set_snmp_community
ln --symbolic /usr/share/clearwater/infrastructure/bin/set_log_level /usr/sbin/cw-set_log_level
ln --symbolic /usr/share/clearwater/bin/clearwater-check-config /usr/sbin/cw-check_config
ln --symbolic /usr/share/clearwater/bin/clearwater-check-config /usr/sbin/clearwater-check-config
ln --symbolic /usr/share/clearwater/bin/clearwater-show-config /usr/sbin/cw-show_config
ln --symbolic /usr/share/clearwater/bin/clearwater-show-config /usr/sbin/clearwater-show-config

# See: debian/clearwater-infrastructure.postinst
sudo -H easy_install virtualenv
/usr/share/clearwater/infrastructure/install/clearwater-infrastructure.postinst

%preun
# See: debian/clearwater-infrastructure.prerm
set -e
/usr/share/clearwater/infrastructure/install/clearwater-infrastructure.prerm

rm --force /usr/bin/cw-gather_diags
rm --force /usr/bin/cw-gather_diags_and_report_location
rm --force /usr/bin/cw-sync_alarms
rm --force /usr/bin/cw-restart_node_processes
rm --force /usr/sbin/cw-run_in_signaling_namespace
rm --force /usr/sbin/cw-set_snmp_community
rm --force /usr/sbin/cw-set_log_level
rm --force /usr/sbin/cw-check_config
rm --force /usr/sbin/clearwater-check-config
rm --force /usr/sbin/cw-show_config
rm --force /usr/sbin/clearwater-show-config

%post -n clearwater-memcached
# See: debian/clearwater-memached.postinst
set -e
/usr/share/clearwater/infrastructure/install/clearwater-memcached.postinst

%preun -n clearwater-memcached
# See: debian/clearwater-memached.prerm
set -e
/usr/share/clearwater/infrastructure/install/clearwater-memcached.prerm

%post -n clearwater-tcp-scalability
# See: debian/clearwater-tcp-scalability.postinst
set -e
/usr/share/clearwater/infrastructure/install/clearwater-tcp-scalability.postinst

%preun -n clearwater-tcp-scalability
# See: debian/clearwater-tcp-scalability.prerm
set -e
/usr/share/clearwater/infrastructure/install/clearwater-tcp-scalability.prerm

%post -n clearwater-secure-connections
# See: debian/clearwater-secure-connections.postinst
set -e
/usr/share/clearwater/infrastructure/install/clearwater-secure-connections.postinst

%preun -n clearwater-secure-connections
# See: debian/clearwater-secure-connections.prerm
set -e
/usr/share/clearwater/infrastructure/install/clearwater-secure-connections.prerm

%post -n clearwater-snmpd
# See: debian/clearwater-snmpd.postinst
set -e
/usr/share/clearwater/infrastructure/install/clearwater-snmpd.postinst

%preun -n clearwater-snmpd
# See: debian/clearwater-snmpd.prerm
set -e
/usr/share/clearwater/infrastructure/install/clearwater-snmpd.prerm

%post -n clearwater-diags-monitor
# See: debian/clearwater-diags-monitor.postinst
set -e
cp --preserve /etc/default/sysstat /etc/clearwater/diags-monitor/sysstat.old
sed --in-place 's/ENABLED=.*/ENABLED="true"/g' /etc/default/sysstat
/usr/share/clearwater/infrastructure/install/clearwater-diags-monitor.postinst

%preun -n clearwater-diags-monitor
# See: debian/clearwater-diags-monitor.prerm
set -e
[ ! -f /etc/clearwater/diags-monitor/sysstat.old ] || cp --preserve /etc/clearwater/diags-monitor/sysstat.old /etc/default/sysstat
rm --force /etc/clearwater/diags-monitor/sysstat.old
/usr/share/clearwater/infrastructure/install/clearwater-diags-monitor.prerm

%post -n clearwater-socket-factory
# See: debian/clearwater-socket-factory.postinst
set -e
service clearwater-socket-factory-mgmt start || /bin/true
service clearwater-socket-factory-sig start || /bin/true
%systemd_post socket-factory-mgmt.service
%systemd_post socket-factory-sig.service

%preun -n clearwater-socket-factory
# See: debian/clearwater-socket-factory.prerm
set -e
service clearwater-socket-factory-mgmt stop || /bin/true
service clearwater-socket-factory-sig stop || /bin/true
rm --force /tmp/clearwater_mgmt_namespace_socket
%systemd_preun socket-factory-mgmt.service
%systemd_preun socket-factory-sig.service

%postun -n clearwater-socket-factory
%systemd_postun_with_restart asocket-factory-mgmt.service
%systemd_postun_with_restart asocket-factory-sig.service
