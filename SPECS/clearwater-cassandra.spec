Name:          clearwater-cassandra
Version:       129
Release:       1%{?dist}
License:       GPLv3+
URL:           https://github.com/Metaswitch/clearwater-cassandra

Source0:       %{name}-%{version}.tar.bz2
Source1:       scriptlet-util.sh

BuildRequires: make

%global debug_package %{nil}

Summary:       Clearwater - Cassandra
Requires:      cassandra
AutoReq:       no

%package -n clearwater-node-cassandra
Summary:       Clearwater Node - Cassandra
Requires:      clearwater-cassandra clearwater-infrastructure
AutoReq:       no

%description
Cassandra configured for Clearwater

%description -n clearwater-node-cassandra
Clearwater Cassandra node

%prep
%setup

%install
# See: debian/clearwater-cassandra.install
mkdir --parents %{buildroot}/usr/share/clearwater/conf/
cp --recursive clearwater-cassandra/* %{buildroot}/
cp modules/clearwater-etcd-plugins/clearwater_cassandra/cassandra_plugin.py %{buildroot}/usr/share/clearwater/conf/
cp modules/clearwater-etcd-plugins/clearwater_cassandra/cassandra_failed_plugin.py %{buildroot}/usr/share/clearwater/conf/
rm %{buildroot}/etc/init.d/cassandra.clearwater
rm %{buildroot}/etc/default/cassandra.clearwater

%files
/usr/share/cassandra/cassandra.in.sh.clearwater
/usr/share/clearwater/bin/do_backup.sh
/usr/share/clearwater/bin/list_backups.sh
/usr/share/clearwater/bin/poll_cassandra.sh
/usr/share/clearwater/bin/poll_cassandra_ring.sh
/usr/share/clearwater/bin/poll_cqlsh.sh
/usr/share/clearwater/bin/remove_site_from_cassandra
/usr/share/clearwater/bin/restore_backup.sh
/usr/share/clearwater/bin/update_cassandra_strategy
/usr/share/clearwater/cassandra/cassandra-env.sh.template
/usr/share/clearwater/cassandra/cassandra.yaml.template
/usr/share/clearwater/cassandra_schema_utils.sh
/usr/share/clearwater/conf/cassandra_failed_plugin.py*
/usr/share/clearwater/conf/cassandra_plugin.py*
/usr/share/clearwater/conf/clearwater-cassandra.monit
/usr/share/clearwater/infrastructure/alarms/cassandra_alarms.json
/usr/share/clearwater/infrastructure/monit_uptime/check-cassandra-uptime
/usr/share/clearwater/infrastructure/scripts/cassandra
/usr/share/clearwater/infrastructure/scripts/cassandra.monit
/usr/share/clearwater/infrastructure/scripts/cassandra_cluster_manager
/usr/share/clearwater/infrastructure/scripts/cassandra_schemas/run_cassandra_schemas

%files -n clearwater-node-cassandra
/usr/share/clearwater/node_type.d/90_cassandra
