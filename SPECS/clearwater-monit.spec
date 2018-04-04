Name:          clearwater-monit
Version:       129
Release:       1%{?dist}
License:       AGPLv3+
URL:           https://github.com/Metaswitch/clearwater-monit

Source0:       %{name}-%{version}.tar.bz2
BuildRequires: make libtool gcc-c++ bison flex
BuildRequires: pam-devel openssl-devel
BuildRequires: systemd

%global debug_package %{nil}

Summary:       Clearwater - Monit
Requires:      clearwater-infrastructure
Requires:      pam openssl-libs

%description
utility for managing and monitoring processes, files, directories, and filesystems

%prep
%setup

%build
./bootstrap
./configure
make all MAKE="make --jobs $(nproc)"

%install
# See: debian/clearwater-monit.install
mkdir --parents %{buildroot}/etc/monit/
mkdir --parents %{buildroot}/usr/bin
install --mode=700 debian/monitrc %{buildroot}/etc/monit/
cp monit %{buildroot}/usr/bin/
cp --recursive clearwater-monit.root/* %{buildroot}/

mkdir --parents %{buildroot}%{_unitdir}/
cp debian/clearwater-monit.service %{buildroot}%{_unitdir}/

%files
/usr/bin/monit
/usr/share/clearwater/clearwater-monit/install/clearwater-monit.postinst
/usr/share/clearwater/infrastructure/alarms/monit_alarms.json
/usr/share/clearwater/infrastructure/monit_uptime/check-monit-uptime
%{_unitdir}/clearwater-monit.service
%config /etc/monit/monitrc
%config /etc/monit/conf.d/monit.monit
%config /etc/monit/conf.d/ntp.monit
%ghost /var/log/monit.log
%ghost /var/lib/monit/state
%ghost /var/lib/monit/id

%post
# See: debian/clearwater-monit.postinst
set -e
mkdir --parents /var/lib/monit/ # this was missing!
/usr/share/clearwater/clearwater-monit/install/clearwater-monit.postinst
%systemd_post clearwater-monit.service

%preun
# See: debian/clearwater-monit.prerm
set -e
%systemd_preun clearwater-monit.service
rm --force /etc/monit/conf.d/mmonit.monit

%postun
# See: debian/clearwater-monit.postrm
set -e
if [ "$1" = 0 ]; then # Uninstall
  rm --force /var/log/monit.log
  rm --force /var/lib/monit/state /var/lib/monit/id
  if [ -f /etc/aliases ] || [ -L /etc/aliases ]; then
    if grep -qi "^monit[[:space:]]*:" /etc/aliases
    then
      sed -i '/^monit[[:space:]]*:.*$/d' /etc/aliases
      test -x /usr/bin/newaliases && newaliases || :
    fi
  fi
fi
