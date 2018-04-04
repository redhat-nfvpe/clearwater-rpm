Name:          clearwater-astaire
Version:       129
Release:       1%{?dist}
License:       GPLv3+
URL:           https://github.com/Metaswitch/astaire

Source0:       %{name}-%{version}.tar.bz2
Source1:       common.sh
BuildRequires: make libtool git gcc-c++
BuildRequires: libevent-devel zeromq-devel zlib-devel boost-devel

# Note: zeromq-devel requires epel-release

%global debug_package %{nil}

Summary:       Clearwater - Astaire
Requires:      clearwater-astaire-libs
Requires:      clearwater-infrastructure clearwater-tcp-scalability clearwater-log-cleanup 
Requires:      clearwater-monit clearwater-debian
Requires:      cpulimit
Requires:      zeromq zlib boost

%package libs
Summary:       Clearwater - Astaire Libraries

%package -n clearwater-rogers
Summary:       Clearwater - Rogers
Requires:      clearwater-rogers-libs
Requires:      clearwater-infrastructure clearwater-tcp-scalability clearwater-log-cleanup 
Requires:      clearwater-monit clearwater-debian
Requires:      zeromq zlib boost

%package -n clearwater-rogers-libs
Summary:       Clearwater - Rogers Libraries

%description
memcached clustering

%description libs
Astaire libraries

%description -n clearwater-rogers
memcached proxy

%description -n clearwater-rogers-libs
Rogers libraries

%prep
%setup

%build
make MAKE="make --jobs $(nproc)"

%install
# See: debian/astaire.install
mkdir --parents %{buildroot}%{_initrddir}/
mkdir --parents %{buildroot}/usr/share/clearwater/bin/
mkdir --parents %{buildroot}/usr/share/clearwater/astaire/bin/
install --mode=755 debian/astaire.init.d %{buildroot}%{_initrddir}/astaire
cp build/bin/astaire %{buildroot}/usr/share/clearwater/bin/
cp modules/cpp-common/scripts/stats-c/cw_stat %{buildroot}/usr/share/clearwater/astaire/bin/
cp --recursive astaire.root/* %{buildroot}/

# See: debian/astaire-libs.install
mkdir --parents %{buildroot}/usr/share/clearwater/astaire/lib/
cp usr/lib/*.so %{buildroot}/usr/share/clearwater/astaire/lib/
cp usr/lib/*.so.* %{buildroot}/usr/share/clearwater/astaire/lib/

# See: debian/rogers.install
install --mode=755 debian/rogers.init.d %{buildroot}%{_initrddir}/rogers
cp build/bin/rogers %{buildroot}/usr/share/clearwater/bin/
cp --recursive rogers.root/* %{buildroot}/

# See: debian/rogers-libs.install
mkdir --parents %{buildroot}/usr/share/clearwater/rogers/lib/
cp usr/lib/*.so %{buildroot}/usr/share/clearwater/rogers/lib/
cp usr/lib/*.so.* %{buildroot}/usr/share/clearwater/rogers/lib/

%files
%{_initrddir}/astaire
/usr/share/clearwater/bin/astaire
/usr/share/clearwater/astaire/bin/cw_stat
/usr/share/clearwater/infrastructure/alarms/astaire_alarms.json
/usr/share/clearwater/infrastructure/monit_uptime/check-astaire-uptime
/usr/share/clearwater/infrastructure/scripts/reload/memcached/astaire_reload
/usr/share/clearwater/infrastructure/scripts/restart/astaire_restart
/usr/share/clearwater/infrastructure/scripts/astaire.monit
%config /etc/cron.hourly/astaire-log-cleanup
%config /etc/init/astaire-throttle.conf
%config /etc/security/limits.conf.astaire

%files libs
/usr/share/clearwater/astaire/lib/

%files -n clearwater-rogers
%{_initrddir}/rogers
/usr/share/clearwater/bin/rogers
/usr/share/clearwater/infrastructure/alarms/rogers_alarms.json
/usr/share/clearwater/infrastructure/monit_uptime/check-rogers-uptime
/usr/share/clearwater/infrastructure/scripts/reload/memcached/rogers_reload
/usr/share/clearwater/infrastructure/scripts/restart/rogers_restart
/usr/share/clearwater/infrastructure/scripts/rogers.monit
%config /etc/cron.hourly/rogers-log-cleanup
%config /etc/security/limits.conf.rogers

%files -n clearwater-rogers-libs
/usr/share/clearwater/rogers/lib/

%post -p /bin/bash
%include %{SOURCE1}
# See: debian/astaire.postinst
cw-create-user astaire
cw-create-log-dir astaire
cw-add-security-limits astaire
# TODO: convert from Upstart to systemd
service-action astaire-throttle start
cw-start astaire

%preun -p /bin/bash
%include %{SOURCE1}
# See: debian/astaire.prerm
cw-stop astaire
service-action astaire-throttle stop
if [ "$1" = 0 ]; then # Uninstall
  cw-remove-user astaire
  cw-remove-log-dir astaire
  cw-remove-run-dir astaire
fi
cw-remove-security-limits astaire

%post -n clearwater-rogers -p /bin/bash
%include %{SOURCE1}
# See: debian/rogers.postinst
cw-create-user rogers
cw-create-log-dir rogers
cw-add-security-limits rogers
cw-start rogers

%preun -n clearwater-rogers -p /bin/bash
%include %{SOURCE1}
# See: debian/rogers.prerm
cw-stop rogers stop
if [ "$1" = 0 ]; then # Uninstall
  cw-remove-user rogers
  cw-remove-log-dir rogers
  cw-remove-run-dir rogers
fi
cw-remove-security-limits rogers
