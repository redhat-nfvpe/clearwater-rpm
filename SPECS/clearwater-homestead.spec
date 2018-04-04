Name:          clearwater-homestead
Version:       129
Release:       1%{?dist}
License:       GPLv3+
URL:           https://github.com/Metaswitch/homestead

Source0:       %{name}-%{version}.tar.bz2
Source1:       common.sh
BuildRequires: make cmake libtool git gcc-c++ bison flex
BuildRequires: libevent-devel lksctp-tools-devel libidn-devel libgcrypt-devel gnutls-devel
BuildRequires: openssl-devel boost-devel boost-static zeromq-devel libcurl-devel net-snmp-devel

# Note: zeromq-devel requires epel-release

%global debug_package %{nil}

Summary:       Clearwater - Homestead
Requires:      clearwater-homestead-libs
Requires:      clearwater-infrastructure clearwater-nginx clearwater-log-cleanup clearwater-monit
Requires:      clearwater-tcp-scalability clearwater-snmpd
Requires:      libidn libgcrypt gnutls openssl-libs zeromq libcurl net-snmp-libs

%package libs
Summary:       Clearwater - Homestead Libraries
Requires:      libevent lksctp-tools

%package cassandra
Summary:       Clearwater - Cassandra for Homestead
Requires:      clearwater-infrastructure clearwater-cassandra

%description
HSS cache/gateway

%description libs
Homestead libraries

%description cassandra
Commission Cassandra for Homestead

%prep
%setup

%build
make MAKE="make --jobs $(nproc)"

%install
# See: debian/homestead.install
mkdir --parents %{buildroot}%{_initrddir}/
mkdir --parents %{buildroot}/usr/share/clearwater/bin/
install --mode=755 debian/homestead.init.d %{buildroot}%{_initrddir}/homestead
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
%{_initrddir}/homestead
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

%post
# See: debian/homestead.postinst
set -e
function add_section()
{
  local FILE=$1
  local TAG=$2
  local DELTA=$3
  { echo "#+$TAG"
    cat $DELTA
    echo "#-$TAG" ; } >> $FILE
}
if ! grep -q "^homestead:" /etc/passwd; then
  useradd --system --no-create-home --home-dir /nonexistent --shell /bin/false homestead
fi
mkdir --parents /var/log/homestead/
chown --recursive homestead /var/log/homestead/
[ ! -x /usr/share/clearwater/bin/clearwater-logging-update ] || /usr/share/clearwater/bin/clearwater-logging-update
add_section /etc/security/limits.conf homestead /etc/security/limits.conf.homestead
service clearwater-infrastructure restart
service homestead stop || /bin/true

%preun
# See: debian/homestead.prerm
set -e
function remove_section()
{
  local FILE=$1
  local TAG=$2
  awk '/^#\+'$TAG'$/,/^#-'$TAG'$/ {next} {print}' "$FILE" > "/tmp/$(basename "$FILE").$$"
  mv "/tmp/$(basename "$FILE").$$" "$FILE"
}
rm --force /etc/monit/conf.d/homestead.monit
service clearwater-monit reload || /bin/true
rm --force /usr/share/clearwater/clearwater-cluster-manager/plugins/homestead*
if [ -x /etc/init.d/clearwater-cluster-manager ]; then
  service clearwater-cluster-manager stop || /bin/true
fi
service homestead stop || /bin/true
if [ "$1" = 0 ]; then # Uninstall
  if grep -q "^homestead:" /etc/passwd; then
    userdel homestead
  fi
  if [ -d /var/log/homestead/ ]; then
    rm --recursive /var/log/homestead/
  fi
  rm --recursive --force /var/run/homestead/
fi
remove_section /etc/security/limits.conf homestead
rm --force /var/lib/homestead/homestead.conf

%post cassandra
# See: debian/homestead-cassandra.postinst
set -e
service clearwater-infrastructure restart
