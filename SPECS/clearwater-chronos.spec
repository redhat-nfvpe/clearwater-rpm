Name:          clearwater-chronos
Version:       129
Release:       1%{?dist}
License:       GPLv3+
URL:           https://github.com/Metaswitch/chronos

Source0:       %{name}-%{version}.tar.bz2
Source1:       scriptlet-util.sh
Source2:       chronos.service
Source3:       chronos.sh

BuildRequires: make cmake libtool gcc-c++ ccache
BuildRequires: libevent-devel openssl-devel zlib-devel zeromq-devel boost-devel net-snmp-devel
BuildRequires: systemd

# Note: zeromq-devel requires epel-release

%global debug_package %{nil}

Summary:       Clearwater - Chronos
Requires:      openssl-libs zlib zeromq boost net-snmp-libs
AutoReq:       no
%{?systemd_requires}
#Requires:      clearwater-infrastructure clearwater-snmpd clearwater-monit clearwater-queue-manager
#Requires:      clearwater-config-manager

%description
distributed timer service

%prep
%setup

%build
make MAKE="make --jobs=$(nproc)"

%install
mkdir --parents %{buildroot}%{_unitdir}/
mkdir --parents %{buildroot}/lib/systemd/scripts/
install --mode=644 %{SOURCE2} %{buildroot}%{_unitdir}/chronos.service
install --mode=755 %{SOURCE3} %{buildroot}/lib/systemd/scripts/chronos.sh

#mkdir --parents %{buildroot}%{_initrddir}/
#install --mode=755 debian/chronos.init.d %{buildroot}%{_initrddir}/chronos

# See: debian/chronos.install
mkdir --parents %{buildroot}/usr/bin/
mkdir --parents %{buildroot}/usr/share/clearwater/chronos/bin/
mkdir --parents %{buildroot}/usr/share/chronos/lib/
mkdir --parents %{buildroot}/usr/share/clearwater/clearwater-cluster-manager/plugins/
mkdir --parents %{buildroot}/usr/share/clearwater/clearwater-queue-manager/plugins/
mkdir --parents %{buildroot}/usr/share/clearwater/clearwater-config-manager/plugins/
mkdir --parents %{buildroot}/usr/share/clearwater/clearwater-queue-manager/scripts/
mkdir --parents %{buildroot}/usr/share/clearwater/clearwater-config-manager/scripts/
cp build/bin/chronos %{buildroot}/usr/bin/
cp modules/cpp-common/scripts/stats-c/cw_stat %{buildroot}/usr/share/clearwater/chronos/bin/
cp usr/lib/*.so %{buildroot}/usr/share/chronos/lib/
cp usr/lib/*.so.* %{buildroot}/usr/share/chronos/lib/
cp --recursive chronos.root/* %{buildroot}/
cp modules/clearwater-etcd-plugins/chronos/chronos_plugin.py %{buildroot}/usr/share/clearwater/clearwater-cluster-manager/plugins/
cp modules/clearwater-etcd-plugins/chronos/apply_chronos_shared_config_plugin.py %{buildroot}/usr/share/clearwater/clearwater-queue-manager/plugins/
cp modules/clearwater-etcd-plugins/chronos/chronos_shared_config_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-manager/plugins/
cp modules/clearwater-etcd-plugins/chronos/scripts/check_chronos_shared_restart_queue_state %{buildroot}/usr/share/clearwater/clearwater-queue-manager/scripts/
cp modules/clearwater-etcd-plugins/chronos/scripts/force_chronos_shared_restart_queue_state %{buildroot}/usr/share/clearwater/clearwater-queue-manager/scripts/
cp modules/clearwater-etcd-plugins/chronos/scripts/upload_chronos_shared_config %{buildroot}/usr/share/clearwater/clearwater-config-manager/scripts/

%files
%{_unitdir}/chronos.service
/lib/systemd/scripts/chronos.sh
/usr/bin/chronos
/usr/share/clearwater/chronos/bin/
/usr/share/chronos/lib/
/usr/share/clearwater/clearwater-cluster-manager/plugins/chronos_plugin.py*
/usr/share/clearwater/clearwater-queue-manager/plugins/apply_chronos_shared_config_plugin.py*
/usr/share/clearwater/clearwater-config-manager/plugins/chronos_shared_config_plugin.py*
/usr/share/clearwater/clearwater-queue-manager/scripts/check_chronos_shared_restart_queue_state
/usr/share/clearwater/clearwater-queue-manager/scripts/force_chronos_shared_restart_queue_state
/usr/share/clearwater/clearwater-config-manager/scripts/upload_chronos_shared_config
/usr/share/chronos/chronos.monit
/usr/share/chronos/write_monit_restart_diags
/usr/share/clearwater/bin/chronos_configuration_split.py*
/usr/share/clearwater/bin/poll_chronos.sh
/usr/share/clearwater/clearwater-diags-monitor/scripts/chronos_diags
/usr/share/clearwater/infrastructure/alarms/chronos_alarms.json
/usr/share/clearwater/infrastructure/monit_stability/chronos-stability
/usr/share/clearwater/infrastructure/monit_uptime/check-chronos-uptime
/usr/share/clearwater/infrastructure/scripts/reload/dns_json/chronos_reload
/usr/share/clearwater/infrastructure/scripts/chronos
/usr/share/clearwater/node_type.d/90_chronos
/etc/cron.hourly/chronos-log-cleanup
/etc/chronos/chronos.conf.sample
%ghost /etc/chronos/chronos.conf

%post -p /bin/bash
%include %{SOURCE1}
# See: debian/chronos.links
ln --symbolic /usr/share/clearwater/clearwater-queue-manager/scripts/check_chronos_shared_restart_queue_state /usr/bin/cw-check_chronos_shared_config_restart_queue_state
ln --symbolic /usr/share/clearwater/clearwater-queue-manager/scripts/force_chronos_shared_restart_queue_state /usr/bin/cw-force_chronos_shared_config_restart_queue_state
ln --symbolic /usr/share/clearwater/clearwater-config-manager/scripts/upload_chronos_shared_config /usr/bin/cw-upload_chronos_shared_config

# See: debian/chronos.postinst
cw-create-user chronos
cw-create-log-dir chronos
%systemd_post chronos.service
cw-start chronos

%preun -p /bin/bash
%include %{SOURCE1}
# See: debian/chronos.prerm
%systemd_preun chronos.service
cw-stop chronos
if [ "$1" = 0 ]; then # Uninstall
  cw-remove-user chronos
  cw-remove-log-dir chronos
fi

# See: debian/chronos.links
rm --force /usr/bin/cw-check_chronos_shared_config_restart_queue_state
rm --force /usr/bin/cw-force_chronos_shared_config_restart_queue_state
rm --force /usr/bin/cw-upload_chronos_shared_config

%postun
%systemd_postun_with_restart chronos.service
