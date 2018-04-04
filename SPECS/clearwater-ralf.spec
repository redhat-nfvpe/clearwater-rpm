Name:          clearwater-ralf
Version:       129
Release:       1%{?dist}
License:       GPLv3+
URL:           https://github.com/Metaswitch/ralf

Source0:       %{name}-%{version}.tar.bz2
Source1:       common.sh
BuildRequires: make cmake libtool gcc-c++ bison flex
BuildRequires: libevent-devel lksctp-tools-devel libidn-devel libgcrypt-devel gnutls-devel
BuildRequires: boost-devel zeromq-devel libcurl-devel

# Note: zeromq-devel requires epel-release

%global debug_package %{nil}

Summary:       Clearwater - Ralf
Requires:      clearwater-ralf-libs
Requires:      clearwater-infrastructure clearwater-tcp-scalability clearwater-socket-factory
Requires:      clearwater-log-cleanup clearwater-monit
Requires:      libidn libgcrypt gnutls boost zeromq libcurl

%package libs
Summary:       Clearwater - Ralf Libraries
Requires:      libevent lksctp-tools

%description
CTF

%description libs
Ralf libraries

%prep
%setup

%build
make MAKE="make --jobs $(nproc)"

%install
# See: debian/ralf.install
mkdir --parents %{buildroot}%{_initrddir}/
mkdir --parents %{buildroot}/usr/share/clearwater/bin/
install --mode=755 debian/ralf.init.d %{buildroot}%{_initrddir}/ralf
cp build/bin/ralf %{buildroot}/usr/share/clearwater/bin/
cp --recursive ralf.root/* %{buildroot}/

# See: debian/ralf-libs.install
mkdir --parents %{buildroot}/usr/share/clearwater/ralf/lib/freeDiameter/
cp usr/lib/*.so %{buildroot}/usr/share/clearwater/ralf/lib/
cp usr/lib/*.so.* %{buildroot}/usr/share/clearwater/ralf/lib/
cp usr/lib/freeDiameter/*.fdx %{buildroot}/usr/share/clearwater/ralf/lib/freeDiameter/

%files
%{_initrddir}/ralf
/usr/
%config /etc/cron.hourly/ralf-log-cleanup
%config /etc/security/limits.conf.ralf

%files libs
/usr/share/clearwater/ralf/lib/

%post
%include %{SOURCE1}
# See: debian/ralf.postinst
function add_section()
{
  local FILE=$1
  local TAG=$2
  local DELTA=$3
  { echo "#+$TAG"
    cat $DELTA
    echo "#-$TAG" ; } >> $FILE
}
if ! grep -q "^ralf:" /etc/passwd; then
  useradd --system --no-create-home --home-dir /nonexistent --shell /bin/false ralf
fi
mkdir --parents /var/log/ralf/
chown --recursive ralf /var/log/ralf/
[ ! -x /usr/share/clearwater/bin/clearwater-logging-update ] || /usr/share/clearwater/bin/clearwater-logging-update
add_section /etc/security/limits.conf ralf /etc/security/limits.conf.ralf
service clearwater-infrastructure restart
if [ -x /etc/init.d/clearwater-cluster-manager ]; then
  service clearwater-cluster-manager stop || /bin/true
fi  
service ralf stop || /bin/true

%preun
%include %{SOURCE1}
# See: debian/ralf.prerm
function remove_section()
{
  local FILE=$1
  local TAG=$2
  awk '/^#\+'$TAG'$/,/^#-'$TAG'$/ {next} {print}' "$FILE" > "/tmp/$(basename "$FILE").$$"
  mv "/tmp/$(basename "$FILE").$$" "$FILE"
}
rm --force /etc/monit/conf.d/ralf.monit
service clearwater-monit reload || /bin/true
rm --force /usr/share/clearwater/clearwater-cluster-manager/plugins/ralf*
if [ -x /etc/init.d/clearwater-cluster-manager ]; then
  service clearwater-cluster-manager stop || /bin/true
fi
service ralf stop || /bin/true
if [ "$1" = 0 ]; then # Uninstall
  if grep -q "^ralf:" /etc/passwd; then
    userdel ralf
  fi
  if [ -d /var/log/ralf/ ]; then
    rm --recursive /var/log/ralf/
  fi
  rm --recursive --force /var/run/ralf/
fi
remove_section /etc/security/limits.conf ralf
rm --force /var/lib/ralf/ralf.conf
