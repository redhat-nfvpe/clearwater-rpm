Name:          clearwater-etcd
Version:       129
Release:       1%{?dist}
License:       GPLv3+
URL:           https://github.com/Metaswitch/clearwater-etcd

Source0:       %{name}-%{version}.tar.bz2
Source1:       common.sh
BuildRequires: make python-virtualenv git gcc-c++
BuildRequires: libffi-devel

%global debug_package %{nil}

Summary:       Clearwater - etcd
Requires:      clearwater-infrastructure clearwater-monit clearwater-log-cleanup
Requires:      python2-pip libffi

%package -n clearwater-cluster-manager
Summary:       Clearwater - Cluster Manager
Requires:      clearwater-etcd clearwater-monit
Requires:      python-virtualenv python2-pip libffi
AutoReq:       no

%package -n clearwater-queue-manager
Summary:       Clearwater - Queue Manager
Requires:      clearwater-etcd clearwater-monit
Requires:      python-virtualenv python2-pip libffi
AutoReq:       no

%package -n clearwater-config-manager
Summary:       Clearwater - Config Manager
Requires:      clearwater-etcd clearwater-queue-manager clearwater-monit
Requires:      python-virtualenv python2-pip python2-requests python2-jsonschema libffi
AutoReq:       no

%description
etcd configured for Clearwater

%description -n clearwater-cluster-manager
cluster manager

%description -n clearwater-queue-manager
queue manager

%description -n clearwater-config-manager
config manager

%prep
%setup

%build
make env MAKE="make --jobs $(nproc)"

