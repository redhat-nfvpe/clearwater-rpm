Name:          clearwater-etcd
Version:       129
Release:       1%{?dist}
License:       GPLv3+
URL:           https://github.com/Metaswitch/clearwater-etcd

Source0:       %{name}-%{version}.tar.bz2
Source1:       common.sh
Source2:       clearwater-etcd.service
Source3:       clearwater-etcd.sh
Source4:       clearwater-cluster-manager.service
Source5:       clearwater-cluster-manager.sh
Source6:       clearwater-queue-manager.service
Source7:       clearwater-queue-manager.sh
Source8:       clearwater-config-manager.service
Source9:       clearwater-config-manager.sh

BuildRequires: make python-virtualenv git gcc-c++ ccache
BuildRequires: libffi-devel
BuildRequires: systemd

%global debug_package %{nil}

Summary:       Clearwater - etcd
AutoReq:       no
%{?systemd_requires}
#Requires:      clearwater-infrastructure clearwater-monit clearwater-log-cleanup

%package -n clearwater-cluster-manager
Summary:       Clearwater - Cluster Manager
Requires:      python-virtualenv libffi
AutoReq:       no
%{?systemd_requires}
#Requires:      clearwater-etcd clearwater-monit

%package -n clearwater-queue-manager
Summary:       Clearwater - Queue Manager
Requires:      python-virtualenv libffi
AutoReq:       no
%{?systemd_requires}
#Requires:      clearwater-etcd clearwater-monit

%package -n clearwater-config-manager
Summary:       Clearwater - Config Manager
Requires:      python-virtualenv libffi
AutoReq:       no
%{?systemd_requires}
#Requires:      python2-pip python2-requests python2-jsonschema
#Requires:      clearwater-etcd clearwater-queue-manager clearwater-monit

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
make env MAKE="make --jobs=$(nproc)"

%install
mkdir --parents %{buildroot}%{_unitdir}/
mkdir --parents %{buildroot}/lib/systemd/scripts/
install --mode=644 %{SOURCE2} %{buildroot}%{_unitdir}/clearwater-etcd.service
install --mode=755 %{SOURCE3} %{buildroot}/lib/systemd/scripts/clearwater-etcd.sh
install --mode=644 %{SOURCE4} %{buildroot}%{_unitdir}/clearwater-cluster-manager.service
install --mode=755 %{SOURCE5} %{buildroot}/lib/systemd/scripts/clearwater-cluster-manager.sh
install --mode=644 %{SOURCE6} %{buildroot}%{_unitdir}/clearwater-queue-manager.service
install --mode=755 %{SOURCE7} %{buildroot}/lib/systemd/scripts/clearwater-queue-manager.sh
install --mode=644 %{SOURCE8} %{buildroot}%{_unitdir}/clearwater-config-manager.service
install --mode=755 %{SOURCE9} %{buildroot}/lib/systemd/scripts/clearwater-config-manager.sh

#mkdir --parents %{buildroot}%{_initrddir}/
#install --mode=755 debian/clearwater-etcd.init.d %{buildroot}%{_initrddir}/clearwater-etcd
#install --mode=755 debian/clearwater-cluster-manager.init.d %{buildroot}%{_initrddir}/clearwater-cluster-manager
#install --mode=755 debian/clearwater-queue-manager.init.d %{buildroot}%{_initrddir}/clearwater-queue-manager
#install --mode=755 debian/clearwater-config-manager.init.d %{buildroot}%{_initrddir}/clearwater-config-manager

