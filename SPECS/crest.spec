Name:          clearwater-crest
Version:       129
Release:       1%{?dist}
License:       GPLv3+
URL:           https://github.com/Metaswitch/crest
Requires:      python-virtualenv
BuildRequires: git, rsync, make, python-virtualenv, gcc-c++
BuildRequires: python-devel, libffi-devel, libxslt-devel

Summary: Clearwater - Crest

%package prov
Summary: Clearwater - Crest Provisioning

%package -n clearwater-homer
Summary: Clearwater - Homer

%package -n clearwater-homer-cassandra
Summary: Clearwater - Cassandra for Homer

%package -n clearwater-homestead-prov
Summary: Clearwater - Homestead Provisioning

%package -n clearwater-homestead-prov-cassandra
Summary: Clearwater - Cassandra for Homestead Provisioning

%description
Cassandra-powered generic RESTful HTTP server platform

%description prov
Provision Crest

%description -n clearwater-homer
XDMS

%description -n clearwater-homer-cassandra
Commission Cassandra for Homer

%description -n clearwater-homestead-prov
Provision Homestead

%description -n clearwater-homestead-prov-cassandra
Commission Cassandra for Homestead Provisioning

%prep
if [ ! -d crest ]; then
  git config --global url."https://github.com/".insteadOf git@github.com:
  git clone --depth 1 --recursive --branch release-%{version} git@github.com:Metaswitch/crest.git
fi

%install
cd %{_builddir}/crest

make env

# See: debian/crest.install
mkdir --parents %{buildroot}/usr/share/clearwater/crest/.wheelhouse/
rsync --recursive crest_wheelhouse/* %{buildroot}/usr/share/clearwater/crest/.wheelhouse/

# See: debian/crest-prov.install
mkdir --parents %{buildroot}/usr/share/clearwater/crest-prov/src/metaswitch/crest/
mkdir --parents %{buildroot}/usr/share/clearwater/crest-prov/tools/sstable_provisioning/
mkdir --parents %{buildroot}/usr/share/clearwater/crest-prov/.wheelhouse/
rsync src/metaswitch/crest/tools %{buildroot}/usr/share/clearwater/crest-prov/src/metaswitch/crest/
rsync src/metaswitch/crest/tools/sstable_provisioning/* %{buildroot}/usr/share/clearwater/crest-prov/tools/sstable_provisioning/
rsync crest_wheelhouse/* %{buildroot}/usr/share/clearwater/crest-prov/.wheelhouse/

# See: debian/homer.install
mkdir --parents %{buildroot}/usr/share/clearwater/homer/.wheelhouse/
mkdir --parents %{buildroot}/usr/share/clearwater/homer/src/metaswitch/homer/
mkdir --parents %{buildroot}/usr/share/clearwater/homer/templates/
rsync homer_wheelhouse/* %{buildroot}/usr/share/clearwater/homer/.wheelhouse/
rsync --recursive src/metaswitch/homer/tools %{buildroot}/usr/share/clearwater/homer/src/metaswitch/homer/
rsync homer.local_settings/local_settings.py %{buildroot}/usr/share/clearwater/homer/templates/
rsync homer.monit %{buildroot}/usr/share/clearwater/homer/templates/
rsync --recursive homer.root/* %{buildroot}/

# See: debian/homer-cassandra.install
rsync --recursive homer-cassandra.root/* %{buildroot}/

# See: debian/homestead-prov.install
mkdir --parents %{buildroot}/usr/share/clearwater/homestead/.wheelhouse/
mkdir --parents %{buildroot}/usr/share/clearwater/homestead/templates/
rsync homestead_prov_wheelhouse/* %{buildroot}/usr/share/clearwater/homestead/.wheelhouse/
rsync homestead.local_settings/local_settings.py %{buildroot}/usr/share/clearwater/homestead/templates/
rsync --recursive homestead.root/* %{buildroot}/

# See: debian/homestead-prov-cassandra.install
rsync --recursive homestead-prov-cassandra.root/* %{buildroot}/

%files
/usr/share/clearwater/crest/.wheelhouse/

%files prov
/usr/share/clearwater/crest-prov/

%files -n clearwater-homer
/usr/share/clearwater/homer/
/etc/clearwater/secure-connections/homer.conf
/etc/cron.hourly/homer-log-cleanup
/usr/share/clearwater/bin/poll_homer.sh
/usr/share/clearwater/clearwater-diags-monitor/scripts/homer_diags
/usr/share/clearwater/infrastructure/scripts/restart/homer_restart
/usr/share/clearwater/infrastructure/scripts/create-homer-nginx-config
/usr/share/clearwater/infrastructure/scripts/homer
/usr/share/clearwater/node_type.d/20_homer

%files -n clearwater-homer-cassandra
/usr/share/clearwater/cassandra/users/homer
/usr/share/clearwater/cassandra-schemas/homer.sh

%files -n clearwater-homestead-prov
/usr/share/clearwater/homestead/
/etc/clearwater/secure-connections/homestead.conf
/etc/cron.hourly/homestead-prov-log-cleanup
/usr/share/clearwater/bin/poll_homestead-prov.sh
/usr/share/clearwater/clearwater-diags-monitor/scripts/homestead_prov_diags
/usr/share/clearwater/infrastructure/scripts/restart/homestead_prov_restart
/usr/share/clearwater/infrastructure/scripts/create-homestead-prov-nginx-config
/usr/share/clearwater/infrastructure/scripts/homestead-prov
/usr/share/clearwater/infrastructure/scripts/homestead-prov.monit

%files -n clearwater-homestead-prov-cassandra
/usr/share/clearwater/cassandra/users/homestead-prov
/usr/share/clearwater/cassandra-schemas/homestead_provisioning.sh
