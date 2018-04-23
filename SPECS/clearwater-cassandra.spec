Name:          clearwater-cassandra
Version:       129
Release:       1%{?dist}
License:       GPLv3+
URL:           https://github.com/Metaswitch/clearwater-cassandra

Source0:       %{name}-%{version}.tar.bz2
Source1:       scriptlet-util.sh
Source2:       clearwater-cassandra.service
Source3:       clearwater-cassandra.sh

BuildRequires: make
BuildRequires: systemd

%global debug_package %{nil}

Summary:       Clearwater - Cassandra
Requires:      cassandra
AutoReq:       no
%{?systemd_requires}

# Note: cassandra is not packaged for CentOS, so this package will require an external repository

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
rm %{buildroot}/usr/share/cassandra/cassandra.in.sh.clearwater

# systemd
mkdir --parents %{buildroot}%{_unitdir}/
mkdir --parents %{buildroot}/lib/systemd/scripts/
install --mode=644 %{SOURCE2} %{buildroot}%{_unitdir}/clearwater-cassandra.service
install --mode=755 %{SOURCE3} %{buildroot}/lib/systemd/scripts/clearwater-cassandra.sh

sed --in-place 's/\/etc\/init.d\/cassandra/service clearwater-cassandra/g' %{buildroot}/usr/share/clearwater/conf/clearwater-cassandra.monit
sed --in-place 's/\/etc\/init.d\/cassandra/service clearwater-cassandra/g' %{buildroot}/usr/share/clearwater/infrastructure/scripts/cassandra.monit
sed --in-place 's/reload clearwater-monit/service reload clearwater-monit/g' %{buildroot}/usr/share/clearwater/infrastructure/scripts/cassandra.monit

%files
%{_unitdir}/clearwater-cassandra.service
/lib/systemd/scripts/clearwater-cassandra.sh
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

%post -p /bin/bash
%include %{SOURCE1}
# See: debian/clearwater-cassandra.links
ln --symbolic /usr/share/clearwater/bin/do_backup.sh /usr/bin/cw-do_backup
ln --symbolic /usr/share/clearwater/bin/list_backups.sh /usr/bin/cw-list_backups
ln --symbolic /usr/share/clearwater/bin/update_cassandra_strategy /usr/sbin/cw-update_cassandra_strategy
ln --symbolic /usr/share/clearwater/bin/remove_site_from_cassandra /usr/sbin/cw-remove_site_from_cassandra
ln --symbolic /usr/share/clearwater/bin/restore_backup.sh /usr/sbin/cw-restore_backup

# See: debian/clearwater-cassandra.postinst
%systemd_post clearwater-cassandra.service
cw-start clearwater-cassandra

%preun -p /bin/bash
%include %{SOURCE1}
# See: debian/astaire.prerm
%systemd_preun clearwater-cassandra.service
cw-stop clearwater-cassandra

# See: debian/clearwater-cassandra.links
rm --force /usr/bin/cw-do_backup
rm --force /usr/bin/cw-list_backups
rm --force /usr/sbin/cw-update_cassandra_strategy
rm --force /usr/sbin/cw-remove_site_from_cassandra
rm --force /usr/sbin/cw-restore_backup

%postun
%systemd_postun_with_restart clearwater-cassandra.service
