Name:          clearwater-memento
Version:       129
Release:       1%{?dist}
License:       GPLv3+
URL:           https://github.com/Metaswitch/memento

Source0:       %{name}-%{version}.tar.bz2
Source1:       scriptlet-util.sh
Source2:       memento.service
Source3:       memento.sh

BuildRequires: make cmake libtool gcc-c++ ccache bison flex
BuildRequires: libevent-devel boost-devel boost-static curl-devel zeromq-devel openssl-devel
BuildRequires: systemd

# Note: zeromq-devel requires epel-release
# Note: we need openssl-devel for libcrypto during build, but will actually be packaging our
# own build

%global debug_package %{nil}

Summary:       Clearwater - Memento Application Server
Requires:      libevent libcurl zeromq
AutoReq:       no
%{?systemd_requires}
#Requires:      clearwater-infrastructure clearwater-tcp-scalability clearwater-log-cleanup
#Requires:      clearwater-monit clearwater-socket-factory

%package nginx
Summary:       Clearwater - Nginx for Memento
Requires:      clearwater-nginx
AutoReq:       no
#Requires:      clearwater-memento
#Requires:      clearwater-infrastructure clearwater-nginx

%package cassandra
Summary:       Clearwater - Cassandra for Memento
Requires:      clearwater-cassandra
AutoReq:       no
#Requires:      clearwater-infrastructure clearwater-cassandra

%package -n clearwater-node-memento
Summary:       Clearwater Node - Memento
Requires:      clearwater-memento clearwater-infrastructure
AutoReq:       no

%description
Application Server responsible for providing network-based call lists

%description nginx
Configure Nginx for Memento

%description cassandra
Commission Cassandra for Memento

%description -n clearwater-node-memento
Clearwater Memento node

%prep
%setup

%build
# Disable concurrent builds for non-supporting modules
sed --in-place '1ioverride MAKE = make' modules/openssl/Makefile.org

make MAKE="make --jobs=$(nproc)"

%install
# See: debian/memento.install
mkdir --parents %{buildroot}/usr/share/clearwater/bin/
cp build/bin/memento %{buildroot}/usr/share/clearwater/bin/
cp --recursive memento.root/* %{buildroot}/

# See: debian/memento-libs.install
mkdir --parents %{buildroot}/usr/share/clearwater/lib/
cp usr/lib/*.so %{buildroot}/usr/share/clearwater/lib/
cp usr/lib/*.so.* %{buildroot}/usr/share/clearwater/lib/

# See: debian/memento-nginx.install
cp --recursive memento-nginx.root/* %{buildroot}/

# See: debian/memento-cassandra.install
cp --recursive memento-cassandra.root/* %{buildroot}/

# systemd
mkdir --parents %{buildroot}%{_unitdir}/
mkdir --parents %{buildroot}/lib/systemd/scripts/
cp %{SOURCE2} %{buildroot}%{_unitdir}/memento.service
cp %{SOURCE3} %{buildroot}/lib/systemd/scripts/memento.sh

sed --in-place 's/\/etc\/init.d\/memento/service memento/g' %{buildroot}/usr/share/clearwater/infrastructure/scripts/memento.monit
sed --in-place 's/reload clearwater-monit/service reload clearwater-monit/g' %{buildroot}/usr/share/clearwater/infrastructure/scripts/memento.monit

#mkdir --parents %{buildroot}%{_initrddir}/
#cp debian/memento.init.d %{buildroot}%{_initrddir}/memento

%files
%attr(644,-,-) %{_unitdir}/memento.service
%attr(755,-,-) /lib/systemd/scripts/memento.sh
%attr(755,-,-) /usr/share/clearwater/bin/memento
%attr(755,-,-) /usr/share/clearwater/bin/poll_memento.sh
%attr(755,-,-) /usr/share/clearwater/bin/memento-disk-usage-stats
%attr(755,-,-) /usr/share/clearwater/bin/memento-disk-usage-functions
/usr/share/clearwater/lib/libcares.so*
/usr/share/clearwater/lib/libcassandra.so
/usr/share/clearwater/lib/libhashkit.so*
/usr/share/clearwater/lib/libmemcached.so*
/usr/share/clearwater/lib/libmemcachedprotocol.so*
/usr/share/clearwater/lib/libmemcachedutil.so*
/usr/share/clearwater/lib/libthrift.so
/usr/share/clearwater/lib/libthrift-0.9.3.so
/usr/share/clearwater/lib/libthriftnb.so
/usr/share/clearwater/lib/libthriftnb-0.9.3.so
/usr/share/clearwater/lib/libthriftz.so
/usr/share/clearwater/lib/libthriftz-0.9.3.so
%attr(755,-,-) /usr/share/clearwater/infrastructure/scripts/reload/memcached/memento_reload
%attr(755,-,-) /usr/share/clearwater/infrastructure/scripts/restart/memento_restart
%attr(755,-,-) /usr/share/clearwater/infrastructure/scripts/memento.monit
/usr/share/clearwater/infrastructure/alarms/memento_alarms.json
%attr(755,-,-) /usr/share/clearwater/infrastructure/monit_uptime/check-memento-uptime
%attr(755,-,-) /usr/share/clearwater/clearwater-diags-monitor/scripts/memento_diags
/etc/security/limits.conf.memento
%attr(755,-,-) /etc/cron.hourly/memento-log-cleanup
%attr(755,-,-) /etc/cron.hourly/memento_disk_usage
%ghost /etc/monit/conf.d/memento.monit

%files nginx
%attr(755,-,-) /usr/share/clearwater/infrastructure/scripts/create-memento-nginx-config
%attr(755,-,-) /usr/share/clearwater/bin/poll_memento_https.sh

%files cassandra
%attr(755,-,-) /usr/share/clearwater/cassandra-schemas/memento.sh

%files -n clearwater-node-memento
/usr/share/clearwater/node_type.d/80_memento

%post -p /bin/bash
%include %{SOURCE1}
# See: debian/memento.postinst
. /usr/share/clearwater/bin/memento-disk-usage-functions
cw-create-user memento
cw-create-log-dir memento
cw-add-security-limits memtno
memento_get_current_use > "$MEMENTO_DISK_USAGE_FILE"
%systemd_post memento.service
cw-start memento

%preun -p /bin/bash
%include %{SOURCE1}
# See: debian/memento.prerm
%systemd_preun astaire.service
. /usr/share/clearwater/bin/memento-disk-usage-functions
cw-stop astaire
if [ "$1" = 0 ]; then # Uninstall
  cw-remove-user memento
  cw-remove-log-dir memento
fi
cw-remove-security-limits memento
rm --force "$MEMENTO_DISK_USAGE_FILE"

%postun
%systemd_postun_with_restart memento.service

%post nginx -p /bin/bash
%include %{SOURCE1}
# See: debian/memento-nginx.postinst
service-action clearwater-infrastructure restart

%preun nginx -p /bin/bash
%include %{SOURCE1}
# See: debian/memento-nginx.prerm
nginx_dissite memento
service-action nginx reload

%post cassandra -p /bin/bash
%include %{SOURCE1}
# See: debian/memento-cassandra.postinst
service-action clearwater-infrastructure restart
