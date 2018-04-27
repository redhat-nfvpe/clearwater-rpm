Name:          clearwater-utils
Version:       129
Release:       1%{?dist}
License:       GPLv3+

Source0:       service.sh

Summary:       Clearwater Utilities
AutoReq:       no

%description
Debian support

%install
mkdir --parents %{buildroot}/usr/share/clearwater/utils/
cp %{SOURCE0} %{buildroot}/usr/share/clearwater/utils/service.sh

%files
/usr/share/clearwater/utils/service.sh
