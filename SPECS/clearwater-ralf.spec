Name:          clearwater-ralf
Version:       129
Release:       1%{?dist}
License:       GPLv3+
URL:           https://github.com/Metaswitch/ralf
BuildRequires: rsync, make, cmake, libtool, gcc-c++, bison, flex
BuildRequires: zeromq-devel, lksctp-tools-devel, gnutls-devel, libidn-devel
Source0:       %{name}-%{version}.tar.bz2

# Note: zeromq-devel requires epel-release

%global debug_package %{nil}

Summary: Clearwater - Ralf

%description
CTF

%prep
%setup

%build
# Note: the modules must be built in order, so unfortunately we can't use --jobs/-J
make

%install
# See: debian/ralf.install
mkdir --parents %{buildroot}/usr/share/clearwater/bin/
rsync build/bin/ralf %{buildroot}/usr/share/clearwater/bin/
rsync --recursive ralf.root/* %{buildroot}/

%files
/usr/
%config /etc/cron.hourly/ralf-log-cleanup
%config /etc/security/limits.conf.ralf
