Name:          clearwater-debian
Version:       129
Release:       1%{?dist}
License:       GPLv3+
Summary:       Clearwater - Debian Support
Source0:       debian.sh
Requires:      dpkg

# Note: the start-stop-daemon command is in dpkg

%description
Debian support

%install
mkdir --parents %{buildroot}/lib/init/
cp %{SOURCE0} %{buildroot}/lib/init/vars.sh

%files
/lib/init/vars.sh
