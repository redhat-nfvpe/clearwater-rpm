Name:          clearwater-astaire
Version:       129
Release:       1%{?dist}
License:       GPLv3+
URL:           https://github.com/Metaswitch/astaire

Source0:       %{name}-%{version}.tar.bz2
BuildRequires: make libtool git gcc-c++
BuildRequires: libevent-devel zeromq-devel zlib-devel boost-devel

%global debug_package %{nil}

Summary:       Clearwater - Astaire
Requires:      clearwater-astaire-libs
Requires:      clearwater-infrastructure clearwater-tcp-scalability clearwater-log-cleanup 
Requires:      clearwater-monit
Requires:      cpulimit
Requires:      zeromq zlib boost

%package libs
Summary:       Clearwater - Astaire Libraries

%package -n clearwater-rogers
Summary:       Clearwater - Rogers
Requires:      clearwater-rogers-libs
Requires:      clearwater-infrastructure clearwater-tcp-scalability clearwater-log-cleanup 
Requires:      clearwater-monit
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
make

%install
# See: debian/astaire.install
mkdir --parents %{buildroot}%{_initrddir}/
mkdir --parents %{buildroot}/usr/share/clearwater/bin/
mkdir --parents %{buildroot}/usr/share/clearwater/astaire/bin/
install -m 755 debian/astaire.init.d %{buildroot}%{_initrddir}/astaire
cp build/bin/astaire %{buildroot}/usr/share/clearwater/bin/
cp modules/cpp-common/scripts/stats-c/cw_stat %{buildroot}/usr/share/clearwater/astaire/bin/
cp --recursive astaire.root/* %{buildroot}/

# See: debian/astaire-libs.install
mkdir --parents %{buildroot}/usr/share/clearwater/astaire/lib/
cp usr/lib/*.so %{buildroot}/usr/share/clearwater/astaire/lib/
cp usr/lib/*.so.* %{buildroot}/usr/share/clearwater/astaire/lib/

# See: debian/rogers.install
install -m 755 debian/rogers.init.d %{buildroot}%{_initrddir}/rogers
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

%post
# See: debian/astaire.postinst
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
if ! grep -q "^astaire:" /etc/passwd; then
  useradd --system --no-create-home --home-dir /nonexistent --shell /bin/false astaire
fi
mkdir --parents /var/log/astaire/
chown --recursive astaire /var/log/astaire/
[ ! -x /usr/share/clearwater/bin/clearwater-logging-update ] || /usr/share/clearwater/bin/clearwater-logging-update
add_section /etc/security/limits.conf astaire /etc/security/limits.conf.astaire
service astaire-throttle start || /bin/true
service clearwater-infrastructure restart
service astaire stop || /bin/true

%preun
# See: debian/astaire.prerm
set -e
function remove_section()
{
  local FILE=$1
  local TAG=$2
  awk '/^#\+'$TAG'$/,/^#-'$TAG'$/ {next} {print}' "$FILE" > "/tmp/$(basename "$FILE").$$"
  mv "/tmp/$(basename "$FILE").$$" "$FILE"
}
rm --force /etc/monit/conf.d/astaire.monit
service clearwater-monit reload || /bin/true
service astaire stop || /bin/true
service astaire-throttle stop || /bin/true
if [ "$1" = 0 ]; then # Uninstall
  if grep -q "^astaire:" /etc/passwd; then
    userdel astaire
  fi
  if [ -d /var/log/astaire/ ]; then
    rm --recursive /var/log/astaire/
  fi
  rm --recursive --force /var/run/astaire/
fi
remove_section /etc/security/limits.conf astaire

%post -n clearwater-rogers
# See: debian/rogers.postinst
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
if ! grep -q "^rogers:" /etc/passwd; then
  useradd --system --no-create-home --home-dir /nonexistent --shell /bin/false rogers
fi
mkdir --parents /var/log/rogers/
chown --recursive rogers /var/log/rogers/
[ ! -x /usr/share/clearwater/bin/clearwater-logging-update ] || /usr/share/clearwater/bin/clearwater-logging-update
add_section /etc/security/limits.conf rogers /etc/security/limits.conf.rogers
service clearwater-infrastructure restart
service rogers stop || /bin/true

%preun -n clearwater-rogers
# See: debian/rogers.prerm
set -e
function remove_section()
{
  local FILE=$1
  local TAG=$2
  awk '/^#\+'$TAG'$/,/^#-'$TAG'$/ {next} {print}' "$FILE" > "/tmp/$(basename "$FILE").$$"
  mv "/tmp/$(basename "$FILE").$$" "$FILE"
}
rm --force /etc/monit/conf.d/rogers.monit
service clearwater-monit reload || /bin/true
service rogers stop || /bin/true
if [ "$1" = 0 ]; then # Uninstall
  if grep -q "^rogers:" /etc/passwd; then
    userdel rogers
  fi
  if [ -d /var/log/rogers/ ]; then
    rm --recursive /var/log/rogers/
  fi
  rm --recursive --force /var/run/rogers/
fi
remove_section /etc/security/limits.conf rogers
