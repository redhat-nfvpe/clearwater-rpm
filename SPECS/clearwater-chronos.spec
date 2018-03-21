Name:          clearwater-chronos
Version:       129
Release:       1%{?dist}
License:       GPLv3+
URL:           https://github.com/Metaswitch/chronos

Source0:       %{name}-%{version}.tar.bz2
BuildRequires: make cmake libtool gcc-c++
BuildRequires: libevent-devel openssl-devel zlib-devel zeromq-devel boost-devel net-snmp-devel

%global debug_package %{nil}

Summary:       Clearwater - Chronos
Requires:      clearwater-infrastructure clearwater-snmpd clearwater-monit clearwater-queue-manager
Requires:      clearwater-config-manager
Requires:      openssl-libs zlib zeromq boost net-snmp-libs

%description
distributed timer service

%prep
%setup

%build
make

%install
# See: debian/chronos.install
mkdir --parents %{buildroot}%{_initrddir}/
mkdir --parents %{buildroot}/usr/bin/
mkdir --parents %{buildroot}/usr/share/clearwater/chronos/bin/
mkdir --parents %{buildroot}/usr/share/chronos/lib/
mkdir --parents %{buildroot}/usr/share/clearwater/clearwater-cluster-manager/plugins/
mkdir --parents %{buildroot}/usr/share/clearwater/clearwater-queue-manager/plugins/
mkdir --parents %{buildroot}/usr/share/clearwater/clearwater-config-manager/plugins/
mkdir --parents %{buildroot}/usr/share/clearwater/clearwater-queue-manager/scripts/
mkdir --parents %{buildroot}/usr/share/clearwater/clearwater-config-manager/scripts/
install -m 755 debian/chronos.init.d %{buildroot}%{_initrddir}/chronos
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
/

%post
# See: debian/chronos.links
set -e
ln --symbolic /usr/share/clearwater/clearwater-queue-manager/scripts/check_chronos_shared_restart_queue_state /usr/bin/cw-check_chronos_shared_config_restart_queue_state
ln --symbolic /usr/share/clearwater/clearwater-queue-manager/scripts/force_chronos_shared_restart_queue_state /usr/bin/cw-force_chronos_shared_config_restart_queue_state
ln --symbolic /usr/share/clearwater/clearwater-config-manager/scripts/upload_chronos_shared_config /usr/bin/cw-upload_chronos_shared_config

# See: debian/chronos.postinst
if ! grep -q "^chronos:" /etc/passwd; then
  useradd --system --no-create-home --home-dir /nonexistent --shell /bin/false chronos
fi
mkdir --parents /var/log/chronos/
chown --recursive chronos /var/log/chronos/
service clearwater-monit reload || /bin/true
if [ -x /etc/init.d/clearwater-cluster-manager"]; then
  service clearwater-cluster-manager stop || /bin/true
fi
if [ -x /etc/init.d/clearwater-config-manager ]; then
  service clearwater-config-manager stop || /bin/true
fi
if [ -x /etc/init.d/clearwater-queue-manager ]; then
  service clearwater-queue-manager stop || /bin/true
fi
service chronos stop || /bin/true

%preun
# See: debian/chronos.prerm
set -e
rm --force /etc/monit/conf.d/chronos.monit
service clearwater-monit reload || /bin/true
rm --force /usr/share/clearwater/clearwater-cluster-manager/plugins/chronos*
if [ -x /etc/init.d/clearwater-cluster-manager ]; then
  service clearwater-cluster-manager stop || /bin/true
fi
service chronos stop || /bin/true
if [ "$1" = 0 ]; then # Uninstall
  if grep -q "^chronos:" /etc/passwd; then
    userdel chronos
  fi
  if [ -d /var/log/chronos/ ]; then
    rm --recursive /var/log/chronos/
  fi
  rm --recursive --force /var/run/chronos/
fi

rm --force /usr/bin/cw-check_chronos_shared_config_restart_queue_state
rm --force /usr/bin/cw-force_chronos_shared_config_restart_queue_state
rm --force /usr/bin/cw-upload_chronos_shared_config
