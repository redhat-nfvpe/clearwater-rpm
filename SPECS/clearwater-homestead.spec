Name:          clearwater-homestead
Version:       129
Release:       1%{?dist}
License:       GPLv3+
URL:           https://github.com/Metaswitch/homestead
BuildRequires: rsync, make, gcc-c++
Source0:       %{name}-%{version}.tar.bz2

%global debug_package %{nil}

Summary: Clearwater - Homestead

%package cassandra
Summary: Clearwater - Cassandra for Homestead

%description
HSS cache/gateway

%description cassandra
Commission Cassandra for Homestead

%prep
%setup

%build
# Note: the modules must be built in order, so unfortunately we can't use --jobs/-J
make

%install
# See: debian/homestead.install
mkdir --parents %{buildroot}/usr/share/clearwater/bin/
rsync build/bin/homestead %{buildroot}/usr/share/clearwater/bin/
rsync --recursive homestead.root/* %{buildroot}/

# See: debian/homestead-cassandra.install
rsync --recursive homestead-cassandra.root/* %{buildroot}/

%files
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

%files cassandra
/usr/share/clearwater/cassandra-schemas/homestead_cache.sh
