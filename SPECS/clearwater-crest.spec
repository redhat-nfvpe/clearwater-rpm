Name:          clearwater-crest
Version:       129
Release:       1%{?dist}
License:       GPLv3+
URL:           https://github.com/Metaswitch/crest

Source0:       %{name}-%{version}.tar.bz2
BuildRequires: rsync make python-virtualenv gcc-c++
BuildRequires: python-devel libffi-devel libxslt-devel openssl-devel

%global debug_package %{nil}

Summary:       Clearwater - Crest
Requires:      clearwater-infrastructure clearwater-nginx clearwater-log-cleanup clearwater-monit
Requires:      python-virtualenv libffi libxslt openssl-libs

%package prov
Summary:       Clearwater - Crest Provisioning

%package -n clearwater-homer
Summary:       Clearwater - Homer
Requires:      clearwater-crest 

%package -n clearwater-homer-cassandra
Summary:       Clearwater - Cassandra for Homer
Requires:      clearwater-cassandra clearwater-infrastructure 

%package -n clearwater-homestead-prov
Summary:       Clearwater - Homestead Provisioning
Requires:      clearwater-crest 

%package -n clearwater-homestead-prov-cassandra
Summary:       Clearwater - Cassandra for Homestead Provisioning
Requires:      clearwater-cassandra clearwater-infrastructure homestead-cassandra 

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
%setup

%build
make env

