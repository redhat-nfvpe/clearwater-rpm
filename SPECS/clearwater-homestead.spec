Name:          clearwater-homestead
Version:       129
Release:       1%{?dist}
License:       GPLv3+
URL:           https://github.com/Metaswitch/homestead

Source0:       %{name}-%{version}.tar.bz2
Source1:       housekeeping.sh
Source2:       homestead.service
Source3:       homestead.sh

BuildRequires: make cmake libtool gcc-c++ ccache bison flex
BuildRequires: libevent-devel lksctp-tools-devel libidn-devel libgcrypt-devel gnutls-devel
BuildRequires: openssl-devel boost-devel boost-static zeromq-devel libcurl-devel net-snmp-devel
BuildRequires: systemd

# Note: zeromq-devel requires epel-release

%global debug_package %{nil}

Summary:       Clearwater - Homestead
Requires:      libevent lksctp-tools libidn libgcrypt gnutls openssl-libs zeromq libcurl
Requires:      net-snmp-libs net-snmp-agent-libs
AutoReq:       no
%{?systemd_requires}
#Requires:      clearwater-infrastructure clearwater-nginx clearwater-log-cleanup clearwater-monit
#Requires:      clearwater-tcp-scalability clearwater-snmpd

%package cassandra
Summary:       Clearwater - Cassandra for Homestead
Requires:      clearwater-cassandra
AutoReq:       no
#Requires:      clearwater-infrastructure clearwater-cassandra

%package -n clearwater-node-homestead
Summary:       Clearwater Node - Homestead
Requires:      clearwater-homestead clearwater-infrastructure
AutoReq:       no

%description
HSS cache/gateway

%description cassandra
Commission Cassandra for Homestead

%description -n clearwater-node-homestead
Clearwater Homestead node

%prep
%setup

%build
make MAKE="make --jobs=$(nproc)"

%install
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

# systemd
mkdir --parents %{buildroot}%{_unitdir}/
mkdir --parents %{buildroot}/lib/systemd/scripts/
cp %{SOURCE2} %{buildroot}%{_unitdir}/homestead.service
cp %{SOURCE3} %{buildroot}/lib/systemd/scripts/homestead.sh

sed --in-place 's/\/etc\/init.d\/homestead/service homestead/g' %{buildroot}/usr/share/clearwater/infrastructure/scripts/homestead.monit
sed --in-place 's/reload clearwater-monit/service reload clearwater-monit/g' %{buildroot}/usr/share/clearwater/infrastructure/scripts/homestead.monit

#mkdir --parents %{buildroot}%{_initrddir}/
#cp debian/homestead.init.d %{buildroot}%{_initrddir}/homestead

%files
%attr(644,-,-) %{_unitdir}/homestead.service
%attr(755,-,-) /lib/systemd/scripts/homestead.sh
%attr(755,-,-) /usr/share/clearwater/bin/homestead
%attr(755,-,-) /usr/share/clearwater/bin/check_cx_health
%attr(755,-,-) /usr/share/clearwater/bin/check_cx_health.py
%attr(755,-,-) /usr/share/clearwater/bin/poll_homestead.sh
/usr/share/clearwater/homestead/lib/
%attr(755,-,-) /usr/share/clearwater/clearwater-diags-monitor/scripts/homestead_diags
/usr/share/clearwater/infrastructure/alarms/homestead_alarms.json
%attr(755,-,-) /usr/share/clearwater/infrastructure/monit_stability/homestead-stability
%attr(755,-,-) /usr/share/clearwater/infrastructure/monit_uptime/check-homestead-uptime
%attr(755,-,-) /usr/share/clearwater/infrastructure/scripts/restart/homestead_restart
%attr(755,-,-) /usr/share/clearwater/infrastructure/scripts/create-homestead-nginx-config
%attr(755,-,-) /usr/share/clearwater/infrastructure/scripts/homestead
%attr(755,-,-) /usr/share/clearwater/infrastructure/scripts/homestead.monit
%attr(755,-,-) /etc/cron.hourly/homestead-log-cleanup
/etc/security/limits.conf.homestead
%ghost /etc/monit/conf.d/homestead.monit

%files cassandra
%attr(755,-,-) /usr/share/clearwater/cassandra-schemas/homestead_cache.sh

%files -n clearwater-node-homestead
/usr/share/clearwater/node_type.d/20_homestead

%post -p /bin/bash
%include %{SOURCE1}
# See: debian/homestead.postinst
mkdir --parents /var/lib/homestead/
cw_create_user homestead
cw_create_log_dir homestead
cw_add_security_limits homestead
%systemd_post homestead.service
cw_activate homestead

%preun -p /bin/bash
%include %{SOURCE1}
# See: debian/homestead.prerm
%systemd_preun homestead.service
cw_deactivate homestead
if [ "$1" = 0 ]; then # Uninstall
  cw_remove_user homestead
  cw_remove_log_dir homestead
fi
cw_remove_security_limits homestead
rm --force /var/lib/homestead/homestead.conf

%postun
%systemd_postun_with_restart homestead.service

%post cassandra -p /bin/bash
%include %{SOURCE1}
# See: debian/homestead-cassandra.postinst
service_action clearwater-infrastructure restart