%install
# See: debian/clearwater-etcd.install
mkdir --parents %{buildroot}%{_initrddir}/
cp debian/clearwater-etcd.init.d %{buildroot}%{_initrddir}/clearwater-etcd
cp --recursive clearwater-etcd/* %{buildroot}/

# See: debian/clearwater-cluster-manager.install
mkdir --parents %{buildroot}/usr/share/clearwater/clearwater-cluster-manager/wheelhouse/
cp debian/clearwater-cluster-manager.init.d %{buildroot}%{_initrddir}/clearwater-cluster-manager
cp cluster_mgr_wheelhouse/* %{buildroot}/usr/share/clearwater/clearwater-cluster-manager/wheelhouse/
cp --recursive clearwater-cluster-manager.root/* %{buildroot}/

# See: debian/clearwater-queue-manager.install
mkdir --parents %{buildroot}/usr/share/clearwater/clearwater-queue-manager/wheelhouse/
mkdir --parents %{buildroot}/usr/share/clearwater/clearwater-queue-manager/plugins/
cp debian/clearwater-queue-manager.init.d %{buildroot}%{_initrddir}/clearwater-queue-manager
cp queue_mgr_wheelhouse/* %{buildroot}/usr/share/clearwater/clearwater-queue-manager/wheelhouse/
cp --recursive clearwater-queue-manager.root/* %{buildroot}/
cp src/clearwater_etcd_plugins/clearwater_queue_manager/apply_config_plugin.py %{buildroot}/usr/share/clearwater/clearwater-queue-manager/plugins/

# See: debian/clearwater-config-manager.install
mkdir --parents %{buildroot}/usr/share/clearwater/clearwater-config-manager/wheelhouse/
mkdir --parents %{buildroot}/usr/share/clearwater/clearwater-config-manager/plugins/
mkdir --parents %{buildroot}/usr/share/clearwater/clearwater-config-access/plugins/
cp debian/clearwater-config-manager.init.d %{buildroot}%{_initrddir}/clearwater-config-manager
cp config_mgr_wheelhouse/* %{buildroot}/usr/share/clearwater/clearwater-config-manager/wheelhouse/
cp --recursive clearwater-config-manager.root/* %{buildroot}/
cp src/clearwater_etcd_plugins/clearwater_config_manager/shared_config_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-manager/plugins/
cp src/clearwater_etcd_plugins/clearwater_config_manager/dns_json_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-manager/plugins/
cp src/clearwater_etcd_plugins/clearwater_config_access/shared_config_config_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-access/plugins/
cp src/clearwater_etcd_plugins/clearwater_config_access/dns_json_config_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-access/plugins/

%files
%{_initrddir}/clearwater-etcd
/usr/bin/clearwater-etcdctl
/usr/share/clearwater/bin/poll_etcd.sh
/usr/share/clearwater/bin/get_etcd_initial_cluster.py*
/usr/share/clearwater/bin/poll_etcd_cluster.sh
/usr/share/clearwater/bin/raise_etcd_cluster_alarm.sh
/usr/share/clearwater/clearwater-etcd/scripts/save_etcd_config.py*
/usr/share/clearwater/clearwater-etcd/scripts/wait_for_etcd
/usr/share/clearwater/clearwater-etcd/scripts/load_etcd_config.py*
/usr/share/clearwater/clearwater-etcd/scripts/load_etcd_config
/usr/share/clearwater/clearwater-etcd/scripts/save_etcd_config
/usr/share/clearwater/clearwater-etcd/2.2.5/etcd-dump-logs
/usr/share/clearwater/clearwater-etcd/2.2.5/etcdctl
/usr/share/clearwater/clearwater-etcd/2.2.5/etcdwrapper
/usr/share/clearwater/clearwater-etcd/2.2.5/etcd
/usr/share/clearwater/clearwater-etcd/3.1.7/etcd-dump-logs
/usr/share/clearwater/clearwater-etcd/3.1.7/etcdctl
/usr/share/clearwater/clearwater-etcd/3.1.7/etcdwrapper
/usr/share/clearwater/clearwater-etcd/3.1.7/etcd
/usr/share/clearwater/infrastructure/alarms/clearwater_etcd_alarms.json
/usr/share/clearwater/infrastructure/monit_uptime/check-etcd-uptime
%config /usr/share/clearwater/conf/clearwater-etcd.monit
%config /etc/logrotate.d/clearwater-etcd

%files -n clearwater-cluster-manager
%{_initrddir}/clearwater-cluster-manager
/usr/share/clearwater/clearwater-cluster-manager/wheelhouse/
/usr/share/clearwater/bin/clearwater-cluster-manager
/usr/share/clearwater/infrastructure/scripts/restart/clearwater_cluster_manager_restart
/usr/share/clearwater/infrastructure/alarms/clearwater_cluster_manager_alarms.json
/usr/share/clearwater/clearwater-cluster-manager/scripts/recreate_homestead_cluster
/usr/share/clearwater/clearwater-cluster-manager/scripts/mark_remote_node_failed
/usr/share/clearwater/clearwater-cluster-manager/scripts/load_from_chronos_cluster
/usr/share/clearwater/clearwater-cluster-manager/scripts/load_from_chronos_cluster.py*
/usr/share/clearwater/clearwater-cluster-manager/scripts/mark_node_failed.py*
/usr/share/clearwater/clearwater-cluster-manager/scripts/load_from_cassandra_cluster.py*
/usr/share/clearwater/clearwater-cluster-manager/scripts/mark_node_failed
/usr/share/clearwater/clearwater-cluster-manager/scripts/force_etcd_state
/usr/share/clearwater/clearwater-cluster-manager/scripts/recreate_cluster.py*
/usr/share/clearwater/clearwater-cluster-manager/scripts/load_from_memcached_cluster.py*
/usr/share/clearwater/clearwater-cluster-manager/scripts/dump_etcd_state
/usr/share/clearwater/clearwater-cluster-manager/scripts/recreate_sprout_cluster
/usr/share/clearwater/clearwater-cluster-manager/scripts/dump_etcd_state.py*
/usr/share/clearwater/clearwater-cluster-manager/scripts/load_from_memcached_cluster
/usr/share/clearwater/clearwater-cluster-manager/scripts/load_from_cassandra_cluster
/usr/share/clearwater/clearwater-cluster-manager/scripts/check_cluster_state
/usr/share/clearwater/clearwater-cluster-manager/scripts/check_cluster_state.py*
/usr/share/clearwater/clearwater-cluster-manager/scripts/force_etcd_state.py*
%config /usr/share/clearwater/conf/clearwater-cluster-manager.monit
%config /etc/logrotate.d/clearwater-cluster-manager
%config /etc/cron.hourly/clearwater-cluster-manager-log-cleanup

%files -n clearwater-queue-manager
%{_initrddir}/clearwater-queue-manager
/usr/share/clearwater/clearwater-queue-manager/wheelhouse/
/usr/share/clearwater/clearwater-queue-manager/plugins/apply_config_plugin.py*
/usr/share/clearwater/bin/clearwater-queue-manager
/usr/share/clearwater/infrastructure/alarms/clearwater_queue_manager_alarms.json
/usr/share/clearwater/infrastructure/monit_uptime/check-queue-manager-uptime
/usr/share/clearwater/clearwater-queue-manager/scripts/get_apply_config_key
/usr/share/clearwater/clearwater-queue-manager/scripts/modify_nodes_in_queue
/usr/share/clearwater/clearwater-queue-manager/scripts/check_restart_queue_state
/usr/share/clearwater/clearwater-queue-manager/scripts/force_restart_queue_state
/usr/share/clearwater/clearwater-queue-manager/scripts/force_queue_state.py*
/usr/share/clearwater/clearwater-queue-manager/scripts/check_node_health.py*
/usr/share/clearwater/clearwater-queue-manager/scripts/check_queue_state.py*
/usr/share/clearwater/clearwater-queue-manager/scripts/modify_nodes_in_queue.py*
%config /usr/share/clearwater/conf/clearwater-queue-manager.monit
%config /etc/cron.hourly/clearwater-queue-manager-log-cleanup

%files -n clearwater-config-manager
%{_initrddir}/clearwater-config-manager
/usr/share/clearwater/clearwater-config-manager/wheelhouse/
/usr/share/clearwater/clearwater-config-manager/plugins/shared_config_plugin.py*
/usr/share/clearwater/clearwater-config-manager/plugins/dns_json_plugin.py*
/usr/share/clearwater/clearwater-config-access/plugins/shared_config_config_plugin.py*
/usr/share/clearwater/clearwater-config-access/plugins/dns_json_config_plugin.py*
/usr/share/clearwater/bin/clearwater-config-manager
/usr/share/clearwater/infrastructure/alarms/clearwater_config_manager_alarms.json
/usr/share/clearwater/clearwater-config-manager/scripts/print-dns-configuration
/usr/share/clearwater/clearwater-config-manager/scripts/cw-config
/usr/share/clearwater/clearwater-config-manager/scripts/upload_generic_json
/usr/share/clearwater/clearwater-config-manager/scripts/validate_json.py*
/usr/share/clearwater/clearwater-config-manager/scripts/check_config_sync.py*
/usr/share/clearwater/clearwater-config-manager/scripts/check_config_sync
/usr/share/clearwater/clearwater-config-manager/scripts/restore_config
/usr/share/clearwater/clearwater-config-manager/scripts/backup_config
/usr/share/clearwater/clearwater-config-manager/scripts/config_validation/dns_schema.json
/usr/share/clearwater/clearwater-config-manager/scripts/print-s-cscf-configuration
/usr/share/clearwater/clearwater-config-manager/scripts/print-enum-configuration
%config /usr/share/clearwater/conf/clearwater-config-manager.monit
%config /etc/rsyslog.d/35-config-manager.conf
%config /etc/logrotate.d/clearwater-config-manager
%config /etc/cron.hourly/clearwater-config-manager-log-cleanup

%post -p /bin/bash
%include %{SOURCE1}
# See: debian/clearwater-etcd.postinst
cw-create-user clearwater-etcd
cw-create-log-dir clearwater-etcd
cw-start clearwater-etcd

%preun -p /bin/bash
%include %{SOURCE1}
# See: debian/clearwater-etcd.prerm
cw-stop clearwater-etcd
if [ "$1" = 0 ]; then # Uninstall
  cw-remove-user clearwater-etcd
  cw-remove-log-dir clearwater-etcd
  cw-remove-run-dir clearwater-etcd
fi

%post -n clearwater-cluster-manager -p /bin/bash
%include %{SOURCE1}
# See: debian/clearwater-cluster-manager.links
ln --symbolic /usr/share/clearwater/clearwater-cluster-manager/scripts/check_cluster_state /usr/bin/cw-check_cluster_state
ln --symbolic /usr/share/clearwater/clearwater-cluster-manager/scripts/mark_node_failed /usr/sbin/cw-mark_node_failed

# See: debian/clearwater-cluster-manager.postinst
cw-create-user clearwater-cluster-manager
cw-create-log-dir clearwater-cluster-manager adm
cw-create-virtualenv clearwater-cluster-manager
cw-start clearwater-cluster-manager

%preun -n clearwater-cluster-manager -p /bin/bash
%include %{SOURCE1}
# See: debian/clearwater-cluster-manager.prerm
cw-stop clearwater-cluster-manager
cw-remove-virtualenv clearwater-cluster-manager
if [ "$1" = 0 ]; then # Uninstall
  cw-remove-user clearwater-cluster-manager
  cw-remove-log-dir clearwater-cluster-manager
  cw-remove-run-dir clearwater-cluster-manager
fi

rm --force /usr/bin/cw-check_cluster_state
rm --force /usr/sbin/cw-mark_node_failed

%post -n clearwater-queue-manager -p /bin/bash
%include %{SOURCE1}
# See: debian/clearwater-queue-manager.links
ln --symbolic /usr/share/clearwater/clearwater-queue-manager/scripts/check_restart_queue_state /usr/bin/cw-check_restart_queue_state

# See: debian/clearwater-queue-manager.postinst
cw-create-user clearwater-queue-manager
cw-create-log-dir clearwater-queue-manager adm
cw-create-virtualenv clearwater-queue-manager
cw-start clearwater-queue-manager

%preun -n clearwater-queue-manager -p /bin/bash
%include %{SOURCE1}
# See: debian/clearwater-queue-manager.prerm
cw-stop clearwater-queue-manager
cw-remove-virtualenv clearwater-queue-manager
if [ "$1" = 0 ]; then # Uninstall
  cw-remove-user clearwater-queue-manager
  cw-remove-log-dir clearwater-queue-manager
  cw-remove-run-dir clearwater-queue-manager
fi

rm --force /usr/bin/cw-check_restart_queue_state

%post -n clearwater-config-manager -p /bin/bash
%include %{SOURCE1}
# See: debian/clearwater-config-manager.links
ln --symbolic /usr/share/clearwater/clearwater-config-manager/scripts/cw-config /usr/bin/cw-config
ln --symbolic /usr/share/clearwater/clearwater-config-manager/scripts/restore_config /usr/bin/cw-restore_config
ln --symbolic /usr/share/clearwater/clearwater-config-manager/scripts/check_config_sync /usr/sbin/cw-check_config_sync
ln --symbolic /usr/share/clearwater/clearwater-config-manager/scripts/backup_config /usr/sbin/cw-backup_config

# See: debian/clearwater-config-manager.postinst
cw-create-user clearwater-config-manager
cw-create-log-dir clearwater-config-manager adm
cw-create-virtualenv clearwater-config-manager
cw-start clearwater-config-manager

%preun -n clearwater-config-manager -p /bin/bash
%include %{SOURCE1}
# See: debian/clearwater-config-manager.prerm
cw-stop clearwater-config-manager
cw-remove-virtualenv clearwater-config-manager
if [ "$1" = 0 ]; then # Uninstall
  cw-remove-user clearwater-config-manager
  cw-remove-log-dir clearwater-config-manager
  cw-remove-run-dir clearwater-config-manager
fi

rm --force /usr/bin/cw-config
rm --force /usr/bin/cw-restore_config
rm --force /usr/sbin/cw-check_config_sync
rm --force /usr/sbin/cw-backup_config
