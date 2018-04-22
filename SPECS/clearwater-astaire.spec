Name:          clearwater-astaire
Version:       129
Release:       1%{?dist}
License:       GPLv3+
URL:           https://github.com/Metaswitch/astaire

Source0:       %{name}-%{version}.tar.bz2
Source1:       scriptlet-util.sh
Source2:       astaire.service
Source3:       astaire.sh
Source4:       rogers.service
Source5:       rogers.sh

BuildRequires: make libtool gcc-c++ ccache
BuildRequires: libevent-devel zeromq-devel zlib-devel boost-devel
BuildRequires: systemd

# Note: zeromq-devel requires epel-release

%global debug_package %{nil}

Summary:       Clearwater - Astaire
Requires:      zeromq zlib boost
AutoReq:       no
%{?systemd_requires}
#Requires:      clearwater-infrastructure clearwater-tcp-scalability clearwater-log-cleanup
#Requires:      clearwater-monit

%package -n clearwater-rogers
Summary:       Clearwater - Rogers
Requires:      zeromq zlib boost
AutoReq:       no
%{?systemd_requires}
#Requires:      clearwater-infrastructure clearwater-tcp-scalability clearwater-log-cleanup
#Requires:      clearwater-monit

%description
memcached clustering

%description -n clearwater-rogers
memcached proxy

%prep
%setup

%build
make MAKE="make --jobs=$(nproc)"

%install
mkdir --parents %{buildroot}%{_unitdir}/
mkdir --parents %{buildroot}/lib/systemd/scripts/
install --mode=644 %{SOURCE2} %{buildroot}%{_unitdir}/astaire.service
install --mode=755 %{SOURCE3} %{buildroot}/lib/systemd/scripts/astaire.sh
install --mode=644 %{SOURCE4} %{buildroot}%{_unitdir}/rogers.service
install --mode=755 %{SOURCE5} %{buildroot}/lib/systemd/scripts/rogers.sh

#mkdir --parents %{buildroot}%{_initrddir}/
#install --mode=755 debian/astaire.init.d %{buildroot}%{_initrddir}/astaire
#install --mode=755 debian/rogers.init.d %{buildroot}%{_initrddir}/rogers

# See: debian/astaire.install
mkdir --parents %{buildroot}/usr/share/clearwater/bin/
mkdir --parents %{buildroot}/usr/share/clearwater/astaire/bin/
cp build/bin/astaire %{buildroot}/usr/share/clearwater/bin/
cp modules/cpp-common/scripts/stats-c/cw_stat %{buildroot}/usr/share/clearwater/astaire/bin/
cp --recursive astaire.root/* %{buildroot}/
rm %{buildroot}/etc/init/astaire-throttle.conf # Upstart script

# See: debian/astaire-libs.install
mkdir --parents %{buildroot}/usr/share/clearwater/astaire/lib/
cp usr/lib/*.so %{buildroot}/usr/share/clearwater/astaire/lib/
cp usr/lib/*.so.* %{buildroot}/usr/share/clearwater/astaire/lib/

# See: debian/rogers.install
cp build/bin/rogers %{buildroot}/usr/share/clearwater/bin/
cp --recursive rogers.root/* %{buildroot}/

# See: debian/rogers-libs.install
mkdir --parents %{buildroot}/usr/share/clearwater/rogers/lib/
cp usr/lib/*.so %{buildroot}/usr/share/clearwater/rogers/lib/
cp usr/lib/*.so.* %{buildroot}/usr/share/clearwater/rogers/lib/

%files
%{_unitdir}/astaire.service
/lib/systemd/scripts/astaire.sh
/usr/share/clearwater/bin/astaire
/usr/share/clearwater/astaire/bin/cw_stat
/usr/share/clearwater/astaire/lib/
/usr/share/clearwater/infrastructure/alarms/astaire_alarms.json
/usr/share/clearwater/infrastructure/monit_uptime/check-astaire-uptime
/usr/share/clearwater/infrastructure/scripts/reload/memcached/astaire_reload
/usr/share/clearwater/infrastructure/scripts/restart/astaire_restart
/usr/share/clearwater/infrastructure/scripts/astaire.monit
/etc/cron.hourly/astaire-log-cleanup
/etc/security/limits.conf.astaire

%files -n clearwater-rogers
%{_unitdir}/rogers.service
/lib/systemd/scripts/rogers.sh
/usr/share/clearwater/bin/rogers
/usr/share/clearwater/rogers/lib/
/usr/share/clearwater/infrastructure/alarms/rogers_alarms.json
/usr/share/clearwater/infrastructure/monit_uptime/check-rogers-uptime
/usr/share/clearwater/infrastructure/scripts/reload/memcached/rogers_reload
/usr/share/clearwater/infrastructure/scripts/restart/rogers_restart
/usr/share/clearwater/infrastructure/scripts/rogers.monit
/etc/cron.hourly/rogers-log-cleanup
/etc/security/limits.conf.rogers

%post -p /bin/bash
%include %{SOURCE1}
# See: debian/astaire.postinst
cw-create-user astaire
cw-create-log-dir astaire
cw-add-security-limits astaire
#service-action astaire-throttle start
%systemd_post astaire.service
cw-start astaire

%preun -p /bin/bash
%include %{SOURCE1}
# See: debian/astaire.prerm
%systemd_preun astaire.service
cw-stop astaire
service-action astaire-throttle stop
if [ "$1" = 0 ]; then # Uninstall
  cw-remove-user astaire
  cw-remove-log-dir astaire
fi
cw-remove-security-limits astaire

%postun
%systemd_postun_with_restart astaire.service

%post -n clearwater-rogers -p /bin/bash
%include %{SOURCE1}
# See: debian/rogers.postinst
cw-create-user rogers
cw-create-log-dir rogers
cw-add-security-limits rogers
%systemd_post rogers.service
cw-start rogers

%preun -n clearwater-rogers -p /bin/bash
%include %{SOURCE1}
# See: debian/rogers.prerm
%systemd_preun rogers.service
cw-stop rogers stop
if [ "$1" = 0 ]; then # Uninstall
  cw-remove-user rogers
  cw-remove-log-dir rogers
fi
cw-remove-security-limits rogers

%postun -n clearwater-rogers
%systemd_postun_with_restart rogers.service
