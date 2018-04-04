Name:          clearwater-memento
Version:       129
Release:       1%{?dist}
License:       GPLv3+
URL:           https://github.com/Metaswitch/memento

Source0:       %{name}-%{version}.tar.bz2
Source1:       common.sh
BuildRequires: make cmake libtool gcc-c++ bison flex
BuildRequires: libevent-devel boost-devel boost-static openssl-devel curl-devel zeromq-devel

# Note: zeromq-devel requires epel-release

%global debug_package %{nil}

Summary:       Clearwater - Memento
Requires:      clearwater-memento-libs
Requires:      clearwater-infrastructure clearwater-tcp-scalability clearwater-log-cleanup
Requires:      clearwater-monit clearwater-socket-factory
Requires:      openssl-libs libcurl zeromq

%package libs
Summary:       Clearwater - Memento Libraries
Requires:      libevent

%package nginx
Summary:       Clearwater - Nginx for Memento
Requires:      clearwater-memento
Requires:      clearwater-infrastructure clearwater-nginx

%package cassandra
Summary:       Clearwater - Cassandra for Memento
Requires:      clearwater-infrastructure clearwater-cassandra

%description
Application Server responsible for providing network-based call lists

%description libs
Memento libraries

%description nginx
Configure Nginx for Memento

%description cassandra
Commission Cassandra for Memento

%prep
%setup

%build
make MAKE="make --jobs $(nproc)"

%install
# See: debian/memento.install
mkdir --parents %{buildroot}%{_initrddir}/
mkdir --parents %{buildroot}/usr/share/clearwater/bin/
install --mode=755 debian/memento.init.d %{buildroot}%{_initrddir}/memento
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

%files
%{_initrddir}/memento
/usr/share/clearwater/bin/memento
/usr/share/clearwater/bin/poll_memento.sh
/usr/share/clearwater/bin/memento-disk-usage-stats
/usr/share/clearwater/bin/memento-disk-usage-functions
/usr/share/clearwater/infrastructure/scripts/reload/memcached
/usr/share/clearwater/infrastructure/scripts/reload/memcached/memento_reload
/usr/share/clearwater/infrastructure/scripts/restart/memento_restart
/usr/share/clearwater/infrastructure/scripts/memento.monit
/usr/share/clearwater/infrastructure/alarms/memento_alarms.json
/usr/share/clearwater/infrastructure/monit_uptime/check-memento-uptime
/usr/share/clearwater/node_type.d/80_memento
/usr/share/clearwater/clearwater-diags-monitor/scripts/memento_diags
%config /etc/security/limits.conf.memento
%config /etc/cron.hourly/memento-log-cleanup
%config /etc/cron.hourly/memento_disk_usage

%files libs
/usr/share/clearwater/lib/

%files nginx
/usr/share/clearwater/infrastructure/scripts/create-memento-nginx-config
/usr/share/clearwater/bin/poll_memento_https.sh

%files cassandra
/usr/share/clearwater/cassandra-schemas/memento.sh

%post
%include %{SOURCE1}
# See: debian/memento.postinst
. /usr/share/clearwater/bin/memento-disk-usage-functions
function add_section()
{
  local FILE=$1
  local TAG=$2
  local DELTA=$3
  { echo "#+$TAG"
    cat $DELTA
    echo "#-$TAG" ; } >> $FILE
}
if ! grep -q "^memento:" /etc/passwd; then
  useradd --system --no-create-home --home-dir /nonexistent --shell /bin/false memento
fi
mkdir --parents /var/log/memento/
chown --recursive memento /var/log/memento/
[ ! -x /usr/share/clearwater/bin/clearwater-logging-update ] || /usr/share/clearwater/bin/clearwater-logging-update
add_section /etc/security/limits.conf memento /etc/security/limits.conf.memento
service clearwater-infrastructure restart
memento_get_current_use > "$MEMENTO_DISK_USAGE_FILE"
if [ -x /etc/init.d/clearwater-cluster-manager ]; then
  service clearwater-cluster-manager stop || /bin/true
fi  
service memento stop || /bin/true

%preun
%include %{SOURCE1}
# See: debian/memento.prerm
. /usr/share/clearwater/bin/memento-disk-usage-functions
function remove_section()
{
  local FILE=$1
  local TAG=$2
  awk '/^#\+'$TAG'$/,/^#-'$TAG'$/ {next} {print}' "$FILE" > "/tmp/$(basename "$FILE").$$"
  mv "/tmp/$(basename "$FILE").$$" "$FILE"
}
rm --force /etc/monit/conf.d/memento.monit
service clearwater-monit reload || /bin/true
rm --force /usr/share/clearwater/clearwater-cluster-manager/plugins/memento*
if [ -x /etc/init.d/clearwater-cluster-manager ]; then
  service clearwater-cluster-manager stop || /bin/true
fi
service memento stop || /bin/true
if [ "$1" = 0 ]; then # Uninstall
  if grep -q "^memento:" /etc/passwd; then
    userdel memento
  fi
  if [ -d /var/log/memento/ ]; then
    rm --recursive /var/log/memento/
  fi
  rm --recursive --force /var/run/memento/
fi
remove_section /etc/security/limits.conf memento
rm --force "$MEMENTO_DISK_USAGE_FILE"

%post nginx
%include %{SOURCE1}
# See: debian/memento-nginx.postinst
service clearwater-infrastructure restart

%preun nginx
%include %{SOURCE1}
# See: debian/memento-nginx.prerm
nginx_dissite memento
service nginx reload

%post cassandra
%include %{SOURCE1}
# See: debian/memento-cassandra.postinst
service clearwater-infrastructure restart