%install
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
mkdir --parents %{buildroot}%{_initrddir}/
mkdir --parents %{buildroot}/usr/share/clearwater/homer/.wheelhouse/
mkdir --parents %{buildroot}/usr/share/clearwater/homer/src/metaswitch/homer/
mkdir --parents %{buildroot}/usr/share/clearwater/homer/templates/
rsync debian/homer.init.d %{buildroot}%{_initrddir}/homer
rsync homer_wheelhouse/* %{buildroot}/usr/share/clearwater/homer/.wheelhouse/
rsync --recursive src/metaswitch/homer/tools %{buildroot}/usr/share/clearwater/homer/src/metaswitch/homer/
rsync homer.local_settings/local_settings.py %{buildroot}/usr/share/clearwater/homer/templates/
rsync homer.monit %{buildroot}/usr/share/clearwater/homer/templates/
rsync --recursive homer.root/* %{buildroot}/

# See: debian/homer-cassandra.install
rsync --recursive homer-cassandra.root/* %{buildroot}/

# See: debian/homestead-prov.install
rsync debian/homestead-prov.init.d %{buildroot}%{_initrddir}/homestead-prov
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
%{_initrddir}/homer
/usr/share/clearwater/homer/
/usr/share/clearwater/bin/poll_homer.sh
/usr/share/clearwater/clearwater-diags-monitor/scripts/homer_diags
/usr/share/clearwater/infrastructure/scripts/restart/homer_restart
/usr/share/clearwater/infrastructure/scripts/create-homer-nginx-config
/usr/share/clearwater/infrastructure/scripts/homer
/usr/share/clearwater/node_type.d/20_homer
%config /etc/clearwater/secure-connections/homer.conf
%config /etc/cron.hourly/homer-log-cleanup
# TODO: %ghost /etc/monit/conf.d/*.monit

%files -n clearwater-homer-cassandra
/usr/share/clearwater/cassandra/users/homer
/usr/share/clearwater/cassandra-schemas/homer.sh

%files -n clearwater-homestead-prov
%{_initrddir}/homestead-prov
/usr/share/clearwater/homestead/
/usr/share/clearwater/bin/poll_homestead-prov.sh
/usr/share/clearwater/clearwater-diags-monitor/scripts/homestead_prov_diags
/usr/share/clearwater/infrastructure/scripts/restart/homestead_prov_restart
/usr/share/clearwater/infrastructure/scripts/create-homestead-prov-nginx-config
/usr/share/clearwater/infrastructure/scripts/homestead-prov
/usr/share/clearwater/infrastructure/scripts/homestead-prov.monit
%config /etc/clearwater/secure-connections/homestead.conf
%config /etc/cron.hourly/homestead-prov-log-cleanup

%files -n clearwater-homestead-prov-cassandra
/usr/share/clearwater/cassandra/users/homestead-prov
/usr/share/clearwater/cassandra-schemas/homestead_provisioning.sh

%post
# See: debian/crest.postinst
set -e
rm --recursive --force /usr/share/clearwater/crest/build/ # TODO: why?
virtualenv /usr/share/clearwater/crest/env/
/usr/share/clearwater/crest/env/bin/pip install --upgrade pip
/usr/share/clearwater/crest/env/bin/pip install --no-index --find-links /usr/share/clearwater/crest/.wheelhouse/ wheel crest
if [ -x %{_initrddir}/clearwater-cluster-manager ]; then
  service clearwater-cluster-manager stop || /bin/true
fi
[ ! -x %{_initrddir}/clearwater-secure-connections ] || %{_initrddir}/clearwater-secure-connections reload

%preun
# See: debian/crest.preun
set -e
rm --recursive --force /usr/share/clearwater/crest/env/

%post prov
# See: debian/crest-prov.postinst
set -e
virtualenv /usr/share/clearwater/crest-prov/env/
/usr/share/clearwater/crest-prov/env/bin/pip install --upgrade pip
/usr/share/clearwater/crest-prov/env/bin/pip install --no-index --find-links /usr/share/clearwater/crest-prov/.wheelhouse/ wheel crest

%post -n clearwater-homer
# See: debian/homer.postinst
set -e
. /etc/clearwater/config
rm --recursive --force /usr/share/clearwater/homer/build/ # TODO: why?
/usr/share/clearwater/crest/env/bin/pip install --no-index --find-links /usr/share/clearwater/crest/.wheelhouse/ --find-links /usr/share/clearwater/homer/.wheelhouse/ homer 
service clearwater-infrastructure restart
/usr/share/clearwater/cassandra-schemas/homer.sh || /bin/true
cp /usr/share/clearwater/homer/templates/*.monit /etc/monit/conf.d/
service clearwater-monit reload || /bin/true
if [ -x %{_initrddir}/clearwater-cluster-manager ]; then
  service clearwater-cluster-manager stop || /bin/true
fi
service homer stop || /bin/true
[ ! -x %{_initrddir}/clearwater-secure-connections ] || %{_initrddir}/clearwater-secure-connections reload

%preun -n clearwater-homer
# See: debian/homer.prerm
set -e
for F in /usr/share/clearwater/homer/templates/*.monit; do rm --force "/etc/monit/conf.d/$(basename "$F")"; done
service clearwater-monit reload || /bin/true
if ( nginx_dissite homer > /dev/null ); then
  service nginx reload
fi
rm --force /usr/share/clearwater/clearwater-cluster-manager/plugins/homer*
if [ -x /etc/init.d/clearwater-cluster-manager ]; then
  service clearwater-cluster-manager stop || /bin/true
fi
service homer stop
rm --recursive --force /usr/share/clearwater/homer/python/ # TODO: why?
rm --force /usr/share/clearwater/homer/local_settings.py

%post -n clearwater-homer-cassandra
# See: debian/homer-cassandra.postinst
set -e
service clearwater-infrastructure restart

%post -n clearwater-homestead-prov
# See: debian/homestead-prov.postinst
set -e
rm --recursive --force /usr/share/clearwater/homestead/build/ # TODO: why?
/usr/share/clearwater/crest/env/bin/pip install --no-index --find-links /usr/share/clearwater/crest/.wheelhouse/ --find-links /usr/share/clearwater/homestead/.wheelhouse/ homestead-prov 
service clearwater-infrastructure restart
service homestead-prov stop || /bin/true
[ ! -x %{_initrddir}/clearwater-secure-connections ] || %{_initrddir}/clearwater-secure-connections reload

%preun -n clearwater-homestead-prov
# See: debian/homestead-prov.prerm
set -e
rm --force /etc/monit/conf.d/homestead-prov.monit
service clearwater-monit reload || /bin/true
if ( nginx_dissite homestead-prov > /dev/null ); then
  service nginx reload
fi
service homestead-prov stop
rm --recursive --force /usr/share/clearwater/homestead/python/ # TODO: why?
rm --force /usr/share/clearwater/homestead/local_settings.py

%post -n clearwater-homestead-prov-cassandra
# See: debian/homestead-prov-cassandra.postinst
set -e
service clearwater-infrastructure restart
