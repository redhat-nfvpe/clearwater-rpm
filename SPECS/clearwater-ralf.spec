Name:          clearwater-ralf
Version:       129
Release:       1%{?dist}
License:       GPLv3+
URL:           https://github.com/Metaswitch/ralf

Source0:       %{name}-%{version}.tar.bz2
Source1:       scriptlet-util.sh
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

%description
CTF

%prep
%setup

%build
make MAKE="make --jobs=$(nproc)"

%install
mkdir --parents %{buildroot}%{_unitdir}/
mkdir --parents %{buildroot}/lib/systemd/scripts/
install --mode=644 %{SOURCE2} %{buildroot}%{_unitdir}/ralf.service
install --mode=755 %{SOURCE3} %{buildroot}/lib/systemd/scripts/ralf.sh

#mkdir --parents %{buildroot}%{_initrddir}/
#install --mode=755 debian/ralf.init.d %{buildroot}%{_initrddir}/ralf

# See: debian/ralf.install
mkdir --parents %{buildroot}/usr/share/clearwater/bin/
cp build/bin/ralf %{buildroot}/usr/share/clearwater/bin/
cp --recursive ralf.root/* %{buildroot}/

# See: debian/ralf-libs.install
mkdir --parents %{buildroot}/usr/share/clearwater/ralf/lib/freeDiameter/
cp usr/lib/*.so %{buildroot}/usr/share/clearwater/ralf/lib/
cp usr/lib/*.so.* %{buildroot}/usr/share/clearwater/ralf/lib/
cp usr/lib/freeDiameter/*.fdx %{buildroot}/usr/share/clearwater/ralf/lib/freeDiameter/

%files
%{_unitdir}/ralf.service
/lib/systemd/scripts/ralf.sh
/usr/share/clearwater/bin/ralf
/usr/share/clearwater/bin/poll_ralf.sh
/usr/share/clearwater/ralf/lib/
/usr/share/clearwater/clearwater-diags-monitor/scripts/ralf_diags
/usr/share/clearwater/infrastructure/alarms/ralf_alarms.json
/usr/share/clearwater/infrastructure/monit_stability/ralf-stability
/usr/share/clearwater/infrastructure/monit_uptime/check-ralf-uptime
/usr/share/clearwater/infrastructure/scripts/reload/memcached/ralf_reload
/usr/share/clearwater/infrastructure/scripts/restart/ralf_restart
/usr/share/clearwater/infrastructure/scripts/ralf
/usr/share/clearwater/infrastructure/scripts/ralf.monit
/usr/share/clearwater/node_type.d/20_ralf
/etc/cron.hourly/ralf-log-cleanup
/etc/security/limits.conf.ralf

%post -p /bin/bash
%include %{SOURCE1}
# See: debian/ralf.postinst
cw-create-user ralf
cw-create-log-dir ralf
cw-add-security-limits ralf
cw-start ralf
%systemd_post ralf.service

%preun -p /bin/bash
%include %{SOURCE1}
# See: debian/ralf.prerm
%systemd_preun ralf.service
cw-stop ralf
if [ "$1" = 0 ]; then # Uninstall
  cw-remove-user ralf
  cw-remove-log-dir ralf
fi
cw-remove-security-limits ralf
rm --force /var/lib/ralf/ralf.conf

%postun
%systemd_postun_with_restart ralf.service
