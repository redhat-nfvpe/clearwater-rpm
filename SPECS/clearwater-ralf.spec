Name:          clearwater-ralf
Version:       129
Release:       1%{?dist}
License:       GPLv3+
URL:           https://github.com/Metaswitch/ralf

Source0:       %{name}-%{version}.tar.bz2
Source1:       housekeeping.sh
Source2:       ralf.service
Source3:       ralf.sh

BuildRequires: make cmake libtool gcc-c++ ccache bison flex
BuildRequires: libevent-devel lksctp-tools-devel libidn-devel libgcrypt-devel gnutls-devel
BuildRequires: boost-devel zeromq-devel libcurl-devel
BuildRequires: systemd

# Note: zeromq-devel requires epel-release

%global debug_package %{nil}

Summary:       Clearwater - Ralf
Requires:      libidn libgcrypt gnutls boost zeromq libcurl
AutoReq:       no
%{?systemd_requires}
#Requires:      clearwater-infrastructure clearwater-tcp-scalability clearwater-socket-factory
#Requires:      clearwater-log-cleanup clearwater-monit

%package -n clearwater-node-ralf
Summary:       Clearwater Node - Ralf
Requires:      clearwater-ralf clearwater-infrastructure
AutoReq:       no

%description
CTF

%description -n clearwater-node-ralf
Clearwater Ralf node

%prep
%setup

%build
make MAKE="make --jobs=$(nproc)"

%install
# See: debian/ralf.install
mkdir --parents %{buildroot}/usr/share/clearwater/bin/
cp build/bin/ralf %{buildroot}/usr/share/clearwater/bin/
cp --recursive ralf.root/* %{buildroot}/

# See: debian/ralf-libs.install
mkdir --parents %{buildroot}/usr/share/clearwater/ralf/lib/freeDiameter/
cp usr/lib/*.so %{buildroot}/usr/share/clearwater/ralf/lib/
cp usr/lib/*.so.* %{buildroot}/usr/share/clearwater/ralf/lib/
cp usr/lib/freeDiameter/*.fdx %{buildroot}/usr/share/clearwater/ralf/lib/freeDiameter/

# systemd
mkdir --parents %{buildroot}%{_unitdir}/
mkdir --parents %{buildroot}/lib/systemd/scripts/
cp %{SOURCE2} %{buildroot}%{_unitdir}/ralf.service
cp %{SOURCE3} %{buildroot}/lib/systemd/scripts/ralf.sh

sed --in-place 's/\/etc\/init.d\/ralf/service ralf/g' %{buildroot}/usr/share/clearwater/infrastructure/scripts/ralf.monit
sed --in-place 's/reload clearwater-monit/service reload clearwater-monit/g' %{buildroot}/usr/share/clearwater/infrastructure/scripts/ralf.monit

#mkdir --parents %{buildroot}%{_initrddir}/
#cp debian/ralf.init.d %{buildroot}%{_initrddir}/ralf

%files
%attr(644,-,-) %{_unitdir}/ralf.service
%attr(755,-,-) /lib/systemd/scripts/ralf.sh
%attr(755,-,-) /usr/share/clearwater/bin/ralf
%attr(755,-,-) /usr/share/clearwater/bin/poll_ralf.sh
/usr/share/clearwater/ralf/lib/
%attr(755,-,-) /usr/share/clearwater/clearwater-diags-monitor/scripts/ralf_diags
/usr/share/clearwater/infrastructure/alarms/ralf_alarms.json
%attr(755,-,-) /usr/share/clearwater/infrastructure/monit_stability/ralf-stability
%attr(755,-,-) /usr/share/clearwater/infrastructure/monit_uptime/check-ralf-uptime
%attr(755,-,-) /usr/share/clearwater/infrastructure/scripts/reload/memcached/ralf_reload
%attr(755,-,-) /usr/share/clearwater/infrastructure/scripts/restart/ralf_restart
%attr(755,-,-) /usr/share/clearwater/infrastructure/scripts/ralf
%attr(755,-,-) /usr/share/clearwater/infrastructure/scripts/ralf.monit
%attr(755,-,-) /etc/cron.hourly/ralf-log-cleanup
/etc/security/limits.conf.ralf
%ghost /etc/monit/conf.d/ralf.monit

%files -n clearwater-node-ralf
/usr/share/clearwater/node_type.d/20_ralf

%post -p /bin/bash
%include %{SOURCE1}
# See: debian/ralf.postinst
cw_create_user ralf
cw_create_log_dir ralf
cw_add_security_limits ralf
cw_activate ralf
%systemd_post ralf.service

%preun -p /bin/bash
%include %{SOURCE1}
# See: debian/ralf.prerm
%systemd_preun ralf.service
cw_deactivate ralf
if [ "$1" = 0 ]; then # Uninstall
  cw_remove_user ralf
  cw_remove_log_dir ralf
fi
cw_remove_security_limits ralf
rm --force /var/lib/ralf/ralf.conf

%postun
%systemd_postun_with_restart ralf.service