# See: debian/clearwater-etcd.install
cp --recursive clearwater-etcd/* %{buildroot}/

# See: debian/clearwater-cluster-manager.install
mkdir --parents %{buildroot}/usr/share/clearwater/clearwater-cluster-manager/.wheelhouse/
cp cluster_mgr_wheelhouse/* %{buildroot}/usr/share/clearwater/clearwater-cluster-manager/.wheelhouse/
cp --recursive clearwater-cluster-manager.root/* %{buildroot}/

# See: debian/clearwater-queue-manager.install
mkdir --parents %{buildroot}/usr/share/clearwater/clearwater-queue-manager/.wheelhouse/
mkdir --parents %{buildroot}/usr/share/clearwater/clearwater-queue-manager/plugins/
cp queue_mgr_wheelhouse/* %{buildroot}/usr/share/clearwater/clearwater-queue-manager/.wheelhouse/
cp --recursive clearwater-queue-manager.root/* %{buildroot}/
cp src/clearwater_etcd_plugins/clearwater_queue_manager/apply_config_plugin.py %{buildroot}/usr/share/clearwater/clearwater-queue-manager/plugins/

# See: debian/clearwater-config-manager.install
mkdir --parents %{buildroot}/usr/share/clearwater/clearwater-config-manager/.wheelhouse/
mkdir --parents %{buildroot}/usr/share/clearwater/clearwater-config-manager/plugins/
mkdir --parents %{buildroot}/usr/share/clearwater/clearwater-config-access/plugins/
cp config_mgr_wheelhouse/* %{buildroot}/usr/share/clearwater/clearwater-config-manager/.wheelhouse/
cp --recursive clearwater-config-manager.root/* %{buildroot}/
cp src/clearwater_etcd_plugins/clearwater_config_manager/shared_config_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-manager/plugins/
cp src/clearwater_etcd_plugins/clearwater_config_manager/dns_json_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-manager/plugins/
cp src/clearwater_etcd_plugins/clearwater_config_access/shared_config_config_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-access/plugins/
cp src/clearwater_etcd_plugins/clearwater_config_access/dns_json_config_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-access/plugins/

%files
%{_unitdir}/clearwater-etcd.service
/lib/systemd/scripts/clearwater-etcd.sh
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
/usr/share/clearwater/conf/clearwater-etcd.monit
/etc/logrotate.d/clearwater-etcd

%files -n clearwater-cluster-manager
%{_unitdir}/clearwater-cluster-manager.service
/lib/systemd/scripts/clearwater-cluster-manager.sh
/usr/share/clearwater/clearwater-cluster-manager/.wheelhouse/
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
/usr/share/clearwater/conf/clearwater-cluster-manager.monit
/etc/logrotate.d/clearwater-cluster-manager
/etc/cron.hourly/clearwater-cluster-manager-log-cleanup
%ghost /usr/share/clearwater/clearwater-cluster-manager/env/

%files -n clearwater-queue-manager
%{_unitdir}/clearwater-queue-manager.service
/lib/systemd/scripts/clearwater-queue-manager.sh
/usr/share/clearwater/clearwater-queue-manager/.wheelhouse/
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
/usr/share/clearwater/conf/clearwater-queue-manager.monit
/etc/cron.hourly/clearwater-queue-manager-log-cleanup
%ghost /usr/share/clearwater/clearwater-queue-manager/env/

%files -n clearwater-config-manager
%{_unitdir}/clearwater-config-manager.service
/lib/systemd/scripts/clearwater-config-manager.sh
/usr/share/clearwater/clearwater-config-manager/.wheelhouse/
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
/usr/share/clearwater/conf/clearwater-config-manager.monit
/etc/rsyslog.d/35-config-manager.conf
/etc/logrotate.d/clearwater-config-manager
/etc/cron.hourly/clearwater-config-manager-log-cleanup
%ghost /usr/share/clearwater/clearwater-config-manager/env/

%post -p /bin/bash
%include %{SOURCE1}
# See: debian/clearwater-etcd.postinst
cw-create-user clearwater-etcd
cw-create-log-dir clearwater-etcd
%systemd_post clearwater-etcd.service
cw-start clearwater-etcd

%preun -p /bin/bash
%include %{SOURCE1}
# See: debian/clearwater-etcd.prerm
%systemd_preun clearwater-etcd.service
cw-stop clearwater-etcd
if [ "$1" = 0 ]; then # Uninstall
  cw-remove-user clearwater-etcd
  cw-remove-log-dir clearwater-etcd
  cw-remove-run-dir clearwater-etcd
fi

%postun
%systemd_postun_with_restart clearwater-etcd.service

%post -n clearwater-cluster-manager -p /bin/bash
%include %{SOURCE1}
# See: debian/clearwater-cluster-manager.links
ln --symbolic /usr/share/clearwater/clearwater-cluster-manager/scripts/check_cluster_state /usr/bin/cw-check_cluster_state
ln --symbolic /usr/share/clearwater/clearwater-cluster-manager/scripts/mark_node_failed /usr/sbin/cw-mark_node_failed

# See: debian/clearwater-cluster-manager.postinst
cw-create-user clearwater-cluster-manager
cw-create-log-dir clearwater-cluster-manager adm
cw-create-virtualenv clearwater-cluster-manager
%systemd_post clearwater-cluster-manager.service
cw-start clearwater-cluster-manager

%preun -n clearwater-cluster-manager -p /bin/bash
%include %{SOURCE1}
# See: debian/clearwater-cluster-manager.prerm
%systemd_preun clearwater-cluster-manager.service
cw-stop clearwater-cluster-manager
cw-remove-virtualenv clearwater-cluster-manager
if [ "$1" = 0 ]; then # Uninstall
  cw-remove-user clearwater-cluster-manager
  cw-remove-log-dir clearwater-cluster-manager
  cw-remove-run-dir clearwater-cluster-manager
fi

# See: debian/clearwater-cluster-manager.links
rm --force /usr/bin/cw-check_cluster_state
rm --force /usr/sbin/cw-mark_node_failed

%postun -n clearwater-cluster-manager
%systemd_postun_with_restart clearwater-cluster-manager.service

%post -n clearwater-queue-manager -p /bin/bash
%include %{SOURCE1}
# See: debian/clearwater-queue-manager.links
ln --symbolic /usr/share/clearwater/clearwater-queue-manager/scripts/check_restart_queue_state /usr/bin/cw-check_restart_queue_state

# See: debian/clearwater-queue-manager.postinst
cw-create-user clearwater-queue-manager
cw-create-log-dir clearwater-queue-manager adm
cw-create-virtualenv clearwater-queue-manager
%systemd_post clearwater-queue-manager.service
cw-start clearwater-queue-manager

%preun -n clearwater-queue-manager -p /bin/bash
%include %{SOURCE1}
# See: debian/clearwater-queue-manager.prerm
%systemd_preun clearwater-queue-manager.service
cw-stop clearwater-queue-manager
cw-remove-virtualenv clearwater-queue-manager
if [ "$1" = 0 ]; then # Uninstall
  cw-remove-user clearwater-queue-manager
  cw-remove-log-dir clearwater-queue-manager
  cw-remove-run-dir clearwater-queue-manager
fi

# See: debian/clearwater-queue-manager.links
rm --force /usr/bin/cw-check_restart_queue_state

%postun -n clearwater-queue-manager
%systemd_postun_with_restart clearwater-queue-manager.service

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
%systemd_post clearwater-config-manager.service
cw-start clearwater-config-manager

%preun -n clearwater-config-manager -p /bin/bash
%include %{SOURCE1}
# See: debian/clearwater-config-manager.prerm
%systemd_preun clearwater-config-manager.service
cw-stop clearwater-config-manager
cw-remove-virtualenv clearwater-config-manager
if [ "$1" = 0 ]; then # Uninstall
  cw-remove-user clearwater-config-manager
  cw-remove-log-dir clearwater-config-manager
  cw-remove-run-dir clearwater-config-manager
fi

# See: debian/clearwater-config-manager.links
rm --force /usr/bin/cw-config
rm --force /usr/bin/cw-restore_config
rm --force /usr/sbin/cw-check_config_sync
rm --force /usr/sbin/cw-backup_config

%postun -n clearwater-config-manager
%systemd_postun_with_restart clearwater-config-manager.service
