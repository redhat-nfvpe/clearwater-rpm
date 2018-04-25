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

# systemd
mkdir --parents %{buildroot}%{_unitdir}/
mkdir --parents %{buildroot}/lib/systemd/scripts/
cp %{SOURCE2} %{buildroot}%{_unitdir}/astaire.service
cp %{SOURCE3} %{buildroot}/lib/systemd/scripts/astaire.sh
cp %{SOURCE4} %{buildroot}%{_unitdir}/rogers.service
cp %{SOURCE5} %{buildroot}/lib/systemd/scripts/rogers.sh

sed --in-place 's/\/etc\/init.d\/astaire/service astaire/g' %{buildroot}/usr/share/clearwater/infrastructure/scripts/astaire.monit
sed --in-place 's/reload clearwater-monit/service reload clearwater-monit/g' %{buildroot}/usr/share/clearwater/infrastructure/scripts/astaire.monit
sed --in-place 's/\/etc\/init.d\/rogers/service rogers/g' %{buildroot}/usr/share/clearwater/infrastructure/scripts/rogers.monit
sed --in-place 's/reload clearwater-monit/service reload clearwater-monit/g' %{buildroot}/usr/share/clearwater/infrastructure/scripts/rogers.monit

#mkdir --parents %{buildroot}%{_initrddir}/
#cp debian/astaire.init.d %{buildroot}%{_initrddir}/astaire
#cp debian/rogers.init.d %{buildroot}%{_initrddir}/rogers

%files
%attr(644,-,-) %{_unitdir}/astaire.service
%attr(755,-,-) /lib/systemd/scripts/astaire.sh
%attr(755,-,-) /usr/share/clearwater/bin/astaire
%attr(755,-,-) /usr/share/clearwater/astaire/bin/cw_stat
/usr/share/clearwater/astaire/lib/
/usr/share/clearwater/infrastructure/alarms/astaire_alarms.json
%attr(755,-,-) /usr/share/clearwater/infrastructure/monit_uptime/check-astaire-uptime
%attr(755,-,-) /usr/share/clearwater/infrastructure/scripts/reload/memcached/astaire_reload
%attr(755,-,-) /usr/share/clearwater/infrastructure/scripts/restart/astaire_restart
%attr(755,-,-) /usr/share/clearwater/infrastructure/scripts/astaire.monit
%attr(755,-,-) /etc/cron.hourly/astaire-log-cleanup
/etc/security/limits.conf.astaire
%ghost /etc/monit/conf.d/astaire.monit

%files -n clearwater-rogers
%attr(644,-,-) %{_unitdir}/rogers.service
%attr(755,-,-) /lib/systemd/scripts/rogers.sh
%attr(755,-,-) /usr/share/clearwater/bin/rogers
/usr/share/clearwater/rogers/lib/
/usr/share/clearwater/infrastructure/alarms/rogers_alarms.json
%attr(755,-,-) /usr/share/clearwater/infrastructure/monit_uptime/check-rogers-uptime
%attr(755,-,-) /usr/share/clearwater/infrastructure/scripts/reload/memcached/rogers_reload
%attr(755,-,-) /usr/share/clearwater/infrastructure/scripts/restart/rogers_restart
%attr(755,-,-) /usr/share/clearwater/infrastructure/scripts/rogers.monit
%attr(755,-,-) /etc/cron.hourly/rogers-log-cleanup
/etc/security/limits.conf.rogers
%ghost /etc/monit/conf.d/rogers.monit

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
