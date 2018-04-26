Name:          clearwater-util
Version:       129
Release:       1%{?dist}
License:       GPLv3+

Source0:       service.sh

Summary:       Clearwater Utilities
AutoReq:       no

%description
Debian support

%install
mkdir --parents %{buildroot}/usr/share/clearwater/util/
cp %{SOURCE0} %{buildroot}/usr/share/clearwater/util/service.sh

%files
/usr/share/clearwater/util/service.sh
