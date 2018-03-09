Name:          clearwater-logging
Version:       129
Release:       1%{?dist}
License:       GPLv3+
URL:           https://github.com/Metaswitch/clearwater-logging
Source0:       %{name}-%{version}.tar.bz2
BuildRequires: rsync

%global debug_package %{nil}

Summary:       Clearwater - Logging
Requires:      nagios nagios-plugins sysstat

%description
Common logging infrastructure

%prep
%setup

%install
# See: debian/clearwater-logging.install
rsync --recursive clearwater-logging/* %{buildroot}/

%files
/opt/
/usr/
%config /etc/nagios3/clearwater/commands.cfg
%config /etc/nagios3/clearwater/nagios.cfg
