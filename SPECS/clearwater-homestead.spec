Name:          clearwater-homestead
Version:       129
Release:       1%{?dist}
License:       GPLv3+
URL:           https://github.com/Metaswitch/homestead

Source0:       %{name}-%{version}.tar.bz2
Source1:       common.sh
Source2:       homestead.service
Source3:       homestead.sh

BuildRequires: make cmake libtool git gcc-c++ bison flex
BuildRequires: libevent-devel lksctp-tools-devel libidn-devel libgcrypt-devel gnutls-devel
BuildRequires: openssl-devel boost-devel boost-static zeromq-devel libcurl-devel net-snmp-devel
BuildRequires: systemd

# Note: zeromq-devel requires epel-release

%global debug_package %{nil}

Summary:       Clearwater - Homestead
Requires:      clearwater-homestead-libs
Requires:      libidn libgcrypt gnutls openssl-libs zeromq libcurl net-snmp-libs
#Requires:      clearwater-infrastructure clearwater-nginx clearwater-log-cleanup clearwater-monit
#Requires:      clearwater-tcp-scalability clearwater-snmpd
%{?systemd_requires}

%package libs
Summary:       Clearwater - Homestead Libraries
Requires:      libevent lksctp-tools

%package cassandra
Summary:       Clearwater - Cassandra for Homestead
#Requires:      clearwater-infrastructure clearwater-cassandra

%description
HSS cache/gateway

%description libs
Homestead libraries

%description cassandra
Commission Cassandra for Homestead

%prep
%setup

%build
make MAKE="make --jobs=$(nproc)"

%install
mkdir --parents %{buildroot}%{_unitdir}/
mkdir --parents %{buildroot}/lib/systemd/scripts/
install --mode=644 %{SOURCE2} %{buildroot}%{_unitdir}/homestead.service
install --mode=755 %{SOURCE3} %{buildroot}/lib/systemd/scripts/homestead.sh

#mkdir --parents %{buildroot}%{_initrddir}/
#install --mode=755 debian/homestead.init.d %{buildroot}%{_initrddir}/homestead

# See: debian/homestead.install
mkdir --parents %{buildroot}/usr/share/clearwater/bin/
cp build/bin/homestead %{buildroot}/usr/share/clearwater/bin/
cp --recursive homestead.root/* %{buildroot}/

# See: debian/homestead-libs.install
mkdir --parents %{buildroot}/usr/share/clearwater/homestead/lib/freeDiameter/
cp usr/lib/*.so %{buildroot}/usr/share/clearwater/homestead/lib/
cp usr/lib/*.so.* %{buildroot}/usr/share/clearwater/homestead/lib/
cp usr/lib/freeDiameter/*.fdx %{buildroot}/usr/share/clearwater/homestead/lib/freeDiameter/

# See: debian/homestead-cassandra.install
cp --recursive homestead-cassandra.root/* %{buildroot}/

%files
%{_unitdir}/homestead.service
/lib/systemd/scripts/homestead.sh
/usr/share/clearwater/bin/homestead
/usr/share/clearwater/bin/check_cx_health
/usr/share/clearwater/bin/check_cx_health.py*
/usr/share/clearwater/bin/poll_homestead.sh
/usr/share/clearwater/clearwater-diags-monitor/scripts/homestead_diags
/usr/share/clearwater/infrastructure/alarms/homestead_alarms.json
/usr/share/clearwater/infrastructure/monit_stability/homestead-stability
/usr/share/clearwater/infrastructure/monit_uptime/check-homestead-uptime
/usr/share/clearwater/infrastructure/scripts/restart/homestead_restart
/usr/share/clearwater/infrastructure/scripts/create-homestead-nginx-config
/usr/share/clearwater/infrastructure/scripts/homestead
/usr/share/clearwater/infrastructure/scripts/homestead.monit
/usr/share/clearwater/node_type.d/20_homestead
%config /etc/cron.hourly/homestead-log-cleanup
%config /etc/security/limits.conf.homestead
%ghost /var/log/homestead/

%files libs
/usr/share/clearwater/homestead/lib/

%files cassandra
/usr/share/clearwater/cassandra-schemas/homestead_cache.sh

%post -p /bin/bash
%include %{SOURCE1}
# See: debian/homestead.postinst
cw-create-user homestead
cw-create-log-dir homestead
cw-add-security-limits homestead
cw-start homestead
%systemd_post homestead.service

%preun -p /bin/bash
%include %{SOURCE1}
# See: debian/homestead.prerm
%systemd_preun homestead.service
cw-stop homestead
if [ "$1" = 0 ]; then # Uninstall
  cw-remove-user homestead
  cw-remove-log-dir homestead
  cw-remove-run-dir homestead
fi
cw-remove-security-limits homestead
rm --force /var/lib/homestead/homestead.conf

%postun
%systemd_postun_with_restart homestead.service

%post cassandra -p /bin/bash
%include %{SOURCE1}
# See: debian/homestead-cassandra.postinst
service-action clearwater-infrastructure restart
