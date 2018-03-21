Name:          clearwater-etcd
Version:       129
Release:       1%{?dist}
License:       GPLv3+
URL:           https://github.com/Metaswitch/clearwater-etcd

Source0:       %{name}-%{version}.tar.bz2
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

%package -n clearwater-queue-manager
Summary:       Clearwater - Queue Manager
Requires:      clearwater-etcd clearwater-monit
Requires:      python-virtualenv python2-pip libffi

%package -n clearwater-config-manager
Summary:       Clearwater - Config Manager
Requires:      clearwater-etcd clearwater-queue-manager clearwater-monit
Requires:      python-virtualenv python2-pip python2-requests python2-jsonschema libffi

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
make env

%install
# See: debian/clearwater-etcd.install
cp --recursive clearwater-etcd/* %{buildroot}/

# See: debian/clearwater-cluster-manager.install
mkdir --parents %{buildroot}/usr/share/clearwater/clearwater-cluster-manager/wheelhouse/
cp cluster_mgr_wheelhouse/* %{buildroot}/usr/share/clearwater/clearwater-cluster-manager/wheelhouse/
cp --recursive clearwater-cluster-manager.root/* %{buildroot}/

# See: debian/clearwater-queue-manager.install
mkdir --parents %{buildroot}/usr/share/clearwater/clearwater-queue-manager/wheelhouse/
mkdir --parents %{buildroot}/usr/share/clearwater/clearwater-queue-manager/plugins/
cp queue_mgr_wheelhouse/* %{buildroot}/usr/share/clearwater/clearwater-queue-manager/wheelhouse/
cp --recursive clearwater-queue-manager.root/* %{buildroot}/
cp src/clearwater_etcd_plugins/clearwater_queue_manager/apply_config_plugin.py %{buildroot}/usr/share/clearwater/clearwater-queue-manager/plugins/

# See: debian/clearwater-config-manager.install
mkdir --parents %{buildroot}/usr/share/clearwater/clearwater-config-manager/wheelhouse/
mkdir --parents %{buildroot}/usr/share/clearwater/clearwater-config-manager/plugins/
mkdir --parents %{buildroot}/usr/share/clearwater/clearwater-config-access/plugins/
cp config_mgr_wheelhouse/* %{buildroot}/usr/share/clearwater/clearwater-config-manager/wheelhouse/
cp --recursive clearwater-config-manager.root/* %{buildroot}/
cp src/clearwater_etcd_plugins/clearwater_config_manager/shared_config_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-manager/plugins/
cp src/clearwater_etcd_plugins/clearwater_config_manager/dns_json_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-manager/plugins/
cp src/clearwater_etcd_plugins/clearwater_config_access/shared_config_config_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-access/plugins/
cp src/clearwater_etcd_plugins/clearwater_config_access/dns_json_config_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-access/plugins/

%files
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

%post
# See: debian/clearwater-etcs.postinst
set -e
if ! grep -q "^clearwater-etcd:" /etc/passwd; then
  useradd --system --no-create-home --home-dir /nonexistent --shell /bin/false clearwater-etcd
fi
mkdir --parents /var/lib/clearwater-etcd/
chown --recursive clearwater-etcd /var/lib/clearwater-etcd/
mkdir --parents /var/log/clearwater-etcd/
chown --recursive clearwater-etcd /var/log/clearwater-etcd/
install --mode=0644 /usr/share/clearwater/conf/clearwater-etcd.monit /etc/monit/conf.d/
service clearwater-monit reload || /bin/true
service clearwater-etcd stop || /bin/true
rm --force /var/run/clearwater-etcd.pid
rm --force /tmp/.clearwater_etcd_alarm_issued

%preun
# See: debian/clearwater-etcs.prerm
set -e
rm --force /etc/monit/conf.d/clearwater-etcd.monit
service clearwater-monit reload || /bin/true
service clearwater-etcd stop || /bin/true
if [ "$1" = 0 ]; then # Uninstall
  if grep -q "^clearwater-etcd:" /etc/passwd; then
    userdel clearwater-etcd
  fi
  rm --recursive --force /var/log/clearwater-etcd/
  rm --recursive --force /var/lib/clearwater-etcd/
  rm --force /tmp/.clearwater_etcd_alarm_issued
  rm --force /tmp/.clearwater_etcd_alarm_to_raise
fi

%post -n clearwater-cluster-manager
# See: debian/clearwater-cluster-manager.links
set -e
ln --symbolic /usr/share/clearwater/clearwater-cluster-manager/scripts/check_cluster_state /usr/bin/cw-check_cluster_state
ln --symbolic /usr/share/clearwater/clearwater-cluster-manager/scripts/mark_node_failed /usr/sbin/cw-mark_node_failed

# See: debian/clearwater-cluster-manager.postinst
# TODO

%preun -n clearwater-cluster-manager
# See: debian/clearwater-cluster-manager.prerm
set -e
# TODO

rm --force /usr/bin/cw-check_cluster_state
rm --force /usr/sbin/cw-mark_node_failed

%post -n clearwater-queue-manager
# See: debian/clearwater-queue-manager.links
set -e
ln --symbolic /usr/share/clearwater/clearwater-queue-manager/scripts/check_restart_queue_state /usr/bin/cw-check_restart_queue_state

# See: debian/clearwater-queue-manager.postinst
# TODO

%preun -n clearwater-queue-manager
# See: debian/clearwater-queue-manager.prerm
set -e
# TODO

rm --force /usr/bin/cw-check_restart_queue_state

%post -n clearwater-config-manager
# See: debian/clearwater-config-manager.links
set -e
ln --symbolic /usr/share/clearwater/clearwater-config-manager/scripts/cw-config /usr/bin/cw-config
ln --symbolic /usr/share/clearwater/clearwater-config-manager/scripts/restore_config /usr/bin/cw-restore_config
ln --symbolic /usr/share/clearwater/clearwater-config-manager/scripts/check_config_sync /usr/sbin/cw-check_config_sync
ln --symbolic /usr/share/clearwater/clearwater-config-manager/scripts/backup_config /usr/sbin/cw-backup_config

# See: debian/clearwater-config-manager.postinst
# TODO

%preun -n clearwater-config-manager
# See: debian/clearwater-config-manager.prerm
set -e
# TODO

rm --force /usr/bin/cw-config
rm --force /usr/bin/cw-restore_config
rm --force /usr/sbin/cw-check_config_sync
rm --force /usr/sbin/cw-backup_config
